import streamlit as st

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
    # ★重要：疲れ度初期化（50固定・3完全排除）
    # =========================
    if (
        "fatigue" not in st.session_state
        or st.session_state.fatigue is None
        or st.session_state.fatigue == 3   # ← 旧バグ完全対策
    ):
        st.session_state.fatigue = 50

    # =========================
    # 疲れ度スライダー
    # =========================
    fatigue = st.slider(
        "😴 疲れ度",
        min_value=0,
        max_value=100,
        step=5,
        value=int(st.session_state.fatigue),
        key="fatigue_slider"
    )

    # ★一方向更新（戻り防止）
    st.session_state.fatigue = fatigue

    # =========================
    # 表示料理（固定キャッシュ）
    # =========================
    if (
        "current_food" not in st.session_state
        or st.session_state.get("last_fatigue") != fatigue
    ):
        food, category = get_food_by_fatigue(fatigue)
        st.session_state.current_food = food
        st.session_state.current_category = category
        st.session_state.last_fatigue = fatigue

    food = st.session_state.current_food
    category = st.session_state.current_category

    mode_label = get_mode_label(category)

    # =========================
    # 表示UI
    # =========================
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
    # ボタン
    # =========================

    if st.button("🍽 これで決定", use_container_width=True, key="decide"):
        set_selected(food)
        return

    if st.button("🛒 食材から選ぶ", use_container_width=True, key="ingredient"):
        set_page("ingredients")
        return

    if st.button("🔁 もう一回", use_container_width=True, key="reroll"):

        # キャッシュ完全削除
        st.session_state.pop("current_food", None)
        st.session_state.pop("current_category", None)
        st.session_state.pop("last_fatigue", None)

        st.rerun()
        return