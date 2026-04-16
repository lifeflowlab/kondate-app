import streamlit as st
import time
from src.logic import (
    get_today_candidates,
    get_default_intent,
    sort_by_intent,
    force_pick,
    get_day_label
)
from src.data import save_log


def render_app(go):

    if st.session_state.page == "home":
        render_home(go)


# =========================
# HOME
# =========================
def render_home(go):

    st.title("🍽 ごはん決める")

    # ===== 初期化 =====
    if "candidates" not in st.session_state:
        st.session_state.candidates = get_today_candidates()

    if "intent" not in st.session_state:
        st.session_state.intent = get_default_intent()

    # ===== 意向ボタン =====
    st.markdown("### 少しだけ条件")

    intents = ["なし", "節約", "ヘルシー", "がっつり", "時短"]
    cols = st.columns(len(intents))

    for i, intent in enumerate(intents):
        with cols[i]:
            if st.button(intent, key=f"intent_{i}"):
                st.session_state.intent = intent

    # ===== 並び替え =====
    sorted_list = sort_by_intent(
        st.session_state.candidates,
        st.session_state.intent
    )

    # ===== 強制決定（最上部）=====
    best = force_pick(sorted_list)

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.18);
        padding: 16px;
        border-radius: 16px;
        text-align:center;
        animation: pulse 1.2s infinite;
    ">
        🤖 これでOK → <b>{best}</b>
    </div>

    <style>
    @keyframes pulse {{
        0% {{transform: scale(1);}}
        50% {{transform: scale(1.05);}}
        100% {{transform: scale(1);}}
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"👉 これで決定：{best}", key="force"):
        finalize(best)

    # ===== 候補表示（視線誘導）=====
    st.markdown("### 👉 他の候補")

    if len(sorted_list) >= 1:
        if st.button(sorted_list[0], key="top"):
            finalize(sorted_list[0])

    if len(sorted_list) >= 2:
        cols = st.columns([1,2,1])
        with cols[1]:
            if st.button(sorted_list[1], key="mid"):
                finalize(sorted_list[1])

    if len(sorted_list) >= 3:
        if st.button(sorted_list[2], key="bot"):
            finalize(sorted_list[2])

    # ===== 再抽選 =====
    st.divider()

    if st.button("🔁 もう一回"):
        st.session_state.candidates = get_today_candidates()
        st.rerun()


# =========================
# 決定処理
# =========================
def finalize(food):

    save_log("final", food)

    st.success(f"{food} に決定！")
    st.info(get_day_label(food))

    time.sleep(1)
    st.session_state.page = "home"
    st.rerun()