import random
import datetime


def get_today_candidates():
    today = datetime.date.today().isoformat()
    random.seed(today)

    return random.sample([
        "カレー", "ラーメン", "焼肉", "パスタ",
        "寿司", "うどん", "鍋", "炒飯"
    ], 3)


def get_default_fatigue():
    return 50


def get_food_by_fatigue(fatigue):

    if fatigue <= 20:
        category = "reward"
    elif fatigue <= 40:
        category = "heavy"
    elif fatigue <= 60:
        category = "normal"
    elif fatigue <= 80:
        category = "light"
    else:
        category = "recovery"

    food_map = {
        "reward": ["焼肉", "寿司", "ステーキ", "カレー"],
        "heavy": ["ラーメン", "パスタ", "炒飯"],
        "normal": ["親子丼", "うどん", "定食"],
        "light": ["そば", "雑炊", "スープ"],
        "recovery": ["おかゆ", "うどん", "スープ"]
    }

    import random
    food = random.choice(food_map[category])

    return food, category


def get_mode_label(category):

    labels = {
        "reward": "ご褒美モード",
        "heavy": "しっかりモード",
        "normal": "バランスモード",
        "light": "軽めモード",
        "recovery": "回復モード"
    }

    return labels.get(category, "バランスモード")