import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
WEATHER_CSV = BASE_DIR / "weather.csv"

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "Moscow"

CSV_FIELDNAMES = [
    "datetime",
    "city",
    "weather_main",
    "weather_description",
    "temp",
    "feels_like",
    "pressure",
    "wind_speed",
]


def fetch_weather(api_key: str, city: str = DEFAULT_CITY) -> dict[str, Any]:
    """получает текущие данные о погоде для city"""
    response = requests.get(
        OPENWEATHER_URL,
        params={
            "q": city,
            "appid": api_key,
            "units": "metric",
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(
            "OpenWeatherMap request failed. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()


def extract_weather_row(weather_data: dict[str, Any]) -> dict[str, Any]:
    """извлекает из ответа OpenWeatherMap данные для записи в csv"""
    weather = weather_data["weather"][0]
    main = weather_data["main"]
    wind = weather_data["wind"]

    return {
        "datetime": datetime.fromtimestamp(weather_data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
        "city": weather_data["name"],
        "weather_main": weather["main"],
        "weather_description": weather["description"],
        "temp": main["temp"],
        "feels_like": main["feels_like"],
        "pressure": main["pressure"],
        "wind_speed": wind["speed"],
    }


def append_weather_row(
    row: dict[str, Any],
    csv_path: Path = WEATHER_CSV,
) -> str:
    """добавляет строку с погодными данными в csv"""
    file_exists = csv_path.exists()
    file_is_empty = not file_exists or csv_path.stat().st_size == 0

    if file_exists and not file_is_empty:
        with open(csv_path, mode="rb") as file:
            file.seek(-1, os.SEEK_END)
            last_char = file.read(1)

        if last_char not in {b"\n", b"\r"}:
            with open(csv_path, mode="a", encoding="utf-8") as file:
                file.write("\n")

    with open(csv_path, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)

        if file_is_empty:
            writer.writeheader()

        writer.writerow(row)

    return str(csv_path)


def collect_weather(
    city: str = DEFAULT_CITY,
    csv_path: Path = WEATHER_CSV,
) -> str:
    """получает погоду для города и записывает новую строку в csv"""
    load_dotenv(ENV_PATH)

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise RuntimeError(
            "API_KEY is not set. Add API_KEY to .env or export it as environment variable."
        )

    weather_data = fetch_weather(api_key=api_key, city=city)
    row = extract_weather_row(weather_data)

    return append_weather_row(row=row, csv_path=csv_path)


if __name__ == "__main__":
    saved_csv_path = collect_weather()
    print(f"Weather data was saved to {saved_csv_path}")