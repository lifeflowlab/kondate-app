import streamlit as st
import pandas as pd
import datetime
import os
import random
import time

st.set_page_config(page_title="やさしいごはんAI", layout="centered", initial_sidebar_state="collapsed")

LOG_FILE = "fatigue_log.csv"

# =========================
# STYLE（iPhone対応・スクロール最小化）
# =========================
st.markdown("""
<style>

* {
    box-sizing: border-box;
}

.block-container{
    background:linear-gradient(180deg, #fffaf6 0%, #fffcf8 50%, #fffaf6 100%);
    padding:12px 16px 80px 16px;
    min-height:100vh;
    max-width:100%;
}

html, body {
    background:#fffaf6;
    margin:0;
    padding:0;
}

.title {
    font-size:24px;
    font-weight:900;
    margin:8px 0;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fdba74 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    letter-spacing:-0.5px;
}

.card {
    background:white;
    border-radius:16px;
    padding:16px;
    border:1px solid rgba(249,115,22,0.08);
    box-shadow:0 4px 12px rgba(249,115,22,0.04);
    transition:all 0.3s ease;
    margin-bottom:12px;
}

.card:hover {
    border:1px solid rgba(249,115,22,0.15);
    box-shadow:0 6px 16px rgba(249,115,22,0.08);
}

.big {
    font-size:18px;
    font-weight:700;
    margin-top:8px;
    color:#78350f;
}

.big-final {
    font-size:48px;
    font-weight:900;
    margin-top:12px;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1.1;
}

.reason {
    font-size:12px;
    color:#92400e;
    margin-top:8px;
    line-height:1.5;
}

.suggestion {
    font-size:13px;
    color:#b45309;
    margin-top:12px;
    padding:12px;
    background:linear-gradient(135deg, rgba(249,115,22,0.06) 0%, rgba(253,186,116,0.04) 100%);
    border-radius:10px;
    border-left:3px solid #f97316;
}

.stButton > button {
    height:48px;
    border-radius:10px;
    font-size:14px;
    font-weight:700;
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%);
    color:#78350f;
    border:none;
    transition: all 0.3s ease;
    text-transform:uppercase;
    letter-spacing:0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(249,115,22,0.3);
}

.stButton > button:active {
    transform: translateY(0);
}

.history-card {
    background:white;
    border-radius:14px;
    padding:12px;
    margin-bottom:8px;
    border:1px solid rgba(249,115,22,0.06);
    box-shadow:0 2px 8px rgba(249,115,22,0.03);
}

.history-date {
    font-size:10px;
    color:#a16207;
    margin-bottom:4px;
}

.history-food {
    font-size:16px;
    font-weight:700;
    color:#f97316;
    margin:6px 0;
}

.history-intent {
    font-size:11px;
    color:#fff;
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%);
    display:inline-block;
    padding:3px 10px;
    border-radius:6px;
}

.stat-box {
    background:white;
    border-radius:14px;
    padding:14px;
    text-align:center;
    border:1px solid rgba(249,115,22,0.08);
    box-shadow:0 2px 8px rgba(249,115,22,0.03);
    transition:all 0.3s ease;
}

.stat-number {
    font-size:32px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fdba74 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}

.stat-label {
    font-size:11px;
    color:#a16207;
    margin-top:4px;
}

.fatigue-card {
    background:linear-gradient(135deg, rgba(249,115,22,0.04) 0%, rgba(253,186,116,0.03) 100%);
    border-radius:16px;
    padding:20px;
    border:1px solid rgba(249,115,22,0.1);
    margin-bottom:12px;
    transition: all 0.3s ease;
    box-shadow:0 4px 12px rgba(249,115,22,0.05);
}

.fatigue-label {
    font-size:12px;
    font-weight:600;
    color:#92400e;
    margin-bottom:8px;
    text-transform:uppercase;
    letter-spacing:0.5px;
}

.fatigue-value {
    font-size:52px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fdba74 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    text-align:center;
    margin:8px 0;
}

.welcome-section {
    background:linear-gradient(135deg, rgba(249,115,22,0.08) 0%, rgba(253,186,116,0.06) 100%);
    border-radius:16px;
    padding:16px;
    margin-bottom:12px;
    text-align:center;
    border:1px solid rgba(249,115,22,0.12);
    box-shadow:0 4px 12px rgba(249,115,22,0.05);
}

.welcome-emoji {
    font-size:40px;
    margin-bottom:8px;
    animation:bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform:translateY(0); }
    50% { transform:translateY(-8px); }
}

.welcome-text {
    font-size:16px;
    font-weight:800;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin-bottom:4px;
}

.welcome-subtitle {
    font-size:12px;
    color:#92400e;
    line-height:1.5;
}

.recommended-card {
    background:white;
    border-radius:16px;
    padding:16px;
    border:1px solid rgba(249,115,22,0.08);
    margin-bottom:12px;
    transition: all 0.3s ease;
    box-shadow:0 4px 12px rgba(249,115,22,0.05);
}

.recommended-label {
    font-size:10px;
    color:#92400e;
    text-transform:uppercase;
    letter-spacing:1px;
    font-weight:700;
}

.recommended-food {
    font-size:32px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin:8px 0;
}

.recommended-reason {
    font-size:12px;
    color:#92400e;
    margin-top:8px;
    line-height:1.5;
}

.recommendation-item {
    background:linear-gradient(135deg, rgba(249,115,22,0.04) 0%, rgba(253,186,116,0.03) 100%);
    border-radius:14px;
    padding:14px;
    margin-bottom:8px;
    border:1px solid rgba(249,115,22,0.08);
    transition: all 0.3s ease;
}

.recommendation-title {
    font-size:11px;
    color:#92400e;
    text-transform:uppercase;
    letter-spacing:0.3px;
    font-weight:700;
    margin-bottom:4px;
}

.recommendation-food-name {
    font-size:26px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin:6px 0;
}

.recommendation-desc {
    font-size:11px;
    color:#92400e;
    line-height:1.4;
}

.streak-badge {
    display:inline-block;
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%);
    color:#78350f;
    padding:8px 16px;
    border-radius:10px;
    font-size:12px;
    font-weight:700;
    margin-bottom:12px;
    box-shadow:0 2px 8px rgba(249,115,22,0.2);
    animation:pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform:scale(1); }
    50% { transform:scale(1.02); }
}

.info-message {
    background:linear-gradient(135deg, rgba(34,197,94,0.06) 0%, rgba(59,130,246,0.04) 100%);
    border-left:3px solid #22c55e;
    border-radius:8px;
    padding:10px;
    font-size:12px;
    color:#15803d;
    border:1px solid rgba(34,197,94,0.1);
    margin-bottom:12px;
}

.warning-message {
    background:linear-gradient(135deg, rgba(249,115,22,0.06) 0%, rgba(253,186,116,0.05) 100%);
    border-left:3px solid #f97316;
    border-radius:8px;
    padding:10px;
    font-size:12px;
    color:#92400e;
    border:1px solid rgba(249,115,22,0.1);
    margin-bottom:12px;
}

.progress-bar {
    background:linear-gradient(90deg, rgba(249,115,22,0.1) 0%, rgba(253,186,116,0.08) 100%);
    height:5px;
    border-radius:3px;
    overflow:hidden;
    margin-top:6px;
}

.progress-fill {
    background:linear-gradient(90deg, #f97316 0%, #fdba74 100%);
    height:100%;
    transition:width 0.5s ease;
    border-radius:3px;
}

hr {
    border:none;
    height:1px;
    background:linear-gradient(90deg, transparent, rgba(249,115,22,0.1), transparent);
    margin:12px 0;
}

.nav-button-home {
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%) !important;
    color:#78350f !important;
}

.nav-button-record {
    background:linear-gradient(135deg, #fed7aa 0%, #fef3c7 100%) !important;
    color:#92400e !important;
}

.nav-button-home:hover {
    box-shadow: 0 6px 12px rgba(249,115,22,0.3) !important;
}

.nav-button-record:hover {
    box-shadow: 0 6px 12px rgba(249,115,22,0.2) !important;
}

@media (max-width: 390px) {
    .block-container {
        padding: 10px 12px 80px 12px;
    }
    
    .title {
        font-size: 22px;
        margin: 6px 0;
    }
    
    .fatigue-value {
        font-size: 48px;
    }
    
    .big-final {
        font-size: 44px;
    }
    
    .stButton > button {
        height: 44px;
        font-size: 13px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA LOADING
# =========================
def load_df():
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            st.warning(f"ファイル読み込みエラー: {e}")
    return pd.DataFrame(columns=["time", "intent", "food", "score"])


# =========================
# SESSION STATE INITIALIZATION
# =========================
if "df" not in st.session_state:
    st.session_state.df = load_df()

if "step" not in st.session_state:
    st.session_state.step = "fatigue"

if "intent" not in st.session_state:
    st.session_state.intent = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "food_choices" not in st.session_state:
    st.session_state.food_choices = None

if "fatigue_level" not in st.session_state:
    st.session_state.fatigue_level = 0

if "fatigue_slider" not in st.session_state:
    st.session_state.fatigue_slider = 0

if "final_food" not in st.session_state:
    st.session_state.final_food = None

if "selected_intent" not in st.session_state:
    st.session_state.selected_intent = None

if "current_recommendations" not in st.session_state:
    st.session_state.current_recommendations = None


# =========================
# FATIGUE DISPLAY SYNCHRONIZATION
# =========================
def on_fatigue_change():
    st.session_state.fatigue_level = st.session_state.fatigue_slider
    st.session_state.current_recommendations = None


# =========================
# FOOD LOGIC
# =========================
INTENT_MAP = {
    "軽めであっさり": [
        "うどん", "おにぎり", "スープ", "そば", "冷麦", "そうめん",
        "トースト", "サンドイッチ", "お粥", "雑炊", "うどん弁当"
    ],
    "栄養しっかり": [
        "焼き魚定食", "親子丼", "野菜炒め定食", "豚汁定食", "目玉焼き定食",
        "生姜焼き定食", "唐揚げ定食", "ハンバーグ定食", "牛肉コロッケ定食",
        "ホイコーロー定食", "鶏そぼろ丼", "カツ丼", "天丼", "中華丼"
    ],
    "気にせずガッツリ": [
        "カレー", "ラーメン", "とんかつ", "オムライス", "ピザ",
        "牛丼", "豚骨ラーメン", "味噌ラーメン", "塩ラーメン", "鶏そば",
        "つけ麺", "パスタ", "ペペロンチーノ", "カルボナーラ", "ボロネーゼ",
        "ステーキ", "焼肉丼", "大盛りチャーハン", "麻婆豆腐丼"
    ]
}

REASON_MAP = {
    "軽めであっさり": "体を休める選択です",
    "栄養しっかり": "バランス重視の選択です",
    "気にせずガッツリ": "満足感重視の選択です"
}

EASY_MEALS = [
    "うどん", "おにぎり", "スープ", "納豆ご飯", "トースト", "そば",
    "冷麦", "雑炊", "そうめん", "やきおにぎり", "お粥", "みそ汁ご飯",
    "卵かけご飯", "のっぺい汁", "豆腐スープ", "わかめうどん", "しゅうまい"
]

NUTRITIOUS_MEALS = [
    "焼き魚定食", "親子丼", "野菜炒め定食", "豚汁定食", "目玉焼き定食",
    "生姜焼き定食", "唐揚げ定食", "ハンバーグ定食", "牛肉コロッケ定食",
    "ホイコーロー定食", "鶏そぼろ丼", "ブリ大根定食", "鮭フライ定食",
    "ビーフシチュー", "チキン南蛮定食", "豚の角煮定食", "鶏むね肉のソテー定食"
]

BALANCED_MEALS = [
    "親子うどん", "卵かけご飯", "味噌汁とご飯", "野菜スープ", "玉子焼き定食",
    "豆ご飯", "きのこご飯", "鶏そぼろ丼", "豚肉の柳川定食", "天玉うどん",
    "きつねうどん", "月見蕎麦", "野菜天丼", "穴子丼", "ホタテ丼",
    "かつ親子丼", "とり天丼", "さくら丼"
]

TOPPING_MAP = {
    "うどん": "プラスアルファでお惣菜のトッピング（天ぷらやねぎ）はどうかな?",
    "おにぎ��": "プラスアルファで味噌汁やお漬物を添えると、より満足感がアップ",
    "スープ": "プラスアルファでサンドイッチやクラッカーと一緒だと良さそう",
    "焼き魚定食": "プラスアルファで香の物やふりかけが活躍しそう",
    "親子丼": "プラスアルファで温泉卵をトッピングするのも良さそう",
    "野菜炒め定食": "プラスアルファで豚肉や海鮮をプラスすると、より満足度UP",
    "カレー": "プラスアルファでチーズやバターをトッピングするのはいかが?",
    "ラーメン": "プラスアルファで味玉やチャーシューをトッピングすると最高",
    "とんかつ": "プラスアルファでキャベツたっぷり盛りで、さらにボリュームアップ",
    "オムライス": "プラスアルファでチーズやキノコを混ぜると、より豪華に",
    "納豆ご飯": "プラスアルファで温泉卵をのせると栄養価UP",
    "トースト": "プラスアルファでチーズやジャムをトッピング",
    "親子うどん": "プラスアルファで薬味ネギたっぷりで",
    "卵かけご飯": "プラスアルファで海苔や刻みネギで風味UP",
    "味噌汁とご飯": "プラスアルファで漬物や佃煮で満足度UP",
    "野菜スープ": "プラスアルファでチーズやクルトン",
    "玉子焼き定食": "プラスアルファで大根おろしで爽やかに",
    "豚汁定食": "プラスアルファで七味唐辛子で味わい深く",
    "目玉焼き定食": "プラスアルファでベーコンやソーセージを追加",
    "そば": "プラスアルファで天ぷらや薬味で美味しさアップ",
    "冷麦": "プラスアルファで夏野菜をトッピング",
    "雑炊": "プラスアルファで卵やわかめで栄養UP",
    "生姜焼き定食": "プラスアルファでキャベツをたっぷり",
    "唐揚げ定食": "プラスアルファでレモンをかけてさっぱりに",
    "豆ご飯": "プラスアルファで塩昆布でご飯がすすむ",
    "きのこご飯": "プラスアルファで海苔をトッピング",
    "そうめん": "プラスアルファで冷しトマトやキュウリを添えて",
    "牛丼": "プラスアルファで卵黄をのせると絶品",
    "ハンバーグ定食": "プラスアルファでデミグラスソースをたっぷり",
    "ピザ": "プラスアルファでチーズやバジルをトッピング",
    "パスタ": "プラスアルファでチーズ粉をかけて風味UP",
    "鶏そぼろ丼": "プラスアルファで温泉卵をのせると最高",
    "カツ丼": "プラスアルファで漬物を添えて",
    "天丼": "プラスアルファで塩をかけて香りを引き立たせよう",
    "中華丼": "プラスアルファでごま油をかけて風味UP",
    "つけ麺": "プラスアルファでチャーシューを追加",
}

MOTIVATION_MESSAGES = [
    "今日も一日頑張りましたね。ごはんで元気を取り戻そう",
    "あなたの体が喜ぶごはんを選びましょう",
    "毎日の食事が、明日の活力になります",
    "疲れた時こそ、おいしいごはんが大事",
    "今日のあなたにぴったりのごはんを見つけよう",
    "食べることは自分をいたわること",
    "良い選択が、良い明日を作ります"
]

# ③ 決定後の満足感を演出する一言コメント
SATISFACTION_MAP = {
    "軽めであっさり": [
        "体にやさしい選択ですね✨",
        "軽やかに、でも大切に食べましょう🍃",
        "体を大切にした選択です😊"
    ],
    "栄養しっかり": [
        "体が喜ぶ選択ですね💪",
        "バランスの取れた良い選択です🥗",
        "しっかり栄養を取って元気に！✨"
    ],
    "気にせずガッツリ": [
        "良い選択です！思いっきり楽しんで🔥",
        "今日はしっかり食べてエネルギー充電💫",
        "満足感たっぷりの選択ですね！🎉"
    ]
}


def get_today_message():
    today = datetime.date.today().toordinal()
    index = today % len(MOTIVATION_MESSAGES)
    return MOTIVATION_MESSAGES[index]


# ⑤ 時間帯判定
def get_time_zone():
    """現在時刻に基づいて時間帯を判定する"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 11:
        return "朝食"
    elif 11 <= hour < 15:
        return "昼食"
    elif 15 <= hour < 22:
        return "夕食"
    else:
        return "夜食"


# ① 直近選択の除外
def get_recent_foods(days=7):
    """過去days日以内に選択されたメニューのリストを返す"""
    try:
        df = st.session_state.df
        if len(df) == 0:
            return []
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['time'], format='%Y-%m-%d %H:%M').dt.date
        recent = df_copy[df_copy['date'] >= cutoff]
        return recent['food'].tolist()
    except Exception:
        return []


