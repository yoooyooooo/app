import streamlit as st
import random
import time
from datetime import datetime

# --- 页面设置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="centered")

# --- 数据初始化 (加入持久化逻辑) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'daily_xp' not in st.session_state:
    st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = []
if 'random_pool' not in st.session_state:
    # 选修任务池
    pool = [
        ("吃一个水果", 1), ("刷牙", 1), ("听英语博客", 2), 
        ("散步半小时", 2), ("学数学两小时", 3), ("推动商业计划", 3)
    ]
    st.session_state.random_pool = random.sample(pool, 3) # 每天随机抽3个

# --- 心理学驱动逻辑：上线自动加分 ---
if 'logged_in' not in st.session_state:
    st.session_state.xp += 1
    st.session_state.daily_xp += 1
    st.session_state.logged_in = True
    st.toast("⚡ 系统接入：上线奖励 +1 XP", icon="🔌")

# --- UI 界面 ---
st.title("⚡ VIBEQUEST_OS")
st.caption(f"STATUS: ACTIVE | {datetime.now().strftime('%Y-%m-%d')}")

# 进度条：每日 10 分上限 (心理学：目标可视化)
st.subheader(f"今日进度: {st.session_state.daily_xp} / 10 XP")
st.progress(min(st.session_state.daily_xp / 10, 1.0))

# --- 任务板块 ---
tab1, tab2, tab3 = st.tabs(["🎯 今日任务", "🏆 成就系统", "🎁 兑换中心"])

with tab1:
    st.markdown("### 基础任务 (必修)")
    base_tasks = {"背单词": 3, "喝一杯水": 1}
    for task, score in base_tasks.items():
        col1, col2 = st.columns([3, 1])
        is_done = task in st.session_state.done_tasks
        col1.write(f"{'✅' if is_done else '◻️'} {task} (+{score}XP)")
        if not is_done:
            if col2.button("完成", key=task):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.rerun()
                else:
                    st.warning("今日能量已满，建议休息。")

    st.markdown("---")
    st.markdown("### 随机挑战 (选修)")
    for task, score in st.session_state.random_pool:
        col1, col2 = st.columns([3, 1])
        is_done = task in st.session_state.done_tasks
        col1.write(f"{'🎲' if not is_done else '✅'} {task} (+{score}XP)")
        if not is_done:
            if col2.button("完成", key=task):
                if st.session_state.daily_xp + score <= 10:
                    st.session_state.xp += score
                    st.session_state.daily_xp += score
                    st.session_state.done_tasks.append(task)
                    st.rerun()
                else:
                    st.warning("今日能量已满。")

with tab2:
    st.subheader("成就列表")
    achievements = [
        ("初级进化", "累计获得 50 XP", 50),
        ("秩序之神", "连续 3 天达成 10 分满分", 150)
    ]
    for title, desc, req in achievements:
        unlocked = st.session_state.xp >= req
        st.write(f"{'👑' if unlocked else '🔒'} **{title}**: {desc}")

with tab3:
    st.subheader("秘密商店")
    st.metric("可用积分", f"{st.session_state.xp} QP")
    if st.button("🧧 消耗 20 积分抽取『随机现实奖励』"):
        if st.session_state.xp >= 20:
            rewards = ["允许看一集番剧", "允许喝一杯奶茶", "允许发呆 15 分钟"]
            st.balloons()
            st.success(f"抽取结果：{random.choice(rewards)}")
            st.session_state.xp -= 20
        else:
            st.error("积分不足，去执行任务吧！")