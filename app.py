import streamlit as st
from src.ui_home import render_app
from src.utils import apply_global_style

st.set_page_config(page_title="やさしいごはんAI", layout="centered")

apply_global_style()

# ===== セッション初期化 =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== 画面遷移 =====
def go(page):
    st.session_state.page = page
    st.rerun()

render_app(go)