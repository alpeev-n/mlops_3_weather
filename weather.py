import os
import csv
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


def fetch_weather(api_key: str, city="Moscow", lat=55.75, lon=37.62) -> dict:
    """Fetch weather data from OpenWeatherMap API using coordinates."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    return weather_data


def save_weather_data(weather_data: dict, csv_file: str = "weather.csv") -> None:
    """Extract weather data from API response and save to CSV file."""
    try:
        # Extract data from API response
        dt = datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        city = weather_data['name']
        weather_main = weather_data['weather'][0]['main']
        weather_description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        
        # Prepare row
        row = [dt, city, weather_main, weather_description, temp, feels_like, pressure, wind_speed]
        
        # Check if file exists and has content
        file_exists = False
        if Path(csv_file).exists() and Path(csv_file).stat().st_size > 0:
            with open(csv_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                # Check if file only has header
                file_exists = 'datetime' in first_line
        
        # Append data to CSV
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header if file doesn't exist or is empty
            if not file_exists:
                writer.writerow(['datetime', 'city', 'weather_main', 'weather_description', 'temp', 'feels_like', 'pressure', 'wind_speed'])
            writer.writerow(row)
        
        print(f"Saved weather data: {dt} - {city}, {weather_main}, {temp}°C")
    except Exception as e:
        print(f"Error saving weather data: {e}")
        raise


if __name__ == "__main__":
    # test weather API and save
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)
    print(data)
    save_weather_data(data)
