import csv
import os
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def fetch_and_save_weather(city: str = "Moscow", csv_path: str = "weather.csv") -> None:
    api_key = os.getenv("OPENWEATHER_API_KEY") or os.getenv("API_KEY")
    data = fetch_weather(api_key=api_key, city=city)

    row = {
        "datetime": datetime.fromtimestamp(data["dt"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "city": data["name"],
        "weather_main": data["weather"][0]["main"],
        "weather_description": data["weather"][0]["description"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
    }

    fieldnames = ["datetime", "city", "weather_main", "weather_description",
                  "temp", "feels_like", "pressure", "wind_speed"]

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)
