import csv
import os
import requests


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def save_to_csv(data: dict, filename="weather.csv"):
    data_to_save = {
            "datetime": data.get("dt"),
            "city": data.get("name"),
            "weather_main": data["weather"][0]["main"] if data.get("weather") else None,
            "weather_description": data["weather"][0]["description"] if data.get("weather") else None,
            "temp": data["main"]["temp"] if data.get("main") else None,
            "feels_like": data["main"]["feels_like"] if data.get("main") else None,
            "pressure": data["main"]["pressure"] if data.get("main") else None,
            "wind_speed": data["wind"]["speed"] if data.get("wind") else None,
    }
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "rb") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
        if last_char != b"\n":
            with open(filename, "a") as f:
                f.write("\n")

    with open(filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_to_save.keys())
        writer.writerow(data_to_save)



def get_weather(api_key: str, city="Moscow", filename="weather.csv") -> dict:
    data = fetch_weather(api_key=api_key, city=city)
    save_to_csv(data, filename=filename)
    return data


if __name__ == "__main__":
    # test weather API
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = get_weather(api_key=api_key, city=city, filename="weather.csv")
    save_to_csv(data, filename="weather.csv")
    print(data)
