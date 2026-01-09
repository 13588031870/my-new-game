import streamlit as st
import json
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 页面配置与 CSS 美化 (灰白极简风)
# ==========================================
st.set_page_config(layout="wide", page_title="AI Infinite Simulator")

# 自定义 CSS 样式
st.markdown("""
<style>
    /* 全局背景色 */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
    }
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: #F7F9FB;
        border-right: 1px solid #E6E6E6;
    }
    /* 按钮样式 - 黑色细边框 */
    div.stButton > button {
        background-color: white;
        color: black;
        border: 1px solid black;
        border-radius: 0px;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: black;
        color: white;
    }
    /* 标题样式 */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 300;
        color: #111111;
    }
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 0px;
        border: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 模拟 AI 后端 (因为这里不能真调API，我写个模拟器方便你预览效果)
# ==========================================
def mock_ai_generate_character(name, age, raw_bio, scenario_type):
    """
    实际开发时，这里会替换为 OpenAI API 调用。
    现在为了演示，根据剧本类型返回模拟数据。
    """
    time.sleep(1.5) # 模拟 AI 思考时间
    
    # 模拟润色后的背景
    polished_bio = f"【AI润色结果】{name}（{age}岁），{raw_bio}。在这个{scenario_type}的世界里，这个身份意味着巨大的挑战与机遇..."
    
    # 模拟生成的属性 (根据不同剧本返回不同维度的属性)
    if scenario_type == "三国":
        attributes = {"统率": random.randint(40,90), "武力": random.randint(40,90), "智力": random.randint(40,90), "政治": random.randint(30,80), "魅力": random.randint(50,90)}
        traits = ["汉室宗亲", "虽远必诛", "屯田"]
    elif scenario_type == "现代":
        attributes = {"智商": random.randint(80,140), "情商": random.randint(60,100), "体质": random.randint(50,90), "资产": random.randint(10,100), "心情": 80}
        traits = ["卷王", "房贷缠身", "社恐"]
    elif scenario_type == "修仙":
        attributes = {"根骨": random.randint(10,100), "悟性": random.randint(10,100), "福源": random.randint(10,100), "神识": random.randint(10,100), "灵力": 0}
        traits = ["天生道体", "桃花劫", "丹毒"]
    elif scenario_type == "末日":
        attributes = {"战术": random.randint(50,90), "生存": random.randint(60,95), "体质": random.randint(60,90), "SAN值": 80, "科技": random.randint(20,70)}
        traits = ["PTSD", "神射手", "囤积癖"]
    else: # 自定义
        attributes = {"力量": 50, "敏捷": 50, "智力": 50, "感知": 50, "魅力": 50}
        traits = ["穿越者", "未知血统"]

    return {
        "polished_bio": polished_bio,
        "attributes": attributes,
        "traits": traits,
        "luck": random.randint(1, 100) # 独立幸运值
    }

# ==========================================
# 3. 状态管理
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 1 # 1:大厅, 2:创建角色, 3:角色展示/开始
if 'selected_scenario' not in st.session_state:
    st.session_state.selected_scenario = {}
if 'character_data' not in st.session_state:
    st.session_state.character_data = {}

# ==========================================
# 4. 侧边栏 (API 设置 & 状态概览)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ 设置")
    api_key = st.text_input("OpenAI / Claude API Key", type="password", help="填入你的 Key 以启用真实 AI 生成")
    
    st.markdown("---")
    if st.session_state.step >= 3:
        st.markdown("### 👤 当前角色")
        st.write(f"**{st.session_state.character_data.get('name', '')}**")
        st.write(f"❤️ 生命: 100/100")
        st.write(f"⚡ 精力: 5/5")
        st.write(f"🍀 幸运: {st.session_state.character_data.get('luck', 0)}")
    else:
        st.info("请先创建角色")

# ==========================================
# 5. 主界面逻辑
# ==========================================

# --- 标题区 ---
st.title("AI INFINITE SIMULATOR")
st.markdown("*无尽世界 · 极简模拟 · 随机人生*")
st.divider()

# --- STEP 1: 剧本选择大厅 ---
if st.session_state.step == 1:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ 三国", "🏙️ 现代", "⚔️ 修仙", "☢️ 末日", "✨ 自定义"])

    def select_scenario(category, sub_title, desc):
        st.session_state.selected_scenario = {"category": category, "sub_title": sub_title, "desc": desc}
        st.session_state.step = 2
        st.rerun()

    with tab1: # 三国
        st.subheader("【乱世烽火】")
        cols = st.columns(3)
        if cols[0].button("董卓入京 (189年)"): select_scenario("三国", "董卓入京", "权倾朝野，至暗时刻。")
        if cols[1].button("赤壁之战 (208年)"): select_scenario("三国", "赤壁之战", "烈火张天，天下三分。")
        if cols[2].button("星落五丈原 (234年)"): select_scenario("三国", "星落五丈原", "丞相的一生遗憾。")

    with tab2: # 现代
        st.subheader("【岁月如歌】")
        mod_opts = ["2008: 激荡年代 (奥运/金融)", "2015: 流量狂欢 (短视频/直播)", "2020: 静默世界 (居家/隔离)", "2026: 当下·围城 (内卷/现实)", "2060: 奇点降临 (AI/仿生人)"]
        choice = st.radio("选择时间线", mod_opts)
        if st.button("进入该时代"): select_scenario("现代", choice, "时代的洪流裹挟着每一个人。")

    with tab3: # 修仙
        st.subheader("【问道长生】")
        c1, c2 = st.columns(2)
        if c1.button("合欢宗·魅影"): select_scenario("修仙", "合欢宗", "以情入道，风险与机遇并存。")
        if c2.button("荒古圣体·霸途"): select_scenario("修仙", "荒古圣体", "举世皆敌，唯我独尊。")
        if c1.button("戒指老爷爷"): select_scenario("修仙", "戒灵", "废柴逆袭，药老相助。")
        if c2.button("魔尊夺舍"): select_scenario("修仙", "魔尊夺舍", "满级账号，新手村重练。")
        
    with tab4: # 末日
        st.subheader("【废土求生】")
        m_cols = st.columns(3)
        if m_cols[0].button("尸潮爆发"): select_scenario("末日", "尸潮爆发", "人性比丧尸更可怕。")
        if m_cols[1].button("核云之下"): select_scenario("末日", "核云之下 (军事战争)", "硬核军事生存，战术对抗。")
        if m_cols[2].button("智械危机 (2090)"): select_scenario("末日", "智械危机", "仿生人试图取代人类。")

    with tab5: # 自定义
        st.subheader("【创世之神】")
        custom_world = st.text_area("输入你想去的世界（如：哈利波特魔法世界，我是斯莱特林学生）")
        if st.button("生成世界") and custom_world:
            select_scenario("自定义", "异世界", custom_world)

# --- STEP 2: 角色创建 ---
elif st.session_state.step == 2:
    st.markdown(f"### 当前剧本：{st.session_state.selected_scenario['category']} - {st.session_state.selected_scenario['sub_title']}")
    st.caption(st.session_state.selected_scenario['desc'])
    
    with st.form("create_char"):
        c_name = st.text_input("姓名")
        c_age = st.number_input("年龄", min_value=1, max_value=1000, value=20)
        c_bio = st.text_area("人物简介 (随便写，AI会帮你润色)", placeholder="例如：我是一个退役特种兵，但是断了一条腿...")
        
        submitted = st.form_submit_button("确认创建并生成属性")
        
        if submitted and c_name and c_bio:
            with st.spinner('AI 正在构建你的灵魂与肉体...'):
                # 调用模拟AI函数
                char_res = mock_ai_generate_character(c_name, c_age, c_bio, st.session_state.selected_scenario['category'])
                
                # 保存数据
                st.session_state.character_data = {
                    "name": c_name,
                    "age": c_age,
                    "bio": char_res['polished_bio'],
                    "attrs": char_res['attributes'],
                    "traits": char_res['traits'],
                    "luck": char_res['luck']
                }
                st.session_state.step = 3
                st.rerun()

# --- STEP 3: 角色确认与展示 (核心五维图) ---
elif st.session_state.step == 3:
    st.success("角色创建成功！")
    
    char = st.session_state.character_data
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"### {char['name']} ({char['age']}岁)")
        st.info(char['bio'])
        st.markdown("**【初始特质】**")
        for trait in char['traits']:
            st.button(trait, disabled=True) # 用按钮样式显示特质标签
            
    with col2:
        st.markdown("### 能力五维图")
        # 使用 Plotly 绘制雷达图
        df = pd.DataFrame(dict(
            r=list(char['attrs'].values()),
            theta=list(char['attrs'].keys())
        ))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line_color='#333333')
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    start_col1, start_col2 = st.columns(2)
    if start_col1.button("⬅️ 重新创建"):
        st.session_state.step = 2
        st.rerun()
    if start_col2.button("🚀 开始模拟 (进入游戏界面)"):
        st.balloons()
        # 这里预留进入 Step 4 (正式玩法界面) 的接口
        st.toast("即将进入正式游戏循环...")
