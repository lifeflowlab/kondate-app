import streamlit as st
import pandas as pd
import datetime
import os
import random
import time

st.set_page_config(page_title="やさしいごはんAI", layout="centered")

LOG_FILE = "fatigue_log.csv"

# =========================
# STYLE（余白＋余韻設計）
# =========================
st.markdown("""
<style>

.block-container{
    background:#f3f5f9;
    padding-bottom:7rem;
}

.title {
    font-size:22px;
    font-weight:800;
    margin:12px 0;
}

.card {
    background:white;
    border-radius:22px;
    padding:22px;
    box-shadow:0 10px 28px rgba(0,0,0,0.08);
    border-left:6px solid #2ecc71;
}

.big {
    font-size:20px;
    font-weight:800;
    margin-top:10px;
}

.reason {
    font-size:13px;
    color:#666;
    margin-top:10px;
    line-height:1.6;
}

.stButton > button {
    height:58px;
    border-radius:14px;
    font-size:15px;
    font-weight:700;
}

.done {
    text-align:center;
    font-size:16px;
    font-weight:700;
    color:#1f7a4d;
    margin-top:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
def load_df():
    if os.path.exists(LOG_FILE):
        try:
            return pd.read_csv(LOG_FILE, encoding="utf-8")
        except:
            pass
    return pd.DataFrame(columns=["time", "state", "food", "score"])


if "df" not in st.session_state:
    st.session_state.df = load_df()

if "step" not in st.session_state:
    st.session_state.step = "intent"

if "intent" not in st.session_state:
    st.session_state.intent = None


# =========================
# FOOD LOGIC
# =========================
INTENT_MAP = {
    "軽くしたい": ["うどん", "おにぎり", "スープ"],
    "ちゃんと食べたい": ["焼き魚定食", "親子丼", "野菜炒め定食"],
    "好きに食べたい": ["カレー", "ラーメン", "とんかつ", "オムライス"]
}

REASON_MAP = {
    "軽くしたい": "体を休める選択です",
    "ちゃんと食べたい": "バランス重視の選択です",
    "好きに食べたい": "満足感重視の選択です"
}


def calc_score(intent):
    return {
        "軽くしたい": 15,
        "ちゃんと食べたい": 12,
        "好きに食べたい": 10
    }.get(intent, 10)


def save(intent, food, score):
    row = pd.DataFrame([{
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "intent": intent,
        "food": food,
        "score": score
    }])

    file_exists = os.path.exists(LOG_FILE)

    row.to_csv(LOG_FILE,
               mode="a" if file_exists else "w",
               header=not file_exists,
               index=False,
               encoding="utf-8")

    st.session_state.df = pd.concat([st.session_state.df, row], ignore_index=True)


# =========================
# HOME
# =========================
def page_home():

    st.markdown('<div class="title">今日はどうしたいですか？</div>', unsafe_allow_html=True)

    # =========================
    # STEP 1：意思決定（ここが本体）
    # =========================
    if st.session_state.step == "intent":

        st.write("### まず気持ちを選んでください")

        intents = list(INTENT_MAP.keys())

        for i in intents:
            if st.button(i, use_container_width=True):
                st.session_state.intent = i
                st.session_state.step = "food"
                st.rerun()

    # =========================
    # STEP 2：料理確定
    # =========================
    elif st.session_state.step == "food":

        intent = st.session_state.intent

        choices = random.sample(INTENT_MAP[intent], k=3)

        st.markdown(f"""
        <div class="card">
            <div style="font-size:13px;color:#888;">あなたの選択</div>
            <div class="big">{intent}</div>
            <div class="reason">{REASON_MAP[intent]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.write("### 🍽 今日のごはん")

        for food in choices:
            if st.button(food, use_container_width=True):

                with st.spinner("決定しています..."):
                    time.sleep(0.6)

                score = calc_score(intent)
                save(intent, food, score)

                st.balloons()

                st.session_state.step = "done"
                st.session_state.final_food = food

                st.rerun()

    # =========================
    # STEP 3：余韻（ここが最重要）
    # =========================
    elif st.session_state.step == "done":

        st.markdown(f"""
        <div class="card">
            <div style="font-size:13px;color:#888;">🎉 今日のごはん</div>
            <div class="big">{st.session_state.final_food}</div>
            <div class="reason">あなたの選択で決まりました</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="done">✔ 記録完了・今日はもう考えなくてOK</div>', unsafe_allow_html=True)

        if st.button("もう一度決める", use_container_width=True):
            st.session_state.step = "intent"
            st.session_state.intent = None
            st.rerun()


# =========================
# LOG
# =========================
def page_log():

    st.title("記録")

    df = st.session_state.df

    if len(df) > 0:
        st.dataframe(df.tail(10), use_container_width=True)
        st.line_chart(df["score"])
    else:
        st.info("まだ記録がありません")


# =========================
# ROUTER
# =========================
page = st.radio("画面", ["ホーム", "記録"], horizontal=True)

if page == "ホーム":
    page_home()
else:
    page_log()