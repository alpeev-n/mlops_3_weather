import os
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def save_weather_to_csv(api_key: str, csv_path: str = "weather.csv", city: str = "Moscow") -> str:
    weather_data = fetch_weather(api_key, city)

    dt = datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    city_name = weather_data['name']
    weather_main = weather_data['weather'][0]['main']
    weather_description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']

    row = [dt, city_name, weather_main, weather_description, temp, feels_like, pressure, wind_speed]

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    return csv_path


if __name__ == "__main__":
    # test weather API
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)
    print(data)
