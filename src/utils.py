import streamlit as st


def apply_global_style():

    st.markdown("""
    <style>

    html, body, [class*="css"] {
        font-family: "Noto Sans JP",
                     "Hiragino Kaku Gothic ProN",
                     sans-serif;
    }

    body {
        background: #121212;
        color: white;
    }

    div.stButton > button {
        height: 55px;
        border-radius: 14px;
        font-size: 18px;
        background: linear-gradient(135deg, #ff6a00, #ffcc00);
        color: black;
        font-weight: bold;
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)