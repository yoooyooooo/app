import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 页面设置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="wide")

# --- 极简 CSS 样式 ---
st.markdown("""
    <style>
        .main .block-container { padding-top: 1.5rem; }
        h1 { font-size: 1.6rem !important; font-weight: 800; }
        h3 { font-size: 1rem !important; color: #888; margin-top: 1rem !important; }
        .stButton>button { border-radius: 8px; margin-bottom: 4px; height: 3rem; }
        /* 进度条颜色逻辑 */
        .stProgress > div > div > div > div { background-color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 任务与奖励库 ---
ALL_RANDOM_TASKS = [
    ("吃水果", 1), ("5个深呼吸", 1), ("拉伸", 1), ("整理桌面", 1), 
    ("看窗外30s", 1), ("擦屏幕", 1), ("刷牙", 2), ("服维他命", 1), 
    ("找人聊天", 1), ("洗脸清醒", 1), ("科普视频", 1), ("摄入兴奋剂", 1),
    ("购入刚需", 2), ("听英语博客", 2), ("散步30min", 2), ("洗澡/理床", 3),
    ("推动商业计划", 3), ("学数学2h", 3), ("吃顿好饭", 2), ("冥想10min", 2)
]

CHEAP_REWARDS = {"玩10min手机": 5, "吃颗喜欢的糖": 5, "听3首歌": 8, "看一集短剧": 12, "喝杯好喝的": 15}
BIG_REWARDS = {"顶级烹饪大餐": 60, "专业全身按摩": 60, "微醺酒精时光": 40, "参加沙龙聚会": 50, "买一本新书": 45}

# --- 数据初始化 ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_xp' not in st.session_state: st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state: st.session_state.done_tasks = []
if 'task_counts' not in st.session_state: st.session_state.task_counts = {}
if 'random_pool' not in st.session_state: st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
if 'streak' not in st.session_state: st.session_state.streak = 1

# --- 每日重置与连登逻辑 ---
today = datetime.now().date()
if 'last_date' not in st.session_state: st.session_state.last_date = today

if st.session_state.last_date < today:
    if st.session_state.last_date == today - timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.daily_xp, st.session_state.done_tasks = 0, []
    st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
    st.session_state.last_date, st.session_state.logged_in = today, False

if 'logged_in' not in st.session_state:
    st.session_state.xp += 1
    st.session_state.daily_xp += 1
    st.session_state.logged_in = True
    st.toast(f"🔌 系统接入！连登第 {st.session_state.streak} 天，奖励 +1 XP")

# --- 金色进度条触发器 ---
is_full = st.session_state.daily_xp >= 10
if is_full:
    st.markdown("<style>.stProgress > div > div > div > div { background-color: #FFD700 !important; box-shadow: 0 0 15px #FFD700; }</style>", unsafe_allow_html=True)

# --- UI 布局 ---
st.title("⚡ VIBEQUEST_OS")
col_header, col_val = st.columns([3, 1])
with col_header:
    if is_full: st.markdown("### 🏆 GOLDEN STATUS ACHIEVED")
    else: st.markdown(f"### 🔋 DAILY_ENERGY: {st.session_state.daily_xp}/10")
with col_val:
    st.metric("TOTAL_QP", f"{st.session_state.xp}")

st.progress(min(st.session_state.daily_xp / 10, 1.0))

tab1, tab2, tab3 = st.tabs(["🎯 任务", "🏆 成就", "🎁 商店"])

with tab1:
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("### 💠 基础协议")
        base_tasks = {"背单词": 3, "喝一杯水": 1}
        for task, score in base_tasks.items():
            done = task in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '◻️'} {task} (+{score})", key=f"b_{task}", use_container_width=True, disabled=done):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score; st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.session_state.task_counts[task] = st.session_state.task_counts.get(task, 0) + 1
                    if st.session_state.daily_xp >= 10: st.balloons()
                    st.rerun()
        
        # 填充左侧空白：每日 Vibe 寄语
        st.markdown("---")
        st.caption("📜 SYSTEM_VIBE:")
        quotes = ["不要藐视规则，要利用规则。", "自律的本质是夺回控制权。", "10分之后的努力是边际递减的。", "保持呼吸，保持同步。"]
        st.info(random.choice(quotes))

    with right_col:
        st.markdown("### 🎲 随机挑战")
        for i, (task, score) in enumerate(st.session_state.random_pool):
            done = task in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '🔹'} {task} (+{score})", key=f"r_{i}", use_container_width=True, disabled=done):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score; st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.session_state.task_counts[task] = st.session_state.task_counts.get(task, 0) + 1
                    if st.session_state.daily_xp >= 10: st.balloons()
                    st.rerun()
                else: st.warning("能量已满")
        
        if st.button("🔄 刷新任务 (-1 XP)", use_container_width=True):
            if st.session_state.xp >= 1:
                st.session_state.xp -= 1
                st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
                st.rerun()

with tab2:
    with st.expander("📅 登录成就", expanded=True):
        st.write(f"当前连续登录：`{st.session_state.streak}` 天")
        if st.session_state.streak >= 7: st.success("🏆 【周常】：连续登录 7 天 (达成)")

    with st.expander("📈 经验成就"):
        st.write(f"累计总经验：`{st.session_state.xp}` XP")
        ach_list = [("🌱 觉醒", 10), ("🔥 燃魂", 100), ("💎 领主", 500)]
        for n, r in ach_list:
            if st.session_state.xp >= r: st.success(f"👑 {n} (累计 {r} XP)")

    with st.expander("🛠️ 任务达人"):
        for t, count in st.session_state.task_counts.items():
            st.write(f"**{t}**: 已完成 `{count}` 次")

with tab3:
    st.markdown("### 🎫 微奖励 (便宜好用)")
    c1, c2 = st.columns(2)
    for i, (item, cost) in enumerate(CHEAP_REWARDS.items()):
        col = c1 if i % 2 == 0 else c2
        if col.button(f"{item} ({cost}XP)", key=f"cheap_{i}", use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost; st.success(f"兑换成功：{item}"); st.rerun()

    st.markdown("### 🎰 运气抽取 (20 XP)")
    if st.button("🧧 消耗 20 XP 随机抽取大奖库", use_container_width=True):
        if st.session_state.xp >= 20:
            st.session_state.xp -= 20
            dice = random.random()
            if dice < 0.2: 
                res = random.choice(list(BIG_REWARDS.keys()))
                st.balloons(); st.success(f"🔥 大奖!! 【{res}】")
            else: st.warning("🕸️ 轮空：未中奖，继续加油")
            st.rerun()

    with st.expander("🏛️ 昂贵大奖 (保底兑换)"):
        for res, cost in BIG_REWARDS.items():
            if st.button(f"购入 {res} ({cost} XP)", key=f"big_{res}", use_container_width=True):
                if st.session_state.xp >= cost:
                    st.session_state.xp -= cost; st.success(f"解锁：{res}"); st.rerun()