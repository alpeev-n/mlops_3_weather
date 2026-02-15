import os
import csv
from datetime import datetime

import requests
from dotenv import load_dotenv


DATASET_PATH = "/opt/airflow/dataset/weather.csv"


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_weather_to_csv(city="Moscow", csv_path=DATASET_PATH):
    load_dotenv("/opt/airflow/.env")

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY not found")

    data = fetch_weather(api_key=api_key, city=city)

    row = {
        "datetime": datetime.fromtimestamp(data["dt"]),
        "city": data["name"],
        "weather_main": data["weather"][0]["main"],
        "weather_description": data["weather"][0]["description"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
    }

    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "datetime",
                "city",
                "weather_main",
                "weather_description",
                "temp",
                "feels_like",
                "pressure",
                "wind_speed",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print("Weather saved:", row)


if __name__ == "__main__":
    save_weather_to_csv()