def filter_recent(pool, recent_foods):
    """直近で選ばれたメニューを除外する（全除外の場合はフルプールを返す）"""
    filtered = [f for f in pool if f not in recent_foods]
    return filtered if filtered else pool


def get_streak_days():
    try:
        df = st.session_state.df
        if len(df) == 0:
            return 0

        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['time'], format='mixed').dt.date
        unique_dates = sorted(df_copy['date'].unique(), reverse=True)

        if len(unique_dates) == 0:
            return 0

        streak = 1
        today = datetime.date.today()

        for i, date in enumerate(unique_dates):
            if i == 0:
                if date != today:
                    return 0
            else:
                if (unique_dates[i-1] - date).days != 1:
                    break
                streak += 1

        return streak
    except Exception:
        return 0


def get_recommendations_by_fatigue(fatigue_level):
    recent_foods = get_recent_foods()
    time_zone = get_time_zone()

    if fatigue_level <= 30:
        pool = filter_recent(INTENT_MAP["軽めであっさり"], recent_foods)
        food = random.choice(pool)
        intent = "軽めであっさり"
        return [{"food": food, "intent": intent, "type": "single"}]

    elif fatigue_level <= 60:
        # ⑤ 時間帯ロジック：時間帯に合わせてインテントを調整
        if time_zone in ("朝食", "夜食"):
            intent = "軽めであっさり"
            pool = filter_recent(INTENT_MAP["軽めであっさり"], recent_foods)
        elif time_zone == "昼食":
            intent = "栄養しっかり"
            pool = filter_recent(INTENT_MAP["栄養しっかり"], recent_foods)
        else:  # 夕食
            intent = "気にせずガッツリ"
            pool = filter_recent(INTENT_MAP["気にせずガッツリ"], recent_foods)
        food = random.choice(pool)
        return [{"food": food, "intent": intent, "type": "single"}]

    else:
        # ① 直近除外フィルタを適用
        easy_pool = filter_recent(EASY_MEALS, recent_foods)
        nutritious_pool = filter_recent(NUTRITIOUS_MEALS, recent_foods)
        balanced_pool = filter_recent(BALANCED_MEALS, recent_foods)

        easy_food = random.choice(easy_pool)
        nutritious_food = random.choice(nutritious_pool)
        balanced_food = random.choice(balanced_pool)

        retry_count = 0
        while (easy_food == nutritious_food or easy_food == balanced_food or nutritious_food == balanced_food) and retry_count < 5:
            if easy_food == nutritious_food:
                nutritious_food = random.choice(nutritious_pool)
            if easy_food == balanced_food:
                balanced_food = random.choice(balanced_pool)
            if nutritious_food == balanced_food:
                balanced_food = random.choice(balanced_pool)
            retry_count += 1

        # ② ラベル強化（疲労60以上）
        recommendations = [
            {"food": easy_food, "intent": "軽めであっさり", "type": "easy", "description": "今すぐできる・軽い"},
            {"food": nutritious_food, "intent": "栄養しっかり", "type": "nutritious", "description": "栄養重視・ボリューム"},
            {"food": balanced_food, "intent": "栄養しっかり", "type": "balanced", "description": "バランス型・無難"}
        ]

        # ⑤ 時間帯ロジック：時間帯に合わせて順序を調整
        time_zone_priority = {
            "朝食": ["easy", "nutritious", "balanced"],
            "昼食": ["nutritious", "easy", "balanced"],
            "夕食": ["balanced", "nutritious", "easy"],
            "夜食": ["easy", "nutritious", "balanced"],
        }
        priority = time_zone_priority.get(time_zone, ["easy", "nutritious", "balanced"])
        type_order = {rec["type"]: rec for rec in recommendations}
        recommendations = [type_order[t] for t in priority if t in type_order]

        return recommendations


