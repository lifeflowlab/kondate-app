import streamlit as st
import pandas as pd
import datetime
import os
import random

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
    font-size:28px;
    font-weight:900;
    margin:16px 0 24px 0;
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
    font-size:16px;
    font-weight:600;
    margin-top:8px;
    color:#92400e;
}

.big-final {
    font-size:56px;
    font-weight:900;
    margin-top:12px;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1.1;
    letter-spacing:-1px;
}

.reason {
    font-size:12px;
    color:#b45309;
    margin-top:6px;
    line-height:1.5;
}

.ai-reason {
    font-size:13px;
    color:#78350f;
    margin-top:12px;
    padding:12px;
    background:linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(37,99,235,0.05) 100%);
    border-radius:10px;
    border-left:4px solid #3b82f6;
    font-weight:500;
    line-height:1.6;
}

.suggestion {
    font-size:13px;
    color:#92400e;
    margin-top:16px;
    padding:12px;
    background:linear-gradient(135deg, rgba(249,115,22,0.08) 0%, rgba(253,186,116,0.05) 100%);
    border-radius:10px;
    border-left:4px solid #f97316;
    font-weight:500;
}

.satisfaction-message {
    font-size:16px;
    color:#78350f;
    font-weight:700;
    margin-bottom:20px;
    padding:14px;
    background:linear-gradient(135deg, rgba(249,115,22,0.1) 0%, rgba(253,186,116,0.08) 100%);
    border-radius:12px;
    text-align:center;
    border:1px solid rgba(249,115,22,0.15);
    animation: slideUpGentle 0.6s ease-out;
}

.cost-badge {
    display:inline-block;
    font-size:11px;
    font-weight:700;
    padding:4px 12px;
    border-radius:8px;
    margin-top:8px;
}

.cost-cheap {
    background:linear-gradient(135deg, rgba(34,197,94,0.15) 0%, rgba(16,185,129,0.1) 100%);
    color:#047857;
    border:1px solid rgba(34,197,94,0.2);
}

.cost-normal {
    background:linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(37,99,235,0.1) 100%);
    color:#1e40af;
    border:1px solid rgba(59,130,246,0.2);
}

.cost-expensive {
    background:linear-gradient(135deg, rgba(168,85,247,0.15) 0%, rgba(147,51,234,0.1) 100%);
    color:#6b21a8;
    border:1px solid rgba(168,85,247,0.2);
}

.cost-message {
    font-size:14px;
    font-weight:600;
    color:#92400e;
    margin-top:16px;
    padding:12px;
    background:linear-gradient(135deg, rgba(249,115,22,0.08) 0%, rgba(253,186,116,0.05) 100%);
    border-radius:10px;
    border-left:4px solid #f97316;
}

.achievement-badge {
    display:inline-block;
    background:linear-gradient(135deg, #ec4899 0%, #db2777 100%);
    color:white;
    padding:6px 14px;
    border-radius:8px;
    font-size:11px;
    font-weight:700;
    margin:4px;
    box-shadow:0 2px 8px rgba(236,72,153,0.3);
}

.insight-panel {
    background:linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(37,99,235,0.05) 100%);
    border-left:4px solid #3b82f6;
    border-radius:10px;
    padding:14px;
    margin:16px 0;
    font-size:13px;
    color:#1e40af;
    font-weight:500;
    line-height:1.6;
}

.weekly-theme {
    background:linear-gradient(135deg, rgba(168,85,247,0.1) 0%, rgba(147,51,234,0.08) 100%);
    border:2px solid rgba(168,85,247,0.3);
    border-radius:12px;
    padding:16px;
    margin-bottom:16px;
    text-align:center;
    font-weight:600;
    color:#6b21a8;
}

@keyframes slideUpGentle {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInLight {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes pulse {
    0%, 100% { transform:scale(1); }
    50% { transform:scale(1.02); }
}

.stButton > button {
    height:48px;
    border-radius:10px;
    font-size:14px;
    font-weight:700;
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%);
    color:#78350f;
    border:none;
    transition: all 0.2s ease;
    letter-spacing:0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(249,115,22,0.25);
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
    margin-right:4px;
}

.history-cost {
    font-size:11px;
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
    font-size:36px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fdba74 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}

.stat-label {
    font-size:11px;
    color:#a16207;
    margin-top:6px;
    font-weight:600;
}

.fatigue-card {
    background:linear-gradient(135deg, rgba(249,115,22,0.08) 0%, rgba(253,186,116,0.06) 100%);
    border-radius:16px;
    padding:24px;
    border:2px solid rgba(249,115,22,0.15);
    margin-bottom:24px;
    margin-top:24px;
    transition: all 0.3s ease;
    box-shadow:0 6px 16px rgba(249,115,22,0.08);
}

.fatigue-label {
    font-size:12px;
    font-weight:700;
    color:#92400e;
    margin-bottom:12px;
    text-transform:uppercase;
    letter-spacing:1px;
}

.fatigue-value {
    font-size:64px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fdba74 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    text-align:center;
    margin:12px 0;
}

.welcome-section {
    background:linear-gradient(135deg, rgba(249,115,22,0.06) 0%, rgba(253,186,116,0.04) 100%);
    border-radius:16px;
    padding:14px;
    margin-bottom:20px;
    text-align:center;
    border:1px solid rgba(249,115,22,0.08);
    box-shadow:0 2px 8px rgba(249,115,22,0.03);
    animation: fadeInLight 0.5s ease-out;
}

.welcome-emoji {
    font-size:40px;
    margin-bottom:6px;
}

.welcome-text {
    font-size:14px;
    font-weight:600;
    color:#92400e;
    margin-bottom:4px;
}

.welcome-subtitle {
    font-size:12px;
    color:#b45309;
    line-height:1.4;
}

.recommended-card {
    background:white;
    border-radius:16px;
    padding:20px;
    border:2px solid rgba(249,115,22,0.12);
    margin-bottom:24px;
    margin-top:24px;
    transition: all 0.3s ease;
    box-shadow:0 8px 20px rgba(249,115,22,0.08);
    animation: slideUpGentle 0.6s ease-out;
}

.recommended-label {
    font-size:10px;
    color:#a16207;
    text-transform:uppercase;
    letter-spacing:1px;
    font-weight:700;
    margin-bottom:8px;
}

.recommended-food {
    font-size:40px;
    font-weight:900;
    background:linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin:12px 0;
}

.recommended-reason {
    font-size:12px;
    color:#92400e;
    margin-top:10px;
    line-height:1.5;
}

.recommendation-item {
    background:white;
    border-radius:14px;
    padding:12px;
    margin-bottom:10px;
    border:1px solid rgba(249,115,22,0.08);
    transition: all 0.25s ease;
    animation: fadeInLight 0.5s ease-out;
}

.recommendation-item:hover {
    border:1px solid rgba(249,115,22,0.15);
    box-shadow:0 4px 10px rgba(249,115,22,0.06);
    transform: translateY(-1px);
}

.recommendation-title {
    font-size:10px;
    color:#b45309;
    text-transform:uppercase;
    letter-spacing:0.2px;
    font-weight:600;
    margin-bottom:6px;
}

.recommendation-food-name {
    font-size:22px;
    font-weight:800;
    color:#f97316;
    margin:6px 0;
}

.streak-badge {
    display:inline-block;
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%);
    color:#78350f;
    padding:8px 16px;
    border-radius:10px;
    font-size:12px;
    font-weight:700;
    margin-bottom:16px;
    box-shadow:0 4px 12px rgba(249,115,22,0.2);
}

.info-message {
    background:linear-gradient(135deg, rgba(34,197,94,0.06) 0%, rgba(59,130,246,0.04) 100%);
    border-left:4px solid #22c55e;
    border-radius:8px;
    padding:12px;
    font-size:12px;
    color:#15803d;
    border:1px solid rgba(34,197,94,0.1);
    margin-bottom:16px;
    margin-top:16px;
    font-weight:500;
}

