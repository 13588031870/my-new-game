import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. 游戏级 UI 引擎 (CSS Engine)
# ==========================================
st.set_page_config(layout="wide", page_title="AI Infinite Simulator", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
    
    /* ---------------- 全局重置 ---------------- */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #e0e6ed;
    }
    
    /* ---------------- 导航栏 ---------------- */
    .nav-bar {
        display: flex;
        align-items: center;
        background: rgba(0, 0, 0, 0.4);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 20px;
        margin: -60px -20px 20px -20px; /* 抵消 streamlit 默认 padding */
        backdrop-filter: blur(10px);
    }
    
    /* ---------------- 高密度 HUD 卡片 ---------------- */
    .hud-card {
        background: rgba(30, 35, 45, 0.6);
        border: 1px solid rgba(100, 200, 255, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        border-radius: 4px; /* 硬朗的游戏风格 */
        padding: 15px;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
    }
    .hud-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #00c6ff;
    }
    
    /* ---------------- 标题与排版 ---------------- */
    .hud-title {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #5d6d7e;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 5px;
    }
    .big-stat {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00c6ff;
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
    }
    
    /* ---------------- 按钮系统 ---------------- */
    div.stButton > button {
        background: linear-gradient(180deg, #2b3a4a 0%, #1a2530 100%);
        border: 1px solid #4a5b6c;
        color: #a0b0c0;
        border-radius: 2px;
        font-weight: 600;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background: #00c6ff;
        color: #090a0f;
        border-color: #00eaff;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4);
    }
    
    /* ---------------- 特质标签 ---------------- */
    .trait-box {
        background: rgba(0,0,0,0.3);
        border: 1px solid #333;
        padding: 5px 10px;
        margin: 3px;
        display: inline-block;
        font-size: 0.85rem;
        color: #ffd700;
        cursor: help;
    }
    .trait-box:hover {
        background: #ffd700;
        color: #000;
    }
    
    /* ---------------- NPC 条目 ---------------- */
    .npc-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255,255,255,0.03);
        padding: 8px;
        margin-bottom: 5px;
        border-left: 2px solid #555;
    }
    
    /* ---------------- 推荐人物卡片 (Selectable) ---------------- */
    .preset-btn-container {
        border: 1px solid #333; 
        padding: 10px; 
        background: rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .preset-btn-container:hover {
        border-color: #00c6ff;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 过程生成引擎 (Procedural Generation Engine)
# ==========================================

# 词库：用于伪装 AI 生成推荐人物
NAME_DB = {
    "三国": ["赵", "钱", "孙", "李", "诸葛", "司马", "夏侯", "关", "张"],
    "现代": ["王", "陈", "林", "周", "徐", "马", "张", "刘"],
    "修仙": ["叶", "萧", "林", "方", "韩", "白", "楚", "秦"],
    "末日": ["杰克", "罗根", "莎拉", "艾达", "里昂", "瑞克", "达里尔"]
}
TITLE_DB = {
    "三国": ["猛将", "谋士", "刺客", "隐士", "校尉", "义士"],
    "现代": ["卷王", "投资人", "黑客", "外卖员", "高管", "UP主"],
    "修仙": ["废柴", "圣女", "魔修", "散修", "丹师", "剑痴"],
    "末日": ["特种兵", "医生", "流浪者", "拾荒者", "机械师", "猎人"]
}

def generate_dynamic_presets(scenario_type):
    """根据剧本类型，动态生成 5 个推荐人物"""
    presets = []
    names = NAME_DB.get(scenario_type, ["未", "知"])
    titles = TITLE_DB.get(scenario_type, ["行者"])
    
    for _ in range(5):
        n = random.choice(names) + (chr(random.randint(0x4e00, 0x9fa5)) if scenario_type != "末日" else "")
        role = random.choice(titles)
        # 简单的随机简介生成
        bios = [
            f"一个试图改变命运的{role}。",
            f"怀揣着秘密的{role}，眼神坚毅。",
            f"在这个时代显得格格不入的{role}。",
            f"拥有惊人天赋的{role}，但性格古怪。"
        ]
        presets.append({
            "name": n,
            "role": role,
            "bio": random.choice(bios)
        })
    return presets

# 剧本数据 (更新后)
SCENARIOS = {
    "三国": [
        {"id": "s1", "name": "公元189年 · 董卓入京", "desc": "汉室倾颓，魔王降临洛阳。"},
        {"id": "s2", "name": "公元194年 · 群雄逐鹿", "desc": "旧秩序崩塌，诸侯割据一方。"},
        {"id": "s3", "name": "公元200年 · 官渡之战", "desc": "北方双雄的宿命对决。"},
        {"id": "s4", "name": "公元208年 · 赤壁鏖兵", "desc": "烈火张天，天下三分。"},
        {"id": "s5", "name": "公元234年 · 星落五丈原", "desc": "丞相的最后一次北伐。"}
    ],
    "现代": [
        {"id": "m1", "name": "2008 · 激荡三十年", "desc": "机遇与危机并存的黄金时代。"},
        {"id": "m2", "name": "2015 · 流量帝国", "desc": "每个人都能成名的15分钟。"},
        {"id": "m3", "name": "2020 · 静默世界", "desc": "大流行背景下的生存挑战。"},
        {"id": "m4", "name": "2026 · 当下·围城", "desc": "极致内卷的现实主义生存。"},
        {"id": "m5", "name": "2060 · 奇点降临", "desc": "仿生人与人类的界限消失。"}
    ],
    "修仙": [
        {"id": "x1", "name": "合欢宗 · 魅影", "desc": "以情入道，游走正魔之间。"},
        {"id": "x2", "name": "荒古圣体 · 霸途", "desc": "举世皆敌的无敌之路。"},
        {"id": "x3", "name": "戒指老爷爷 · 博弈", "desc": "废柴逆袭，药老相助。"},
        {"id": "x4", "name": "夺舍 · 魔尊归来", "desc": "满级账号重练新手村。"}
    ],
    "末日": [
        {"id": "d1", "name": "尸潮爆发 · 生化", "desc": "秩序崩塌的最初72小时。"},
        {"id": "d2", "name": "核云之下 · 战争", "desc": "2030三战，硬核军事生存。"},
        {"id": "d3", "name": "智械危机 · 2090", "desc": "天网觉醒，人类的反击。"}
    ]
}

# 核心 AI 模拟器 (Mock)
def mock_ai_generator(name, age, bio, scenario):
    time.sleep(1.2) # 模拟计算延迟
    
    # 属性生成逻辑
    if scenario == "三国":
        stats = {"统率": random.randint(50,95), "武力": random.randint(40,99), "智力": random.randint(40,95), "政治": random.randint(30,85), "魅力": random.randint(50,90)}
        npcs = [
            {"name": "曹操", "role": "枭雄", "rel": -10, "desc": "对你心存疑虑"},
            {"name": "刘备", "role": "皇叔", "rel": 20, "desc": "觉得你相貌不凡"}
        ]
    elif scenario == "现代":
        stats = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(10,100), "心情": 80}
        npcs = [
            {"name": "HR经理", "role": "面试官", "rel": 0, "desc": "正在审视你的简历"},
            {"name": "房东", "role": "债主", "rel": -5, "desc": "准备涨房租"}
        ]
    elif scenario == "修仙":
        stats = {"根骨": random.randint(20,90), "悟性": random.randint(40,100), "福源": random.randint(10,100), "神识": random.randint(30,80), "灵力": 0}
        npcs = [
            {"name": "神秘师姐", "role": "宗门天骄", "rel": 50, "desc": "暗中关注你"},
            {"name": "外门执事", "role": "小反派", "rel": -40, "desc": "想抢你的玉佩"}
        ]
    else: # 末日
        stats = {"战术": random.randint(50,95), "射击": random.randint(60,100), "体质": random.randint(60,90), "理智": 70, "领导": random.randint(20,80)}
        npcs = [
            {"name": "老兵", "role": "幸存者", "rel": 30, "desc": "欣赏你的眼神"},
            {"name": "掠夺者首领", "role": "敌对势力", "rel": -100, "desc": "悬赏你的人头"}
        ]

    # 特质生成 (带详细描述)
    traits = [
        {"name": "天命之人", "desc": "关键时刻运气爆发，全属性判定+5"},
        {"name": "异类", "desc": "初始人际关系-20，但特殊事件触发率提升"},
        {"name": "坚毅", "desc": "San值/心情 消耗减半"}
    ]

    return {
        "polished_bio": f"【系统档案】\n{name}，{age}岁。\n{bio}\n(系统评价：此子入局，必将掀起一番风浪...)",
        "stats": stats,
        "traits": traits,
        "npcs": npcs
    }

# ==========================================
# 3. 状态管理与工具函数
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'presets' not in st.session_state: st.session_state.presets = []

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 4. 页面渲染逻辑
# ==========================================

# --- 首页：剧本选择 ---
if st.session_state.page == 'home':
    # 顶部 Title
    st.markdown("<h1>AI INFINITE SIMULATOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 40px;'>v3.0.1 | 沉浸式模拟引擎 | 深度角色构建</p>", unsafe_allow_html=True)
    
    # API 状态栏 (更隐蔽美观)
    with st.expander("🔌 神经漫游网络配置 (API Settings)"):
        c1, c2 = st.columns([3, 1])
        c1.text_input("Gateway Address", value="https://api.openai.com/v1")
        c2.text_input("Access Key", type="password")

    # 剧本 Tabs
    tabs = st.tabs(["🏛️ 三国乱世", "🏙️ 现代都市", "⚔️ 问道修仙", "☢️ 末日废土", "✨ 虚空创世"])
    
    def render_scenario_list(key):
        for s in SCENARIOS[key]:
            # 使用高密度布局
            col_text, col_btn = st.columns([4, 1])
            with col_text:
                st.markdown(f"""
                <div style="padding: 10px; border-left: 3px solid #00c6ff;">
                    <h3 style="margin:0; color:white;">{s['name']}</h3>
                    <p style="margin:0; font-size:0.9rem; color:#888;">{s['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                # 垂直居中按钮
                st.write("")
                if st.button("INIT", key=s['id'], use_container_width=True):
                    st.session_state.current_scenario = {"type": key, "info": s}
                    # 每次进入创建页，重新生成推荐人物
                    st.session_state.presets = generate_dynamic_presets(key)
                    navigate_to('create')
            st.markdown("---")

    with tabs[0]: render_scenario_list("三国")
    with tabs[1]: render_scenario_list("现代")
    with tabs[2]: render_scenario_list("修仙")
    with tabs[3]: render_scenario_list("末日")
    with tabs[4]:
        st.info("输入一段文字，AI 将自动解析世界观并构建规则。")
        st.text_area("世界观描述", height=100)
        st.button("解析并生成")

# --- 角色创建页 ---
elif st.session_state.page == 'create':
    scen = st.session_state.current_scenario
    
    # 顶部导航
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 返回"): navigate_to('home')
    c2.markdown(f"**当前载入模组：{scen['type']} > {scen['info']['name']}**")
    
    st.markdown("---")

    col_left, col_right = st.columns([1.5, 2])
    
    # 左侧：动态推荐系统
    with col_left:
        st.markdown("<div class='hud-title'>⚡ 快速身份 (AI 生成)</div>", unsafe_allow_html=True)
        
        # 5个推荐人物，使用紧凑型 Grid
        for i, p in enumerate(st.session_state.presets):
            # 模拟卡片按钮
            if st.button(f"{p['name']} | {p['role']}\n{p['bio'][:15]}...", key=f"pre_{i}", use_container_width=True):
                st.session_state.user_input_name = p['name']
                st.session_state.user_input_bio = p['bio']
                st.rerun()
                
        if st.button("🔄 刷新随机库"):
            st.session_state.presets = generate_dynamic_presets(scen['type'])
            st.rerun()

    # 右侧：详细定制
    with col_right:
        st.markdown("<div class='hud-title'>📝 深度定制</div>", unsafe_allow_html=True)
        with st.form("char_create"):
            name = st.text_input("姓名", value=st.session_state.get('user_input_name', ''))
            age = st.slider("骨龄/年龄", 14, 80, 20)
            bio = st.text_area("人物背景 (越详细生成越精准)", value=st.session_state.get('user_input_bio', ''), height=150)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 启动模拟 (GENERATE)", use_container_width=True)
            
            if submit and name and bio:
                with st.spinner("AI 正在构建神经网络..."):
                    res = mock_ai_generator(name, age, bio, scen['type'])
                    st.session_state.character = {
                        "name": name, "age": age,
                        "hp": 100, "energy": 5, "luck": random.randint(1,100),
                        "data": res
                    }
                    navigate_to('preview')

# --- 角色预览与确认页 (核心信息面板) ---
elif st.session_state.page == 'preview':
    c = st.session_state.character
    d = c['data']
    
    # 顶部导航
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 重塑"): navigate_to('create')
    c2.markdown(f"**身份确认阶段**")

    # 布局： 2:1:1
    col_bio, col_stats, col_social = st.columns([2, 1.5, 1.5])
    
    # 1. 左侧：档案卡
    with col_bio:
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:#00c6ff; margin:0;'>{c['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#888;'>年龄: {c['age']} | 幸运: {c['luck']}</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height:1.6;'>{d['polished_bio']}</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='hud-title' style='margin-top:20px;'>🧬 固有特质</div>", unsafe_allow_html=True)
        # 特质显示
        for t in d['traits']:
            st.markdown(f"<span class='trait-box' title='{t['desc']}'>{t['name']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 开始按钮
        st.button("✅ 确认并连接神经元 (START GAME)", type="primary", use_container_width=True, on_click=lambda: navigate_to('game'))

    # 2. 中间：属性面板 (分离 图表 和 数值)
    with col_stats:
        # A. 五维图 (锁定交互，纯视觉)
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        st.markdown("<div class='hud-title'>📊 能力雷达</div>", unsafe_allow_html=True)
        
        df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            dragmode=False, # 禁止拖拽
            margin=dict(l=30, r=30, t=30, b=20), # 修复遮挡
            polar=dict(
                bgcolor='rgba(0,0,0,0.3)',
                radialaxis=dict(visible=False, range=[0, 100]), # 隐藏轴数字
                angularaxis=dict(linecolor='#444', color='#00c6ff')
            )
        )
        fig.update_traces(fill='toself', line_color='#00c6ff', fillcolor='rgba(0, 198, 255, 0.2)')
        # 关键：禁用 Plotly 工具栏
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        st.markdown("</div>", unsafe_allow_html=True)
        
        # B. 详细数值列表
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        st.markdown("<div class='hud-title'>🔢 详细参数</div>", unsafe_allow_html=True)
        for k, v in d['stats'].items():
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; border-bottom:1px solid #333; padding:5px 0;">
                <span style="color:#aaa;">{k}</span>
                <span style="color:#fff; font-weight:bold; font-family:monospace;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. 右侧：社会关系 (羁绊)
    with col_social:
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        st.markdown("<div class='hud-title'>🕸️ 初始人际网</div>", unsafe_allow_html=True)
        
        for npc in d['npcs']:
            # 颜色逻辑：正数为绿，负数为红
            color = "#00ff00" if npc['rel'] > 0 else "#ff0000"
            st.markdown(f"""
            <div style="margin-bottom:15px; background:rgba(0,0,0,0.2); padding:10px; border-left:3px solid {color};">
                <div style="font-weight:bold; color:#fff;">{npc['name']} <span style="font-size:0.8rem; color:#888;">({npc['role']})</span></div>
                <div style="font-size:0.8rem; color:#aaa; margin-top:3px;">"{npc['desc']}"</div>
                <div style="margin-top:5px; height:4px; background:#333; width:100%;">
                    <div style="height:100%; width:{abs(npc['rel'])}%; background:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 资源栏
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        st.markdown("<div class='hud-title'>📦 携带物资</div>", unsafe_allow_html=True)
        st.markdown("<ul><li>新手礼包 x1</li><li>身份铭牌 x1</li></ul>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 游戏主界面 (预留) ---
elif st.session_state.page == 'game':
    # 顶部导航
    c1, c2 = st.columns([1, 10])
    if c1.button("🛑 退出"): navigate_to('home')
    c2.markdown(f"**Day 1** | {st.session_state.current_scenario['info']['name']}")
    
    st.success("UI 架构重构完成。所有已知 UI/UX 痛点已修复。准备接入下一步的 GPT 剧情逻辑。")
