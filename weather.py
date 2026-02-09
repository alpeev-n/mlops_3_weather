import os
import csv
from datetime import datetime

import requests
from dotenv import load_dotenv


def fetch_weather(api_key: str, city: str = "Moscow") -> dict:
    """
    Call OpenWeatherMap API and return raw response as dict.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    return weather_data


def append_weather_to_csv(api_key: str, city: str = "Moscow", csv_path: str = "weather.csv") -> None:
    """
    Fetch current weather and append a new row to weather.csv.

    Columns:
    datetime, city, weather_main, weather_description,
    temp, feels_like, pressure, wind_speed
    """
    weather = fetch_weather(api_key=api_key, city=city)

    dt_unix = weather.get("dt")
    dt_iso = datetime.utcfromtimestamp(dt_unix).isoformat() if dt_unix is not None else ""

    city_name = weather.get("name", city)

    weather_list = weather.get("weather") or []
    first_weather = weather_list[0] if weather_list else {}
    weather_main = first_weather.get("main", "")
    weather_description = first_weather.get("description", "")

    main_info = weather.get("main", {})
    temp = main_info.get("temp")
    feels_like = main_info.get("feels_like")
    pressure = main_info.get("pressure")

    wind_info = weather.get("wind", {})
    wind_speed = wind_info.get("speed")

    fieldnames = [
        "datetime",
        "city",
        "weather_main",
        "weather_description",
        "temp",
        "feels_like",
        "pressure",
        "wind_speed",
    ]

    row = {
        "datetime": dt_iso,
        "city": city_name,
        "weather_main": weather_main,
        "weather_description": weather_description,
        "temp": temp,
        "feels_like": feels_like,
        "pressure": pressure,
        "wind_speed": wind_speed,
    }

    file_exists = os.path.isfile(csv_path)
    file_exists_and_not_empty = file_exists and os.path.getsize(csv_path) > 0
    if file_exists_and_not_empty:
        with open(csv_path, "rb") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                with open(csv_path, "a") as f:
                    f.write("\n")

    with open(csv_path, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists_and_not_empty:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY is not set in .env")

    append_weather_to_csv(api_key=api_key, city="Moscow")