.seasonal-highlight {
    background:linear-gradient(135deg, rgba(34,197,94,0.08) 0%, rgba(59,130,246,0.06) 100%);
    border-left:4px solid #10b981;
    border-radius:8px;
    padding:12px;
    font-size:13px;
    color:#047857;
    border:1px solid rgba(34,197,94,0.15);
    margin-bottom:16px;
    margin-top:16px;
    font-weight:600;
    animation: slideUpGentle 0.6s ease-out;
}

.warning-message {
    background:linear-gradient(135deg, rgba(249,115,22,0.08) 0%, rgba(253,186,116,0.05) 100%);
    border-left:4px solid #f97316;
    border-radius:8px;
    padding:12px;
    font-size:12px;
    color:#92400e;
    border:1px solid rgba(249,115,22,0.15);
    margin-bottom:16px;
    margin-top:16px;
    font-weight:500;
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

.section-separator {
    height: 28px;
}

.section-title {
    font-size:16px;
    font-weight:700;
    color:#78350f;
    margin:20px 0 14px 0;
}

.season-label {
    font-size:13px;
    font-weight:600;
    color:#92400e;
    margin-bottom:8px;
    display:inline-block;
    padding:6px 12px;
    background:linear-gradient(135deg, rgba(249,115,22,0.1) 0%, rgba(253,186,116,0.08) 100%);
    border-radius:8px;
    border:1px solid rgba(249,115,22,0.12);
}

.season-detail {
    font-size:12px;
    color:#b45309;
    margin-top:8px;
    line-height:1.6;
    font-weight:500;
}

.scene-card {
    background:white;
    border-radius:14px;
    padding:14px;
    margin-bottom:10px;
    border:1px solid rgba(249,115,22,0.1);
    transition: all 0.25s ease;
}

.scene-card:hover {
    border:1px solid rgba(249,115,22,0.2);
    box-shadow:0 4px 12px rgba(249,115,22,0.1);
    transform: translateY(-2px);
}

.scene-title {
    font-size:14px;
    font-weight:700;
    color:#f97316;
    margin-bottom:4px;
}

.scene-desc {
    font-size:11px;
    color:#92400e;
    line-height:1.4;
}

hr {
    border:none;
    height:1px;
    background:linear-gradient(90deg, transparent, rgba(249,115,22,0.1), transparent);
    margin:16px 0;
}

.nav-button-home {
    background:linear-gradient(135deg, #fb923c 0%, #fdba74 100%) !important;
    color:#78350f !important;
    font-weight:700 !important;
}

.nav-button-record {
    background:linear-gradient(135deg, #fed7aa 0%, #fef3c7 100%) !important;
    color:#92400e !important;
    font-weight:700 !important;
}

.nav-button-home:hover {
    box-shadow: 0 6px 12px rgba(249,115,22,0.3) !important;
}

.nav-button-record:hover {
    box-shadow: 0 6px 12px rgba(249,115,22,0.2) !important;
}

.stSlider label {
    font-size: 12px;
    font-weight: 600;
    color: #92400e;
}

@media (max-width: 390px) {
    .block-container {
        padding: 10px 12px 80px 12px;
    }
    
    .title {
        font-size: 24px;
        margin: 12px 0 20px 0;
    }
    
    .fatigue-value {
        font-size: 56px;
    }
    
    .big-final {
        font-size: 48px;
    }
    
    .recommended-food {
        font-size: 32px;
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
    """CSVファイルからデータをロード。cost列が無い場合は追加"""
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE, encoding="utf-8-sig")
            if df.shape[0] == 0:
                return pd.DataFrame(columns=["time", "intent", "food", "score", "cost"])
            df.columns = df.columns.str.strip()
            if "cost" not in df.columns:
                df["cost"] = "普通"
            return df
        except Exception as e:
            st.warning(f"ファイル読み込みエラー: {e}")
            return pd.DataFrame(columns=["time", "intent", "food", "score", "cost"])
    return pd.DataFrame(columns=["time", "intent", "food", "score", "cost"])


# =========================
# SESSION STATE INITIALIZATION
# =========================
if "df" not in st.session_state:
    st.session_state.df = load_df()

if "step" not in st.session_state:
    st.session_state.step = "fatigue"

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home"

if "intent" not in st.session_state:
    st.session_state.intent = None

if "cost_level" not in st.session_state:
    st.session_state.cost_level = "気にしない"

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

if "selected_cost" not in st.session_state:
    st.session_state.selected_cost = "普通"

if "current_recommendations" not in st.session_state:
    st.session_state.current_recommendations = None

if "show_roulette" not in st.session_state:
    st.session_state.show_roulette = False

if "ingredient_category" not in st.session_state:
    st.session_state.ingredient_category = None

if "season" not in st.session_state:
    st.session_state.season = None

if "scene" not in st.session_state:
    st.session_state.scene = None

if "selection_method" not in st.session_state:
    st.session_state.selection_method = None

if "ingredient_mode" not in st.session_state:
    st.session_state.ingredient_mode = None

if "genre" not in st.session_state:
    st.session_state.genre = None


# =========================
# CONSTANTS
# =========================
COST_MAP = {
    "うどん": "安い", "おにぎり": "安い", "スープ": "普通", "そば": "普通", "冷麦": "安い", "そうめん": "安い",
    "トースト": "安い", "サンドイッチ": "普通", "お粥": "安い", "雑炊": "普通", "うどん弁当": "普通",
    "焼き魚定食": "普通", "親子丼": "普通", "野菜炒め定食": "普通", "豚汁定食": "普通", "目玉焼き定食": "普通",
    "生姜焼き定食": "普通", "唐揚げ定食": "普通", "ハンバーグ定食": "普通", "牛肉コロッケ定食": "普通",
    "ホイコーロー定食": "普通", "鶏そぼろ丼": "普通", "カツ丼": "高め", "天丼": "高め", "中華丼": "普通",
    "カレー": "普通", "ラーメン": "普通", "とんかつ": "高め", "オムライス": "普通", "ピザ": "高め",
    "牛丼": "普通", "豚骨ラーメン": "普通", "味噌ラーメン": "普通", "塩ラーメン": "普通", "鶏そば": "普通",
    "つけ麺": "普通", "パスタ": "普通", "ペペロンチーノ": "普通", "カルボナーラ": "高め", "ボロネーゼ": "普通",
    "ステーキ": "高い", "焼肉丼": "高め", "大盛りチャーハン": "普通", "麻婆豆腐丼": "普通",
    "納豆ご飯": "安い", "やきおにぎり": "安い", "みそ汁ご飯": "安い", "卵かけご飯": "安い", "のっぺい汁": "安い",
    "豆腐スープ": "安い", "わかめうどん": "安い", "しゅうまい": "普通", "親子うどん": "普通", "味噌汁とご飯": "安い",
    "野菜スープ": "安い", "玉子焼き定食": "普通", "豆ご飯": "安い", "きのこご飯": "普通", "豚肉の柳川定食": "普通",
    "天玉うどん": "普通", "きつねうどん": "普通", "月見蕎麦": "普通", "野菜天丼": "普通", "穴子丼": "高い",
    "ホタテ丼": "高い", "かつ親子丼": "高め", "とり天丼": "普通", "さくら丼": "高め",
    "春キャベツのパスタ": "普通", "新玉ねぎスープ": "普通", "菜の花のパスタ": "普通", "あさりの味噌汁": "普通",
    "たけのこご飯": "普通", "山菜蕎麦": "普通", "冷たいきゅうり": "安い", "きゅうりサラダ": "安い",
    "ゴーヤチャンプルー": "普通", "ナス炒め定食": "普通", "焼き芋": "安い", "さつまいも天ぷら": "普通",
    "かぼちゃ煮": "安い", "さんま定食": "普通", "鮭フライ定食": "高め", "きのこ炊き込みご飯": "普通",
    "栗ご飯": "高め", "白菜鍋": "普通", "ねぎ焼き": "普通", "ぶり大根": "高め", "寄せ鍋": "普通",
    "牡蠣鍋": "高い", "ビーフシチュー": "高め", "チキン南蛮定食": "普通", "豚の角煮定食": "高め",
    "蒸し鶏定食": "普通", "ブリ大根定食": "高め", "八宝菜": "普通", "酢豚": "普通", "春巻き": "普通",
    "餃子": "普通", "キムチ鍋": "普通", "エビフライ定食": "高め",
    "新玉ねぎのグラタン": "普通", "新玉ねぎのおひたし": "安い", "あさりの酒蒸し": "普通",
    "菜の花のおひたし": "安い", "たけのこ炊き込みご飯": "普通", "山菜天ぷら": "普通",
    "大根おろし定食": "普通", "大根鍋": "普通", "かぼちゃスープ": "普通",
}

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

COST_NAMES = {
    "安い": "節約",
    "普通": "コスパ良",
    "高め": "ちょい贅沢",
    "高い": "ちょい贅沢"
}

COST_MESSAGE_MAP = {
    "気にしない": {"prefix": "", "message": "食べたいもの選びましょう！"},
    "ちょっと節約": {"prefix": "💡 ", "message": "無理せず節約できる選択です"},
    "しっかり節約": {"prefix": "💰 ", "message": "今日はコスパ最強の日です"}
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
    "ビーフシチュー", "チキン南蛮定食", "豚の角煮定食", "蒸し鶏定食"
]

BALANCED_MEALS = [
    "親子うどん", "卵かけご飯", "味噌汁とご飯", "野菜スープ", "玉子焼き定食",
    "豆ご飯", "きのこご飯", "鶏そぼろ丼", "豚肉の柳川定食", "天玉うどん",
    "きつねうどん", "月見蕎麦", "野菜天丼", "穴子丼", "ホタテ丼",
    "かつ親子丼", "とり天丼", "さくら丼"
]

GENRE_MAP = {
    "和食": [
        "親子丼", "焼き魚定食", "うどん", "そば", "天丼", "わかめうどん",
        "月見蕎麦", "唐揚げ定食", "生姜焼き定食", "ホイコーロー定食",
        "カツ丼", "穴子丼", "親子うどん", "きつねうどん", "たけのこご飯", "山菜蕎麦"
    ],
    "洋食": [
        "オムライス", "ハンバーグ定食", "ビーフシチュー", "パスタ",
        "ペペロンチーノ", "カルボナーラ", "ボロネーゼ", "ステーキ",
        "サンドイッチ", "ピザ", "チキン南蛮定食", "エビフライ定食"
    ],
    "中華": [
        "ラーメン", "豚骨ラーメン", "味噌ラーメン", "塩ラーメン",
        "つけ麺", "中華丼", "麻婆豆腐丼", "焼肉丼", "大盛りチャーハン",
        "八宝菜", "酢豚", "春巻き", "餃子"
    ]
}

INGREDIENT_RECIPES = {
    "肉類": {
        "豚肉": ["生姜焼き定食", "豚汁定食", "豚骨���ーメン", "焼肉丼", "とんかつ", "豚肉の柳川定食"],
        "鶏肉（もも）": ["唐揚げ定食", "親子丼", "鶏そば"],
        "鶏肉（むね）": ["蒸し鶏定食", "鶏そぼろ丼", "チキン南蛮定食", "とり天丼"],
        "牛肉": ["ビーフシチュー", "ステーキ", "牛丼", "カレー", "焼肉丼"],
        "ひき肉": ["ハンバーグ定食", "麻婆豆腐丼", "大盛りチャーハン"],
    },
    "魚介類": {
        "鮭": ["鮭フライ定食", "焼き魚定食"],
        "鯖": ["焼き魚定食"],
        "ぶり": ["焼き魚定食", "ぶり大根", "ブリ大根定食"],
        "エビ": ["エビフライ定食"],
        "ホタテ": ["ホタテ丼"],
        "あさり": ["あさりの味噌汁", "あさりの酒蒸し"],
        "さんま": ["さんま定食"],
    },
    "野菜・いも類": {
        "キャベツ": ["野菜炒め定食", "とんかつ", "春キャベツのパスタ", "野菜スープ"],
        "きゅうり": ["きゅうりサラダ", "冷たいきゅうり"],
        "なす": ["ナス炒め定食"],
        "じゃがいも": ["カレー", "ビーフシチュー"],
        "さつまいも": ["焼き芋"],
        "かぼちゃ": ["かぼちゃ煮"],
        "白菜": ["白菜鍋"],
    },
}

SEASONAL_RECIPES = {
    "🌸 春（3〜5月）": {
        "emoji": "🌸",
        "tagline": "春の新鮮さで体をリセット",
        "description": "体を整える・軽め・デトックス系",
        "scenes": {
            "疲れてる": {
                "description": "春の軽さで疲労回復",
                "foods": {
                    "春キャベツ 🌱": ["春キャベツのパスタ"],
                    "新玉ねぎ ✨": ["新玉ねぎスープ"],
                    "菜の花 🌼": ["菜の花のパスタ"]
                }
            },
            "さっぱりしたい": {
                "description": "軽やかに爽やかに",
                "foods": {
                    "あさり 🦪": ["あさりの味噌汁"],
                    "たけのこ 🎋": ["たけのこご飯"]
                }
            },
            "ちょっと贅沢": {
                "description": "春の味覚を堪能",
                "foods": {
                    "山菜 🌿": ["山菜蕎麦"],
                    "筍 🎋": ["たけのこ炊き込みご飯"]
                }
            }
        }
    },
    "☀️ 夏（6〜8月）": {
        "emoji": "☀️",
        "tagline": "冷たさで体を冷やして元気回復",
        "description": "疲労回復・さっぱり・水分補給",
        "scenes": {
            "だるい・疲れてる": {
                "description": "夏バテ対策で回復",
                "foods": {
                    "きゅうり 🥒": ["冷たいきゅうり", "きゅうりサラダ"],
                    "そうめん 🍜": ["そうめん"]
                }
            },
            "さっぱりしたい": {
                "description": "清涼感で気分リセット",
                "foods": {
                    "トマト 🍅": ["冷やしトマト"],
                    "ゴーヤ 💚": ["ゴーヤチャンプルー"]
                }
            },
            "栄養補給したい": {
                "description": "夏の栄養不足を補給",
                "foods": {
                    "ナス 🍆": ["ナス炒め定食"],
                    "枝豆 💚": ["野菜スープ"]
                }
            }
        }
    },
    "🍁 秋（9〜11月）": {
        "emoji": "🍁",
        "tagline": "実りの季節で満足感を充電",
        "description": "栄養補給・食欲UP・満足感",
        "scenes": {
            "栄養補給したい": {
                "description": "秋の栄養で体を整える",
                "foods": {
                    "さつまいも 🟠": ["焼き芋"],
                    "かぼちゃ 🎃": ["かぼちゃ煮"]
                }
            },
            "食欲がある": {
                "description": "秋の味覚で満足感を",
                "foods": {
                    "さんま 🐟": ["さんま定食"],
                    "鮭 🌊": ["鮭フライ定食"]
                }
            },
            "体を温めたい": {
                "description": "秋の温かさで体を整える",
                "foods": {
                    "きのこ 🍄": ["きのこ炊き込みご飯"],
                    "栗 🌰": ["栗ご飯"]
                }
            }
        }
    },
    "❄️ 冬（12〜2月）": {
        "emoji": "❄️",
        "tagline": "温かさで心と体をリセット",
        "description": "体を温める・高栄養・回復系",
        "scenes": {
            "温まりたい": {
                "description": "温かさで体を回復",
                "foods": {
                    "白菜 🥬": ["白菜鍋"],
                    "ねぎ 🌱": ["ねぎ焼き"]
                }
            },
            "栄養補給したい": {
                "description": "冬の高栄養で元気に",
                "foods": {
                    "ぶり 🐟": ["ぶり大根"],
                    "大根 ⚪": ["大根おろし定食"]
                }
            },
            "ぜいたくしたい": {
                "description": "冬の味覚で豊かに",
                "foods": {
                    "鍋料理 🍲": ["寄せ鍋", "キムチ鍋"],
                    "牡蠣 🦪": ["牡蠣鍋"]
                }
            }
        }
    }
}

TOPPING_MAP = {
    "うどん": "プラスアルファでお惣菜のトッピング（天ぷらやねぎ）はどうかな?",
    "おにぎり": "プラスアルファで味噌汁やお漬物を添えると、より満足感がアップ",
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
    "ビーフシチュー": "プラスアルファでアイスクリームをのせても",
    "チキン南蛮定食": "プラスアルファでタルタルソースたっぷり",
}

SATISFACTION_MESSAGES = {
    "朝食時": [
        "朝はしっかり食べて、元気に出発しましょう！",
        "良い朝食が一日の活力になります。体が喜んでいますね",
        "朝から栄養をとる賢い選択です",
        "体が目覚める選択をしましたね"
    ],
    "昼食時": [
        "昼間の疲れを吹き飛ばす良い選択です",
        "バランスの取れた選択で午後も頑張ろう",
        "昼食に最適な選択をしましたね",
        "体が喜ぶ選択です"
    ],
    "夕食時": [
        "夜も元気よく過ごすための良い選択です",
        "疲れた体を労る素敵な選択です",
        "夜にぴったりの満足感がある選択ですね",
        "今日一日お疲れさま。ごはんで回復しましょう"
    ],
    "夜食時": [
        "夜遅くでも優しい選択をしましたね",
        "夜食にぴったりの軽めな選択です",
        "体に優しい選択をしましたね",
        "遅い時間の食事には理想的な選択です"
    ]
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


# =========================
# HELPER FUNCTIONS
# =========================
def weighted_choice(meals):
    """過去の選択を反映した加重選択"""
    if not meals or len(meals) == 0:
        return None
    
    if len(meals) == 1:
        return meals[0]
    
    try:
        history = st.session_state.df
        weights = []

        for meal in meals:
            try:
                count = len(history[history["food"] == meal]) if len(history) > 0 else 0
            except Exception:
                count = 0
            weight = 1.0 / (float(count) + 1.0)
            weights.append(weight)

        total_weight = sum(weights) if weights else 0
        if total_weight <= 0:
            return random.choice(meals)
        
        try:
            weights_normalized = [float(w) / float(total_weight) for w in weights]
            result = random.choices(meals, weights=weights_normalized, k=1)
            return result[0] if result and len(result) > 0 else random.choice(meals)
        except Exception:
            return random.choice(meals)
    except Exception:
        return random.choice(meals) if meals else None


def generate_reason(food, fatigue_level, cost_level):
    """ダイナミックな選択理由を生成"""
    try:
        if not food or not isinstance(food, str):
            return "あなたにぴったりな選択です。"
        
        reasons = []

        if fatigue_level > 70:
            reasons.append("疲れているので消化が良く簡単に食べられるものを優先しました")
        elif fatigue_level > 40:
            reasons.append("適度に栄養を摂取できるバランスの取れたものを選びました")
        else:
            reasons.append("体が元気だから好みのものを選びました")

        cost_map_val = COST_MAP.get(food, "普通")
        if cost_level == "しっかり節約" and cost_map_val == "安い":
            reasons.append("さらにコストも抑えられます")
        elif cost_level == "気にしない":
            reasons.append("栄養と満足度を最優先にしました")

        if "うどん" in food or "そば" in food:
            reasons.append("消化が良く体に優しいです")
        elif "定食" in food:
            reasons.append("バランスの良い栄養が摂取できます")
        elif "ラーメン" in food or "カレー" in food:
            reasons.append("満足感が高く気分がリセットできます")
        elif "ご飯" in food:
            reasons.append("シンプルで体に負担がありません")

        try:
            if len(st.session_state.df) > 0:
                food_count = len(st.session_state.df[st.session_state.df["food"] == food])
            else:
                food_count = 0
        except Exception:
            food_count = 0
            
        if food_count == 0:
            reasons.append("新しい選択肢に挑戦できます")
        elif food_count >= 3:
            reasons.append("あなたが好むメニューです")

        return "。\n".join(reasons) + "。" if reasons else "あなたにぴったりな選択です。"
    except Exception:
        return "あなたにぴったりな選択です。"


def get_weekly_theme():
    """週間テーマを取得"""
    try:
        week_num = datetime.datetime.now().isocalendar()[1]
        themes = [
            ("節約週間", "💰 今週は節約を意識した選択を続けましょう"),
            ("栄養週間", "🥗 バランスの良い食事を心がけましょう"),
            ("簡単調理週間", "⚡ 簡単に準備できる食事を優先しましょう"),
            ("季節食材週間", "🌿 旬の食材を活用しましょう"),
            ("挑戦週間", "🎯 新しいメニューに挑戦しましょう"),
        ]
        if len(themes) == 0:
            return ("今週のテーマ", "ごはんを楽しみましょう")
        
        theme_idx = week_num % len(themes)
        return themes[theme_idx]
    except Exception:
        return ("今週のテーマ", "ごはんを楽しみましょう")


def get_achievement_badges():
    """実績バッジを取得"""
    try:
        df = st.session_state.df
        if len(df) == 0:
            return []
        
        badges = []
        
        streak = get_streak_days()
        if streak >= 3:
            badges.append(f"🔥 {streak}日連続")
        if streak >= 7:
            badges.append("🏆 1週間達成")
        if streak >= 30:
            badges.append("👑 1ヶ月達成")
        
        try:
            cheap_count = len(df[df["cost"] == "安い"]) if "cost" in df.columns else 0
        except Exception:
            cheap_count = 0
        if cheap_count >= 5:
            badges.append("💰 節約マスター")
        if cheap_count >= 10:
            badges.append("💎 節約王")
        
        try:
            unique_foods = df["food"].nunique() if "food" in df.columns else 0
        except Exception:
            unique_foods = 0
        if unique_foods >= 10:
            badges.append("🌈 多様性マスター")
        if unique_foods >= 20:
            badges.append("🎭 食事エクスプローラー")
        
        try:
            nutritious_count = len(df[df["intent"] == "栄養しっかり"]) if "intent" in df.columns else 0
        except Exception:
            nutritious_count = 0
        if nutritious_count >= 5:
            badges.append("🥗 栄養重視")
        
        return badges
    except Exception:
        return []


def analyze_eating_patterns():
    """食事パターンを分析"""
    try:
        df = st.session_state.df
        if len(df) < 3:
            return None
        
        analysis = {}
        
        try:
            if len(df) > 0 and "food" in df.columns:
                recent_df = df.tail(7)
                food_counts = recent_df["food"].value_counts()
                
                if len(food_counts) > 0:
                    most_food = food_counts.index[0]
                    count = food_counts.iloc[0]
                    if count >= 2:
                        analysis["frequent"] = f"最近{most_food}を{count}回選んでいますね"
        except Exception:
            pass
        
        try:
            if "intent" in df.columns and len(df) > 0:
                nutritious_count = len(df[df["intent"] == "栄養しっかり"])
                nutritious_pct = (nutritious_count / len(df)) * 100
                if nutritious_pct < 30:
                    analysis["nutrition"] = "栄養バランスが少し不足気味。定食系の選択を増やすのがおすすめです"
                elif nutritious_pct > 70:
                    analysis["nutrition"] = "栄養バランスをしっかり意識した選択ができていますね！"
        except Exception:
            pass
        
        try:
            if "cost" in df.columns and len(df) > 0:
                cheap_count = len(df[df["cost"] == "安い"])
                cheap_pct = (cheap_count / len(df)) * 100
                if cheap_pct > 60:
                    analysis["cost"] = "節約意識が高いですね。時には贅沢な選択も大切です"
                elif cheap_pct < 20:
                    analysis["cost"] = "予算に余裕があるのですね。時には節約を意識してみるのもいいかもしれません"
        except Exception:
            pass
        
        return analysis if analysis else None
    except Exception:
        return None


def generate_insight_message():
    """AI洞察メッセージを生成"""
    try:
        analysis = analyze_eating_patterns()
        if not analysis:
            return None
        
        messages = []
        if "frequent" in analysis:
            messages.append(f"📊 {analysis['frequent']}")
        if "nutrition" in analysis:
            messages.append(f"🥗 {analysis['nutrition']}")
        if "cost" in analysis:
            messages.append(f"💰 {analysis['cost']}")
        
        return "\n".join(messages) if messages else None
    except Exception:
        return None


def spin_roulette(meals):
    """ルーレット機能"""
    if not meals or len(meals) == 0:
        return None
    
    try:
        selected = weighted_choice(meals)
        return selected if selected else (random.choice(meals) if meals else None)
    except Exception:
        return random.choice(meals) if meals else None


def on_fatigue_change():
    """スライダー変更時のコールバック"""
    st.session_state.fatigue_level = st.session_state.fatigue_slider
    st.session_state.current_recommendations = None


def get_today_message():
    """今日のモチベーションメッセージを取得"""
    try:
        today = datetime.date.today().toordinal()
        if not MOTIVATION_MESSAGES or len(MOTIVATION_MESSAGES) == 0:
            return "ごはんで元気を取り戻そう"
        index = today % len(MOTIVATION_MESSAGES)
        return MOTIVATION_MESSAGES[index]
    except Exception:
        return "ごはんで元気を取り戻そう"


def get_streak_days():
    """連続選択日数を取得"""
    try:
        df = st.session_state.df
        if len(df) == 0:
            return 0

        df_copy = df.copy()
        try:
            df_copy['date'] = pd.to_datetime(df_copy['time'], format='mixed').dt.date
        except Exception:
            return 0
        
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
                try:
                    if (unique_dates[i-1] - date).days != 1:
                        break
                except Exception:
                    break
                streak += 1

        return streak
    except Exception:
        return 0


def get_current_season():
    """現在の季節を取得"""
    try:
        now = datetime.datetime.now()
        month = now.month
        
        if 3 <= month <= 5:
            return "🌸 春（3〜5月）"
        elif 6 <= month <= 8:
            return "☀️ 夏（6〜8月）"
        elif 9 <= month <= 11:
            return "🍁 秋（9〜11月）"
        else:
            return "❄️ 冬（12〜2月）"
    except Exception:
        return "🌸 春（3〜5月）"


def get_recommendations_by_fatigue(fatigue_level):
    """疲労度に基づく推奨メニューを取得"""
    try:
        if fatigue_level <= 30:
            try:
                food = weighted_choice(INTENT_MAP.get("軽めであっさり", [])) or random.choice(INTENT_MAP.get("軽めであっさり", ["うどん"]))
            except Exception:
                food = "うどん"
            if not food:
                food = "うどん"
            intent = "軽めであっさり"
            cost = COST_MAP.get(food, "普通")
            return [{"food": food, "intent": intent, "cost": cost, "type": "single"}]

        elif fatigue_level <= 60:
            try:
                food = weighted_choice(INTENT_MAP.get("栄養しっかり", [])) or random.choice(INTENT_MAP.get("栄養しっかり", ["焼き魚定食"]))
            except Exception:
                food = "焼き魚定食"
            if not food:
                food = "焼き魚定食"
            intent = "栄養しっかり"
            cost = COST_MAP.get(food, "普通")
            return [{"food": food, "intent": intent, "cost": cost, "type": "single"}]

        else:
            try:
                easy_meals_valid = [m for m in EASY_MEALS if m and isinstance(m, str)]
                nutritious_meals_valid = [m for m in NUTRITIOUS_MEALS if m and isinstance(m, str)]
                balanced_meals_valid = [m for m in BALANCED_MEALS if m and isinstance(m, str)]
                
                if not easy_meals_valid:
                    easy_meals_valid = ["うどん"]
                if not nutritious_meals_valid:
                    nutritious_meals_valid = ["焼き魚定食"]
                if not balanced_meals_valid:
                    balanced_meals_valid = ["親子うどん"]
                
                easy_food = weighted_choice(easy_meals_valid) or random.choice(easy_meals_valid)
                nutritious_food = weighted_choice(nutritious_meals_valid) or random.choice(nutritious_meals_valid)
                balanced_food = weighted_choice(balanced_meals_valid) or random.choice(balanced_meals_valid)

                retry_count = 0
                while (easy_food == nutritious_food or easy_food == balanced_food or nutritious_food == balanced_food) and retry_count < 5:
                    if easy_food == nutritious_food:
                        nutritious_food = weighted_choice(nutritious_meals_valid) or random.choice(nutritious_meals_valid)
                    if easy_food == balanced_food:
                        balanced_food = weighted_choice(balanced_meals_valid) or random.choice(balanced_meals_valid)
                    if nutritious_food == balanced_food:
                        balanced_food = weighted_choice(balanced_meals_valid) or random.choice(balanced_meals_valid)
                    retry_count += 1

                return [
                    {"food": easy_food, "intent": "軽めであっさり", "cost": COST_MAP.get(easy_food, "普通"), "type": "easy", "description": "今すぐできる・軽い"},
                    {"food": nutritious_food, "intent": "栄養しっかり", "cost": COST_MAP.get(nutritious_food, "普通"), "type": "nutritious", "description": "栄養重視・ボリューム"},
                    {"food": balanced_food, "intent": "栄養しっかり", "cost": COST_MAP.get(balanced_food, "普通"), "type": "balanced", "description": "バランス型・無難"}
                ]
            except Exception:
                return [{"food": "うどん", "intent": "軽めであっさり", "cost": "安い", "type": "single"}]
    except Exception as e:
        st.warning(f"推奨取得エラー: {e}")
        return [{"food": "うどん", "intent": "軽めであっさり", "cost": "安い", "type": "single"}]


def get_fatigue_message(fatigue_level):
    """疲労度メッセージを取得"""
    if fatigue_level == 0:
        return "疲れ度合いをスライダーで設定するか、迷ったらおまかせしましょう"
    elif fatigue_level <= 30:
        return "今日はゆっくり休みましょう。軽めのごはんがおすすめです"
    elif fatigue_level <= 60:
        return "適度に疲れていますね。バランスの取れたごはんで回復しましょう"
    else:
        return "かなり疲れているみたいですね。3つの選択肢から選んでください"


def calc_score(intent):
    """スコアを計算"""
    try:
        return {
            "軽めであっさり": 15,
            "栄養しっかり": 12,
            "気にせずガッツリ": 10
        }.get(intent, 10)
    except Exception:
        return 10


def save(intent, food, score, cost="普通"):
    """選択記録を保存"""
    try:
        row = pd.DataFrame([{
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "intent": intent,
            "food": food,
            "score": score,
            "cost": cost
        }])

        file_exists = os.path.exists(LOG_FILE)

        try:
            row.to_csv(LOG_FILE,
                       mode="a" if file_exists else "w",
                       header=not file_exists,
                       index=False,
                       encoding="utf-8-sig")
        except Exception as e:
            st.warning(f"ファイル保存エラー: {e}")
            return

        try:
            st.session_state.df = pd.concat([st.session_state.df, row], ignore_index=True)
        except Exception:
            st.session_state.df = row
    except Exception as e:
        st.warning(f"保存エラー: {e}")


def get_satisfaction_message():
    """満足度メッセージを取得"""
    try:
        now = datetime.datetime.now()
        hour = now.hour
        
        if 5 <= hour < 11:
            meal_period = "朝食時"
        elif 11 <= hour < 15:
            meal_period = "昼食時"
        elif 15 <= hour < 22:
            meal_period = "夕食時"
        else:
            meal_period = "夜食時"
        
        messages = SATISFACTION_MESSAGES.get(meal_period, [])
        if messages and len(messages) > 0:
            return random.choice(messages)
        return "良い選択です！体が喜んでいますね"
    except Exception:
        return "良い選択です！"


def get_cost_badge_class(cost):
    """コストバッジのCSSクラスを取得"""
    try:
        if cost == "安い":
            return "cost-cheap"
        elif cost == "普通":
            return "cost-normal"
        else:
            return "cost-expensive"
    except Exception:
        return "cost-normal"


def get_cost_label(cost):
    """コストラベルを取得"""
    return COST_NAMES.get(cost, cost) if cost else "普通"


def reset_to_home():
    """ホーム画面にリセット"""
    st.session_state.step = "fatigue"
    st.session_state.fatigue_level = 0
    st.session_state.fatigue_slider = 0
    st.session_state.intent = None
    st.session_state.cost_level = "気にしない"
    st.session_state.food_choices = None
    st.session_state.final_food = None
    st.session_state.selected_intent = None
    st.session_state.selected_cost = "普通"
    st.session_state.current_recommendations = None
    st.session_state.show_roulette = False
    st.session_state.ingredient_category = None
    st.session_state.season = None
    st.session_state.scene = None
    st.session_state.selection_method = None
    st.session_state.ingredient_mode = None
    st.session_state.genre = None


# =========================
# PAGE: HOME
# =========================
def page_home():
    """ホーム画面"""

    if st.session_state.step == "fatigue":

        st.markdown('<div class="title">今日のごはんを決めましょう</div>', unsafe_allow_html=True)

        theme_title, theme_message = get_weekly_theme()
        st.markdown(f"""
        <div class="weekly-theme">
        🎯 今週のテーマ: {theme_title}
        <br>{theme_message}
        </div>
        """, unsafe_allow_html=True)

        badges = get_achievement_badges()
        if badges:
            badges_html = " ".join([f'<span class="achievement-badge">{badge}</span>' for badge in badges])
            st.markdown(f'<div style="text-align:center;margin-bottom:16px;">{badges_html}</div>', unsafe_allow_html=True)

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

        insight = generate_insight_message()
        if insight:
            st.markdown(f"""
            <div class="insight-panel">
            📊 AI分析
            <br>{insight}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="fatigue-card">
            <div class="fatigue-label">疲れ度合い</div>
            <div class="fatigue-value">{st.session_state.fatigue_level}%</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            fatigue = st.slider(
                label="疲労度を選択",
                min_value=0,
                max_value=100,
                value=st.session_state.fatigue_level,
                step=5,
                key="fatigue_slider",
                on_change=on_fatigue_change
            )

        if fatigue != st.session_state.fatigue_level:
            st.session_state.fatigue_level = fatigue
            st.session_state.current_recommendations = None

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">今日はどれくらい節約する？</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="small")
        
        with col1:
            if st.button("気にしない", use_container_width=True, key="cost_free",
                         type="primary" if st.session_state.cost_level == "気にしない" else "secondary"):
                st.session_state.cost_level = "気にしない"
                st.session_state.current_recommendations = None
                st.rerun()
        
        with col2:
            if st.button("ちょっと節約", use_container_width=True, key="cost_light",
                         type="primary" if st.session_state.cost_level == "ちょっと節約" else "secondary"):
                st.session_state.cost_level = "ちょっと節約"
                st.session_state.current_recommendations = None
                st.rerun()
        
        with col3:
            if st.button("しっかり節約", use_container_width=True, key="cost_hard",
                         type="primary" if st.session_state.cost_level == "しっかり節約" else "secondary"):
                st.session_state.cost_level = "しっかり節約"
                st.session_state.current_recommendations = None
                st.rerun()

        msg_data = COST_MESSAGE_MAP.get(st.session_state.cost_level, {})
        cost_message = msg_data.get("message", "")
        cost_prefix = msg_data.get("prefix", "")
        
        if cost_message:
            st.markdown(f'<div class="cost-message">{cost_prefix}{cost_message}</div>', unsafe_allow_html=True)

        message = get_fatigue_message(st.session_state.fatigue_level)
        if st.session_state.fatigue_level == 0:
            st.markdown(f'<div class="warning-message">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-message">{message}</div>', unsafe_allow_html=True)

        if st.session_state.show_roulette:
            st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

            if st.button("ルーレット回す", use_container_width=True, key="spin_btn"):
                selected = spin_roulette(NUTRITIOUS_MEALS)
                if selected:
                    cost = COST_MAP.get(selected, "普通")

                    st.session_state.step = "done"
                    st.session_state.final_food = selected
                    st.session_state.selected_intent = "栄養しっかり"
                    st.session_state.selected_cost = cost
                    st.session_state.show_roulette = False
                    st.balloons()
                    st.rerun()

            if st.button("← 戻る", use_container_width=True, key="back_from_roulette"):
                st.session_state.show_roulette = False
                st.rerun()
        elif st.session_state.fatigue_level == 0:
            st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1], gap="small")
            with col1:
                if st.button("自分で選ぶ", use_container_width=True, key="select_method_btn"):
                    st.session_state.step = "select_method"
                    st.rerun()
            with col2:
                if st.button("迷ったら\nおまかせ", use_container_width=True, key="random_choice_btn"):
                    st.session_state.show_roulette = True
                    st.rerun()
            with col3:
                if st.button("3候補見る", use_container_width=True, key="quick_recommend"):
                    st.session_state.fatigue_level = 50
                    st.session_state.fatigue_slider = 50
                    st.session_state.current_recommendations = None
                    st.rerun()
        else:
            if st.session_state.current_recommendations is None:
                st.session_state.current_recommendations = get_recommendations_by_fatigue(st.session_state.fatigue_level)

            recommendations = st.session_state.current_recommendations
            if not recommendations or len(recommendations) == 0:
                recommendations = [{"food": "うどん", "intent": "軽めであっさり", "cost": "安い", "type": "single"}]

            if len(recommendations) == 1:
                rec = recommendations[0]
                if rec and "food" in rec and rec.get("food"):
                    cost_label = get_cost_label(rec.get('cost', '普通'))
                    ai_reason = generate_reason(rec['food'], st.session_state.fatigue_level, st.session_state.cost_level)
                    
                    st.markdown(f"""
                    <div class="recommended-card">
                        <div class="recommended-label">おすすめ</div>
                        <div class="recommended-food">{rec['food']}</div>
                        <div class="recommended-reason">{REASON_MAP.get(rec.get('intent', ''), '')}</div>
                        <div class="cost-badge {get_cost_badge_class(rec.get('cost', '普通'))}">{cost_label}</div>
                        <div class="ai-reason">💡 {ai_reason}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
                    with col1:
                        if st.button("別の選択肢", use_container_width=True, key="alt1"):
                            st.session_state.step = "select_method"
                            st.rerun()
                    with col2:
                        if st.button("迷ったら\nおまかせ", use_container_width=True, key="roulette_btn"):
                            st.session_state.show_roulette = True
                            st.rerun()
                    with col3:
                        if st.button("決定", use_container_width=True, key="dec1"):
                            score = calc_score(rec.get('intent', '栄養しっかり'))
                            save(rec['intent'], rec['food'], score, rec.get('cost', '普通'))
                            st.session_state.step = "done"
                            st.session_state.final_food = rec['food']
                            st.session_state.selected_intent = rec.get('intent')
                            st.session_state.selected_cost = rec.get('cost', '普通')
                            st.balloons()
                            st.rerun()

            else:
                st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">おすすめ3選</div>', unsafe_allow_html=True)

                for i, rec in enumerate(recommendations):
                    if rec and "food" in rec and rec.get("food"):
                        cost_label = get_cost_label(rec.get('cost', '普通'))
                        ai_reason = generate_reason(rec['food'], st.session_state.fatigue_level, st.session_state.cost_level)
                        
                        st.markdown(f"""
                        <div class="recommendation-item">
                            <div class="recommendation-title">{rec.get('description', '')}</div>
                            <div class="recommendation-food-name">{rec['food']}</div>
                            <div class="cost-badge {get_cost_badge_class(rec.get('cost', '普通'))}">{cost_label}</div>
                            <div class="ai-reason">💡 {ai_reason}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"この「{rec['food']}」にする", use_container_width=True, key=f"recommend_{i}"):
                            score = calc_score(rec.get('intent', '栄養しっかり'))
                            save(rec['intent'], rec['food'], score, rec.get('cost', '普通'))
                            st.session_state.step = "done"
                            st.session_state.final_food = rec['food']
                            st.session_state.selected_intent = rec.get('intent')
                            st.session_state.selected_cost = rec.get('cost', '普通')
                            st.balloons()
                            st.rerun()

                st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2, gap="small")
                with col1:
                    if st.button("別の選択肢", use_container_width=True, key="alt2"):
                        st.session_state.step = "select_method"
                        st.rerun()
                with col2:
                    if st.button("迷ったら\nおまかせ", use_container_width=True, key="roulette_btn2"):
                        st.session_state.show_roulette = True
                        st.rerun()

    elif st.session_state.step == "select_method":

        st.markdown('<div class="title">どんな選び方をしたい？</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="small")
        
        with col1:
            if st.button("気分で\n選ぶ", use_container_width=True, key="select_mood"):
                st.session_state.step = "mood"
                st.session_state.selection_method = "mood"
                st.rerun()

        with col2:
            if st.button("ジャンルで\n選ぶ", use_container_width=True, key="select_genre"):
                st.session_state.step = "genre"
                st.session_state.selection_method = "genre"
                st.rerun()

        with col3:
            if st.button("具材から\n選ぶ", use_container_width=True, key="select_ingredient"):
                st.session_state.step = "ingredient"
                st.session_state.selection_method = "ingredient"
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_select_method"):
            st.session_state.step = "fatigue"
            st.rerun()

    elif st.session_state.step == "mood":

        st.markdown('<div class="title">気分で選ぶ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        intents = list(INTENT_MAP.keys()) if INTENT_MAP else []

        for intent_key in intents:
            if st.button(intent_key, use_container_width=True, key=f"mood_{intent_key}"):
                st.session_state.intent = intent_key
                st.session_state.selected_intent = intent_key
                st.session_state.step = "food"
                available_foods = INTENT_MAP.get(intent_key, [])
                if available_foods and len(available_foods) > 0:
                    num_choices = min(3, len(available_foods))
                    st.session_state.food_choices = random.sample(available_foods, k=num_choices)
                else:
                    st.session_state.food_choices = available_foods if available_foods else []
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_mood"):
            st.session_state.step = "select_method"
            st.rerun()

    elif st.session_state.step == "genre":

        st.markdown('<div class="title">ジャンルで選ぶ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        genres = list(GENRE_MAP.keys()) if GENRE_MAP else []

        for genre in genres:
            if st.button(genre, use_container_width=True, key=f"genre_{genre}"):
                st.session_state.genre = genre
                st.session_state.step = "food"
                available_foods = GENRE_MAP.get(genre, [])
                if available_foods and len(available_foods) > 0:
                    num_choices = min(3, len(available_foods))
                    st.session_state.food_choices = random.sample(available_foods, k=num_choices)
                else:
                    st.session_state.food_choices = available_foods if available_foods else []
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_genre"):
            st.session_state.step = "select_method"
            st.rerun()

    elif st.session_state.step == "ingredient":

        st.markdown('<div class="title">具材から選ぶ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="small")

        with col1:
            if st.button("具材カテゴリ\nから選ぶ", use_container_width=True, key="ingredient_category_select"):
                st.session_state.ingredient_mode = "category"
                st.session_state.step = "ingredient_category"
                st.rerun()

        with col2:
            if st.button("旬の食材\nから選ぶ", use_container_width=True, key="seasonal_select"):
                st.session_state.ingredient_mode = "seasonal"
                st.session_state.step = "ingredient_seasonal"
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_ingredient"):
            st.session_state.step = "select_method"
            st.rerun()

    elif st.session_state.step == "ingredient_category":

        st.markdown('<div class="title">具材から選ぶ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">具材カテゴリ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        categories = list(INGREDIENT_RECIPES.keys()) if INGREDIENT_RECIPES else []

        for category in categories:
            if st.button(category, use_container_width=True, key=f"ingredient_cat_{category}"):
                st.session_state.ingredient_category = category
                st.session_state.step = "ingredient_item"
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_ingredient_category"):
            st.session_state.step = "ingredient"
            st.rerun()

    elif st.session_state.step == "ingredient_item":

        category = st.session_state.ingredient_category
        if not category or category not in INGREDIENT_RECIPES:
            st.error("カテゴリが選択されていません")
            if st.button("← 戻る", use_container_width=True, key="back_from_ingredient_item_error"):
                st.session_state.step = "ingredient_category"
                st.rerun()
            return
            
        st.markdown('<div class="title">具材から選ぶ</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="section-title">{category}から選択</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        items = list(INGREDIENT_RECIPES.get(category, {}).keys())

        for item in items:
            if st.button(item, use_container_width=True, key=f"ingredient_item_{item}"):
                recipes = INGREDIENT_RECIPES.get(category, {}).get(item, [])
                st.session_state.step = "food"
                if recipes and len(recipes) > 0:
                    num_choices = min(3, len(recipes))
                    st.session_state.food_choices = random.sample(recipes, k=num_choices)
                else:
                    st.session_state.food_choices = recipes if recipes else []
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_ingredient_item"):
            st.session_state.step = "ingredient_category"
            st.rerun()

    elif st.session_state.step == "ingredient_seasonal":

        st.markdown('<div class="title">旬の食材から選ぶ</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        seasons = list(SEASONAL_RECIPES.keys()) if SEASONAL_RECIPES else []
        current_season = get_current_season()

        for season in seasons:
            is_current = " ⭐ 今が旬" if season == current_season else ""
            if st.button(season + is_current, use_container_width=True, key=f"season_{season}"):
                st.session_state.season = season
                st.session_state.scene = None
                st.session_state.step = "ingredient_seasonal_scene"
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_ingredient_seasonal"):
            st.session_state.step = "ingredient"
            st.rerun()

    elif st.session_state.step == "ingredient_seasonal_scene":

        season = st.session_state.season
        if not season or season not in SEASONAL_RECIPES:
            st.error("シーズンが選択されていません")
            if st.button("← 戻る", use_container_width=True, key="back_from_seasonal_scene_error"):
                st.session_state.step = "ingredient_seasonal"
                st.rerun()
            return
            
        season_data = SEASONAL_RECIPES[season]
        current_season = get_current_season()
        is_current = season == current_season

        st.markdown('<div class="title">どんな気分ですか？</div>', unsafe_allow_html=True)

        if is_current:
            st.markdown(f"""
            <div class="seasonal-highlight">
            🎯 今のあなたに一番合う旬の食材です
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div class="season-label">{season}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="season-detail">{season_data.get("description", "")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        scenes = list(season_data.get("scenes", {}).keys())

        for scene in scenes:
            scene_data = season_data.get("scenes", {}).get(scene, {})
            st.markdown(f"""
            <div class="scene-card">
                <div class="scene-title">{scene}</div>
                <div class="scene-desc">{scene_data.get("description", "")}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"{scene}を選ぶ", use_container_width=True, key=f"scene_{scene}"):
                st.session_state.scene = scene
                st.session_state.step = "ingredient_seasonal_food"
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_seasonal_scene"):
            st.session_state.step = "ingredient_seasonal"
            st.rerun()

    elif st.session_state.step == "ingredient_seasonal_food":

        season = st.session_state.season
        scene = st.session_state.scene
        
        if not season or season not in SEASONAL_RECIPES or not scene:
            st.error("シーズンまたはシーンが選択されていません")
            if st.button("← 戻る", use_container_width=True, key="back_from_seasonal_food_error"):
                st.session_state.step = "ingredient_seasonal_scene"
                st.rerun()
            return
            
        season_data = SEASONAL_RECIPES[season]
        scene_data = season_data.get("scenes", {}).get(scene, {})
        
        st.markdown('<div class="title">旬の食材から選ぶ</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="season-label">{season} - {scene}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="season-detail">{scene_data.get("description", "")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        foods = scene_data.get("foods", {})

        for food_name, recipes in foods.items():
            st.markdown(f'<div class="recommendation-food-name">{food_name}</div>', unsafe_allow_html=True)

            for recipe in recipes:
                cost = COST_MAP.get(recipe, "普通")
                cost_label = get_cost_label(cost)
                
                if st.button(f"{recipe} • {cost_label}", use_container_width=True, key=f"seasonal_food_{recipe}"):
                    st.session_state.step = "food"
                    st.session_state.food_choices = [recipe]
                    st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_seasonal_food"):
            st.session_state.step = "ingredient_seasonal_scene"
            st.rerun()

    elif st.session_state.step == "food":

        intent = st.session_state.intent
        choices = st.session_state.food_choices or []

        if intent:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:11px;color:#92400e;">選択中</div>
                <div class="big">{intent}</div>
                <div class="reason">{REASON_MAP.get(intent, '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:11px;color:#92400e;">選択中</div>
                <div class="big">おすすめ</div>
                <div class="reason">厳選メニュー</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">候補</div>', unsafe_allow_html=True)

        if not choices or len(choices) == 0:
            st.warning("選択肢が見つかりません")
            if st.button("← 戻る", use_container_width=True, key="back_from_food_empty"):
                if st.session_state.ingredient_mode == "seasonal" and st.session_state.scene:
                    st.session_state.step = "ingredient_seasonal_food"
                elif st.session_state.selection_method == "mood":
                    st.session_state.step = "mood"
                elif st.session_state.selection_method == "genre":
                    st.session_state.step = "genre"
                elif st.session_state.selection_method == "ingredient":
                    if st.session_state.ingredient_mode == "category":
                        st.session_state.step = "ingredient_item"
                    else:
                        st.session_state.step = "ingredient"
                else:
                    st.session_state.step = "select_method"
                st.rerun()
            return

        for food in choices:
            try:
                cost = COST_MAP.get(food, "普通")
                cost_label = get_cost_label(cost)
                ai_reason = generate_reason(food, st.session_state.fatigue_level, st.session_state.cost_level)
            except Exception:
                cost = "普通"
                cost_label = "コスパ良"
                ai_reason = "あなたにぴったりな選択です。"
            
            st.markdown(f"""
            <div class="recommendation-item">
                <div class="recommendation-food-name">{food}</div>
                <div class="cost-badge {get_cost_badge_class(cost)}">{cost_label}</div>
                <div class="ai-reason">💡 {ai_reason}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"この「{food}」にする", use_container_width=True, key=f"food_choice_{food}"):
                score = calc_score(intent or "栄養しっかり")
                save(intent or "栄養しっかり", food, score, cost)
                st.session_state.step = "done"
                st.session_state.final_food = food
                st.session_state.selected_intent = intent or "栄養しっかり"
                st.session_state.selected_cost = cost
                st.balloons()
                st.rerun()

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("← 戻る", use_container_width=True, key="back_from_food"):
            if st.session_state.ingredient_mode == "seasonal" and st.session_state.scene:
                st.session_state.step = "ingredient_seasonal_food"
            elif st.session_state.selection_method == "mood":
                st.session_state.step = "mood"
            elif st.session_state.selection_method == "genre":
                st.session_state.step = "genre"
            elif st.session_state.selection_method == "ingredient":
                if st.session_state.ingredient_mode == "category":
                    st.session_state.step = "ingredient_item"
                else:
                    st.session_state.step = "ingredient"
            else:
                st.session_state.step = "select_method"
            st.rerun()

    elif st.session_state.step == "done":

        st.markdown('<div class="title">決定完了!</div>', unsafe_allow_html=True)

        final_food = st.session_state.final_food or "うどん"
        final_cost = st.session_state.selected_cost or "普通"
        cost_label = get_cost_label(final_cost)
        ai_reason = generate_reason(final_food, st.session_state.fatigue_level, st.session_state.cost_level)

        satisfaction_msg = get_satisfaction_message()
        st.markdown(f"""
        <div class="satisfaction-message">
            ✨ {satisfaction_msg}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="recommended-card">
            <div class="recommended-label">今日のごはん</div>
            <div class="big-final">{final_food}</div>
            <div class="cost-badge {get_cost_badge_class(final_cost)}">{cost_label}</div>
            <div class="ai-reason">💡 {ai_reason}</div>
        </div>
        """, unsafe_allow_html=True)

        if final_food in TOPPING_MAP:
            topping = TOPPING_MAP.get(final_food, "")
            if topping:
                st.markdown(f"""
                <div class="suggestion">
                {topping}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        if st.button("もう一度", use_container_width=True):
            reset_to_home()
            st.rerun()


# =========================
# PAGE: LOG
# =========================
def page_log():
    """記録画面"""

    st.title("記録")

    df = st.session_state.df

    if len(df) > 0 and "food" in df.columns:

        st.markdown('<div class="section-title">統計</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="small")

        with col1:
            total_meals = len(df)
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{total_meals}</div>
                <div class="stat-label">決定回数</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            try:
                if len(df) > 0 and df["food"].notna().sum() > 0:
                    most_food = df["food"].value_counts().index[0]
                else:
                    most_food = "なし"
            except Exception:
                most_food = "なし"
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">🍽</div>
                <div class="stat-label">{most_food}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            total_score = 0
            if "score" in df.columns:
                try:
                    total_score = int(df["score"].sum())
                except Exception:
                    total_score = 0
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{total_score}</div>
                <div class="stat-label">累計スコア</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

        if "intent" in df.columns:
            st.markdown('<div class="section-title">パターン</div>', unsafe_allow_html=True)
            try:
                intent_counts = df["intent"].value_counts()

                for intent_key in ["軽めであっさり", "栄養しっかり", "気にせずガッツリ"]:
                    if intent_key in intent_counts.index:
                        count = intent_counts[intent_key]
                        percentage = (count / len(df)) * 100
                        st.write(f"**{intent_key}**: {count}回")
                        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{percentage}%"></div></div>', unsafe_allow_html=True)
            except Exception:
                pass

        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">最近</div>', unsafe_allow_html=True)

        try:
            recent_df = df.tail(10).iloc[::-1]

            for idx, row in recent_df.iterrows():
                try:
                    time_str = row['time']
                    cost = row.get('cost', '普通')
                    cost_label = get_cost_label(cost)
                    cost_class = get_cost_badge_class(cost)
                    
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="history-date">{time_str}</div>
                        <div class="history-food">{row['food']}</div>
                        <span class="history-intent">{row['intent']}</span>
                        <span class="history-cost {cost_class}">{cost_label}</span>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception:
                    pass
        except Exception:
            pass

    else:
        st.info("記録がありません")


# =========================
# MAIN LAYOUT
# =========================
if st.session_state.view_mode == "home":
    page_home()
else:
    page_log()

st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="small")

with col1:
    if st.button("🏠 ホーム", use_container_width=True, key="nav_home"):
        reset_to_home()
        st.session_state.view_mode = "home"
        st.rerun()

with col2:
    if st.button("📊 記録", use_container_width=True, key="nav_log"):
        st.session_state.view_mode = "log"
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