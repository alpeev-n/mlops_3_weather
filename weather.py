import os
import requests
import csv
from dotenv import load_dotenv
from pathlib import Path


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

CSV_HEADER = [
    "datetime",
    "city",
    "weather_main",
    "weather_description",
    "temp",
    "feels_like",
    "pressure",
    "wind_speed",
]

def save_weather_to_csv(weather_data: dict, filename="weather.csv") -> None:
    row = [
        weather_data["dt"],
        weather_data["name"],
        weather_data["weather"][0]["main"],
        weather_data["weather"][0]["description"],
        weather_data["main"]["temp"],
        weather_data["main"]["feels_like"],
        weather_data["main"]["pressure"],
        weather_data["wind"]["speed"],
    ]

    file_exists = os.path.exists(filename)

    if not file_exists:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
            writer.writerow(row)
        return

    with open(filename, "r", newline="", encoding="utf-8") as file:
        first_line = file.readline().strip()

    if first_line != ",".join(CSV_HEADER):
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if os.path.getsize(filename) == 0:
                writer.writerow(CSV_HEADER)

            writer.writerow(row)
    else:
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)

def collect_weather(city: str, path: str = ""):
    load_dotenv(".env")

    load_dotenv(Path(path) / ".env")
    api_key = os.getenv("API_KEY","")

    data = fetch_weather(api_key=api_key, city=city)
    filename = f"{path}/weather.csv"

    save_weather_to_csv(data, filename)

    print("Weather data saved")

if __name__ == "__main__":
    # test weather API
    collect_weather("Moscow")
