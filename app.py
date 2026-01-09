import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 视觉引擎 V6.5 (基于V6结构的精准优化)
# ==========================================
st.set_page_config(layout="wide", page_title="你的新人生", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
    
    /* 1. 背景重构：深灰 + 淡紫 + 深蓝 星云渐变 */
    .stApp {
        background: radial-gradient(100% 100% at 50% 0%, #2d2b3e 0%, #1f2029 50%, #0f1016 100%);
        font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif !important;
        color: #e0e6ed;
    }

    /* 2. 输入框强制修正 (解决白底白字问题) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #252630 !important; /* 深蓝灰背景 */
        color: #ffffff !important;             /* 纯白文字 */
        border: 1px solid #4a4e69 !important;  /* 淡紫边框 */
        border-radius: 4px;
        font-weight: 500;
    }
    /* 输入框上方的 Label 高亮 */
    .stTextInput label, .stTextArea label, .stSlider label, .stNumberInput label {
        color: #a29bfe !important; /* 淡紫色高亮 */
        font-size: 1.1rem !important;
        font-weight: bold !important;
        letter-spacing: 1px;
    }

    /* 3. Tab 导航栏 (保持 V6 的大尺寸设计) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 4px;
        flex-grow: 1;
    }
    .stTabs [data-baseweb="tab"] div {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #888;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #6c5ce7, #0984e3); /* 紫蓝渐变 */
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] div {
        color: white !important;
    }

    /* 4. 紧凑型属性网格 (修复预览页空隙过大) */
    .stat-grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 两列展示 */
        gap: 8px;
        margin-top: 10px;
        background: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 6px;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #444;
        padding: 4px 0;
    }
    .stat-name { color: #aaa; font-size: 0.9rem; }
    .stat-val { color: #00d2d3; font-weight: bold; font-family: monospace; font-size: 1.1rem; }

    /* 通用卡片 */
    .game-card {
        background: rgba(35, 35, 45, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 剧本数据库 (保持 V6 完整性)
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
        {"id": "m1", "name": "2008 · 激荡三十年", "desc": "【黄金时代】奥运盛典，金融海啸，智能手机前夜。这是改变命运的最佳年份。"},
        {"id": "m2", "name": "2015 · 流量帝国", "desc": "【风口之猪】短视频爆发，千播大战。只要敢露脸，人人都能成名15分钟。"},
        {"id": "m3", "name": "2020 · 静默世界", "desc": "【生存挑战】未知的流行病席卷全球。居家隔离的日子里，如何守护家庭？"},
        {"id": "m4", "name": "2026 · 当下·围城", "desc": "【现实主义】考公、内卷、房贷。在存量博弈的时代，普通人如何突围？"},
        {"id": "m5", "name": "2060 · 奇点降临", "desc": "【东方赛博】仿生人普及，图灵法案废除。你发现你的AI伴侣产生了自我意识。"}
    ],
    "修仙": [
        {"id": "x1", "name": "合欢宗 · 魅影", "desc": "【情缘流】游走正魔，以情证道。让圣女动心，让魔头挡劫。"},
        {"id": "x2", "name": "荒古圣体 · 霸途", "desc": "【无敌流】肉身无双，举世皆敌。一条用拳头杀出来的登天路。"},
        {"id": "x3", "name": "戒指老爷爷 · 凡人", "desc": "【养成流】被退婚的废柴，随身老爷爷指点迷津，莫欺少年穷。"},
        {"id": "x4", "name": "夺舍 · 魔尊归来", "desc": "【策略流】满级魔尊夺舍正道杂役。扮猪吃虎，重回巅峰。"}
    ],
    "末日": [
        {"id": "d1", "name": "尸潮 · 燕京沦陷", "desc": "【生化危机】千万人口的都城一夜瘫痪。手里只有一把菜刀，邻居在挠门。"},
        {"id": "d2", "name": "战争 · 东方防线", "desc": "【硬核军事】核冬笼罩，坚守长江防线。敌人不仅是军队，还有辐射。"},
        {"id": "d3", "name": "智械 · 机械天网", "desc": "【人机战争】2090年，超级AI觉醒。人类在钢铁洪流下苟延残喘。"}
    ]
}

# ==========================================
# 3. 智能生成引擎 (无改动，保持稳定)
# ==========================================

HISTORY_HEROES = {
    "s1": [{"name": "曹操", "role": "校尉", "bio": "热血青年，意图刺董。"}, {"name": "董卓", "role": "相国", "bio": "残暴无道，权倾朝野。"}, {"name": "刘备", "role": "县尉", "bio": "织席贩履，胸怀大志。"}],
    "s4": [{"name": "诸葛亮", "role": "军师", "bio": "隆中对策，三分天下。"}, {"name": "周瑜", "role": "都督", "bio": "雅量高致，火烧赤壁。"}, {"name": "赵云", "role": "将军", "bio": "浑身是胆，忠勇无双。"}]
}

def generate_presets(scenario_type, scenario_id):
    if scenario_type == "三国" and scenario_id in HISTORY_HEROES: return HISTORY_HEROES[scenario_id]
    presets = []
    last_names = "赵钱孙李周吴郑王冯陈"
    given_names = ["伟", "芳", "强", "敏", "军", "丽", "杰", "静"]
    role_map = {
        "三国": ["流民", "逃兵", "富商", "书生"],
        "现代": ["大厂员工", "外卖员", "医生", "老师", "拆二代"],
        "修仙": ["杂役", "散修", "世家子", "乞丐"],
        "末日": ["退伍兵", "护士", "卡车司机", "学生"],
        "自定义": ["旅人", "土著", "勇者"]
    }
    roles = role_map.get(scenario_type, role_map["自定义"])
    for _ in range(5):
        name = random.choice(last_names) + random.choice(given_names)
        r = random.choice(roles)
        presets.append({"name": name, "role": r, "bio": f"在{scenario_type}背景下，一个试图改变命运的{r}。"})
    return presets

def mock_ai_generator(name, age, bio, s_type):
    time.sleep(1)
    # 属性生成
    stats = {}
    if s_type == "三国": stats = {"统率": random.randint(40,95), "武力": random.randint(30,99), "智力": random.randint(30,95), "政治": random.randint(30,90), "魅力": random.randint(50,90)}
    elif s_type == "现代": stats = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(0,100), "心情": 80}
    elif s_type == "修仙": stats = {"根骨": random.randint(10,100), "悟性": random.randint(10,100), "福源": random.randint(10,100), "神识": random.randint(10,100), "灵力": 0}
    elif s_type == "末日": stats = {"战术": random.randint(40,90), "射击": random.randint(40,90), "体质": random.randint(40,90), "理智": 80, "运气": random.randint(10,90)}
    else: stats = {"力量": 50, "敏捷": 50, "体质": 50, "智力": 50, "感知": 50}

    # 特质逻辑
    traits = []
    bio_text = str(bio) + str(name)
    if "剑" in bio_text: traits.append({"name": "剑心", "desc": "剑系伤害+20%"})
    if "强" in bio_text or "兵" in bio_text: traits.append({"name": "格斗", "desc": "近战判定+10"})
    while len(traits) < 3:
        t = random.choice([{"name": "坚韧", "desc": "抗压能力强"}, {"name": "强运", "desc": "运气爆棚"}, {"name": "平庸", "desc": "无特殊效果"}])
        if t not in traits: traits.append(t)
    return {
        "polished_bio": f"【系统档案】\n姓名：{name}\n年龄：{age}\n评估：{bio}\n(注：接入API后此处将生成完整人物传记)",
        "stats": stats,
        "traits": traits,
        "npcs": [{"name": "神秘人", "role": "观察者", "rel": 0, "desc": "暗中注视"}]
    }

# ==========================================
# 4. 页面路由控制
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
    
    def render_cards(key, t_idx):
        with tabs[t_idx]:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, s in enumerate(SCENARIOS[key]):
                with cols[i%2]:
                    st.markdown(f"""
                    <div class="game-card">
                        <h3 style="margin-top:0; color:#a29bfe;">{s['name']}</h3>
                        <p style="color:#ccc;">{s['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"进入世界: {s['name']}", key=s['id'], use_container_width=True):
                        st.session_state.curr = {"type": key, "info": s}
                        st.session_state.presets = generate_presets(key, s['id'])
                        nav('create')
    render_cards("三国", 0)
    render_cards("现代", 1)
    render_cards("修仙", 2)
    render_cards("末日", 3)
    
    with tabs[4]:
        st.markdown("<br><div class='game-card'>", unsafe_allow_html=True)
        w_in = st.text_area("输入你的世界观", height=150)
        if st.button("开始创世", use_container_width=True):
            st.session_state.curr = {"type": "自定义", "info": {"name": "自定义位面", "desc": w_in, "id": "custom"}}
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

# --- 预览页 (重要优化：紧凑布局) ---
elif st.session_state.page == 'preview':
    c = st.session_state.char
    d = c['data']
    
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 重塑"): nav('create')
    c2.markdown("## 身份确认")
    
    # 左右布局：左侧信息，右侧数据
    col_bio, col_stats = st.columns([1.5, 1])
    
    with col_bio:
        st.markdown(f"""
        <div class="game-card">
            <h2 style="color:#00d2d3; margin:0;">{c['name']}</h2>
            <p style="color:#888;">AGE: {c['age']}</p>
            <hr style="border-color:#444;">
            <p style="line-height:1.8; color:#eee;">{d['polished_bio']}</p>
            <br>
            <div style="background:rgba(0,0,0,0.2); padding:10px; border-radius:4px;">
                <div style="font-size:0.9rem; color:#a29bfe; margin-bottom:5px;">天赋特质</div>
                {''.join([f'<span style="display:inline-block; border:1px solid #6c5ce7; color:#a29bfe; padding:2px 8px; border-radius:4px; margin-right:5px; margin-bottom:5px; font-size:0.85rem;">{t["name"]} ({t["desc"]})</span>' for t in d['traits']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("✅ 确认并开始", type="primary", use_container_width=True, on_click=lambda: nav('game'))

    with col_stats:
        # 使用 HTML/CSS 强制排版：雷达图在上，紧凑数值在下
        st.markdown('<div class="game-card" style="padding:10px;">', unsafe_allow_html=True)
        
        # 1. 雷达图
        try:
            df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            fig.update_layout(
                height=250, # 限制高度
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                polar=dict(
                    bgcolor='rgba(0,0,0,0.3)',
                    radialaxis=dict(visible=False, range=[0, 100]),
                    angularaxis=dict(color='#00d2d3', size=10)
                ),
                margin=dict(l=20,r=20,t=10,b=10),
                dragmode=False
            )
            fig.update_traces(fill='toself', line_color='#00d2d3', fillcolor='rgba(0, 210, 211, 0.2)')
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        except Exception: st.write("图表生成中...")

        # 2. 紧凑数值网格 (核心修复)
        grid_html = '<div class="stat-grid-container">'
        for k, v in d['stats'].items():
            grid_html += f'<div class="stat-row"><span class="stat-name">{k}</span><span class="stat-val">{v}</span></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 游戏页 ---
elif st.session_state.page == 'game':
    c1, c2 = st.columns([1, 10])
    if c1.button("退出"): nav('home')
    c2.markdown(f"**第 1 天** | {st.session_state.curr['info']['name']}")
    st.info("系统就绪。V6.5 修正版：背景已设为星云渐变，输入框清晰可见，预览面板紧凑无缝隙。")

