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
ALL_SCORES = {**BASE_TASKS, **dict(RANDOM_TASKS_POOL)}
MILESTONE_STEPS = [(1, 1), (3, 2), (10, 3), (20, 5)]

CHEAP_REWARDS = {"玩10min手机": 5, "吃颗喜欢的糖": 5, "听3首歌": 8, "看一集短剧": 12, "喝杯好喝的": 15}
BIG_REWARDS = {"顶级烹饪大餐": 60, "专业全身按摩": 60, "微醺酒精时光": 40, "参加沙龙聚会": 50, "买一本新书": 45}

# --- 数据初始化 ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_xp' not in st.session_state: st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state: st.session_state.done_tasks = []
if 'task_counts' not in st.session_state: st.session_state.task_counts = {}
if 'claimed_milestones' not in st.session_state: st.session_state.claimed_milestones = {}
if 'random_pool' not in st.session_state: st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
if 'streak' not in st.session_state: st.session_state.streak = 1
# 新增：今日达标奖励是否已领取
if 'daily_bonus_claimed' not in st.session_state: st.session_state.daily_bonus_claimed = False

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
    # 每日重置领赏状态
    st.session_state.daily_bonus_claimed = False

if 'logged_in' not in st.session_state:
    # 登录给分锁死在10分逻辑
    gain = 1 if st.session_state.daily_xp < 10 else 0
    st.session_state.xp += gain
    st.session_state.daily_xp += gain
    st.session_state.logged_in = True
    st.toast(f"🔌 系统接入！连登第 {st.session_state.streak} 天，奖励 +{gain} XP")

# --- 核心逻辑函数：做任务 ---
def do_task(task_name, score):
    # 计算能涨的能量 (锁死10分)
    space_left = 10 - st.session_state.daily_xp
    gain = min(score, space_left) if space_left > 0 else 0
    
    st.session_state.xp += gain
    st.session_state.daily_xp += gain
    st.session_state.done_tasks.append(task_name)
    st.session_state.task_counts[task_name] = st.session_state.task_counts.get(task_name, 0) + 1
    
    if st.session_state.daily_xp >= 10: st.balloons()
    st.rerun()

# --- 进度条变色逻辑 ---
is_full = st.session_state.daily_xp >= 10
if is_full:
    st.markdown("<style>.stProgress > div > div > div > div { background-color: #FFD700 !important; box-shadow: 0 0 15px #FFD700; }</style>", unsafe_allow_html=True)

# --- UI 布局 ---
st.title("⚡ VIBEQUEST_OS")
c_h, c_v = st.columns([3, 1])
with c_h:
    if is_full: st.markdown("### 🏆 GOLDEN STATUS ACHIEVED")
    else: st.markdown(f"### 🔋 DAILY_ENERGY: {st.session_state.daily_xp}/10")
with c_v:
    st.metric("TOTAL_QP", f"{st.session_state.xp}")

st.progress(min(st.session_state.daily_xp / 10, 1.0))

# --- 满分反馈区域 ---
if is_full:
    with st.container():
        st.success("🎊 恭喜完成今日目标！系统能量已满盈。")
        if not st.session_state.daily_bonus_claimed:
            if st.button("🧧 领取今日达标奖励 (+5 XP)", type="primary", use_container_width=True):
                st.session_state.xp += 5
                st.session_state.daily_bonus_claimed = True
                st.toast("获得额外达标奖励！", icon="🎁")
                st.rerun()
        else:
            st.info("💡 今日达标奖励已领取，明天继续保持。")

tab1, tab2, tab3 = st.tabs(["🎯 任务中心", "🏆 成就阶梯", "🎁 秘密商店"])

# --- Tab 1: 任务中心 ---
with tab1:
    left, right = st.columns(2)
    with left:
        st.markdown("### 💠 基础协议")
        for t, s in BASE_TASKS.items():
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '◻️'} {t} (+{s})", key=f"b_{t}", use_container_width=True, disabled=done):
                do_task(t, s)
    
    with right:
        st.markdown("### 🎲 随机挑战")
        for i, (t, s) in enumerate(st.session_state.random_pool):
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '🔹'} {t} (+{s})", key=f"r_{i}", use_container_width=True, disabled=done):
                do_task(t, s)
        
        if st.button("🔄 刷新任务池 (-1 XP)", use_container_width=True):
            if st.session_state.xp >= 1:
                st.session_state.xp -= 1
                st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
                st.rerun()

