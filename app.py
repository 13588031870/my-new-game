import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 视觉引擎 V5.0 (高对比度 & 档案风)
# ==========================================
st.set_page_config(layout="wide", page_title="你的新人生", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
    
    /* 全局样式修正 */
    .stApp {
        background: radial-gradient(circle at center, #1e2024 0%, #000000 100%);
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #f0f0f0;
    }

    /* ---------------- 核心修复：文字可读性 ---------------- */
    /* 强制所有输入框 Label 变大、变白 */
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSlider label {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    /* 输入框内部文字 */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* 普通文本颜色提亮 */
    p, li, span {
        color: #d0d0d0 !important;
        font-size: 1.05rem;
    }

    /* ---------------- Tab 导航栏增强 ---------------- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid #444;
        border-radius: 6px;
    }
    .stTabs [data-baseweb="tab"] div {
        font-size: 1.6rem !important;
        font-weight: 900 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%); /* 帝王黄渐变 */
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] div {
        color: #000 !important; /* 选中后文字变黑 */
    }

    /* ---------------- 档案卡片系统 ---------------- */
    .dossier-card {
        background: rgba(30, 32, 38, 0.95);
        border-top: 4px solid #F1C40F; /* 金色顶边 */
        border-bottom: 1px solid #444;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .card-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #F1C40F;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 8px;
        display: flex;
        justify-content: space-between;
    }

    /* ---------------- 剧本描述文本 ---------------- */
    .scenario-desc {
        color: #cccccc !important;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        background: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 4px;
    }

    /* ---------------- 特质条目 ---------------- */
    .trait-row {
        background: rgba(255, 215, 0, 0.1);
        border-left: 3px solid #FFD700;
        padding: 8px 12px;
        margin-bottom: 6px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 史诗级剧本数据库 (Lore Database)
# ==========================================

SCENARIOS = {
    "三国": [
        {"id": "s1", "name": "189年 · 董卓入京", "desc": "【汉室至暗时刻】\n公元189年，洛阳的苍穹被火光染红。十常侍之乱刚刚平息，西凉军阀董卓的铁蹄便踏碎了帝都的宁静。他废少帝，杀太后，夜宿龙床，权倾朝野。此时，曹操尚未刺董，刘备还在编织草鞋，十八路诸侯各怀鬼胎。你置身于这乱世的熔炉，是助纣为虐，还是手持七星宝刀，做那个刺破黑暗的孤勇者？"},
        {"id": "s2", "name": "194年 · 群雄逐鹿", "desc": "【军阀混战时代】\n董卓已死，但和平未至。李傕郭汜祸乱长安，袁绍公孙瓒决战河北，曹操在兖州四面楚歌，孙策以玉玺借兵横扫江东。旧的秩序已然崩塌，新的秩序由刀剑书写。这是野心家的乐园，只要你有兵有粮，草头王也能问鼎九五。"},
        {"id": "s3", "name": "200年 · 官渡之战", "desc": "【北方宿命对决】\n袁绍坐拥四州之地，带甲七十万南下；曹操兵微将寡，粮草将尽。两雄对峙于官渡。这是一场关于后勤、人心与奇谋的豪赌。若你身在袁营，能否识破许攸的背叛？若在曹营，敢不敢夜袭乌巢，一把火烧出个新时代？"},
        {"id": "s4", "name": "208年 · 赤壁鏖兵", "desc": "【三国鼎立序幕】\n曹操挥师百万南下，饮马长江，意图一统山河。孙刘两家在绝望中结盟。这一年的冬天，东南风起，铁索连舟。周公瑾羽扇纶巾，诸葛亮借风祈雨。烈火张天，烧尽了曹公的壮志，也烧出了三分天下的格局。"},
        {"id": "s5", "name": "234年 · 星落五丈原", "desc": "【英雄最后的挽歌】\n蜀汉丞相诸葛亮第六次北伐，身体已至极限。司马懿坚守不出，耗尽了蜀军最后的锐气。秋风萧瑟，长明灯若灭。你是否拥有逆天改命之能，延续大汉最后的气数？"}
    ],
    "现代": [
        {"id": "m1", "name": "2008 · 激荡三十年", "desc": "【黄金时代的开端】\n这是一个悲喜交加的年份。年初的雪灾，五月的国殇，八月的奥运盛典，九月的全球金融海啸。股市从6124点狂泻，楼市在观望中蓄力，智能手机即将改变世界。站在时代的风口浪尖，每一个选择都可能造就十年后的首富。"},
        {"id": "m4", "name": "2026 · 当下·围城", "desc": "【极度写实的生存】\n经济进入存量博弈。考公报录比达到千分之一，大厂裁员成为常态，房贷与育儿成本像两座大山。这不是爽文，这是关于普通人在“内卷”与“躺平”之间挣扎的真实记录。你，能破局吗？"},
        {"id": "m5", "name": "2060 · 奇点降临", "desc": "【东方赛博朋克】\n在上海和深圳的霓虹之下，仿生人已全面融入家庭。由于《图灵法案》的废除，人类与AI的界限模糊不清。你买了一个叫“小艾”的伴侣型仿生人，某天深夜，你发现她似乎正在自行修改核心代码..."}
    ],
    "修仙": [
        {"id": "x1", "name": "合欢宗 · 魅影", "desc": "【魔门情缘流】\n你重生为合欢宗的一名外门弟子。此宗门不重苦修，专攻红尘炼心。你需要游走在正魔两道的天之骄子之间，让圣女为你动凡心，让魔头为你挡天劫。记住，动情是修行的开始，也是陨落的先兆。"},
        {"id": "x2", "name": "荒古圣体 · 霸途", "desc": "【举世皆敌流】\n开局觉醒荒古圣体，肉身无双，同阶无敌。但此体质为天地所不容，进阶消耗资源是常人的百倍。所有宗门都把你视为“人形大药”。这是一条用拳头杀出来的血路，要么踏碎凌霄，要么身死道消。"},
        {"id": "x3", "name": "戒指老爷爷 · 凡人", "desc": "【传统养成流】\n你本是家族弃子，被未婚妻当众退婚。绝望之际，戒指里飘出一个上古残魂：“小娃娃，想变强吗？”从此，你背负着复活恩师的使命，从一个小山村开始，一步步走向诸天万界。"}
    ],
    "末日": [
        {"id": "d1", "name": "尸潮 · 燕京沦陷", "desc": "【本土生化危机】\n不明病毒在燕京爆发的第三天。五环路堵成了钢铁坟墓，地铁站变成了修罗场。你被困在通州的出租屋里，手里只有一把菜刀和三包方便面。门外传来了邻居奇怪的抓挠声..."},
        {"id": "d2", "name": "战争 · 长江防线", "desc": "【硬核军事末世】\n203X年，战争全面爆发。核冬天的阴云笼罩大地，你作为东部战区的预备役，正坚守在长江防线的战壕里。这里没有变异怪，只有呼啸的炮火、辐射尘埃以及比冬天更冷的人心。"}
    ]
}

# ==========================================
# 3. 智能逻辑引擎
# ==========================================

# 历史人物数据库 (保持不变，确保准确性)
HISTORY_HEROES = {
    "s1": [{"name": "曹操", "role": "校尉", "bio": "热血青年，意图刺董。"}, {"name": "董卓", "role": "相国", "bio": "残暴无道，权倾朝野。"}, {"name": "刘备", "role": "县尉", "bio": "织席贩履，胸怀大志。"}],
    "s4": [{"name": "诸葛亮", "role": "军师", "bio": "隆中对策，三分天下。"}, {"name": "周瑜", "role": "都督", "bio": "雅量高致，火烧赤壁。"}, {"name": "赵云", "role": "将军", "bio": "浑身是胆，忠勇无双。"}]
}

def generate_presets(scenario_type, scenario_id):
    """生成推荐人物：历史精确匹配 OR 随机生成"""
    if scenario_type == "三国" and scenario_id in HISTORY_HEROES:
        return HISTORY_HEROES[scenario_id]
    
    # 通用随机池
    presets = []
    first_names = ["张", "李", "王", "赵", "陈", "刘", "林", "杨"]
    last_names = ["伟", "强", "勇", "杰", "涛", "敏", "静", "雪"]
    
    roles_map = {
        "三国": ["流民", "逃兵", "富商", "书生"],
        "现代": ["程序员", "外卖员", "医生", "老师"],
        "修仙": ["杂役", "散修", "世家子", "乞丐"],
        "末日": ["退伍兵", "护士", "司机", "学生"],
        "自定义": ["旅人", "观察者", "土著", "勇者"]
    }
    
    roles = roles_map.get(scenario_type, roles_map["自定义"])
    
    for _ in range(5):
        name = random.choice(first_names) + random.choice(last_names)
        role = random.choice(roles)
        presets.append({"name": name, "role": role, "bio": f"一个在{scenario_type}背景下努力生存的{role}。"})
    
    return presets

def mock_ai_generator(name, age, bio, scenario_type):
    """AI 模拟生成核心 - 增加特质关联性"""
    time.sleep(1)
    
    # 1. 属性生成 (确保不全是0)
    stats = {}
    if scenario_type == "三国": stats = {"统率": random.randint(30,90), "武力": random.randint(30,90), "智力": random.randint(30,90), "政治": random.randint(30,90), "魅力": random.randint(30,90)}
    elif scenario_type == "现代": stats = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(0,100), "心情": 80}
    elif scenario_type == "修仙": stats = {"根骨": random.randint(10,100), "悟性": random.randint(10,100), "福源": random.randint(10,100), "神识": random.randint(10,100), "灵力": 0}
    else: stats = {"力量": random.randint(30,90), "敏捷": random.randint(30,90), "体质": random.randint(30,90), "感知": random.randint(30,90), "意志": random.randint(30,90)}

    # 2. 特质智能匹配 (简单的关键词匹配)
    traits = []
    bio_text = bio + name
    
    if "剑" in bio_text: traits.append({"name": "剑道天才", "desc": "使用剑类武器伤害+20%"})
    if "医" in bio_text: traits.append({"name": "妙手回春", "desc": "治疗效果+30%"})
    if "强" in bio_text or "兵" in bio_text: traits.append({"name": "格斗精通", "desc": "近战判定修正+10"})
    if "智" in bio_text or "谋" in bio_text: traits.append({"name": "算无遗策", "desc": "计谋成功率提升"})
    
    # 补足特质
    defaults = [
        {"name": "坚韧", "desc": "逆境中San值下降减半"},
        {"name": "强运", "desc": "随机事件结果倾向于正面"},
        {"name": "平庸", "desc": "没有任何特殊效果"},
        {"name": "魅力非凡", "desc": "初始好感度+10"}
    ]
    while len(traits) < 3:
        t = random.choice(defaults)
        if t not in traits: traits.append(t)

    # 3. 补充信息
    extra_info = {
        "出身": "幽州涿郡" if scenario_type=="三国" else "江海市",
        "身份": "平民",
        "阵营": "中立"
    }

    return {
        "polished_bio": f"【天机推演】\n{name}，{age}岁。{bio}\n(系统注：此人命格奇特，看似普通，实则暗藏玄机...)",
        "stats": stats,
        "traits": traits,
        "npcs": [{"name": "神秘人", "role": "观察者", "rel": 0, "desc": "暗中注视"}],
        "extra": extra_info
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
    
    # 渲染通用函数
    def render_tab_content(key, tab_index):
        with tabs[tab_index]:
            st.write("")
            cols = st.columns(2)
            for i, s in enumerate(SCENARIOS[key]):
                with cols[i%2]:
                    st.markdown(f"""
                    <div class="dossier-card" style="border-top-color: {'#e63946' if i%2==0 else '#457b9d'};">
                        <div class="card-header">{s['name']}</div>
                        <div class="scenario-desc">{s['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"进入世界 ({s['name']})", key=s['id'], use_container_width=True):
                        st.session_state.curr = {"type": key, "info": s}
                        st.session_state.presets = generate_presets(key, s['id'])
                        nav('create')

    render_tab_content("三国", 0)
    render_tab_content("现代", 1)
    render_tab_content("修仙", 2)
    render_tab_content("末日", 3)
    
    with tabs[4]: # 自定义修复
        st.markdown("<br><div class='dossier-card'>", unsafe_allow_html=True)
        user_world = st.text_area("输入你的世界观...", height=150, help="例如：哈利波特魔法世界")
        if st.button("开始创世", use_container_width=True):
            if user_world:
                st.session_state.curr = {"type": "自定义", "info": {"name": "未知位面", "desc": user_world, "id": "custom"}}
                st.session_state.presets = generate_presets("自定义", "custom")
                nav('create')
        st.markdown("</div>", unsafe_allow_html=True)

# --- 创建页 ---
elif st.session_state.page == 'create':
    curr = st.session_state.curr
    
    # 导航栏
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 返回"): nav('home')
    c2.markdown(f"## {curr['type']} > {curr['info']['name']}")
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.markdown("### 🎲 推荐身份")
        for i, p in enumerate(st.session_state.presets):
            if st.button(f"{p['name']} | {p['role']}", key=f"p{i}", use_container_width=True):
                st.session_state.u_name = p['name']
                st.session_state.u_bio = p['bio']
                st.rerun()
        if st.button("🔄 刷新列表"):
            st.session_state.presets = generate_presets(curr['type'], curr['info']['id'])
            st.rerun()

    with col_r:
        st.markdown("### ✍️ 档案录入")
        with st.form("c_form"):
            # 这里的 label 已经被 CSS 强制改白、变大了
            name = st.text_input("姓名", value=st.session_state.get('u_name', ''))
            age = st.slider("年龄", 1, 100, 20)
            bio = st.text_area("背景故事", value=st.session_state.get('u_bio', ''), height=180)
            
            if st.form_submit_button("生成角色档案", use_container_width=True):
                if name and bio:
                    with st.spinner("AI 正在推演命格..."):
                        res = mock_ai_generator(name, age, bio, curr['type'])
                        st.session_state.char = {"name": name, "age": age, "hp": 100, "data": res}
                        nav('preview')

# --- 预览页 (重构：档案风格) ---
elif st.session_state.page == 'preview':
    c = st.session_state.char
    d = c['data']
    
    c1, c2 = st.columns([1, 10])
    if c1.button("⬅ 重塑"): nav('create')
    c2.markdown("## 📁 绝密档案 (CONFIDENTIAL)")
    
    # 布局：左侧信息，右侧雷达
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown(f"""
        <div class="dossier-card">
            <div class="card-header">基本资料</div>
            <p><strong>姓名：</strong> <span style="color:#F1C40F; font-size:1.2rem;">{c['name']}</span></p>
            <p><strong>年龄：</strong> {c['age']} 岁</p>
            <p><strong>出身：</strong> {d['extra']['出身']} | <strong>身份：</strong> {d['extra']['身份']}</p>
            <hr style="border-color:#555;">
            <p style="color:#ddd; line-height:1.6;">{d['polished_bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dossier-card">
            <div class="card-header">天赋特质 (Traits)</div>
            <!-- 特质列表直接显示，不隐藏在悬停里 -->
            {''.join([f'<div class="trait-row"><strong>[{t["name"]}]</strong>：{t["desc"]}</div>' for t in d['traits']])}
        </div>
        """, unsafe_allow_html=True)
        
        st.button("✅ 确认档案并开始人生", type="primary", use_container_width=True, on_click=lambda: nav('game'))

    with col2:
        st.markdown("<div class='dossier-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>能力评估</div>", unsafe_allow_html=True)
        
        # 修复雷达图颜色：帝王黄
        df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.5)',
                radialaxis=dict(visible=False),
                angularaxis=dict(color='#F1C40F', size=14) # 金色轴字体
            ),
            margin=dict(l=30,r=30,t=20,b=20),
            dragmode=False
        )
        fig.update_traces(fill='toself', line_color='#F1C40F', fillcolor='rgba(241, 196, 15, 0.3)')
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        
        # 数值列表
        for k,v in d['stats'].items():
            st.markdown(f"<div style='display:flex; justify-content:space-between; border-bottom:1px solid #444; padding:5px;'><span>{k}</span><span style='color:#F1C40F; font-weight:bold;'>{v}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 游戏页 ---
elif st.session_state.page == 'game':
    c1, c2 = st.columns([1, 10])
    if c1.button("退出"): nav('home')
    c2.markdown(f"**第 1 天** | {st.session_state.curr['info']['name']}")
    st.success("欢迎进入《你的新人生》。UI重构完毕，全流程已修复。")

