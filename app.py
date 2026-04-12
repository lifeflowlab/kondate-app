import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="献立ガイド", layout="centered")

# =====================
# 🎨 アプリ風デザイン
# =====================
st.markdown(
    """
<style>
body {
    background-color: #f7f7f7;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
.card {
    background-color: white;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}
.title {
    font-size: 22px;
    font-weight: bold;
}
.menu-title {
    font-size: 18px;
    font-weight: bold;
}
.menu-desc {
    font-size: 14px;
    color: #666;
}
button {
    background-color: #ff8c42 !important;
    color: white !important;
    height: 55px;
    border-radius: 12px;
    font-size: 16px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================
# セッション初期化
# =====================
if "step" not in st.session_state:
    st.session_state.step = "setup"

if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "selected_meal" not in st.session_state:
    st.session_state.selected_meal = None

if "show_recipe" not in st.session_state:
    st.session_state.show_recipe = False

if "last_state" not in st.session_state:
    st.session_state.last_state = "ちょい疲れ"

# =====================
# レシピデータ
# =====================
recipe_data = {
    "親子丼": [
        "① 玉ねぎを薄切り",
        "② 鶏肉を炒める",
        "③ だし・醤油・砂糖を入れる",
        "④ 溶き卵を流し入れる",
        "⑤ ご飯に乗せて完成",
    ],
    "生姜焼き": [
        "① 豚肉を焼く",
        "② 玉ねぎを炒める",
        "③ 醤油・みりん・生姜を加える",
        "④ 全体を絡める",
        "⑤ 盛り付けて完成",
    ],
    "カレー": [
        "① 肉と野菜を炒める",
        "② 水を入れて煮る",
        "③ アクを取る",
        "④ ルーを入れる",
        "⑤ 10分煮込む",
    ],
    "野菜炒め": [
        "① 野菜を切る",
        "② 強火で炒める",
        "③ 塩コショウ",
        "④ 仕上げに醤油",
        "⑤ 完成",
    ],
}

# =====================
# 初期設定
# =====================
if st.session_state.step == "setup":
    st.markdown('<div class="title">🍳 まずは設定（1分）</div>', unsafe_allow_html=True)

    work_style = st.radio("生活スタイル", ["平日中心", "不規則"])
    cook_time = st.radio("料理時間", ["10分", "20分", "30分"])
    priority = st.radio("重視すること", ["楽したい", "バランス", "満足感"])

    if st.button("スタート"):
        st.session_state.settings = {
            "work_style": work_style,
            "cook_time": cook_time,
            "priority": priority,
        }
        st.session_state.step = "main"
        st.rerun()

# =====================
# メイン画面
# =====================
elif st.session_state.step == "main":

    st.markdown(
        '<div class="title">🍳 今日の夕飯どうする？</div>', unsafe_allow_html=True
    )

    state = st.radio(
        "",
        ["かなり疲れた", "ちょい疲れ", "余裕あり"],
        index=["かなり疲れた", "ちょい疲れ", "余裕あり"].index(
            st.session_state.last_state
        ),
    )

    st.session_state.last_state = state

    with st.spinner("献立を考え中..."):
        now = datetime.now()
        hour = now.hour
        settings = st.session_state.settings

        # =====================
        # ロジック
        # =====================
        plan = []

        if state == "かなり疲れた":
            plan.append("時短")
        elif state == "ちょい疲れ":
            plan.append("バランス")
        else:
            plan.append("満足感")

        if hour >= 20:
            plan.append("軽め")

        if settings["priority"] == "楽したい":
            plan.append("時短")
        elif settings["priority"] == "満足感":
            plan.append("満足感")

        menus = {
            "時短": ["野菜炒め", "卵かけご飯", "冷やしうどん"],
            "満足感": ["生姜焼き", "カレー", "親子丼"],
            "軽め": ["焼き魚", "サラダ", "冷奴"],
            "バランス": ["親子丼", "焼き魚定食", "野菜炒め"],
        }

        candidates = []
        for p in plan:
            candidates += menus.get(p, [])

        candidates = [c for c in candidates if c not in st.session_state.history[-3:]]

        random.shuffle(candidates)
        suggestions = list(dict.fromkeys(candidates))[:3]

    # =====================
    # 導き
    # =====================
    st.markdown("👉 今日はこれでいきましょう")

    if random.random() < 0.2:
        st.markdown("✨ ちょっと違うのもアリ")

    # =====================
    # メニュー表示
    # =====================
    for i, meal in enumerate(suggestions):

        st.markdown(
            f"""
        <div class="card">
            <div class="menu-title">🍽 {meal}</div>
            <div class="menu-desc">⏰ 約15分 / すぐできて満足</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        label = "これにする（おすすめ）" if i == 0 else "これにする"

        if st.button(label, key=meal):
            st.session_state.selected_meal = meal
            st.session_state.history.append(meal)
            st.session_state.favorites[meal] = (
                st.session_state.favorites.get(meal, 0) + 1
            )
            st.rerun()

    st.info(f"迷ったら 👉 {suggestions[0] if suggestions else ''}")
    st.markdown("👉 今日はこれで十分です")

    # =====================
    # 決定後画面
    # =====================
    if st.session_state.selected_meal:

        meal = st.session_state.selected_meal

        data = recipe_data.get(meal, ["① 準備中です"])

        st.markdown(
            '<div class="title">🍳 今日の献立はこちら！</div>', unsafe_allow_html=True
        )

        st.markdown(
            f"""
        <div class="card">
            <div class="menu-title">🍽 {meal}</div>
            <div class="menu-desc">👉 今日はこれで決まり</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # ボタン群
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📖 レシピを見る"):
                st.session_state.show_recipe = True

        with col2:
            st.button("🛒 買い物メモ")

        # レシピ表示
        if st.session_state.show_recipe:
            st.markdown("### 📖 作り方")
            for step in data:
                st.markdown(f"- {step}")

            if st.button("閉じる"):
                st.session_state.show_recipe = False
                st.rerun()

        st.markdown("---")

        if st.button("もう一度考える"):
            st.session_state.selected_meal = None
            st.session_state.show_recipe = False
            st.rerun()

        st.stop()
