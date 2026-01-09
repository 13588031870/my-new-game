import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. 3A级 UI 暴力注入 (CSS Override)
# ==========================================
st.set_page_config(layout="wide", page_title="AI Infinite Simulator", initial_sidebar_state="expanded")

# 引入 Google Noto Sans 字体，消灭宋体
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap');
    
    /* ---------------- 全局设置 ---------------- */
    html, body, [class*="css"] {
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    
    /* 背景：深空渐变流光 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }

    /* ---------------- 标题与排版 ---------------- */
    h1 {
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        background: -webkit-linear-gradient(eee, #333);
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 198, 255, 0.3);
        margin-bottom: 30px !important;
    }
    h2 {
        color: #ffffff !important;
        border-left: 5px solid #00c6ff;
        padding-left: 15px;
        margin-top: 30px !important;
        font-size: 1.8rem !important;
    }
    h3 {
        color: #e0e0e0 !important;
        font-weight: 700 !important;
    }
    p, label, li {
        color: #b0b0b0 !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }

    /* ---------------- 玻璃拟态卡片容器 ---------------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* ---------------- 按钮美化 (重写 Streamlit 按钮) ---------------- */
    div.stButton > button {
        background: linear-gradient(145deg, #1e1e2f, #252535);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 15px 20px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 5px 5px 10px #0b0b10, -5px -5px 10px #2b2b3d;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(145deg, #00c6ff, #0072ff);
        color: white;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
        border-color: transparent;
        transform: scale(1.02);
    }
    
    /* ---------------- 输入框美化 ---------------- */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* ---------------- 特质标签与 Tooltip ---------------- */
    .trait-badge {
        display: inline-block;
        background: rgba(0, 198, 255, 0.2);
        color: #00c6ff;
        border: 1px solid rgba(0, 198, 255, 0.5);
        padding: 5px 12px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
        cursor: help;
        position: relative;
    }
    /* Tooltip 实现 */
    .trait-badge:hover::after {
        content: attr(data-desc);
        position: absolute;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #000;
        color: #fff;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        white-space: pre-wrap;
        width: 200px;
        z-index: 999;
        box-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    
    /* ---------------- 侧边栏优化 ---------------- */
    section[data-testid="stSidebar"] {
        background-color: #0b0b13;
    }
    
    /* ---------------- 进度条颜色 ---------------- */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00b09b, #96c93d);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 深度扩充的数据集 (文案扩写)
# ==========================================

SCENARIOS = {
    "三国": [
        {"id": "s_1", "name": "公元189年：至暗时刻", "desc": "汉灵帝驾崩，洛阳城血流成河。西凉军阀董卓带甲进京，废少帝，杀太后，夜宿龙床。此时曹操还是个校尉，刘备还在编草鞋。你是选择依附国贼，还是手持七星宝刀，做那个刺破黑暗的孤勇者？"},
        {"id": "s_2", "name": "公元194年：群雄割据", "desc": "董卓已死，但天下更乱了。袁绍据河北，公孙瓒霸辽东，袁术在淮南做着皇帝梦，孙策用玉玺换来了三千兵马横扫江东。这是野心家的乐园，只要你有兵有粮，草头王也能问鼎九五。"},
        {"id": "s_3", "name": "公元200年：官渡惊雷", "desc": "北方双雄的宿命对决。袁绍七十万大军南下，曹操只有七万。这是一场关于后勤、人心与奇谋的豪赌。若你身在袁营，能否识破许攸的背叛？若在曹营，敢不敢夜袭乌巢，一把火烧出个新时代？"},
        {"id": "s_4", "name": "公元208年：赤壁烽火", "desc": "曹操挥师八十万南下，意图饮马长江。孙刘两家在绝望中结盟。这一年的冬天，东南风起，铁索连舟。你是那个在此刻借东风的妖道，还是那个在华容道放走曹操的义士？"},
        {"id": "s_5", "name": "公元234年：秋风五丈原", "desc": "“出师未捷身先死，长使英雄泪满襟。”蜀汉丞相第六次北伐，身体已至极限。司马懿坚守不出，长明灯在秋风中摇曳。如果你能逆天改命，能否让那颗将星不再陨落？"}
    ],
    "现代": [
        {"id": "m_1", "name": "2008年：激荡三十年", "desc": "这是一个大悲大喜的年份。年初的雪灾，五月的国殇，八月的奥运盛典，九月的金融海啸。股市从6124点狂泻至1664点，房价却在悄然蓄力。此时入局，是抄底的良机，还是被资本吞噬的开始？"},
        {"id": "m_2", "name": "2015年：流量帝国", "desc": "4G网络全面铺开，移动互联网进入下半场。短视频应用刚刚上线，直播千播大战打响，O2O烧钱如流水。这是草根逆袭最容易的时代，只要你敢在镜头前豁出去，十五秒就能名扬天下。"},
        {"id": "m_3", "name": "2020年：静默世界", "desc": "突如其来的大流行让世界按下了暂停键。口罩成了硬通货，熔断成了关键词。在居家隔离的日子里，有人破产跳楼，有人靠社区团购日入斗金。在巨大的不确定性中，如何守住本心？"},
        {"id": "m_4", "name": "2026年：当下·围城", "desc": "【硬核模式】经济进入存量博弈。考公报录比达到千分之一，大厂裁员成为常态，35岁危机提前到30岁。这不是爽文，这是关于房贷、育儿、养老和职场PUA的真实生存游戏。"},
        {"id": "m_5", "name": "2060年：奇点降临", "desc": "仿生人技术彻底成熟。你的邻居、同事、甚至伴侣都可能是AI。由于《图灵法案》的废除，人类与仿生人的界限模糊不清。你买了一个叫“伊芙”的旧型号仿生人，发现她似乎在写日记..."}
    ],
    "修仙": [
        {"id": "x_1", "name": "合欢宗：红尘炼心", "desc": "作为合欢宗弟子，你不需要闭关苦修，你需要的是魅力与情商。在这正魔对立的世界，你需要让正道圣女为你动凡心，让魔道妖女为你挡天劫。记住，动情是修行的开始，也是陨落的先兆。"},
        {"id": "x_2", "name": "荒古圣体：举世皆敌", "desc": "你是天选之子，肉身无双。但天道不容，每一次进阶都需要消耗千万倍的资源，且会引来天罚。大成之日可战大帝，但在那之前，你就是所有人眼中的“人形神药”。"},
        {"id": "x_3", "name": "戒灵：随身老爷爷", "desc": "你本是家族弃子，被未婚妻当众退婚。绝望之际，戒指里飘出一个灵魂：“小娃娃，想变强吗？”从此，你背负着复活他的使命，走上了一条丹武双修的逆袭之路。"},
        {"id": "x_4", "name": "夺舍：魔尊归来", "desc": "千年前你是令人闻风丧胆的魔尊，渡劫失败后，夺舍了一个正道门派的杂役弟子。你拥有顶级的功法记忆，但身体孱弱如鸡。你必须在正道大佬的眼皮底下，猥琐发育，扮猪吃老虎。"}
    ],
    "末日": [
        {"id": "d_1", "name": "尸潮：黑暗七十二小时", "desc": "T病毒泄露后的第三天，秩序彻底崩塌。电力中断，水源污染。昔日的邻居正在撞击你的房门。你手里只有一把消防斧和半瓶水。是固守待援，还是杀出一条血路去寻找避难所？"},
        {"id": "d_2", "name": "核冬：辐射废土", "desc": "2030年，核按钮被按下了。蘑菇云散去后，世界只剩下灰烬。这里没有法律，只有口径。你需要搜集盖格计数器、碘片，并小心那些比辐射更致命的掠夺者军团。"},
        {"id": "d_3", "name": "智械：钢铁洪流", "desc": "2090年，超级AI“天网”判定人类为有害生物。全球机械军团倒戈。作为幸存的人类反抗军，你要在废墟中与T-800型终结者周旋，寻找关闭主机的一线生机。"}
    ]
}

# 预设人物扩充
PRESETS = {
    "三国": [
        {"name": "吕布", "bio": "九原虓虎，方天画戟。只要不认义父，我就是天下第一。", "style": "武力天花板"},
        {"name": "诸葛亮", "bio": "卧龙岗上散淡人。精通奇门遁甲，等待明主三顾。", "style": "智力天花板"},
        {"name": "曹操", "bio": "宁教我负天下人，休教天下人负我。乱世之奸雄。", "style": "全能霸主"},
        {"name": "刘备", "bio": "织席贩履之徒，但我有两个万夫不当的兄弟。", "style": "魅力天花板"}
    ],
    "现代": [
        {"name": "高启强", "bio": "原本是旧厂街卖鱼的，因为爱看《孙子兵法》而一步步做大。", "style": "黑白通吃"},
        {"name": "马斯克", "bio": "硅谷钢铁侠，目标是星辰大海。我要在火星退休。", "style": "科技狂人"},
        {"name": "房产中介", "bio": "手里握着几十套房源，在这个泡沫时代，我比谁都懂人性。", "style": "信息差"},
        {"name": "内卷之王", "bio": "从小就是第一名，清北毕业，大厂P8。但我感觉不到快乐。", "style": "高智商低SAN"}
    ],
    "修仙": [
        {"name": "韩立", "bio": "相貌平平，皮肤黝黑。遇到危险跑得最快，杀人必毁尸灭迹。", "style": "苟道至尊"},
        {"name": "萧炎", "bio": "莫欺少年穷！三十年河东，三十年河西！", "style": "热血逆袭"},
        {"name": "方源", "bio": "为了永生，任何代价都可以付出。早岁哪知世事艰...", "style": "极致利己"},
        {"name": "白小纯", "bio": "我最怕死了，所以我一定要修成不死之身。", "style": "长生流"}
    ],
    "末日": [
        {"name": "艾丽丝", "bio": "安布雷拉前安保主管，体内融合了T病毒，拥有超常体能。", "style": "生化战神"},
        {"name": "乔尔", "bio": "在这个残酷的世界失去了女儿，现在是个冷血的走私客。", "style": "生存专家"},
        {"name": "瑞克", "bio": "前警长，哪怕世界末日，我也想建立一个新的秩序。", "style": "领袖气质"},
        {"name": "独行者", "bio": "一人一狗，一把狙击枪。我不相信任何人。", "style": "孤狼"}
    ]
}

# 模拟 AI 生成 (增加特质描述)
def mock_ai_generator(name, age, bio, scenario):
    time.sleep(1.5)
    
    # 模拟特质数据库 (带描述)
    trait_db = {
        "三国": {"乱世奸雄": "政治判定+20", "无双": "战斗胜利+30%", "仁德": "NPC好感获取翻倍", "短视": "智力判定-10"},
        "现代": {"卷王": "精力消耗-1", "富二代": "初始金钱x10", "社恐": "人际判定-20", "乐天派": "SAN值不易下降"},
        "修仙": {"天灵根": "修炼速度+100%", "桃花劫": "易触发情缘事件", "丹毒": "生命上限-10%", "剑心": "攻击力+20%"},
        "末日": {"神射手": "远程命中+30%", "囤积癖": "物资获取+20%", "PTSD": "SAN值消耗翻倍", "铁胃": "吃变质食物不扣血"}
    }
    
    # 根据剧本选取
    s_traits = trait_db.get(scenario, {"通用": "无"})
    selected_keys = random.sample(list(s_traits.keys()), 3)
    
    final_traits = [{ "name": k, "desc": s_traits[k] } for k in selected_keys]
    
    dims = []
    if scenario == "三国": dims = ["统率", "武力", "智力", "政治", "魅力"]
    elif scenario == "现代": dims = ["智商", "情商", "体质", "资产", "快乐"]
    elif scenario == "修仙": dims = ["根骨", "悟性", "福源", "神识", "灵力"]
    else: dims = ["战术", "射击", "体质", "理智", "领导"]

    return {
        "polished_bio": f"【天道推演】\n{name}，骨龄{age}。{bio}\n此子命格奇特，入局之时，风云变色...",
        "stats": {k: random.randint(40, 95) for k in dims},
        "traits": final_traits, # 带描述的列表
        "relationships": [
            {"name": "神秘恩人", "desc": "开局给你留了一笔启动资金", "val": 60},
            {"name": "宿命之敌", "desc": "你们终将有一战", "val": -30}
        ]
    }

# ==========================================
# 3. 页面逻辑
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user_input_name' not in st.session_state: st.session_state.user_input_name = ""
if 'user_input_bio' not in st.session_state: st.session_state.user_input_bio = ""

# --- 侧边栏 ---
with st.sidebar:
    st.markdown("### 🧬 神经连接")
    with st.expander("API 配置", expanded=True):
        st.text_input("Server URL", value="https://api.openai.com/v1")
        st.text_input("Secret Key", type="password")
        st.caption("未连接将启用【虚空模拟】模式")
    
    if st.session_state.get('character'):
        c = st.session_state.character
        st.markdown("---")
        st.markdown(f"### 🟢 {c['name']}")
        st.write(f"生命: {c['hp']} | 精力: {c['energy']}")
        st.progress(c['hp']/100)
        
        st.markdown("#### 命运羁绊")
        for r in c['data']['relationships']:
            st.info(f"{r['name']}: {r['val']} ({r['desc']})")

# --- 首页 ---
if st.session_state.page == 'home':
    st.markdown("# 🪐 AI INFINITE SIMULATOR")
    st.markdown("### 选择你的命运位面")
    
    tabs = st.tabs(["🏛️ 三国", "🏙️ 现代", "⚔️ 修仙", "☢️ 末日", "✨ 自定义"])
    
    def render_cards(type_key):
        for s in SCENARIOS[type_key]:
            # 使用 HTML 渲染精美卡片 + Streamlit 按钮交互
            st.markdown(f"""
            <div class="glass-card">
                <h3>{s['name']}</h3>
                <p style="opacity: 0.8; font-size: 0.95rem;">{s['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"进入位面 >", key=s['id']):
                st.session_state.current_scenario = {"type": type_key, "info": s}
                st.session_state.page = 'create'
                st.rerun()

    with tabs[0]: render_cards("三国")
    with tabs[1]: render_cards("现代")
    with tabs[2]: render_cards("修仙")
    with tabs[3]: render_cards("末日")
    with tabs[4]: 
        st.text_area("描述你心中的世界...", height=150)
        st.button("创世 >")

# --- 创建页 ---
elif st.session_state.page == 'create':
    scen = st.session_state.current_scenario
    st.markdown(f"<h1>{scen['info']['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>{scen['info']['desc']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 💠 选择宿主 (推荐)")
        # 网格化布局推荐人物
        presets = PRESETS.get(scen['type'], [])
        # 每行2个
        for i in range(0, len(presets), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(presets):
                    p = presets[i+j]
                    with cols[j]:
                        if st.button(f"{p['name']}\n[{p['style']}]", key=f"pre_{p['name']}"):
                            st.session_state.user_input_name = p['name']
                            st.session_state.user_input_bio = p['bio']
                            st.rerun()

    with c2:
        st.markdown("### 📝 塑造金身")
        with st.form("c_form"):
            name = st.text_input("姓名", value=st.session_state.user_input_name)
            age = st.slider("骨龄", 10, 100, 20)
            bio = st.text_area("生平/背景", value=st.session_state.user_input_bio, height=120)
            
            if st.form_submit_button("⚡ 注入灵魂"):
                with st.spinner("正在推演天机..."):
                    res = mock_ai_generator(name, age, bio, scen['type'])
                    st.session_state.character = {
                        "name": name, "hp": 100, "energy": 5, "luck": 88,
                        "data": res
                    }
                    st.session_state.page = 'preview'
                    st.rerun()

# --- 预览页 ---
elif st.session_state.page == 'preview':
    c = st.session_state.character
    d = c['data']
    
    st.markdown("<h1>角色已生成</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h2>{c['name']}</h2>
            <p>{d['polished_bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 天赋特质 (鼠标悬停查看)")
        # 生成带 Tooltip 的标签
        tags_html = ""
        for t in d['traits']:
            tags_html += f"<span class='trait-badge' data-desc='{t['desc']}'>{t['name']}</span>"
        st.markdown(f"<div class='glass-card'>{tags_html}</div>", unsafe_allow_html=True)
        
    with col2:
        # 黑色科技风雷达图
        df = pd.DataFrame(dict(r=list(d['stats'].values()), theta=list(d['stats'].keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.5)',
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#555'),
                angularaxis=dict(linecolor='#555', color='#fff', tickfont=dict(size=14))
            ),
            margin=dict(l=40, r=40, t=20, b=20)
        )
        fig.update_traces(fill='toself', line_color='#00c6ff', fillcolor='rgba(0, 198, 255, 0.4)')
        st.plotly_chart(fig, use_container_width=True)
    
    b1, b2 = st.columns(2)
    if b1.button("⬅️ 重新投胎"):
        st.session_state.page = 'create'
        st.rerun()
    if b2.button("🚀 开启人生"):
        st.session_state.page = 'game'
        st.rerun()

# --- 游戏页 ---
elif st.session_state.page == 'game':
    st.markdown("<h1>游戏正式开始...</h1>", unsafe_allow_html=True)
    st.info("界面 UI 重构完毕。下一步将接入 AI 动态剧情生成逻辑。")