def get_fatigue_message(fatigue_level):
    if fatigue_level == 0:
        return "疲れ度合いをスライダーで設定してください"
    elif fatigue_level <= 30:
        return "今日はゆっくり休みましょう。軽めのごはんがおすすめです"
    elif fatigue_level <= 60:
        return "適度に疲れていますね。バランスの取れたごはんで回復しましょう"
    else:
        return "かなり疲れているみたいですね。3つの選択肢から選んでください"


def calc_score(intent):
    return {
        "軽めであっさり": 15,
        "栄養しっかり": 12,
        "気にせずガッツリ": 10
    }.get(intent, 10)


def save(intent, food, score):
    row = pd.DataFrame([{
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "intent": intent,
        "food": food,
        "score": score
    }])

    file_exists = os.path.exists(LOG_FILE)

    row.to_csv(LOG_FILE,
               mode="a" if file_exists else "w",
               header=not file_exists,
               index=False,
               encoding="utf-8-sig")

    st.session_state.df = pd.concat([st.session_state.df, row], ignore_index=True)


# =========================
# HOME
# =========================
def page_home():

    if st.session_state.step == "fatigue":

        st.markdown('<div class="title">今日のごはんを決めましょう</div>', unsafe_allow_html=True)

        streak = get_streak_days()
        st.markdown(f"""
        <div class="welcome-section">
            <div class="welcome-emoji">🍚</div>
            <div class="welcome-text">ごはん選びをサポート</div>
            <div class="welcome-subtitle">{get_today_message()}</div>
        </div>
        """, unsafe_allow_html=True)

        if streak > 0:
            st.markdown(f"""
            <div style="text-align:center;">
                <span class="streak-badge">🔥 {streak}日連続!</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="fatigue-card">
            <div class="fatigue-label">疲れ度合い</div>
            <div class="fatigue-value">{st.session_state.fatigue_level}%</div>
        </div>
        """, unsafe_allow_html=True)

        fatigue = st.slider(
            "設定",
            min_value=0,
            max_value=100,
            value=st.session_state.fatigue_level,
            step=5,
            label_visibility="collapsed",
            key="fatigue_slider",
            on_change=on_fatigue_change
        )

        if fatigue != st.session_state.fatigue_level:
            st.session_state.fatigue_level = fatigue
            st.session_state.current_recommendations = None

        message = get_fatigue_message(st.session_state.fatigue_level)
        if st.session_state.fatigue_level == 0:
            st.markdown(f'<div class="warning-message">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-message">{message}</div>', unsafe_allow_html=True)

        if st.session_state.fatigue_level == 0:
            if st.button("自分で選びたい", use_container_width=True):
                st.session_state.step = "intent"
                st.rerun()
        else:
            if st.session_state.current_recommendations is None:
                st.session_state.current_recommendations = get_recommendations_by_fatigue(st.session_state.fatigue_level)

            recommendations = st.session_state.current_recommendations

            if len(recommendations) == 1:
                rec = recommendations[0]
                st.markdown(f"""
                <div class="recommended-card">
                    <div class="recommended-label">おすすめ</div>
                    <div class="recommended-food">{rec['food']}</div>
                    <div class="recommended-reason">{REASON_MAP[rec['intent']]}</div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2, gap="small")
                with col1:
                    if st.button("別の選択肢", use_container_width=True, key="alt1"):
                        st.session_state.step = "intent"
                        st.rerun()

                with col2:
                    if st.button("決定", use_container_width=True, key="dec1"):
                        score = calc_score(rec['intent'])
                        save(rec['intent'], rec['food'], score)
                        st.session_state.step = "done"
                        st.session_state.final_food = rec['food']
                        st.session_state.selected_intent = rec['intent']
                        st.balloons()
                        st.rerun()

            else:
                st.write("### おすすめ3選")

                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class="recommendation-item">
                        <div class="recommendation-title">{rec['description']}</div>
                        <div class="recommendation-food-name">{rec['food']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"{rec['food']}", use_container_width=True, key=f"recommend_{i}"):
                        score = calc_score(rec['intent'])
                        save(rec['intent'], rec['food'], score)
                        st.session_state.step = "done"
                        st.session_state.final_food = rec['food']
                        st.session_state.selected_intent = rec['intent']
                        st.balloons()
                        st.rerun()

                if st.button("別の選択肢", use_container_width=True):
                    st.session_state.step = "intent"
                    st.rerun()

    elif st.session_state.step == "intent":

        st.markdown('<div class="title">気持ちで選ぶ</div>', unsafe_allow_html=True)

        st.write("### どうしたい?")

        intents = list(INTENT_MAP.keys())

        for i in intents:
            if st.button(i, use_container_width=True, key=f"intent_{i}"):
                st.session_state.intent = i
                st.session_state.selected_intent = i
                st.session_state.step = "food"
                available_foods = INTENT_MAP[i]
                num_choices = min(3, len(available_foods))
                st.session_state.food_choices = random.sample(available_foods, k=num_choices)
                st.rerun()

    elif st.session_state.step == "food":

        intent = st.session_state.intent
        choices = st.session_state.food_choices

        st.markdown(f"""
        <div class="card">
            <div style="font-size:11px;color:#92400e;">選択中</div>
            <div class="big">{intent}</div>
            <div class="reason">{REASON_MAP[intent]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("### 候補")

        for food in choices:
            if st.button(food, use_container_width=True, key=f"food_choice_{food}"):
                score = calc_score(intent)
                save(intent, food, score)
                st.session_state.step = "done"
                st.session_state.final_food = food
                st.session_state.selected_intent = intent
                st.balloons()
                st.rerun()

    elif st.session_state.step == "done":

        st.markdown('<div class="title">決定完了!</div>', unsafe_allow_html=True)

        final_food = st.session_state.final_food

        st.markdown(f"""
        <div class="card">
            <div style="font-size:11px;color:#92400e;">今日のごはん</div>
            <div class="big-final">{final_food}</div>
        </div>
        """, unsafe_allow_html=True)

        # ③ 満足感を演出する一言コメント
        selected_intent = st.session_state.selected_intent
        if selected_intent in SATISFACTION_MAP:
            messages = SATISFACTION_MAP[selected_intent]
            msg = messages[datetime.date.today().toordinal() % len(messages)]
            st.markdown(f"""
            <div class="info-message" style="text-align:center;font-size:14px;font-weight:600;">
                {msg}
            </div>
            """, unsafe_allow_html=True)

        if final_food in TOPPING_MAP:
            st.markdown(f"""
            <div class="suggestion">
            {TOPPING_MAP[final_food]}
            </div>
            """, unsafe_allow_html=True)

        if st.button("もう一度", use_container_width=True):
            st.session_state.step = "fatigue"
            st.session_state.fatigue_level = 0
            st.session_state.fatigue_slider = 0
            st.session_state.intent = None
            st.session_state.food_choices = None
            st.session_state.final_food = None
            st.session_state.selected_intent = None
            st.session_state.current_recommendations = None
            st.rerun()


# =========================
# LOG
# =========================
def page_log():

    st.title("記録")

    df = st.session_state.df

    if len(df) > 0 and "food" in df.columns:

        st.write("### 統計")

        col1, col2 = st.columns(2, gap="small")

        with col1:
            total_meals = len(df)
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{total_meals}</div>
                <div class="stat-label">決定回数</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if len(df) > 0 and df["food"].notna().sum() > 0:
                most_food = df["food"].value_counts().index[0]
            else:
                most_food = "なし"
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">🍽</div>
                <div class="stat-label">{most_food}</div>
            </div>
            """, unsafe_allow_html=True)

        # ④ 累計スコア表示
        st.write("")
        total_score = int(df["score"].fillna(0).sum()) if "score" in df.columns else 0
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{total_score}</div>
            <div class="stat-label">累計スコア</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if "intent" in df.columns:
            st.write("### パターン")
            intent_counts = df["intent"].value_counts()

            intent_names = {
                "軽めであっさり": "軽めであっさり",
                "栄養しっかり": "栄養しっかり",
                "気にせずガッツリ": "気にせずガッツリ"
            }

            for intent_key in ["軽めであっさり", "栄養しっかり", "気にせずガッツリ"]:
                if intent_key in intent_counts.index:
                    count = intent_counts[intent_key]
                    percentage = (count / len(df)) * 100
                    st.write(f"**{intent_key}**: {count}回")
                    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{percentage}%"></div></div>', unsafe_allow_html=True)

        st.write("")
        st.write("### 最近")

        recent_df = df.tail(10).iloc[::-1]

        for idx, row in recent_df.iterrows():
            time_str = row['time']
            st.markdown(f"""
            <div class="history-card">
                <div class="history-date">{time_str}</div>
                <div class="history-food">{row['food']}</div>
                <div class="history-intent"><span class="history-intent">{row['intent']}</span></div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("記録がありません")


# =========================
# MAIN LAYOUT
# =========================
if st.session_state.page == "home":
    page_home()
else:
    page_log()

st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="small")

with col1:
    if st.button("🏠 ホーム", use_container_width=True, key="nav_home"):
        st.session_state.page = "home"
        st.rerun()

with col2:
    if st.button("📊 記録", use_container_width=True, key="nav_log"):
        st.session_state.page = "log"
        st.rerun()

st.markdown("""
<script>
    setTimeout(function() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(btn => {
            if(btn.textContent.includes('ホーム')) {
                btn.classList.add('nav-button-home');
            }
            if(btn.textContent.includes('記録')) {
                btn.classList.add('nav-button-record');
            }
        });
    }, 100);
</script>
""", unsafe_allow_html=True)