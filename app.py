import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 视觉引擎 V4.0 (本土化 & 巨型Tab优化)
# ==========================================
st.set_page_config(layout="wide", page_title="你的新人生", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
    
    /* 全局中文化 */
    .stApp {
        background: radial-gradient(circle at center, #202025 0%, #050505 100%);
        font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif !important;
        color: #e0e6ed;
    }

    /* -------------------------------------------
       核心修改：巨型模块导航栏 (Tabs Override)
    ------------------------------------------- */
    /* Tab 容器 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding-bottom: 20px;
    }
    /* 单个 Tab 按钮 */
    .stTabs [data-baseweb="tab"] {
        height: 60px; /* 加高 */
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0 30px;
        flex-grow: 1; /* 撑满宽度 */
    }
    /* Tab 文字样式 (变大) */
    .stTabs [data-baseweb="tab"] div {
        font-size: 1.5rem !important; /* 字体加大 */
        font-weight: 900 !important;
        color: #888;
    }
    /* 选中状态 */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #b92b27, #1565C0); /* 红蓝渐变 */
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] div {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* ---------------- HUD 卡片系统 ---------------- */
    .hud-card {
        background: rgba(35, 35, 40, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .hud-card-title {
        color: #a0a0a0;
        font-size: 0.9rem;
        letter-spacing: 1px;
        margin-bottom: 10px;
        border-bottom: 1px solid #444;
        padding-bottom: 5px;
    }
    
    /* 标题样式 */
    h1 {
        font-size: 4rem !important;
        background: linear-gradient(to right, #ffffff, #888888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 10px !important;
    }
    
    /* 按钮优化 */
    div.stButton > button {
        background-color: #333;
        color: white;
        border: 1px solid #555;
        font-size: 1rem;
        padding: 12px 24px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #e63946; /* 中国红高亮 */
        border-color: #e63946;
        transform: translateY(-2px);
    }
    
    /* 推荐人物卡片 */
    .preset-card {
        border: 1px solid #444;
        padding: 10px;
        background: #1a1a1a;
        margin-bottom: 10px;
        cursor: pointer;
        transition: 0.2s;
    }
    .preset-card:hover {
        border-color: #e63946;
        background: #252525;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 本土化数据逻辑引擎
# ==========================================

# --- 三国历史人物库 (按年代精确匹配) ---
HISTORY_HEROES = {
    # 189年: 董卓乱政时期
    "s1": [
        {"name": "曹操", "role": "骁骑校尉", "bio": "此时的曹孟德还是个热血青年，手持七星宝刀，意图刺杀国贼。"},
        {"name": "董卓", "role": "西凉刺史", "bio": "权倾朝野的魔王。如果你想体验反派的快感，这是最佳选择。"},
        {"name": "刘备", "role": "县尉", "bio": "还在编草鞋的汉室宗亲，虽然落魄，但身后跟着两个万人敌。"},
        {"name": "吕布", "role": "董卓义子", "bio": "人中吕布，马中赤兔。武力值天花板，但智力堪忧。"},
        {"name": "袁绍", "role": "盟主", "bio": "四世三公，名门望族。此时的他意气风发，号令天下诸侯。"}
    ],
    # 208年: 赤壁时期
    "s4": [
        {"name": "诸葛亮", "role": "蜀军军师", "bio": "躬耕陇亩刚出山。这一年，他要借东风，烧战船。"},
        {"name": "周瑜", "role": "东吴大都督", "bio": "雄姿英发，羽扇纶巾。谈笑间，樯橹灰飞烟灭。"},
        {"name": "曹操", "role": "大汉丞相", "bio": "此时已统一北方，挥师百万南下，是他离天下统一最近的一次。"},
        {"name": "赵云", "role": "牙门将军", "bio": "长坂坡七进七出。忠肝义胆，浑身是胆。"},
        {"name": "孙权", "role": "江东之主", "bio": "生子当如孙仲谋。不仅要防曹操，还要防身边的盟友。"}
    ]
}

# --- 现代/末日随机中文名库 ---
CN_SURNAMES = list("赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜")
CN_GIVEN_NAMES_M = ["伟", "强", "军", "磊", "涛", "明", "超", "秀", "杰", "刚", "平", "辉"]
CN_GIVEN_NAMES_F = ["芳", "娜", "敏", "静", "丽", "艳", "娟", "霞", "洁", "婷", "琳", "薇"]

def get_random_cn_name():
    """生成真实的中文名"""
    surname = random.choice(CN_SURNAMES)
    given = random.choice(CN_GIVEN_NAMES_M + CN_GIVEN_NAMES_F)
    if random.random() > 0.5: given += random.choice(CN_GIVEN_NAMES_M + CN_GIVEN_NAMES_F)
    return surname + given

def generate_localized_presets(scenario_type, scenario_id):
    """
    智能推荐系统：
    1. 三国：根据具体年份返回历史人物。
    2. 其他：生成具有中国特色的随机人物。
    """
    # 1. 历史精确匹配模式
    if scenario_type == "三国" and scenario_id in HISTORY_HEROES:
        return HISTORY_HEROES[scenario_id]
    
    # 2. 随机生成模式 (保底)
    presets = []
    
    if scenario_type == "三国": # 其他年份的随机
        roles = ["西凉骑兵", "黄巾余党", "落魄书生", "世家子弟"]
        bios = ["在这个乱世中寻找活下去的机会。", "希望能投奔一位明主。", "家里有三千亩良田，但被兵灾毁了。"]
    elif scenario_type == "现代":
        roles = ["大厂程序员", "外卖骑手", "考研党", "拆二代", "创业老板", "小镇做题家"]
        bios = ["每天在燕京的地铁里挤两个小时通勤。", "虽然身家过亿，但感到精神空虚。", "背负着三十年房贷，不敢辞职。", "试图在直播风口中分一杯羹。"]
    elif scenario_type == "修仙":
        roles = ["外门弟子", "杂役", "修真家族少爷", "凡人", "魔教卧底"]
        bios = ["资质平平，但捡到了一个神秘小绿瓶。", "被未婚妻退婚，立誓要报仇。", "天生灵根残缺，被家族遗弃。"]
    else: # 末日
        roles = ["退伍军人", "外科医生", "卡车司机", "在校大学生", "机械修理工"]
        bios = ["在江海市避难所苟延残喘。", "手里只有一把扳手和半块压缩饼干。", "为了寻找失散的女儿，穿越了整个沦陷区。"]
    
    for _ in range(5):
        name = get_random_cn_name()
        if scenario_type == "末日":
            if random.random() > 0.7: name = "老" + name[0] # 比如 "老张"
        
        r = random.choice(roles)
        presets.append({
            "name": name,
            "role": r,
            "bio": f"{name}，{r}。{random.choice(bios)}"
        })
        
    return presets

# 剧本数据 (更新文字为中文语境)
SCENARIOS = {
    "三国": [
        {"id": "s1", "name": "189年 · 董卓入京", "desc": "【汉末开端】洛阳火起，国贼当道。"},
        {"id": "s2", "name": "194年 · 群雄逐鹿", "desc": "【诸侯混战】中原大地，军阀混战。"},
        {"id": "s3", "name": "200年 · 官渡之战", "desc": "【北方决战】曹袁对峙，以弱胜强。"},
        {"id": "s4", "name": "208年 · 赤壁鏖兵", "desc": "【三国鼎立】火烧连营，划江而治。"},
        {"id": "s5", "name": "234年 · 星落五丈原", "desc": "【英雄迟暮】秋风萧瑟，孔明归天。"}
    ],
    "现代": [
        {"id": "m1", "name": "2008 · 激荡三十年", "desc": "【黄金时代】奥运、股市与大国崛起。"},
        {"id": "m4", "name": "2026 · 当下·围城", "desc": "【现实主义】内卷、考公与房贷压力。"},
        {"id": "m5", "name": "2060 · 奇点降临", "desc": "【未来科幻】仿生人技术在东方普及。"}
    ],
    "修仙": [
        {"id": "x1", "name": "合欢宗 · 魅影", "desc": "【情缘流】游走正魔，以情证道。"},
        {"id": "x2", "name": "荒古圣体 · 霸途", "desc": "【无敌流】举世皆敌，唯我独尊。"},
        {"id": "x3", "name": "戒指老爷爷 · 凡人", "desc": "【养成流】药老相助，逆天改命。"},
        {"id": "x4", "name": "夺舍 · 魔尊归来", "desc": "【策略流】满级账号，重练小号。"}
    ],
    "末日": [
        {"id": "d1", "name": "尸潮 · 燕京沦陷", "desc": "【生化危机】拥有两千万人口的都城一夜瘫痪。"},
        {"id": "d2", "name": "战争 · 东方防线", "desc": "【硬核军事】在核冬天的废墟中守卫长江防线。"},
        {"id": "d3", "name": "智械 · 机械天网", "desc": "【赛博末日】被AI统治的东方大陆。"}
    ]
}

# 模拟 AI 生成 (中文优化)
def mock_ai_generator(name, age, bio, scenario):
    time.sleep(1)
    # 根据背景微调属性
    npcs = []
    if scenario == "三国":
        npcs = [{"name": "荀彧", "role": "令君", "rel": 10, "desc": "对你的才华颇为赞赏"}, {"name": "吕布", "role": "温侯", "rel": -20, "desc": "看你不太顺眼"}]
    elif scenario == "现代":
        npcs = [{"name": "张总", "role": "直属领导", "rel": -5, "desc": "准备把你优化掉"}, {"name": "李阿姨", "role": "邻居", "rel": 30, "desc": "想给你介绍对象"}]
    elif scenario == "末日":
        npcs = [{"name": "王队长", "role": "搜救队", "rel": 50, "desc": "救过你的命"}, {"name": "变异体0号", "role": "未知", "rel": -100, "desc": "在暗处盯着你"}]
    else:
        npcs = [{"name": "大师姐", "role": "护道者", "rel": 60, "desc": "对你青眼有加"}]

    return {
        "polished_bio": f"【天机阁档案】\n姓名：{name}\n骨龄：{age}\n背景概述：{bio}\n(系统批注：此子命格不凡，入局之时，东方震动...)",
        "stats": {k: random.randint(30, 95) for k in ["体质/武力", "智力/悟性", "魅力/交际", "家境/资源", "运气"]},
        "traits": [{"name": "龙的传人", "desc": "在东方背景下全属性+5"}, {"name": "坚韧", "desc": "逆境中生存能力极强"}],
        "npcs": npcs
    }

# ==========================================
# 3. 页面逻辑控制
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'presets' not in st.session_state: st.session_state.presets = []

def navigate(p):
    st.session_state.page = p
    st.rerun()

# --- 首页：你的新人生 ---
if st.session_state.page == 'home':
    st.markdown("<h1>你的新人生</h1>", unsafe_allow_html=True)
    
    with st.expander("⚙️ API 配置 (可选)"):
        st.text_input("API 地址", value="https://api.openai.com/v1")
        st.text_input("API Key", type="password")

    # 巨型 Tabs
    tab_names = ["🔥 三国乱世", "🏙️ 现代都市", "🏔️ 问道修仙", "☢️ 末日求生", "🌌 虚空创世"]
    tabs = st.tabs(tab_names)

    def render_scenario_list(key, tab_idx):
        with tabs[tab_idx]:
            st.markdown("<br>", unsafe_allow_html=True) # 增加间距
            cols = st.columns(2) # 双列布局，更大气
            for i, s in enumerate(SCENARIOS[key]):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="hud-card" style="border-left: 5px solid #e63946;">
                        <h3 style="margin-top:0; color: white;">{s['name']}</h3>
                        <p style="color: #aaa; font-size: 1rem;">{s['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"进入世界", key=s['id'], use_container_width=True):
                        st.session_state.current_scenario = {"type": key, "info": s}
                        # 生成特定的历史/本土化推荐人物
                        st.session_state.presets = generate_localized_presets(key, s['id'])
                        navigate('create')

    render_scenario_list("三国", 0)
    render_scenario_list("现代", 1)
    render_scenario_list("修仙", 2)
    render_scenario_list("末日", 3)
    
    with tabs[4]:
        st.markdown("<br><div class='hud-card'>", unsafe_allow_html=True)
        st.text_area("输入你的世界观...", height=150)
        st.button("开始创世", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 角色创建页 ---
elif st.session_state.page == 'create':
    scen = st.session_state.current_scenario
    
    # 顶部栏
    c1, c2 = st.columns([1, 8])
    if c1.button("⬅ 返回"): navigate('home')
    c2.markdown(f"## {scen['type']} > {scen['info']['name']}")
    
    col_l, col_r = st.columns([1.2, 2])
    
    with col_l:
        st.markdown("### 🎲 推荐身份 (已本土化)")
        for i, p in enumerate(st.session_state.presets):
            # 推荐人物卡片
            if st.button(f"【{p['name']}】 {p['role']}", key=f"pre_{i}", use_container_width=True):
                st.session_state.user_input_name = p['name']
                st.session_state.user_input_bio = p['bio']
                st.rerun()
        
        if st.button("🔄 换一批"):
            st.session_state.presets = generate_localized_presets(scen['type'], scen['info']['id'])
            st.rerun()

    with col_r:
        st.markdown("### ✍️ 撰写人生")
        with st.form("create_form"):
            name = st.text_input("姓名", value=st.session_state.get('user_input_name', ''))
            age = st.slider("年龄", 1, 100, 20)
            bio = st.text_area("人物背景", value=st.session_state.get('user_input_bio', ''), height=200)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("开始新的人生", use_container_width=True):
                if name and bio:
                    with st.spinner("正在推演天机..."):
                        res = mock_ai_generator(name, age, bio, scen['type'])
                        st.session_state.character = {"name": name, "age": age, "hp": 100, "energy": 5, "luck": 88, "data": res}
                        navigate('preview')

# --- 预览页 ---
elif st.session_state.page == 'preview':
    c = st.session_state.character
    d = c['data']
    
    c1, c2 = st.columns([1, 8])
    if c1.button("⬅ 重塑"): navigate('create')
    c2.markdown("## 身份确认")
    
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    
    with col1:
        st.markdown(f"""
        <div class="hud-card">
            <h2 style="color: #e63946; margin:0;">{c['name']}</h2>
            <p>年龄: {c['age']} | 幸运: {c['luck']}</p>
            <hr style="border-color: #444;">
            <p style="line-height: 1.8; color: #ccc;">{d['polished_bio']}</p>
            <br>
            <div class="hud-card-title">天赋特质</div>
            {' '.join([f'<span style="background:#333; padding:2px 8px; border:1px solid #555;">{t["name"]}</span>' for t in d['traits']])}
        </div>
        """, unsafe_allow_html=True)
        st.button("✅ 确认并进入游戏", type="primary", use_container_width=True, on_click=lambda: navigate('game'))

    with col2:
        st.markdown("<div class='hud-card-title'>能力雷达</div>", unsafe_allow_html=True)
        df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(bgcolor='rgba(0,0,0,0.5)', radialaxis=dict(visible=False), angularaxis=dict(color='#ccc')),
            margin=dict(l=20,r=20,t=20,b=20),
            dragmode=False
        )
        fig.update_traces(fill='toself', line_color='#e63946')
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        
        st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
        for k,v in d['stats'].items():
            st.write(f"**{k}**: {v}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='hud-card-title'>初始人际网</div>", unsafe_allow_html=True)
        for npc in d['npcs']:
            color = "#4caf50" if npc['rel'] > 0 else "#f44336"
            st.markdown(f"""
            <div class="hud-card" style="padding: 10px; margin-bottom: 10px; border-left: 3px solid {color};">
                <div style="font-weight:bold;">{npc['name']} <span style="font-size:0.8em; color:#888;">{npc['role']}</span></div>
                <div style="font-size:0.8em; color:#aaa;">"{npc['desc']}"</div>
            </div>
            """, unsafe_allow_html=True)

# --- 游戏页 ---
elif st.session_state.page == 'game':
    c1, c2 = st.columns([1, 8])
    if c1.button("退出"): navigate('home')
    c2.markdown(f"**第 1 天** | {st.session_state.current_scenario['info']['name']}")
    st.info("UI 界面本土化重构完成。请检查历史人物生成逻辑与中文排版效果。")
