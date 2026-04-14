import streamlit as st
import random
from datetime import datetime, timedelta
import json
import os

# ====================== 【持久化函数】 ======================
DATA_FILE = "vibequest_data.json"

def save_all_data():
    data = {
        "xp": st.session_state.xp,
        "daily_xp": st.session_state.daily_xp,
        "done_tasks": st.session_state.done_tasks,
        "task_counts": st.session_state.task_counts,
        "claimed_milestones": st.session_state.claimed_milestones,
        "random_pool": st.session_state.random_pool,
        "streak": st.session_state.streak,
        "daily_bonus_claimed": st.session_state.daily_bonus_claimed,
        "last_draw_res": st.session_state.last_draw_res,
        "last_date": st.session_state.last_date.strftime("%Y-%m-%d"),
        "logged_in": st.session_state.logged_in,
        "cycle_claimed": st.session_state.cycle_claimed,
        "claimed_levels": st.session_state.claimed_levels,
        "redeem_msg": st.session_state.redeem_msg
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_all_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        st.session_state.xp = data.get("xp", 0)
        st.session_state.daily_xp = data.get("daily_xp", 0)
        st.session_state.done_tasks = data.get("done_tasks", [])
        st.session_state.task_counts = data.get("task_counts", {})
        st.session_state.claimed_milestones = data.get("claimed_milestones", {})
        st.session_state.random_pool = data.get("random_pool", random.sample(RANDOM_TASKS_POOL, 5))
        st.session_state.streak = data.get("streak", 1)
        st.session_state.daily_bonus_claimed = data.get("daily_bonus_claimed", False)
        st.session_state.last_draw_res = data.get("last_draw_res", None)
        st.session_state.logged_in = data.get("logged_in", False)
        st.session_state.cycle_claimed = data.get("cycle_claimed", [])
        st.session_state.claimed_levels = data.get("claimed_levels", {})
        st.session_state.redeem_msg = data.get("redeem_msg", None)

        last_date_str = data.get("last_date")
        if last_date_str:
            try:
                st.session_state.last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            except:
                st.session_state.last_date = datetime.now().date()
        else:
            st.session_state.last_date = datetime.now().date()
    else:
        init_default_state()

def init_default_state():
    st.session_state.xp = 0
    st.session_state.daily_xp = 0
    st.session_state.done_tasks = []
    st.session_state.task_counts = {}
    st.session_state.claimed_milestones = {}
    st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
    st.session_state.streak = 1
    st.session_state.daily_bonus_claimed = False
    st.session_state.last_draw_res = None
    st.session_state.last_date = datetime.now().date()
    st.session_state.logged_in = False
    st.session_state.cycle_claimed = []
    st.session_state.claimed_levels = {}
    st.session_state.redeem_msg = None

# ============================================================

# --- 1. 页面配置 ---
st.set_page_config(page_title="VibeQuest: 进化终端", page_icon="💊", layout="wide")

st.markdown("""
    <style>
        .main .block-container { padding-top: 1.5rem; }
        h1 { font-size: 1.6rem !important; font-weight: 800; }
        h3 { font-size: 1rem !important; color: #888; margin-top: 0.8rem !important; }
        .stButton>button { border-radius: 8px; margin-bottom: 4px; height: 3rem; }
        .stProgress > div > div > div > div { background-color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心配置 ---
BASE_TASKS = {"背单词": 3, "喝一杯水": 1}
RANDOM_TASKS_POOL = [
    ("吃水果", 1), ("5个深呼吸", 1), ("拉伸", 1), ("整理桌面", 1), 
    ("看窗外30s", 1), ("擦屏幕", 1), ("刷牙", 2), ("服维他命", 1), 
    ("找人聊天", 1), ("洗脸清醒", 1), ("科普视频", 1), ("摄入兴奋剂", 1),
    ("购入刚需", 2), ("听英语博客", 2), ("散步30min", 2), ("洗澡/理床", 3),
    ("推动商业计划", 3), ("学数学2h", 3), ("吃顿好饭", 2), ("冥想10min", 2)
]
ALL_SCORES = {**BASE_TASKS, **dict(RANDOM_TASKS_POOL)}

CHEAP_REWARDS = {"玩10min手机": 5, "吃颗喜欢的糖": 5, "听3首歌": 8, "看一集短剧": 12, "喝杯好喝的": 15}
BIG_REWARDS = {"顶级烹饪大餐": 60, "专业全身按摩": 70, "微醺酒精时光": 45, "参加沙龙聚会": 55, "买一本新书": 50}

# --- 3. 加载数据 ---
load_all_data()

# --- 4. 每日重置 ---
today = datetime.now().date()
if 'last_date' not in st.session_state:
    st.session_state.last_date = today

if isinstance(st.session_state.last_date, str):
    try:
        st.session_state.last_date = datetime.strptime(st.session_state.last_date, "%Y-%m-%d").date()
    except:
        st.session_state.last_date = today

if st.session_state.last_date < today:
    if st.session_state.last_date == today - timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.daily_xp = 0
    st.session_state.done_tasks = []
    st.session_state.random_pool = random.sample(RANDOM_TASKS_POOL, 5)
    st.session_state.last_date = today
    st.session_state.daily_bonus_claimed = False
    save_all_data()

if not st.session_state.logged_in:
    gain = 1 if st.session_state.daily_xp < 10 else 0
    st.session_state.xp += gain
    st.session_state.daily_xp += gain
    st.session_state.logged_in = True
    save_all_data()
    st.toast(f"🔌 系统接入！连登第 {st.session_state.streak} 天")

# --- 5. 任务执行 ---
def run_task(name, score):
    st.session_state.task_counts[name] = st.session_state.task_counts.get(name, 0) + 1
    st.session_state.done_tasks.append(name)
    space = 10 - st.session_state.daily_xp
    gain = min(score, space) if space > 0 else 0
    st.session_state.xp += gain
    st.session_state.daily_xp += gain
    if st.session_state.daily_xp >= 10:
        st.balloons()
    save_all_data()
    st.rerun()

# --- 6. UI ---
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

if is_full:
    if not st.session_state.daily_bonus_claimed:
        if st.button("🧧 领取今日达标奖励 (+5 XP)", type="primary", use_container_width=True):
            st.session_state.xp += 5
            st.session_state.daily_bonus_claimed = True
            save_all_data()
            st.toast("额外积分已存入宝库！")
            st.rerun()
    else:
        st.info("💡 今日任务已达成，额外奖励已入账。")

# --- 标签页 ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 任务中心", "🏆 成就阶梯", "🎁 秘密商店", "⚙️ 设置"])

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
                save_all_data()
                st.rerun()

with tab2:
    st.markdown("### 📅 七日循環進化序列")
    day_in_cycle = ((st.session_state.streak - 1) % 7) + 1
    cycle_count = (st.session_state.streak - 1) // 7
    cycle_rewards = {1:2,2:2,3:8,4:3,5:15,6:5,7:30}
    st.write(f"🌀 當前週期：第 {cycle_count + 1} 輪")
    st.progress(day_in_cycle / 7)
    cols = st.columns(7)
    for i in range(1,8):
        with cols[i-1]:
            r = cycle_rewards[i]
            if i < day_in_cycle:
                st.markdown(f"<div style='text-align:center;color:#888'>D{i}<br>✅<br><small>{r}XP</small></div>", unsafe_allow_html=True)
            elif i == day_in_cycle:
                st.markdown(f"<div style='text-align:center;color:#3498db;font-weight:bold'>D{i}<br>📍<br><small>{r}XP</small></div>", unsafe_allow_html=True)
            else:
                lb = "🎁" if i<7 else "👑"
                st.markdown(f"<div style='text-align:center'>D{i}<br>{lb}<br><small>{r}XP</small></div>", unsafe_allow_html=True)
    st.write("")
    claim_key = f"cycle_{cycle_count}_day_{day_in_cycle}"
    if claim_key not in st.session_state.cycle_claimed:
        current_bonus = cycle_rewards[day_in_cycle]
        btn = f"🚀 領取 Day {day_in_cycle} 獎勵：+{current_bonus} XP"
        if st.button(btn, type="primary" if day_in_cycle==7 else "secondary", use_container_width=True):
            st.session_state.xp += current_bonus
            st.session_state.cycle_claimed.append(claim_key)
            if day_in_cycle==7:
                st.balloons()
                st.toast("🎉 周期完成！",icon="🏆")
            else:
                st.toast(f"+{current_bonus} XP",icon="⚡")
            save_all_data()
            st.rerun()
    else:
        st.button(f"📅 Day {day_in_cycle} 已領取", disabled=True, use_container_width=True)
    st.markdown("---")
    st.markdown("### 🛠️ 技能专精系统")
    st.info("💡 进化规则：每完成 10 次任务升一级。奖励 = 基础分 × (等级+1) ×5")
    for t_name, count in st.session_state.task_counts.items():
        current_lv = count //10
        next_lv_count = (current_lv+1)*10
        progress = (count%10)/10
        with st.container():
            col_info, col_btn = st.columns([3,1])
            with col_info:
                st.write(f"**{t_name}** | `LV.{current_lv}`")
                st.progress(progress)
                st.caption(f"{count%10}/10 还差 {10-(count%10)} 次")
            last_claimed = st.session_state.claimed_levels.get(t_name,-1)
            if current_lv > last_claimed:
                base = ALL_SCORES.get(t_name,1)
                reward = base*(current_lv+1)*5
                if col_btn.button(f"+{reward}",key=f"lv_{t_name}",use_container_width=True):
                    st.session_state.xp += reward
                    st.session_state.claimed_levels[t_name] = current_lv
                    save_all_data()
                    st.rerun()
            else:
                col_btn.button(f"LV.{current_lv}",disabled=True,key=f"done_{t_name}",use_container_width=True)
        st.write("")

with tab3:
    if st.session_state.redeem_msg:
        st.success(st.session_state.redeem_msg)
        st.session_state.redeem_msg = None
        save_all_data()
    st.markdown("### 🎫 微奖励")
    c1,c2 = st.columns(2)
    for i,(item,cost) in enumerate(CHEAP_REWARDS.items()):
        col = c1 if i%2==0 else c2
        if col.button(f"{item} ({cost}XP)",key=f"c_{i}",use_container_width=True):
            if st.session_state.xp >= cost:
                st.session_state.xp -= cost
                st.session_state.redeem_msg = f"✅ 兑换成功：{item}"
                save_all_data()
                st.toast("兑换成功！",icon="🎁")
                st.rerun()
            else:
                st.error("XP不足")
    st.markdown("---")
    st.markdown("### 🎰 混沌抽奖 (20 XP)")
    if st.button("🧧 启动抽奖",use_container_width=True):
        if st.session_state.xp >=20:
            st.session_state.xp -=20
            dice = random.random()
            if dice<0.75:
                p = random.choice(list(CHEAP_REWARDS.keys()))
                st.session_state.last_draw_res = ("info",f"🍃 小奖：{p}")
                st.toast(f"中奖：{p}")
            elif dice<0.85:
                p = random.choice(list(BIG_REWARDS.keys()))
                st.session_state.last_draw_res = ("success",f"🔥 大奖：{p}！")
                st.balloons()
                st.toast("大奖！",icon="👑")
            elif dice<0.95:
                st.session_state.last_draw_res = ("warning","✨ 自由发挥！")
            else:
                st.session_state.last_draw_res = ("error","🕸️ 轮空")
            save_all_data()
            st.rerun()
        else:
            st.error("XP不足")
    if st.session_state.last_draw_res:
        t,m = st.session_state.last_draw_res
        if t=="info":st.info(m)
        elif t=="success":st.success(m)
        elif t=="warning":st.warning(m)
        elif t=="error":st.error(m)
    st.markdown("---")
    with st.expander("🏛️ 秘密宝库"):
        for item,cost in BIG_REWARDS.items():
            if st.button(f"兑换：{item} ({cost}XP)",key=f"big_{item}",use_container_width=True):
                if st.session_state.xp >= cost:
                    st.session_state.xp -= cost
                    st.session_state.redeem_msg = f"🏆 兑换成功：{item}"
                    save_all_data()
                    st.toast("大奖解锁！",icon="🏆")
                    st.rerun()
                else:
                    st.error("XP不足")

# --- 【新增：设置页 + 重置按钮】 ---
with tab4:
    st.markdown("### ⚙️ 系统设置")
    st.markdown("#### 🗑️ 数据管理")
    st.warning("⚠️ 重置后所有数据（XP、等级、连登、任务历史）将永久删除，无法恢复！")
    
    col1, col2 = st.columns([3,1])
    with col1:
        confirm_reset = st.checkbox("我已确认，要彻底重置所有数据")
    with col2:
        if st.button("执行重置", type="secondary", use_container_width=True, disabled=not confirm_reset):
            # 删除数据文件
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            # 清空 session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ 系统已重置！页面即将重启...")
            st.rerun()
    
    st.markdown("---")
    st.markdown("#### ℹ️ 关于")
    st.info("VibeQuest OS v1.0\n赛博朋克风格每日自律进化系统")