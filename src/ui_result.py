import streamlit as st


def render_result():

    food = st.session_state.selected

    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:40px;
        margin-top:80px;
    ">
        🍽 {food}
    </div>
    """, unsafe_allow_html=True)

    st.success("決定しました")

    if st.button("ホームに戻る", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()