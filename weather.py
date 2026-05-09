import os
import requests
from pprint import pprint
from dotenv import load_dotenv


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def append_weather_csv(api_key: str, city='Moscow') -> None:
    weather_data = fetch_weather(api_key, city)

    new_record = (
        "\n"
        f"{weather_data["dt"]},"
        f"{city},"
        f"{weather_data["weather"][0]["main"]},"
        f"{weather_data["weather"][0]["description"]},"
        f"{weather_data["main"]["temp"]},"
        f"{weather_data["main"]["feels_like"]},"
        f"{weather_data["main"]["pressure"]},"
        f"{weather_data["wind"]["speed"]}"
    )
    with open('weather.csv', 'a') as f:
        f.write(new_record)


if __name__ == "__main__":
    # test weather API
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)
    append_weather_csv(api_key, city)
    pprint(data)
