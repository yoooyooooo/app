import streamlit as st
import random
from datetime import datetime, timedelta

# --- 页面设置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="wide")

# --- 极简 CSS 与金色进度条 ---
st.markdown("""
    <style>
        .main .block-container { padding-top: 1.5rem; }
        h1 { font-size: 1.6rem !important; font-weight: 800; }
        h3 { font-size: 1rem !important; color: #888; margin-top: 1rem !important; }
        .stButton>button { border-radius: 8px; margin-bottom: 4px; height: 3rem; }
        /* 进度条基础颜色 */
        .stProgress > div > div > div > div { background-color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 全局配置 ---
BASE_TASKS = {"背单词": 3, "喝一杯水": 1}
RANDOM_TASKS_POOL = [
    ("吃水果", 1), ("5个深呼吸", 1), ("拉伸", 1), ("整理桌面", 1), 
    ("看窗外30s", 1), ("擦屏幕", 1), ("刷牙", 2), ("服维他命", 1), 
    ("找人聊天", 1), ("洗脸清醒", 1), ("科普视频", 1), ("摄入兴奋剂", 1),
    ("购入刚需", 2), ("听英语博客", 2), ("散步30min", 2), ("洗澡/理床", 3),
    ("推动商业计划", 3), ("学数学2h", 3), ("吃顿好饭", 2), ("冥想10min", 2)
]
# 合并所有任务用于查询分值
ALL_SCORES = {**BASE_TASKS, **dict(RANDOM_TASKS_POOL)}

# 成就阶梯: (次数阈值, 奖励倍数)
MILESTONE_STEPS = [(1, 1), (3, 2), (10, 3), (20, 5)]

CHEAP_REWARDS = {"玩10min手机": 5, "吃颗喜欢的糖": 5, "听3首歌": 8, "看一集短剧": 12, "喝杯好喝的": 15}
BIG_REWARDS = {"顶级烹饪大餐": 60, "专业全身按摩": 60, "微醺酒精时光": 40, "参加沙龙聚会": 50, "买一本新书": 45}

# --- 数据初始化 ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_xp' not in st.session_state: st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state: st.session_state.done_tasks = []
if 'task_counts' not in st.session_state: st.session_state.task_counts = {}
if 'claimed_milestones' not in st.session_state: st.session_state.claimed_milestones = {} # {任务名: 达成的阶梯索引}
if 'random_pool' not in st.session_state: st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
if 'streak' not in st.session_state: st.session_state.streak = 1

# --- 每日重置与连登 ---
today = datetime.now().date()
if 'last_date' not in st.session_state: st.session_state.last_date = today

if st.session_state.last_date < today:
    if st.session_state.last_date == today - timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.daily_xp, st.session_state.done_tasks = 0, []
    st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
    st.session_state.last_date, st.session_state.logged_in = today, False

if 'logged_in' not in st.session_state:
    st.session_state.xp += 1; st.session_state.daily_xp += 1
    st.session_state.logged_in = True
    st.toast(f"🔌 系统接入！连登第 {st.session_state.streak} 天，奖励 +1 XP")

# --- 进度条变色逻辑 ---
is_full = st.session_state.daily_xp >= 10
if is_full:
    st.markdown("<style>.stProgress > div > div > div > div { background-color: #FFD700 !important; box-shadow: 0 0 15px #FFD700; }</style>", unsafe_allow_html=True)

# --- UI 布局 ---
st.title("⚡ VIBEQUEST_OS")
c_h, c_v = st.columns([3, 1])
with c_h:
    if is_full: st.markdown("### 🏆 GOLDEN STATUS")
    else: st.markdown(f"### 🔋 DAILY_ENERGY: {st.session_state.daily_xp}/10")
with c_v:
    st.metric("TOTAL_QP", f"{st.session_state.xp}")

st.progress(min(st.session_state.daily_xp / 10, 1.0))

tab1, tab2, tab3 = st.tabs(["🎯 任务中心", "🏆 成就阶梯", "🎁 秘密商店"])

# --- Tab 1: 任务中心 (左右排版) ---
with tab1:
    left, right = st.columns(2)
    with left:
        st.markdown("### 💠 基础协议")
        for t, s in BASE_TASKS.items():
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '◻️'} {t} (+{s})", key=f"b_{t}", use_container_width=True, disabled=done):
                if st.session_state.daily_xp + s <= 10:
                    st.session_state.xp += s; st.session_state.daily_xp += s
                    st.session_state.done_tasks.append(t)
                    st.session_state.task_counts[t] = st.session_state.task_counts.get(t, 0) + 1
                    if st.session_state.daily_xp >= 10: st.balloons()
                    st.rerun()
    
    with right:
        st.markdown("### 🎲 随机挑战")
        for i, (t, s) in enumerate(st.session_state.random_pool):
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '🔹'} {t} (+{s})", key=f"r_{i}", use_container_width=True, disabled=done):
                if st.session_state.daily_xp + s <= 10:
                    st.session_state.xp += s; st.session_state.daily_xp += s
                    st.session_state.done_tasks.append(t)
                    st.session_state.task_counts[t] = st.session_state.task_counts.get(t, 0) + 1
                    if st.session_state.daily_xp >= 10: st.balloons()
                    st.rerun()
        
        if st.button("🔄 刷新任务池 (-1 XP)", use_container_width=True):
            if st.session_state.xp >= 1:
                st.session_state.xp -= 1
                st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
                st.rerun()

# --- Tab 2: 成就系统 (阶梯奖励) ---
with tab2:
    exp1 = st.expander("📅 连登里程碑", expanded=True)
    with exp1:
        st.write(f"当前连登：`{st.session_state.streak}` 天")
        # 简单连登成就示例
        if st.session_state.streak >= 7: st.success("🏆 [达成] 连续登录 7 天：你已进入深度自律状态")

    exp2 = st.expander("🛠️ 任务熟练度奖励", expanded=True)
    with exp2:
        for t_name, count in st.session_state.task_counts.items():
            # 获取当前领到了第几个阶梯
            current_milestone_idx = st.session_state.claimed_milestones.get(t_name, -1)
            next_idx = current_milestone_idx + 1
            
            if next_idx < len(MILESTONE_STEPS):
                target_count, multiplier = MILESTONE_STEPS[next_idx]
                base_score = ALL_SCORES.get(t_name, 1)
                reward_val = base_score * multiplier
                
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"**{t_name}** | 进度: `{count}/{target_count}`")
                
                if count >= target_count:
                    if col_b.button(f"领取 +{reward_val}XP", key=f"claim_{t_name}_{next_idx}", use_container_width=True):
                        st.session_state.xp += reward_val
                        st.session_state.claimed_milestones[t_name] = next_idx
                        st.toast(f"成就达成！获得 {reward_val} XP", icon="⭐")
                        st.rerun()
                else:
                    col_b.button(f"奖励 +{reward_val}XP", disabled=True, key=f"lock_{t_name}_{next_idx}", use_container_width=True)
            else:
                st.write(f"✅ **{t_name}**: 已达成最高熟练度等级！")

# --- Tab 3: 商店中心 (混沌抽奖) ---
with tab3:
    st.markdown("### 🎫 微奖励 (小确幸)")
    c1, c2 = st.columns(2)
    for i, (item, cost) in enumerate(CHEAP_REWARDS.items()):
        col = c1 if i % 2 == 0 else c2
        if col.button(f"{item} ({cost}XP)", key=f"c_{i}", use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost; st.success(f"兑换成功：{item}"); st.rerun()

    st.markdown("---")
    st.markdown("### 🎰 混沌抽奖 (20 XP)")
    if st.button("🧧 消耗 20 XP 抽取脉冲奖励", use_container_width=True):
        if st.session_state.xp >= 20:
            st.session_state.xp -= 20
            dice = random.random()
            # 概率: 小奖 75% | 大奖 10% | 自由发挥 10% | 轮空 5%
            if dice < 0.75:
                res = "小奖：" + random.choice(list(CHEAP_REWARDS.keys()))
                st.info(f"🍃 {res}")
            elif dice < 0.85:
                res = "🔥 大奖：" + random.choice(list(BIG_REWARDS.keys()))
                st.balloons(); st.success(res)
            elif dice < 0.95:
                res = "✨ 自由发挥：去做一件让你快乐的随机小事吧！"
                st.warning(res)
            else:
                st.error("🕸️ 轮空：未命中奖励信号。")
            st.rerun()

    with st.expander("🏛️ 昂贵大奖 (保底兑换)"):
        for item, cost in BIG_REWARDS.items():
            if st.button(f"购入 {item} ({cost}XP)", key=f"big_{item}", use_container_width=True):
                if st.session_state.xp >= cost:
                    st.session_state.xp -= cost; st.success(f"解锁：{item}"); st.rerun()