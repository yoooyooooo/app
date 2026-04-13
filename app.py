import streamlit as st
import random
from datetime import datetime, timedelta

# --- 1. 页面配置与赛博风格 CSS ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="wide")

st.markdown("""
    <style>
        .main .block-container { padding-top: 1.5rem; }
        h1 { font-size: 1.6rem !important; font-weight: 800; }
        h3 { font-size: 1rem !important; color: #888; margin-top: 0.8rem !important; }
        .stButton>button { border-radius: 8px; margin-bottom: 4px; height: 3rem; }
        /* 进度条基础颜色 */
        .stProgress > div > div > div > div { background-color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心配置 (任务、奖励、成就阶梯) ---
BASE_TASKS = {"背单词": 3, "喝一杯水": 1}
RANDOM_TASKS_POOL = [
    ("吃水果", 1), ("5个深呼吸", 1), ("拉伸", 1), ("整理桌面", 1), 
    ("看窗外30s", 1), ("擦屏幕", 1), ("刷牙", 2), ("服维他命", 1), 
    ("找人聊天", 1), ("洗脸清醒", 1), ("科普视频", 1), ("摄入兴奋剂", 1),
    ("购入刚需", 2), ("听英语博客", 2), ("散步30min", 2), ("洗澡/理床", 3),
    ("推动商业计划", 3), ("学数学2h", 3), ("吃顿好饭", 2), ("冥想10min", 2)
]
ALL_SCORES = {**BASE_TASKS, **dict(RANDOM_TASKS_POOL)}

# 成就阶梯: (次数阈值, 奖励倍数)


CHEAP_REWARDS = {"玩10min手机": 5, "吃颗喜欢的糖": 5, "听3首歌": 8, "看一集短剧": 12, "喝杯好喝的": 15}
BIG_REWARDS = {"顶级烹饪大餐": 60, "专业全身按摩": 70, "微醺酒精时光": 45, "参加沙龙聚会": 55, "买一本新书": 50}

# --- 3. 数据持久化初始化 ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_xp' not in st.session_state: st.session_state.daily_xp = 0
if 'done_tasks' not in st.session_state: st.session_state.done_tasks = []
if 'task_counts' not in st.session_state: st.session_state.task_counts = {}
if 'claimed_milestones' not in st.session_state: st.session_state.claimed_milestones = {}
if 'random_pool' not in st.session_state: st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'daily_bonus_claimed' not in st.session_state: st.session_state.daily_bonus_claimed = False
if 'last_draw_res' not in st.session_state: st.session_state.last_draw_res = None

# --- 4. 每日重置与报错修复逻辑 ---
today = datetime.now().date()

# 修复 TypeError: '<' not supported between instances of 'str' and 'datetime.date'
if 'last_date' not in st.session_state:
    st.session_state.last_date = today

if isinstance(st.session_state.last_date, str):
    try:
        st.session_state.last_date = datetime.strptime(st.session_state.last_date, "%Y-%m-%d").date()
    except:
        st.session_state.last_date = today

# 跨日重置
if st.session_state.last_date < today:
    if st.session_state.last_date == today - timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.daily_xp, st.session_state.done_tasks = 0, []
    st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
    st.session_state.last_date = today
    st.session_state.daily_bonus_claimed, st.session_state.logged_in = False, False

# 登录逻辑
if 'logged_in' not in st.session_state:
    gain = 1 if st.session_state.daily_xp < 10 else 0
    st.session_state.xp += gain; st.session_state.daily_xp += gain
    st.session_state.logged_in = True
    st.toast(f"🔌 系统接入！连登第 {st.session_state.streak} 天")

# --- 5. 任务执行核心算法 ---
def run_task(name, score):
    # 无论是否满分，都记录次数
    st.session_state.task_counts[name] = st.session_state.task_counts.get(name, 0) + 1
    st.session_state.done_tasks.append(name)
    
    # 计算积分增量 (受10分上限限制)
    space = 10 - st.session_state.daily_xp
    gain = min(score, space) if space > 0 else 0
    
    st.session_state.xp += gain
    st.session_state.daily_xp += gain
    
    if st.session_state.daily_xp >= 10: st.balloons()
    st.rerun()

# --- 6. UI 顶栏渲染 ---
is_full = st.session_state.daily_xp >= 10
if is_full:
    st.markdown("<style>.stProgress > div > div > div > div { background-color: #FFD700 !important; box-shadow: 0 0 15px #FFD700; }</style>", unsafe_allow_html=True)

st.title("⚡ VIBEQUEST_OS")
c_title, c_metric = st.columns([3, 1])
with c_title:
    st.markdown(f"### {'🏆 GOLDEN STATUS' if is_full else '🔋 ENERGY: ' + str(st.session_state.daily_xp) + '/10'}")
with c_metric:
    st.metric("TOTAL_QP", st.session_state.xp)

st.progress(min(st.session_state.daily_xp / 10, 1.0))

# 满分领赏区
if is_full:
    if not st.session_state.daily_bonus_claimed:
        if st.button("🧧 领取今日达标奖励 (+5 XP)", type="primary", use_container_width=True):
            st.session_state.xp += 5
            st.session_state.daily_bonus_claimed = True
            st.toast("额外积分已存入宝库！")
            st.rerun()
    else:
        st.info("💡 今日任务已达成，额外奖励已入账。")

# --- 7. 标签页系统 ---
tab1, tab2, tab3 = st.tabs(["🎯 任务中心", "🏆 成就阶梯", "🎁 秘密商店"])

with tab1:
    l, r = st.columns(2)
    with l:
        st.markdown("### 💠 基础协议")
        for t, s in BASE_TASKS.items():
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '◻️'} {t} (+{s})", key=f"b_{t}", use_container_width=True, disabled=done):
                run_task(t, s)
    with r:
        st.markdown("### 🎲 随机挑战")
        for i, (t, s) in enumerate(st.session_state.random_pool):
            done = t in st.session_state.done_tasks
            if st.button(f"{'✅' if done else '🔹'} {t} (+{s})", key=f"r_{i}", use_container_width=True, disabled=done):
                run_task(t, s)
        if st.button("🔄 刷新池 (-1 XP)", use_container_width=True):
            if st.session_state.xp >= 1:
                st.session_state.xp -= 1
                st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
                st.rerun()

# --- 在 Tab 2: 成就阶梯 中替换 ---
with tab2:
    st.markdown("### 📅 七日循環進化序列")
    
    # --- 1. 核心數據計算 ---
    # 計算當前在 7 天週期中的第幾天 (1-7)
    day_in_cycle = ((st.session_state.streak - 1) % 7) + 1
    cycle_count = (st.session_state.streak - 1) // 7
    
    # 定義獎勵梯度
    cycle_rewards = {
        1: 2, 2: 2, 3: 8, 
        4: 3, 5: 15, 6: 5, 
        7: 30  # 周慶大賞
    }
    
    # --- 2. 七日進度條視覺化 ---
    st.write(f"🌀 當前週期：第 {cycle_count + 1} 輪")
    
    # 整體進度條 (例如：第3天 = 3/7 = 42%)
    progress_value = day_in_cycle / 7
    st.progress(progress_value)
    
    # 獎勵預覽面板
    cols = st.columns(7)
    for i in range(1, 8):
        with cols[i-1]:
            # 根據狀態顯示不同樣式
            reward_amt = cycle_rewards[i]
            if i < day_in_cycle:
                st.markdown(f"<div style='text-align:center; color:#888;'>D{i}<br>✅<br><small>{reward_amt}XP</small></div>", unsafe_allow_html=True)
            elif i == day_in_cycle:
                st.markdown(f"<div style='text-align:center; color:#3498db; font-weight:bold;'>D{i}<br>📍<br><small>{reward_amt}XP</small></div>", unsafe_allow_html=True)
            else:
                # 特別加強 Day 7 的視覺效果
                label = "🎁" if i < 7 else "👑"
                st.markdown(f"<div style='text-align:center;'>D{i}<br>{label}<br><small>{reward_amt}XP</small></div>", unsafe_allow_html=True)

    st.write("") # 留白

    # --- 3. 領取按鈕與特效 ---
    claim_key = f"cycle_{cycle_count}_day_{day_in_cycle}"
    if 'cycle_claimed' not in st.session_state:
        st.session_state.cycle_claimed = []

    if claim_key not in st.session_state.cycle_claimed:
        current_bonus = cycle_rewards[day_in_cycle]
        btn_label = f"🚀 領取 Day {day_in_cycle} 獎勵：+{current_bonus} XP"
        
        # 如果是第七天，按鈕顏色加深
        if st.button(btn_label, type="primary" if day_in_cycle == 7 else "secondary", use_container_width=True):
            st.session_state.xp += current_bonus
            st.session_state.cycle_claimed.append(claim_key)
            
            # --- 特效觸發 ---
            if day_in_cycle == 7:
                st.balloons() # 第七天放氣球
                st.toast("🎉 恭喜完成一個進化週期！全系統獎勵已發放。", icon="🏆")
            else:
                st.toast(f"進度推進！獲得 {current_bonus} XP", icon="⚡")
            
            st.rerun()
    else:
        st.button(f"📅 Day {day_in_cycle} 已領取 (明天再來！)", disabled=True, use_container_width=True)

    st.markdown("---")
    # 下方繼續接你的技能專精系統 (LV 系統)...

    # --- 2. 任务熟练度等级系统 ---
    st.markdown("### 🛠️ 技能专精系统")
    st.info("💡 进化规则：每完成 10 次任务升一级。奖励 = 任务基础分 × (当前等级+1) × 5")

    if 'claimed_levels' not in st.session_state:
        st.session_state.claimed_levels = {}

    for t_name, count in st.session_state.task_counts.items():
        # 计算等级
        current_lv = count // 10
        next_lv_count = (current_lv + 1) * 10
        progress = (count % 10) / 10
        
        # UI 容器
        with st.container():
            col_info, col_btn = st.columns([3, 1])
            
            # 左侧：等级显示与进度条
            with col_info:
                st.write(f"**{t_name}** | `LV.{current_lv}`")
                st.progress(progress)
                st.caption(f"进度：{count % 10} / 10 (距下一级还需 {10 - (count % 10)} 次)")
            
            # 右侧：领取逻辑
            last_claimed = st.session_state.claimed_levels.get(t_name, -1)
            
            if current_lv > last_claimed:
                # 有等级可以领取
                base_score = ALL_SCORES.get(t_name, 1)
                reward = base_score * (current_lv + 1) * 5
                if col_btn.button(f"晋升奖励 +{reward}", key=f"lv_up_{t_name}_{current_lv}", use_container_width=True):
                    st.session_state.xp += reward
                    st.session_state.claimed_levels[t_name] = current_lv
                    st.rerun()
            else:
                # 已领取或未达成
                col_btn.button(f"LV.{current_lv} 已达成", disabled=True, key=f"lv_done_{t_name}", use_container_width=True)
        st.write("") # 间距
with tab3:
    st.markdown("### 🎫 微奖励")
    c1, c2 = st.columns(2)
    for i, (item, cost) in enumerate(CHEAP_REWARDS.items()):
        col = c1 if i % 2 == 0 else c2
        if col.button(f"{item} ({cost}XP)", key=f"c_{i}", use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost
                st.toast(f"兑换成功：{item}", icon="✅")
                st.rerun()
            else:
                st.error("余额不足")

    st.markdown("---")
    st.markdown("### 🎰 混沌抽奖 (20 XP)")
    if st.button("🧧 消耗 20 XP 启动概率脉冲", use_container_width=True):
        if st.session_state.xp >= 20:
            st.session_state.xp -= 20
            dice = random.random()
            if dice < 0.75: # 小奖
                p_name = random.choice(list(CHEAP_REWARDS.keys()))
                st.session_state.last_draw_res = ("info", f"🍃 抽取结果：【小奖 - {p_name}】")
            elif dice < 0.85: # 大奖
                p_name = random.choice(list(BIG_REWARDS.keys()))
                st.balloons()
                st.session_state.last_draw_res = ("success", f"🔥 抽取结果：【大奖 - {p_name}！】")
            elif dice < 0.95: # 自由发挥
                st.session_state.last_draw_res = ("warning", "✨ 自由发挥：去做一件让你快乐的随机小事吧！")
            else: # 轮空
                st.session_state.last_draw_res = ("error", "🕸️ 轮空：未命中奖励信号。")
            st.rerun()
        else:
            st.error("XP 不足")

    if st.session_state.last_draw_res:
        t, m = st.session_state.last_draw_res
        if t == "info": st.info(m)
        elif t == "success": st.success(m)
        elif t == "warning": st.warning(m)
        elif t == "error": st.error(m)

    st.markdown("---")
    with st.expander("🏛️ 秘密宝库 (保底大奖)"):
        for item, cost in BIG_REWARDS.items():
            if st.button(f"购入 {item} ({cost}XP)", key=f"big_{item}", use_container_width=True):
                if st.session_state.xp >= cost:
                    st.session_state.xp -= cost
                    st.toast(f"解锁大奖：{item}！", icon="🏆")
                    st.rerun()
                else:
                    st.error("QP 余额不足")