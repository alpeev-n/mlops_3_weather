import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Загрузка ключа из .env
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITY = 'Moscow'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather_data():
    """Запрашивает текущую погоду через API."""
    params = {
        'q': CITY,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе к API: {e}')
        return None

def save_to_csv(weather_data, filename='weather.csv'):
    """Сохраняет данные в CSV файл."""
    if weather_data:
        # Извлечение нужных полей из ответа API
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = {
            'timestamp': current_time,
            'city': CITY,
            'temp': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': weather_data['wind']['speed'],
            'description': weather_data['weather'][0]['description']
        }

        # Создание DataFrame и сохранение
        df = pd.DataFrame([record])
        file_exists = os.path.isfile(filename)
        df.to_csv(filename, mode='a', header=not file_exists, index=False)
        print(f'Данные сохранены в {filename}: {record}')
    else:
        print('Нет данных для сохранения.')

if __name__ == '__main__':
    # Точка входа для локального тестирования
    data = get_weather_data()
    if data:
        save_to_csv(data)