import streamlit as st


def init_state():

    defaults = {
        "page": "home",
        "candidates": [],
        "fatigue": 3,
        "selected": ""
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def set_page(page: str):
    st.session_state.page = page
    st.rerun()


def set_selected(food: str):
    st.session_state.selected = food
    st.session_state.page = "result"
    st.rerun()


def reset_candidates(candidates):
    st.session_state.candidates = candidates