import streamlit as st
import random

from src.logic import (
    get_today_candidates,
    get_default_fatigue,
    get_food_by_fatigue,
    get_mode_label
)

from src.state import set_page, set_selected, reset_candidates


def render_home():

    st.title("🍽 ごはんAI")

    # =========================
    # 候補初期化
    # =========================
    if not st.session_state.candidates:
        reset_candidates(get_today_candidates())

    # =========================
    # ★重要：疲れ度初期化（50固定保証）
    # =========================
    if (
        "fatigue" not in st.session_state
        or st.session_state.fatigue is None
        or st.session_state.fatigue == 3   # ← 旧バグ対策（ここ重要）
    ):
        st.session_state.fatigue = get_default_fatigue()

    # =========================
    # 疲れ度スライダー（0-100 / 5刻み）
    # =========================
    fatigue = st.slider(
        "😴 疲れ度",
        min_value=0,
        max_value=100,
        step=5,
        value=int(st.session_state.fatigue),
        key="fatigue_slider"
    )

    # ★一方向更新（戻り・ズレ防止）
    st.session_state.fatigue = fatigue

    # =========================
    # AI提案
    # =========================
    food, category = get_food_by_fatigue(fatigue)
    mode_label = get_mode_label(category)

    st.markdown(f"""
    <div style="
        text-align:center;
        padding:18px;
        border-radius:16px;
        background: rgba(255,255,255,0.12);
        margin-bottom: 12px;
    ">
        <div style="font-size:14px; opacity:0.8;">
            🤖 {mode_label}
        </div>
        <div style="font-size:28px; font-weight:bold; margin-top:6px;">
            {food}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =========================
    # ボタン群
    # =========================

    if st.button("🍽 これで決定", use_container_width=True, key="decide"):
        set_selected(food)
        return

    if st.button("🛒 食材から選ぶ", use_container_width=True, key="ingredient"):
        set_page("ingredients")
        return

    if st.button("🔁 もう一回", use_container_width=True, key="reroll"):
        reset_candidates(get_today_candidates())
        st.rerun()
        return