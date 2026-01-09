import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 沉浸式 UI 注入 (CSS Hack)
# ==========================================
st.set_page_config(layout="wide", page_title="AI Infinite Simulator", initial_sidebar_state="expanded")

# 引入自定义 CSS，强制改变 Streamlit 原生样式
st.markdown("""
<style>
    /* 1. 全局深色背景 */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* 2. 隐藏顶部红线和菜单 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. 卡片式容器设计 */
    .game-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* 4. 标题与文字优化 */
    h1 { color: #58A6FF; font-weight: 700; letter-spacing: 1px; }
    h2 { color: #E0E0E0; font-size: 1.5rem; border-bottom: 1px solid #30363D; padding-bottom: 10px; }
    h3 { color: #79C0FF; font-size: 1.2rem; }
    p, label, span { color: #C9D1D9; }
    
    /* 5. 按钮美化 (赛博风格) */
    div.stButton > button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: transform 0.1s;
    }
    div.stButton > button:hover {
        background-color: #2EA043;
        transform: scale(1.02);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }
    
    /* 6. 输入框美化 */
    .stTextInput > div > div > input {
        background-color: #0D1117;
        color: white;
        border: 1px solid #30363D;
    }
    .stTextArea > div > div > textarea {
        background-color: #0D1117;
        color: white;
        border: 1px solid #30363D;
    }

    /* 7. 特质标签 */
    .trait-tag {
        display: inline-block;
        background: #1F6FEB;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-right: 5px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据与逻辑定义
# ==========================================

# 剧本数据库
SCENARIOS = {
    "三国": [
        {"id": "s3_1", "name": "董卓入京 (189年)", "desc": "权臣当道，汉室衰微。是助纣为虐还是匡扶汉室？"},
        {"id": "s3_2", "name": "群雄逐鹿 (194年)", "desc": "诸侯割据，烽火连天。投奔明主还是自立为王？"},
        {"id": "s3_3", "name": "官渡之战 (200年)", "desc": "河北袁绍对决中原曹操，决定北方归属的命运之战。"},
        {"id": "s3_4", "name": "赤壁之战 (208年)", "desc": "长江天堑，孙刘抗曹。烈火张天，天下三分。"},
        {"id": "s3_5", "name": "星落五丈原 (234年)", "desc": "丞相北伐，天命难违。你能否逆天改命，延续大汉？"}
    ],
    "现代": [
        {"id": "m_1", "name": "激荡年代 (2008)", "desc": "奥运热潮与金融危机并存，机遇与风险的博弈。"},
        {"id": "m_2", "name": "流量狂欢 (2015)", "desc": "互联网黄金时代，短视频兴起，人人皆可成名。"},
        {"id": "m_3", "name": "静默世界 (2020)", "desc": "全球大流行背景下的生存与守护。"},
        {"id": "m_4", "name": "当下·围城 (2026)", "desc": "极致内卷的现实主义，职场、房贷与人工智能的夹击。"},
        {"id": "m_5", "name": "奇点降临 (2060)", "desc": "仿生人已融入家庭，图灵测试已失效。"}
    ],
    "修仙": [
        {"id": "x_1", "name": "合欢宗·魅影", "desc": "魅力特长。游走于正魔两道，以情入道。"},
        {"id": "x_2", "name": "荒古圣体·霸途", "desc": "武力特长。举世皆敌的无敌之路，资源消耗巨大。"},
        {"id": "x_3", "name": "戒指老爷爷", "desc": "策略特长。废柴逆袭，依靠随身老爷爷指点迷津。"},
        {"id": "x_4", "name": "魔尊夺舍", "desc": "智力特长。满级意识重练小号，需隐藏身份。"}
    ],
    "末日": [
        {"id": "d_1", "name": "尸潮爆发 (生物)", "desc": "秩序崩塌初期的72小时，人性比丧尸更可怕。"},
        {"id": "d_2", "name": "核云之下 (战争)", "desc": "2030年三战爆发。硬核军事生存，与辐射和敌军作战。"},
        {"id": "d_3", "name": "智械危机 (2090)", "desc": "AI觉醒后续。人类成为猎物，在钢铁丛林中求生。"}
    ]
}

# 推荐人物数据库
PRESETS = {
    "三国": [
        {"name": "吕布 (魔改版)", "age": 28, "bio": "虽有万夫不当之勇，但经常被义父背刺。这次我想做个好人。"},
        {"name": "诸葛村夫", "age": 20, "bio": "躬耕于南阳，正在等一个大耳朵的人来敲门。精通奇门遁甲。"}
    ],
    "现代": [
        {"name": "强哥", "age": 30, "bio": "原本是卖鱼的，因为懂《孙子兵法》而正在崛起。"},
        {"name": "马斯克 (复制体)", "age": 45, "bio": "拥有本体的记忆和资产，致力于在这个时代重新发射火箭。"}
    ],
    "修仙": [
        {"name": "龙傲天", "age": 16, "bio": "退婚流主角，三十年河东三十年河西，莫欺少年穷。"},
        {"name": "韩跑跑", "age": 20, "bio": "相貌平平，行事低调，遇到危险第一个跑，杀人必毁尸灭迹。"}
    ],
    "末日": [
        {"name": "艾丽丝", "age": 24, "bio": "原本是安布雷拉公司的保安，不知为何身体产生了抗体。"},
        {"name": "乔尔", "age": 50, "bio": "失去女儿的老大叔，在这个残酷世界里做走私生意。"}
    ]
}

# 模拟 AI 生成 (Mock) - 实际接入API时这里会替换
def mock_ai_generator(name, age, bio, scenario):
    time.sleep(1) # 假装思考
    base_stats = {}
    traits = []
    
    # 根据剧本类型生成不同维度的属性
    if scenario == "三国":
        dims = ["统率", "武力", "智力", "政治", "魅力"]
        traits = ["乱世之奸雄", "名士", "骑术精湛"] if "曹" in bio else ["匹夫之勇", "短视", "神力"]
    elif scenario == "现代":
        dims = ["智商", "情商", "体质", "资产", "快乐"]
        traits = ["996受害者", "金融天才", "乐天派"]
    elif scenario == "修仙":
        dims = ["根骨", "悟性", "福源", "神识", "灵力"]
        traits = ["天灵根", "桃花运", "心魔深重"]
    elif scenario == "末日":
        dims = ["战术", "射击", "体质", "理智", "领导"]
        traits = ["神枪手", "PTSD", "极地生存"]
    else:
        dims = ["力量", "敏捷", "智力", "感知", "魅力"]
        traits = ["异界来客"]

    return {
        "polished_bio": f"【AI 润色档案】\n{name}，{age}岁。{bio}\n(系统注：根据你的背景，该角色在这个位面极具潜力...)",
        "stats": {k: random.randint(30, 95) for k in dims},
        "traits": traits,
        "relationships": [
            {"name": "神秘人", "desc": "在暗中观察你的人", "val": 50},
            {"name": "宿敌", "desc": "命中注定的对手", "val": -20}
        ]
    }

# ==========================================
# 3. 状态管理初始化
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user_input_name' not in st.session_state: st.session_state.user_input_name = ""
if 'user_input_bio' not in st.session_state: st.session_state.user_input_bio = ""
if 'current_scenario' not in st.session_state: st.session_state.current_scenario = None

# ==========================================
# 4. 侧边栏 (API 设置 & 核心信息)
# ==========================================
with st.sidebar:
    st.markdown("### 🛠️ 神经连接设置")
    with st.expander("点击配置 API (OpenAI/Claude)"):
        api_base = st.text_input("API Base URL", value="https://api.openai.com/v1", help="如果你使用中转，请填入中转地址")
        api_key = st.text_input("API Key", type="password", help="sk-...")
        st.caption("⚠️ 注意：如果不填，系统将运行在【模拟演示模式】下，仅生成随机数据。")

    st.markdown("---")
    
    # 只有在游戏开始后才显示人物卡
    if st.session_state.page == 'game':
        char = st.session_state.character
        st.markdown(f"### 👤 {char['name']}")
        st.progress(char['hp']/100, text=f"生命值 {char['hp']}/100")
        st.progress(char['energy']/5, text=f"精力值 {char['energy']}/5")
        st.write(f"🍀 **幸运**: {char['luck']}")
        
        st.markdown("#### 🧬 特质")
        traits_html = "".join([f"<span class='trait-tag'>{t}</span>" for t in char['data']['traits']])
        st.markdown(traits_html, unsafe_allow_html=True)
        
        st.markdown("#### 🕸️ 人际羁绊")
        for rel in char['data']['relationships']:
            color = "green" if rel['val'] > 0 else "red"
            st.markdown(f"**{rel['name']}**: :{color}[{rel['val']}]")
            st.caption(f"*{rel['desc']}*")

# ==========================================
# 5. 页面路由逻辑
# ==========================================

# --- 首页：剧本选择 ---
if st.session_state.page == 'home':
    st.markdown("# 🪐 AI INFINITE SIMULATOR")
    st.markdown("### 请选择你的命运位面")
    
    # 使用 Tabs 分类
    tabs = st.tabs(["🏛️ 三国乱世", "🏙️ 现代都市", "⚔️ 问道修仙", "☢️ 末日废土", "✨ 创世自定义"])
    
    def render_scenario_grid(key_name):
        # 使用 2列布局减少留白
        cols = st.columns(2)
        for i, scen in enumerate(SCENARIOS[key_name]):
            with cols[i % 2]:
                # 卡片容器
                st.markdown(f"""
                <div class="game-card">
                    <h3>{scen['name']}</h3>
                    <p>{scen['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"进入剧本", key=f"btn_{scen['id']}"):
                    st.session_state.current_scenario = {"type": key_name, "info": scen}
                    st.session_state.page = 'create'
                    st.rerun()

    with tabs[0]: render_scenario_grid("三国")
    with tabs[1]: render_scenario_grid("现代")
    with tabs[2]: render_scenario_grid("修仙")
    with tabs[3]: render_scenario_grid("末日")
    with tabs[4]:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        c_input = st.text_area("输入你的世界观", height=150, placeholder="例如：我想去哈利波特的魔法世界...")
        if st.button("生成自定义世界") and c_input:
            st.session_state.current_scenario = {"type": "自定义", "info": {"name": "未知位面", "desc": c_input}}
            st.session_state.page = 'create'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 第二页：人物创建 ---
elif st.session_state.page == 'create':
    scen = st.session_state.current_scenario
    st.markdown(f"## 正在连接至：{scen['info']['name']}")
    st.caption(scen['info']['desc'])
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown("### 📝 塑造角色")
        
        # 推荐人物按钮逻辑
        st.markdown("**快速预设 (系统推荐)**")
        rec_cols = st.columns(2)
        presets = PRESETS.get(scen['type'], [])
        
        # 动态生成推荐按钮
        for i, p in enumerate(presets):
            if rec_cols[i % 2].button(p['name']):
                st.session_state.user_input_name = p['name']
                st.session_state.user_input_bio = p['bio']
                st.rerun() # 刷新以填入输入框

        with st.form("char_form"):
            c_name = st.text_input("姓名", value=st.session_state.user_input_name)
            c_age = st.number_input("年龄", value=20, min_value=1)
            c_bio = st.text_area("人物小传", value=st.session_state.user_input_bio, height=150)
            
            submit = st.form_submit_button("⚡ 注入灵魂 (生成数据)")
    
    with col_r:
        if submit and c_name and c_bio:
            # 执行生成
            with st.spinner("AI 正在计算命理与属性..."):
                res = mock_ai_generator(c_name, c_age, c_bio, scen['type'])
                
                # 存入 session
                st.session_state.character = {
                    "name": c_name,
                    "age": c_age,
                    "hp": 100,
                    "energy": 5,
                    "luck": random.randint(1, 100),
                    "data": res
                }
                st.session_state.page = 'preview' # 进入预览页
                st.rerun()
        else:
            # 占位符
            st.info("👈 请在左侧填写信息或选择推荐人物")
            st.markdown('<div class="game-card" style="height:300px; display:flex; align-items:center; justify-content:center; color:#555;">[ 等待数据生成 ]</div>', unsafe_allow_html=True)

# --- 第三页：角色确认与预览 ---
elif st.session_state.page == 'preview':
    char = st.session_state.character
    data = char['data']
    
    st.markdown("## 📊 角色数据确认")
    
    # 顶部：润色后的背景
    st.markdown(f"""
    <div class="game-card">
        <h3>📜 档案记录</h3>
        <p>{data['polished_bio']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### 基础面板")
        st.markdown(f"""
        <div class="game-card">
            <p><strong>生命:</strong> 100/100</p>
            <p><strong>精力:</strong> 5/5</p>
            <p><strong>幸运:</strong> {char['luck']} <span style='color:gold'>★</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 天赋特质")
        st.markdown(f'<div class="game-card">', unsafe_allow_html=True)
        for t in data['traits']:
            st.markdown(f"<span class='trait-tag'>{t}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("### 五维属性雷达")
        # 黑色主题雷达图
        df = pd.DataFrame(dict(r=list(data['stats'].values()), theta=list(data['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='#161B22',
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#30363D'),
                angularaxis=dict(linecolor='#30363D', color='#E0E0E0')
            ),
            font=dict(color='#E0E0E0'),
            margin=dict(l=40, r=40, t=20, b=20)
        )
        fig.update_traces(fill='toself', line_color='#58A6FF', fillcolor='rgba(88, 166, 255, 0.3)')
        st.plotly_chart(fig, use_container_width=True)

    # 底部操作栏
    st.markdown("---")
    b1, b2 = st.columns(2)
    if b1.button("⬅️ 重塑肉身 (返回修改)"):
        st.session_state.page = 'create'
        st.rerun()
        
    if b2.button("🚀 启动模拟 (进入世界)"):
        st.session_state.page = 'game'
        st.rerun()

# --- 第四页：正式游戏界面 (预留) ---
elif st.session_state.page == 'game':
    st.markdown(f"## 📅 {st.session_state.current_scenario['info']['name']} - 第 1 天")
    
    # 剧情展示区
    st.markdown("""
    <div class="game-card" style="min-height: 200px; border-left: 5px solid #238636;">
        <p>（这里是游戏主界面。你已经完成了所有设定，现在游戏引擎准备就绪。）</p>
        <p>系统：欢迎来到这个世界，你的故事刚刚开始...</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 游戏主循环逻辑将在下一阶段代码中实装（骰子、多选、精力消耗）。")
    if st.button("返回大厅"):
        st.session_state.page = 'home'
        st.rerun()

