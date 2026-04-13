import streamlit as st
import random
import time
from datetime import datetime

# --- 页面设置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="wide") # 设为宽屏模式

# --- 样式美化：精简标题与金色进度条 ---
st.markdown("""
    <style>
        .main .block-container { padding-top: 1rem; }
        h1 { font-size: 1.5rem !important; }
        h3 { font-size: 1.1rem !important; margin-bottom: 0.5rem !important; }
        .stProgress > div > div > div > div {
            background-color: #FFD700;
            box-shadow: 0 0 10px #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

# --- 任务库定义 ---
ALL_RANDOM_TASKS = [
    ("吃水果", 1), ("5个深呼吸", 1), ("拉伸", 1), ("整理桌面", 1), 
    ("看窗外30s", 1), ("擦屏幕", 1), ("刷牙", 2), ("服维他命", 1), 
    ("找人聊天", 1), ("洗脸清醒", 1), ("科普视频", 1), ("摄入兴奋剂", 1),
    ("购入刚需", 2), ("听英语博客", 2), ("散步30min", 2), ("洗澡/理床", 3),
    ("推动商业计划", 3), ("学数学2h", 3), ("吃顿好饭", 2), ("冥想10min", 2)
]

# --- 奖励库定义 ---
SMALL_REWARDS = ["喝一杯冰可乐", "听一首喜欢的歌", "休息5分钟", "玩手机10分钟"]
BIG_REWARDS = ["顶级烹饪大餐", "专业全身按摩", "微醺酒精时光", "参加沙龙聚会", "买一本实体书", "无罪恶游戏3h"]

# --- 数据初始化 ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_xp' not in st.session_state: st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state: st.session_state.done_tasks = []
if 'task_counts' not in st.session_state: st.session_state.task_counts = {}
if 'random_pool' not in st.session_state: st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)

# --- 每日重置逻辑 ---
today = datetime.now().strftime('%Y-%m-%d')
if 'last_date' not in st.session_state: st.session_state.last_date = today
if st.session_state.last_date != today:
    st.session_state.daily_xp, st.session_state.done_tasks = 0, []
    st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
    st.session_state.last_date, st.session_state.logged_in = today, False

if 'logged_in' not in st.session_state:
    st.session_state.xp += 1
    st.session_state.daily_xp += 1
    st.session_state.logged_in = True
    st.toast("⚡ 系统接入奖励 +1 XP", icon="🔌")

# --- UI 顶部 ---
col_t1, col_t2 = st.columns([2, 1])
with col_t1:
    st.title("⚡ VIBEQUEST_OS")
with col_t2:
    st.metric("TOTAL_XP", f"{st.session_state.xp} QP")

# 进度条
prog = min(st.session_state.daily_xp / 10, 1.0)
st.progress(prog)
if prog >= 1.0: st.caption("✨ GOLDEN STATUS: 今日已满级")
else: st.caption(f"Progress: {st.session_state.daily_xp}/10 XP")

tab1, tab2, tab3 = st.tabs(["🎯 任务大厅", "🏆 成就系统", "🎁 兑换中心"])

with tab1:
    # 左右排版
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("### 💠 基础协议")
        base_tasks = {"背单词": 3, "喝一杯水": 1}
        for task, score in base_tasks.items():
            is_done = task in st.session_state.done_tasks
            if st.button(f"{'✅' if is_done else '◻️'} {task} +{score}", key=f"b_{task}", use_container_width=True, disabled=is_done):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.session_state.task_counts[task] = st.session_state.task_counts.get(task, 0) + 1
                    st.rerun()

    with right_col:
        st.markdown("### 🎲 随机挑战")
        for i, (task, score) in enumerate(st.session_state.random_pool):
            is_done = task in st.session_state.done_tasks
            if st.button(f"{'✅' if is_done else '🔹'} {task} +{score}", key=f"r_{i}", use_container_width=True, disabled=is_done):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.session_state.task_counts[task] = st.session_state.task_counts.get(task, 0) + 1
                    st.rerun()
        
        if st.button("🔄 刷新任务 (-1 XP)", use_container_width=True):
            if st.session_state.xp >= 1:
                st.session_state.xp -= 1
                st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
                st.rerun()

with tab2:
    st.markdown("### 🏅 里程碑")
    # 次数成就
    for t_name, count in st.session_state.task_counts.items():
        if count >= 10: st.success(f"🏆 {t_name}达人: 已完成{count}次 (奖励+10已入账)")
    
    # XP 成就
    ach_list = [("🌱 觉醒", 10), ("🔥 燃魂", 100), ("💎 领主", 500)]
    for name, req in ach_list:
        if st.session_state.xp >= req: st.success(f"👑 {name}: 累计 {req} XP")
        else: st.info(f"🔒 {name}: 目标 {req} XP")

with tab3:
    st.markdown("### 🎰 抽奖中心 (期望值之选)")
    if st.button(f"🧧 消耗 20 XP 抽取随机奖励", use_container_width=True):
        if st.session_state.xp >= 20:
            st.session_state.xp -= 20
            dice = random.random()
            if dice < 0.15: 
                res = random.choice(BIG_REWARDS)
                st.balloons(); st.success(f"🔥 大奖!! 【{res}】")
            elif dice < 0.7: 
                res = random.choice(SMALL_REWARDS)
                st.info(f"🍃 小奖：【{res}】")
            else: st.warning("🕸️ 轮空：系统未检测到奖励信号")
            st.rerun()
    
    st.markdown("### 🏛️ 必中兑换 (昂贵但稳定)")
    for res in BIG_REWARDS:
        cost = 60 # 兑换统一价格
        if st.button(f"购入 {res} ({cost} XP)", use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost
                st.success(f"已解锁：{res}")
                st.rerun()