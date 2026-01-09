import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 视觉引擎 V6.0 (修复版：深空星云风)
# ==========================================
st.set_page_config(layout="wide", page_title="你的新人生", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
    
    /* 1. 背景优化：不再是纯黑，而是深空星云渐变 */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #e0e6ed;
    }

    /* 2. 修复输入框：深灰底白字，绝不白底白字 */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #25262b !important; /* 深灰背景 */
        color: #ffffff !important;             /* 亮白文字 */
        border: 1px solid #4a4e57 !important;
        border-radius: 4px;
    }
    /* 输入框上方的 Label */
    .stTextInput label, .stTextArea label, .stSlider label, .stNumberInput label {
        color: #00c6ff !important; /* 赛博蓝高亮 */
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    /* 3. Tab 导航栏回滚：采用你喜欢的 V4.0 大尺寸设计 */
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
        padding: 0 20px;
        flex-grow: 1;
    }
    .stTabs [data-baseweb="tab"] div {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #888;
    }
    /* 选中状态：红蓝渐变 */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #b92b27, #1565C0);
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] div {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* 4. 卡片容器美化 */
    .game-card {
        background: rgba(30, 35, 40, 0.7); /* 半透明磨砂 */
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* 标题美化 */
    h1 {
        background: -webkit-linear-gradient(#eee, #999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
    }
    h3 { color: #f0f0f0 !important; }
    p { color: #cfcfcf !important; line-height: 1.6; }

    /* 按钮美化 */
    div.stButton > button {
        background: linear-gradient(to bottom, #2c3e50, #000000);
        color: #fff;
        border: 1px solid #444;
    }
    div.stButton > button:hover {
        border-color: #00c6ff;
        color: #00c6ff;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 完整剧本数据库 (补全丢失内容)
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
# 3. 智能生成引擎 (修复五维图Bug)
# ==========================================

# 历史人物映射
HISTORY_HEROES = {
    "s1": [{"name": "曹操", "role": "校尉", "bio": "热血青年，意图刺董。"}, {"name": "董卓", "role": "相国", "bio": "残暴无道，权倾朝野。"}, {"name": "刘备", "role": "县尉", "bio": "织席贩履，胸怀大志。"}],
    "s4": [{"name": "诸葛亮", "role": "军师", "bio": "隆中对策，三分天下。"}, {"name": "周瑜", "role": "都督", "bio": "雅量高致，火烧赤壁。"}, {"name": "赵云", "role": "将军", "bio": "浑身是胆，忠勇无双。"}]
}

def generate_presets(scenario_type, scenario_id):
    """生成推荐人物"""
    if scenario_type == "三国" and scenario_id in HISTORY_HEROES:
        return HISTORY_HEROES[scenario_id]
    
    # 随机生成
    presets = []
    # 本土化名字库
    family_names = "赵钱孙李周吴郑王冯陈"
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
        name = random.choice(family_names) + random.choice(given_names)
        role = random.choice(roles)
        presets.append({"name": name, "role": role, "bio": f"一个在{scenario_type}乱世中努力生存的{role}。"})
    
    return presets

def mock_ai_generator(name, age, bio, scenario_type):
    """
    修复点：确保 stats 返回的是纯数字字典，避免 Plotly 绘图失败。
    """
    time.sleep(1)
    
    # 1. 属性生成 (Key-Value)
    stats = {}
    if scenario_type == "三国": 
        stats = {"统率": random.randint(40,95), "武力": random.randint(30,99), "智力": random.randint(30,95), "政治": random.randint(30,90), "魅力": random.randint(50,90)}
    elif scenario_type == "现代": 
        stats = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(0,100), "心情": 80}
    elif scenario_type == "修仙": 
        stats = {"根骨": random.randint(10,100), "悟性": random.randint(10,100), "福源": random.randint(10,100), "神识": random.randint(10,100), "灵力": 0}
    elif scenario_type == "末日":
        stats = {"战术": random.randint(40,90), "射击": random.randint(40,90), "体质": random.randint(40,90), "理智": 80, "运气": random.randint(10,90)}
    else: 
        stats = {"力量": 50, "敏捷": 50, "体质": 50, "智力": 50, "感知": 50}

    # 2. 特质生成 (智能匹配)
    traits = []
    bio_text = str(bio) + str(name)
    
    if "剑" in bio_text: traits.append({"name": "剑心", "desc": "剑系伤害+20%"})
    if "强" in bio_text or "兵" in bio_text: traits.append({"name": "格斗", "desc": "近战判定+10"})
    if "智" in bio_text or "谋" in bio_text: traits.append({"name": "鬼谋", "desc": "计策成功率UP"})
    
    while len(traits) < 3:
        t = random.choice([
            {"name": "坚韧", "desc": "抗压能力强"},
            {"name": "强运", "desc": "运气爆棚"},
            {"name": "平庸", "desc": "无特殊效果"},
            {"name": "富有", "desc": "初始金钱+500"}
        ])
        if t not in traits: traits.append(t)

    return {
        "polished_bio": f"【系统档案】\n姓名：{name}\n年龄：{age}\n评估：{bio}\n(系统注：此人命格奇特...)",
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

    # 渲染 Tab
    tabs = st.tabs(["🔥 三国乱世", "🏙️ 现代都市", "🏔️ 问道修仙", "☢️ 末日求生", "🌌 虚空创世"])
    
    def render_cards(key, t_idx):
        with tabs[t_idx]:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, s in enumerate(SCENARIOS[key]):
                with cols[i%2]:
                    # 卡片渲染
                    st.markdown(f"""
                    <div class="game-card">
                        <h3 style="margin-top:0; color:#00c6ff;">{s['name']}</h3>
                        <p>{s['desc']}</p>
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
        w_in = st.text_area("输入你的世界观 (例如：赛博朋克2077，我是个黑客)", height=150)
        if st.button("开始创世", use_container_width=True):
            st.session_state.curr = {"type": "自定义", "info": {"name": "自定义位面", "desc": w_in, "id": "custom"}}
            st.session_state.presets = generate_presets("自定义", "custom")
            nav('create')
        st.markdown("</div>", unsafe_allow_html=True)

# --- 创建页 ---
elif st.session_state.page == 'create':
    curr = st.session_state.curr
    
    # 顶部导航
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

# --- 预览页 ---
elif st.session_state.page == 'preview':
    c = st.session_state.char
    d = c['data']
    
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 重塑"): nav('create')
    c2.markdown("## 身份确认")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown(f"""
        <div class="game-card">
            <h2 style="color:#00c6ff; margin-top:0;">{c['name']}</h2>
            <p><strong>年龄：</strong> {c['age']} 岁</p>
            <hr style="border-color:#555;">
            <p>{d['polished_bio']}</p>
            <br>
            <h4 style="color:#eee;">天赋特质</h4>
            {''.join([f'<div style="background:#333; padding:5px 10px; margin:2px 0; border-left:3px solid #00c6ff;"><strong>{t["name"]}</strong>：{t["desc"]}</div>' for t in d['traits']])}
        </div>
        """, unsafe_allow_html=True)
        st.button("✅ 确认并开始", type="primary", use_container_width=True, on_click=lambda: nav('game'))

    with col2:
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#eee; text-align:center;'>能力雷达</h4>", unsafe_allow_html=True)
        
        # 修复雷达图渲染问题
        try:
            df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                polar=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    radialaxis=dict(visible=False, range=[0, 100]),
                    angularaxis=dict(color='#ccc')
                ),
                margin=dict(l=20,r=20,t=20,b=20),
                dragmode=False
            )
            fig.update_traces(fill='toself', line_color='#00c6ff', fillcolor='rgba(0, 198, 255, 0.3)')
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        except Exception as e:
            st.error(f"图表渲染失败: {e}")

        # 显示数值
        st.table(pd.DataFrame(list(d['stats'].items()), columns=['属性', '数值']).set_index('属性'))
        st.markdown("</div>", unsafe_allow_html=True)

# --- 游戏页 ---
elif st.session_state.page == 'game':
    c1, c2 = st.columns([1, 10])
    if c1.button("退出"): nav('home')
    c2.markdown(f"**第 1 天** | {st.session_state.curr['info']['name']}")
    st.balloons()
    st.info("UI 修复完毕。背景更换为深空蓝，剧本内容已补全，输入框清晰度已修复。")

