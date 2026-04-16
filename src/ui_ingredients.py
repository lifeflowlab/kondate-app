import streamlit as st

from src.state import set_selected, set_page


FOODS = {
    "肉": ["焼肉", "カレー", "ハンバーグ"],
    "魚": ["寿司", "焼き魚", "海鮮丼"],
    "麺": ["ラーメン", "うどん", "パスタ"],
    "米": ["炒飯", "親子丼", "カレー"]
}


def render_ingredients():

    st.title("🛒 食材から選ぶ")

    category = st.radio("カテゴリ", list(FOODS.keys()))

    foods = FOODS[category]

    for i, food in enumerate(foods):

        if st.button(food, key=f"{category}_{i}", use_container_width=True):
            set_selected(food)
            return

    st.divider()

    if st.button("← 戻る", use_container_width=True):
        set_page("home")
        return