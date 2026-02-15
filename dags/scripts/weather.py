import os
import csv
import requests


CSV_FILE = "/opt/airflow/data/weather.csv"

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()


def save_weather(city="Moscow"):
    """Fetch weather and save to CSV"""
    data = fetch_weather(API_KEY, city)

    dt = data['dt']
    city = data['name']
    weather_main = data['weather'][0]['main']
    weather_description = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']

    row = [dt, city, weather_main, weather_description, temp, feels_like, pressure, wind_speed]

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['datetime', 'city', 'weather_main', 'weather_description',
                             'temp', 'feels_like', 'pressure', 'wind_speed'])
        writer.writerow(row)


if __name__ == "__main__":
    save_weather()