# --- Tab 2: 成就系统 (阶梯奖励不受每日10分限制) ---
with tab2:
    exp1 = st.expander("📅 连登里程碑", expanded=True)
    with exp1:
        st.write(f"当前连登：`{st.session_state.streak}` 天")
        if st.session_state.streak >= 7: st.success("🏆 [达成] 连续登录 7 天：你已进入深度自律状态")

    exp2 = st.expander("🛠️ 任务熟练度奖励", expanded=True)
    with exp2:
        for t_name, count in st.session_state.task_counts.items():
            curr_idx = st.session_state.claimed_milestones.get(t_name, -1)
            next_idx = curr_idx + 1
            if next_idx < len(MILESTONE_STEPS):
                target, mult = MILESTONE_STEPS[next_idx]
                base = ALL_SCORES.get(t_name, 1)
                reward = base * mult
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"**{t_name}** | 进度: `{count}/{target}`")
                if count >= target:
                    if col_b.button(f"领取 +{reward}", key=f"claim_{t_name}_{next_idx}", use_container_width=True):
                        st.session_state.xp += reward
                        st.session_state.claimed_milestones[t_name] = next_idx
                        st.rerun()
                else:
                    col_b.button(f"+{reward}", disabled=True, key=f"l_{t_name}", use_container_width=True)

# --- Tab 3: 秘密商店 ---
with tab3:
    st.markdown("### 🎫 微奖励 (小确幸)")
    c1, c2 = st.columns(2)
    for i, (item, cost) in enumerate(CHEAP_REWARDS.items()):
        col = c1 if i % 2 == 0 else c2
        if col.button(f"{item} ({cost}XP)", key=f"c_{i}", use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost
                st.toast(f"兑换成功：{item}！祝享受愉快。", icon="✅")
                st.rerun()
            else:
                st.error("余额不足")

    # --- 抽奖中心逻辑块 ---
st.markdown("---")
st.markdown("### 🎰 混沌抽奖 (20 XP)")

if st.button("🧧 消耗 20 XP 启动概率脉冲", use_container_width=True):
    # 1. 第一步：检查余额
    if st.session_state.xp >= 20:
        # 2. 第二步：扣除 XP
        st.session_state.xp -= 20
        
        # 3. 第三步：摇骰子 (0.0 到 1.0)
        dice = random.random()
        
        # 4. 第四步：概率判定
        # [概率分布: 大奖 10%, 小奖 75%, 自由发挥 10%, 轮空 5%]
        if dice < 0.75:  # 0.0 ~ 0.75 (75% 概率)
            prize_name = random.choice(list(CHEAP_REWARDS.keys()))
            st.info(f"🍃 抽取结果：【小奖 - {prize_name}】")
            st.toast(f"中奖反馈：获得 {prize_name}", icon="✔️")
            
        elif dice < 0.85:  # 0.75 ~ 0.85 (10% 概率)
            prize_name = random.choice(list(BIG_REWARDS.keys()))
            st.balloons() # 全屏彩带庆祝
            st.success(f"🔥 抽取结果：【大奖 - {prize_name}！】")
            st.toast(f"极稀有奖项已解锁！", icon="👑")
            
        elif dice < 0.95:  # 0.85 ~ 0.95 (10% 概率)
            st.warning("✨ 自由发挥：去做一件让你快乐的随机小事吧！")
            st.toast("系统判定：自由行动模式", icon="🎨")
            
        else:  # 0.95 ~ 1.0 (5% 概率)
            st.error("🕸️ 轮空：未命中奖励信号。")
            st.toast("抽取失败，下次好运", icon="💀")
            
        # 5. 第五步：强制刷新页面，让顶部的 TOTAL_QP 跟着变
        st.rerun()
        
    else:
        # 余额不足的反馈
        st.error("XP 不足，无法抽奖。快去完成任务攒分吧！")
        st.toast("余额不足", icon="❌")

    st.markdown("---")
    with st.expander("🏛️ 秘密宝库 (高阶保底兑换)"):
        for item, cost in BIG_REWARDS.items():
            if st.button(f"购入 {item} ({cost}XP)", key=f"b_{item}", use_container_width=True):
                if st.session_state.xp >= cost:
                    st.session_state.xp -= cost
                    st.toast(f"成功购入高级资产：{item}", icon="🏆")
                    st.success(f"已解锁：{item}")
                    st.rerun()
                else:
                    st.error("QP 余额不足")