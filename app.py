import streamlit as st
import pandas as pd
from datetime import datetime

# --- 页面配置 (仪式感第一步) ---
st.set_page_config(page_title="VibeQuest: Core", page_icon="⚡", layout="centered")

# --- 模拟数据库 (实际建议接入 Supabase) ---
if 'pts' not in st.session_state:
    st.session_state.pts = 0
if 'tasks_done' not in st.session_state:
    st.session_state.tasks_done = set()

# --- 游戏逻辑函数 ---
def calculate_reward(task_count):
    if task_count == 0: return 1  # 登录分
    if task_count <= 2: return 3  # 前两个任务性价比最高
    if task_count == 3: return 4  # 达标关键分
    return 0.5                    # 之后的任务收益递减

# --- UI 渲染 ---
st.title("⚡ VIBEQUEST_OS")
st.caption(f"SYSTEM DATE: {datetime.now().strftime('%Y-%m-%d')} | USER: ADMIN")

# 1. 状态看板
col1, col2 = st.columns(2)
with col1:
    st.metric("CURRENT_PTS", f"{st.session_state.pts} QP")
with col2:
    progress = min(len(st.session_state.tasks_done) / 3, 1.0)
    st.write(f"DAILY_ACTIVE: {int(progress*100)}%")
    st.progress(progress)

st.divider()

# 2. 任务大厅 (Quests)
quests = {
    "Q1": "深色模式深度工作 (2h)",
    "Q2": "生理机能维护 (运动/健身)",
    "Q3": "精神内核升级 (阅读/学习)",
    "Q4": "环境有序化 (整理/打扫)",
    "Q5": "随机探索 (陌生领域尝试)"
}

st.subheader("ACTIVE_QUESTS")
for qid, desc in quests.items():
    is_done = qid in st.session_state.tasks_done
    if st.button(f"{'✅' if is_done else '◻️'} {desc}", key=qid):
        if qid not in st.session_state.tasks_done:
            reward = calculate_reward(len(st.session_state.tasks_done) + 1)
            st.session_state.pts += reward
            st.session_state.tasks_done.add(qid)
            st.toast(f"SYSC: Reward +{reward} QP Cached.", icon="💾")
            st.rerun()

# 3. 兑换逻辑 (针对你的低物欲)
st.divider()
with st.expander("DECODE_REWARDS (兑换中心)"):
    st.info("当前奖励：积分用于解锁下周『系统皮肤』或『随机大冒险指令』")
    if st.button("消耗 10 QP 抽取『强制随机行动建议』"):
        if st.session_state.pts >= 10:
            st.success("指令：去买一瓶从没喝过的饮料。")
            st.session_state.pts -= 10
        else:
            st.error("INSUFFICIENT_FUNDS: 积分不足")