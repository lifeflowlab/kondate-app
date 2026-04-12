import streamlit as st

st.set_page_config(
    page_title="Kondate AI",
    layout="wide",
)

# ===== 横画面前提CSS =====
st.markdown("""
<style>
/* 全体を横画面寄せ */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* 右・左の比率調整 */
[data-testid="column"] {
    padding: 0 10px;
}

/* 下部バー風エリア */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #ffffff;
    border-top: 1px solid #ddd;
    padding: 10px;
    z-index: 999;
}

/* ボタン大きく（iPhone想定） */
.stButton > button {
    width: 100%;
    height: 50px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ===== ヘッダー =====
st.title("🍳 Kondate AI（横画面モード）")
st.caption("横画面での使用を推奨しています")

# ===== レイアウト（左右分割） =====
left, right = st.columns([1, 2])

# ===== 左：操作パネル =====
with left:
    st.subheader("🔎 レシピ選択")

    search = st.text_input("レシピ検索")
    category = st.selectbox("カテゴリ", ["和食", "中華", "洋食", "その他"])

    st.markdown("### お気に入り")
    st.button("⭐ カレーライス")
    st.button("⭐ 餃子")
    st.button("⭐ 生姜焼き")

    st.markdown("### 最近使った")
    st.button("🥘 親子丼")
    st.button("🍝 パスタ")

# ===== 右：表示パネル =====
with right:
    st.subheader("📖 レシピ表示")

    recipe = st.selectbox(
        "レシピ",
        ["カレーライス", "餃子", "生姜焼き"]
    )

    st.markdown("### 材料")
    st.write("- 玉ねぎ\n- 肉\n- じゃがいも\n- ルー")

    st.markdown("### 手順")
    st.write("1. 材料を切る\n2. 炒める\n3. 煮込む\n4. ルー投入")

    st.info("💡 AIアドバイス：弱火でじっくり煮込むと旨味UP")

# ===== 下部バー（調味料コントロール） =====
st.markdown("""
<div class="bottom-bar">
    <b>さしすせそコントロール</b>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.button("砂糖")
with col2:
    st.button("塩")
with col3:
    st.button("醤油")
with col4:
    st.button("酢")
with col5:
    st.button("味噌")

st.slider("分量調整", 0, 10, 3)

st.button("🔥 ワンタップ投入（AI自動計算）")