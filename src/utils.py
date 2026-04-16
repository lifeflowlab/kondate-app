import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>

    body {
        background: linear-gradient(180deg, #0f0f10, #1c1c1e);
        color: white;
    }

    div.stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 16px;
        font-size: 18px;
        margin-bottom: 8px;
        background: rgba(255,255,255,0.08);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }

    div.stButton > button:hover {
        transform: scale(1.02);
    }

    </style>
    """, unsafe_allow_html=True)