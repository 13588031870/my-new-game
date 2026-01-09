import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 视觉引擎 V7.0 (深空磨砂 HUD 风格)
# ==========================================
st.set_page_config(layout="wide", page_title="你的新人生", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
    
    /* ---------------- 全局字体与背景重构 ---------------- */
    html, body, [class*="css"] {
        font-family: 'Microsoft YaHei', 'Noto Sans SC', sans-serif !important; /* 强制无衬线字体 */
    }
    
    .stApp {
        /* 深空背景：使用径向渐变模拟星空/深海，而非纯黑 */
        background-color: #1a1a2e;
        background-image: radial-gradient(circle at 50% 0%, #2e2e42 0%, #1a1a2e 80%);
        color: #e6e6e6;
    }

    /* ---------------- 输入框美化 (高对比度) ---------------- */
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSlider label {
        color: #00d4ff !important; /* 霓虹蓝 Label */
        font-size: 1.1rem !important;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #fff !important;
        border-radius: 4px;
    }
    
    /* ---------------- Tab 导航栏 (V4 经典版) ---------------- */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: none; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: rgba(255,255,255,0.03);
        border: 1px solid #333;
        border-radius: 4px;
        flex-grow: 1;
    }
    .stTabs [data-baseweb="tab"] div {
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        color: #666;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #FF4B2B, #FF416C); /* 活力红渐变 */
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] div { color: white !important; }

    /* ---------------- HUD 信息面板 (游戏感核心) ---------------- */
    .hud-container {
        background: rgba(30, 35, 45, 0.6);
        backdrop-filter: blur(12px); /* 磨砂玻璃 */
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .hud-header {
        border-left: 4px solid #00d4ff;
        padding-left: 10px;
        margin-bottom: 15px;
        color: #fff;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ---------------- 属性网格系统 (解决文字隔太远的问题) ---------------- */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 两列布局 */
        gap: 10px;
    }
    .stat-box {
        background: rgba(0,0,0,0.3);
        border: 1px solid #444;
        padding: 8px 12px;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stat-label { color: #aaa; font-size: 0.9rem; }
    .stat-value { color: #00d4ff; font-weight: bold; font-family: 'Consolas', monospace; font-size: 1.1rem; }

    /* ---------------- 特质胶囊 ---------------- */
    .trait-capsule {
        background: rgba(255, 75, 43, 0.15);
        border: 1px solid rgba(255, 75, 43, 0.4);
        color: #FF416C;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        margin-right: 5px;
        margin-bottom: 5px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 剧本数据库 (完整版)
# ==========================================
SCENARIOS = {
    "三国": [
        {"id": "s1", "name": "189年 · 董卓入京", "desc": "【汉室至暗】洛阳火起，国贼当道。你是刺董的勇士，还是助纣的枭雄？"},
        {"id": "s2", "name": "194年 · 群雄逐鹿", "desc": "【诸侯混战】董卓已死，天下更乱。袁绍据河北，孙策霸江东，中原无主。"},
        {"id": "s3", "name": "200年 · 官渡之战", "desc": "【北方决战】曹袁对峙。这是一场关于后勤、人心与奇谋的豪赌。"},
        {"id": "s4", "name": "208年 · 赤壁鏖兵", "desc": "【三分天下】烈火张天，铁索连舟。周郎妙计安天下。"},
        {"id": "s5", "name": "234年 · 星落五丈原", "desc": "【英雄迟暮】丞相北伐，天命难违。你能否逆天改命，延续大汉？"}
    ],
    "现代": [
        {"id": "m1", "name": "2008 · 激荡三十年", "desc": "【黄金时代】奥运盛典，金融海啸。这是改变命运的最佳年份。"},
        {"id": "m2", "name": "2015 · 流量帝国", "desc": "【风口之猪】短视频爆发。只要敢露脸，人人都能成名15分钟。"},
        {"id": "m3", "name": "2020 · 静默世界", "desc": "【生存挑战】流行病席卷全球。居家隔离的日子里，如何守护家庭？"},
        {"id": "m4", "name": "2026 · 当下·围城", "desc": "【现实主义】考公、内卷、房贷。在存量博弈的时代，普通人如何突围？"},
        {"id": "m5", "name": "2060 · 奇点降临", "desc": "【东方赛博】仿生人普及。你发现你的AI伴侣产生了自我意识。"}
    ],
    "修仙": [
        {"id": "x1", "name": "合欢宗 · 魅影", "desc": "【情缘流】游走正魔，以情证道。让圣女动心，让魔头挡劫。"},
        {"id": "x2", "name": "荒古圣体 · 霸途", "desc": "【无敌流】肉身无双，举世皆敌。一条用拳头杀出来的登天路。"},
        {"id": "x3", "name": "戒指老爷爷 · 凡人", "desc": "【养成流】被退婚的废柴，随身老爷爷指点迷津，莫欺少年穷。"},
        {"id": "x4", "name": "夺舍 · 魔尊归来", "desc": "【策略流】满级魔尊夺舍正道杂役。扮猪吃虎，重回巅峰。"}
    ],
    "末日": [
        {"id": "d1", "name": "尸潮 · 燕京沦陷", "desc": "【生化危机】都城一夜瘫痪。手里只有一把菜刀，邻居在挠门。"},
        {"id": "d2", "name": "战争 · 东方防线", "desc": "【硬核军事】核冬笼罩，坚守长江防线。敌人不仅是军队，还有辐射。"},
        {"id": "d3", "name": "智械 · 机械天网", "desc": "【人机战争】2090年，超级AI觉醒。人类在钢铁洪流下苟延残喘。"}
    ]
}

# ==========================================
# 3. 智能引擎
# ==========================================
HISTORY_HEROES = {
    "s1": [{"name": "曹操", "role": "校尉", "bio": "热血青年，意图刺董。"}, {"name": "董卓", "role": "相国", "bio": "残暴无道，权倾朝野。"}, {"name": "刘备", "role": "县尉", "bio": "织席贩履，胸怀大志。"}],
    "s4": [{"name": "诸葛亮", "role": "军师", "bio": "隆中对策，三分天下。"}, {"name": "周瑜", "role": "都督", "bio": "雅量高致，火烧赤壁。"}, {"name": "赵云", "role": "将军", "bio": "浑身是胆，忠勇无双。"}]
}

def generate_presets(scenario_type, scenario_id):
    if scenario_type == "三国" and scenario_id in HISTORY_HEROES:
        return HISTORY_HEROES[scenario_id]
    
    presets = []
    # 随机中文名生成
    last_names = "赵钱孙李周吴郑王冯陈"
    first_names = ["伟", "强", "军", "磊", "芳", "娜", "敏", "静"]
    
    role_map = {
        "三国": ["流民", "逃兵", "富商", "书生"],
        "现代": ["大厂员工", "外卖员", "医生", "老师", "拆二代"],
        "修仙": ["杂役", "散修", "世家子", "乞丐"],
        "末日": ["退伍兵", "护士", "卡车司机", "学生"],
        "自定义": ["旅人", "土著", "勇者"]
    }
    roles = role_map.get(scenario_type, role_map["自定义"])
    
    for _ in range(5):
        name = random.choice(last_names) + random.choice(first_names)
        r = random.choice(roles)
        presets.append({"name": name, "role": r, "bio": f"在{scenario_type}背景下，一个试图改变命运的{r}。"})
    return presets

def mock_ai_generator(name, age, bio, s_type):
    time.sleep(1)
    stats = {}
    if s_type == "三国": stats = {"统率": random.randint(40,95), "武力": random.randint(30,99), "智力": random.randint(30,95), "政治": random.randint(30,90), "魅力": random.randint(50,90)}
    elif s_type == "现代": stats = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(0,100), "心情": 80}
    elif s_type == "修仙": stats = {"根骨": random.randint(10,100), "悟性": random.randint(10,100), "福源": random.randint(10,100), "神识": random.randint(10,100), "灵力": 0}
    elif s_type == "末日": stats = {"战术": random.randint(40,90), "射击": random.randint(40,90), "体质": random.randint(40,90), "理智": 80, "运气": random.randint(10,90)}
    else: stats = {"力量": 50, "敏捷": 50, "体质": 50, "智力": 50, "感知": 50}

    traits = [{"name": "坚韧", "desc": "抗压能力强"}, {"name": "强运", "desc": "运气爆棚"}, {"name": "平庸", "desc": "无特殊效果"}]
    
    return {
        "polished_bio": f"【系统档案】\n姓名：{name}\n年龄：{age}\n评估：{bio}\n(系统注：此人命格奇特，若接入真实API，此处将生成500字深度背景故事...)",
        "stats": stats,
        "traits": traits,
        "npcs": [{"name": "神秘人", "role": "观察者", "rel": 0, "desc": "暗中注视"}]
    }

# ==========================================
# 4. 页面控制
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'presets' not in st.session_state: st.session_state.presets = []

def nav(p): st.session_state.page = p; st.rerun()

# --- 首页 ---
if st.session_state.page == 'home':
    st.markdown("<h1>你的新人生</h1>", unsafe_allow_html=True)
    
    with st.expander("🔌 API 配置"):
        st.text_input("API URL", value="https://api.openai.com/v1")
        st.text_input("API Key", type="password")

    tabs = st.tabs(["🔥 三国乱世", "🏙️ 现代都市", "🏔️ 问道修仙", "☢️ 末日求生", "🌌 虚空创世"])
    
    def render(key, idx):
        with tabs[idx]:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, s in enumerate(SCENARIOS[key]):
                with cols[i%2]:
                    # 卡片容器
                    st.markdown(f"""
                    <div class="hud-container" style="border-left: 5px solid #FF4B2B;">
                        <div style="font-size:1.2rem; font-weight:bold; color:#fff; margin-bottom:5px;">{s['name']}</div>
                        <div style="color:#aaa; font-size:0.95rem;">{s['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"进入世界: {s['name']}", key=s['id'], use_container_width=True):
                        st.session_state.curr = {"type": key, "info": s}
                        st.session_state.presets = generate_presets(key, s['id'])
                        nav('create')
    
    render("三国", 0)
    render("现代", 1)
    render("修仙", 2)
    render("末日", 3)
    
    with tabs[4]:
        st.markdown("<br><div class='hud-container'>", unsafe_allow_html=True)
        w = st.text_area("输入你的世界观", height=150)
        if st.button("开始创世", use_container_width=True):
            st.session_state.curr = {"type": "自定义", "info": {"name": "自定义位面", "desc": w, "id": "custom"}}
            st.session_state.presets = generate_presets("自定义", "custom")
            nav('create')
        st.markdown("</div>", unsafe_allow_html=True)

# --- 创建页 ---
elif st.session_state.page == 'create':
    curr = st.session_state.curr
    
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 返回"): nav('home')
    c2.markdown(f"## {curr['type']} > {curr['info']['name']}")
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.markdown("### 🎲 推荐身份")
        for i, p in enumerate(st.session_state.presets):
            if st.button(f"【{p['name']}】 {p['role']}", key=f"p{i}", use_container_width=True):
                st.session_state.u_name = p['name']
                st.session_state.u_bio = p['bio']
                st.rerun()
        if st.button("🔄 刷新"):
            st.session_state.presets = generate_presets(curr['type'], curr['info']['id'])
            st.rerun()

    with col_r:
        st.markdown("### ✍️ 档案录入")
        with st.form("c_form"):
            name = st.text_input("姓名", value=st.session_state.get('u_name', ''))
            age = st.slider("年龄", 1, 100, 20)
            bio = st.text_area("背景故事", value=st.session_state.get('u_bio', ''), height=150)
            
            if st.form_submit_button("生成角色", use_container_width=True):
                if name and bio:
                    with st.spinner("AI 正在构建..."):
                        res = mock_ai_generator(name, age, bio, curr['type'])
                        st.session_state.char = {"name": name, "age": age, "hp": 100, "data": res}
                        nav('preview')

# --- 预览页 (重构：紧凑美观布局) ---
elif st.session_state.page == 'preview':
    c = st.session_state.char
    d = c['data']
    
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 重塑"): nav('create')
    c2.markdown("## 身份确认")
    
    # 布局：左(剧情与特质) 1.5 : 右(雷达与属性) 1
    col_bio, col_stats = st.columns([1.5, 1])
    
    with col_bio:
        # 人物档案卡
        st.markdown(f"""
        <div class="hud-container">
            <div class="hud-header">{c['name']} <span style="font-size:0.8rem; color:#888; margin-left:10px;">AGE: {c['age']}</span></div>
            <p style="line-height:1.8; color:#ddd;">{d['polished_bio']}</p>
            <br>
            <div style="margin-top:10px;">
                <div style="font-size:0.9rem; color:#aaa; margin-bottom:5px;">天赋特质</div>
                {''.join([f'<span class="trait-capsule">{t["name"]}</span>' for t in d['traits']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("✅ 确认档案并开始", type="primary", use_container_width=True, on_click=lambda: nav('game'))

    with col_stats:
        # 雷达图 + 属性网格
        st.markdown('<div class="hud-container">', unsafe_allow_html=True)
        
        # 1. 雷达图 (上方)
        df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.3)',
                radialaxis=dict(visible=False, range=[0, 100]),
                angularaxis=dict(color='#00d4ff', size=10)
            ),
            margin=dict(l=20,r=20,t=10,b=10),
            dragmode=False
        )
        fig.update_traces(fill='toself', line_color='#00d4ff', fillcolor='rgba(0, 212, 255, 0.2)')
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        
        # 2. 紧凑属性网格 (下方)
        # 使用 HTML 生成紧凑网格
        grid_html = '<div class="stat-grid">'
        for k, v in d['stats'].items():
            grid_html += f'<div class="stat-box"><span class="stat-label">{k}</span><span class="stat-value">{v}</span></div>'
        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 游戏页 ---
elif st.session_state.page == 'game':
    c1, c2 = st.columns([1, 10])
    if c1.button("退出"): nav('home')
    c2.markdown(f"**第 1 天** | {st.session_state.curr['info']['name']}")
    st.info("UI 重构完毕：背景升级为深空蓝，信息面板采用 HUD 网格布局，字体全线优化。")

