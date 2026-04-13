import streamlit as st
import random
import time
from datetime import datetime

# --- 页面设置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="centered")

# --- 样式美化：金色进度条 ---
if 'daily_xp' in st.session_state and st.session_state.daily_xp >= 10:
    # 当达到10分时，通过CSS把进度条变成金色并加一点闪烁效果
    st.markdown("""
        <style>
            .stProgress > div > div > div > div {
                background-color: #FFD700;
                box-shadow: 0 0 10px #FFD700;
            }
        </style>
    """, unsafe_allow_html=True)

# --- 任务库定义 (在这里修改你的任务) ---
ALL_RANDOM_TASKS = [
    ("吃一个水果", 1), ("做5个深呼吸", 1), ("站起来拉伸", 1),
    ("丢掉3件垃圾", 1), ("看窗外30秒", 1), ("擦一下手机屏幕", 1),
    ("翻开书看1页", 1), ("听一首新歌", 1), ("给老友点赞", 1),
    ("洗个脸清醒下", 1), ("记录一句心情", 1), ("手冲一杯咖啡", 1),
    ("听英语博客", 2), ("散步20分钟", 2), ("整理代码逻辑", 3),
    ("推动商业计划", 3), ("学数学1小时", 3), ("冥想10分钟", 2)
]

# --- 数据初始化 ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'daily_xp' not in st.session_state:
    st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = []
if 'random_pool' not in st.session_state:
    # 初始随机抽 5 个任务
    st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)

# --- 每日重置逻辑 (简单模拟) ---
today = datetime.now().strftime('%Y-%m-%d')
if 'last_date' not in st.session_state:
    st.session_state.last_date = today

if st.session_state.last_date != today:
    st.session_state.daily_xp = 0
    st.session_state.done_tasks = []
    st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
    st.session_state.last_date = today
    st.session_state.logged_in = False

# --- 心理学：上线自动加分 ---
if 'logged_in' not in st.session_state:
    st.session_state.xp += 1
    st.session_state.daily_xp += 1
    st.session_state.logged_in = True
    st.toast("⚡ 系统接入：上线奖励 +1 XP", icon="🔌")

# --- UI 界面 ---
st.title("⚡ VIBEQUEST_OS")
st.caption(f"STATUS: ACTIVE | {today} | TOTAL_XP: {st.session_state.xp}")

# 进度条展示
if st.session_state.daily_xp >= 10:
    st.subheader("🎊 今日目标已达成！(GOLDEN STATUS)")
else:
    st.subheader(f"今日进度: {st.session_state.daily_xp} / 10 XP")

st.progress(min(st.session_state.daily_xp / 10, 1.0))

# --- 标签页切换 ---
tab1, tab2, tab3 = st.tabs(["🎯 任务大厅", "🏆 成就系统", "🎁 兑换中心"])

with tab1:
    # 基础任务
    st.markdown("### 💠 基础协议 (必修)")
    base_tasks = {"背单词": 3, "喝一杯水": 1}
    
    for task, score in base_tasks.items():
        col1, col2 = st.columns([3, 1])
        is_done = task in st.session_state.done_tasks
        if is_done:
            col1.write(f"✅ ~~{task}~~ (+{score})")
            col2.button("已完", key=f"base_{task}", disabled=True)
        else:
            col1.write(f"◻️ {task} (+{score}XP)")
            if col2.button("执行", key=f"base_{task}"):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.rerun()
                else:
                    st.warning("能量将超出上限，请选择更简单的任务或休息。")

    st.divider()

    # 随机任务
    col_head, col_refresh = st.columns([3, 1])
    col_head.markdown("### 🎲 随机挑战 (选修)")
    
    # 刷新按钮逻辑：扣1分
    if col_refresh.button("🔄 刷新 (-1XP)"):
        if st.session_state.xp >= 1:
            st.session_state.xp -= 1
            st.session_state.random_pool = random.sample(ALL_RANDOM_TASKS, 5)
            st.toast("正在重新扫描任务脉冲...", icon="📡")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("积分不足！")

    for i, (task, score) in enumerate(st.session_state.random_pool):
        col1, col2 = st.columns([3, 1])
        is_done = task in st.session_state.done_tasks
        if is_done:
            col1.write(f"✅ ~~{task}~~ (+{score})")
            col2.button("已完", key=f"rand_done_{i}", disabled=True)
        else:
            col1.write(f"🔹 {task} (+{score}XP)")
            if col2.button("领赏", key=f"rand_{i}"):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("今日经验已达 10 分上限！")

with tab2:
    st.subheader("成就奖章")
    # 这里可以根据 xp 动态显示
    ach_list = [
        ("🌱 初觉醒", "累计 10 XP", 10),
        ("🔥 燃魂者", "累计 100 XP", 100),
        ("💎 秩序主教", "累计 500 XP", 500)
    ]
    for name, desc, req in ach_list:
        if st.session_state.xp >= req:
            st.success(f"👑 **{name}** - {desc} (已达成)")
        else:
            st.write(f"🔒 **{name}** - {desc} (需要 {req} XP)")

with tab3:
    st.subheader("积分兑换")
    st.metric("可用 QP", st.session_state.xp)
    
    cost = 20
    if st.button(f"🧧 消耗 {cost} XP 抽取现实奖励"):
        if st.session_state.xp >= cost:
            rewards = ["点一份好吃的晚餐", "看一部喜欢的电影", "奖励一段纯粹的玩游戏时间", "买一个想买很久的小玩意"]
            res = random.choice(rewards)
            st.balloons()
            st.session_state.xp -= cost
            st.success(f"抽取结果：【{res}】")
            st.rerun()
        else:
            st.error("QP 余额不足！")