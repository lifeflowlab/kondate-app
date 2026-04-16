import os
import pandas as pd
from datetime import datetime

DATA_PATH = "data/fatigue_log.csv"

def init_data():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["datetime", "action", "value"])
        df.to_csv(DATA_PATH, index=False)

def save_log(action, value):
    init_data()

    df = pd.read_csv(DATA_PATH)

    new_row = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "value": value
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def load_logs():
    init_data()
    return pd.read_csv(DATA_PATH)