import streamlit as st

from src.state import init_state
from src.ui_home import render_home
from src.ui_ingredients import render_ingredients
from src.ui_result import render_result
from src.utils import apply_global_style


st.set_page_config(page_title="ごはんAI", layout="centered")

apply_global_style()
init_state()


if st.session_state.page == "home":
    render_home()

elif st.session_state.page == "ingredients":
    render_ingredients()

elif st.session_state.page == "result":
    render_result()