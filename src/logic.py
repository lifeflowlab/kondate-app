import random
import datetime

# ===== 日替わり候補 =====
def get_today_candidates():

    today = datetime.date.today().isoformat()
    random.seed(today)

    foods = [
        "カレー", "ラーメン", "焼肉", "パスタ",
        "寿司", "うどん", "鍋", "炒飯"
    ]

    return random.sample(foods, 3)


# ===== 意向デフォルト =====
def get_default_intent():
    hour = datetime.datetime.now().hour

    if hour < 10:
        return "時短"
    elif hour < 15:
        return "節約"
    elif hour < 21:
        return "がっつり"
    else:
        return "ヘルシー"


# ===== 並び替え（中身固定）=====
def sort_by_intent(candidates, intent):

    priority_map = {
        "節約": ["パスタ", "炒飯"],
        "ヘルシー": ["鍋"],
        "がっつり": ["焼肉", "カレー"],
        "時短": ["うどん", "炒飯"],
    }

    if intent not in priority_map:
        return candidates

    priority = priority_map[intent]

    return sorted(candidates, key=lambda x: 0 if x in priority else 1)


# ===== 強制決定 =====
def force_pick(candidates):
    return candidates[0] if candidates else "カレー"


# ===== 今日のラベル =====
def get_day_label(food):
    return f"今日は『{food}の日』です 🍽"