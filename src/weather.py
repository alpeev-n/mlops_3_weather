import csv
import os
import requests
from dotenv import load_dotenv


def fetch_weather(api_key: str, city="Moscow") -> dict:
    if not api_key or not isinstance(api_key, str) or len(api_key.strip()) < 5:
        raise ValueError(f"Неверный API ключ: '{api_key}'")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            raise ValueError(f"API Error {data.get('cod')}: {data.get('message', 'Unknown error')}")

        return data
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка сети при запросе к API: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Ошибка получения погоды: {str(e)}")


def save_weather_to_csv(api_key: str="a4e46e946cbaa29f04bc37550825b874", city="Moscow", filename="/opt/airflow/src/weather.csv") -> None:
    # api_key = os.getenv("API_KEY")
    # Получаем данные о погоде
    weather_data = fetch_weather(api_key, city)

    # Проверяем успешность запроса
    if weather_data.get("cod") != 200:
        print(f"Ошибка получения данных: {weather_data.get('message', 'Unknown error')}")
        return

    # Извлекаем необходимые данные
    dt = weather_data.get("dt")
    city_name = weather_data.get("name")

    # Извлекаем данные о погоде
    weather_info = weather_data.get("weather", [{}])[0] if weather_data.get("weather") else {}
    weather_main = weather_info.get("main", "")
    weather_description = weather_info.get("description", "")

    # Извлекаем данные о температуре и давлении
    main_data = weather_data.get("main", {})
    temp = main_data.get("temp")
    feels_like = main_data.get("feels_like")
    pressure = main_data.get("pressure")

    # Извлекаем данные о ветре
    wind_data = weather_data.get("wind", {})
    wind_speed = wind_data.get("speed")

    # Подготавливаем данные для записи
    row_data = {
        "datetime": dt,
        "city": city_name,
        "weather_main": weather_main,
        "weather_description": weather_description,
        "temp": temp,
        "feels_like": feels_like,
        "pressure": pressure,
        "wind_speed": wind_speed
    }

    # Проверяем существование файла
    file_exists = os.path.exists(filename)

    # Определяем заголовки столбцов
    fieldnames = ["datetime", "city", "weather_main", "weather_description",
                  "temp", "feels_like", "pressure", "wind_speed"]

    # Открываем файл для записи
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Если файл не существует, записываем заголовки
        if not file_exists:
            writer.writeheader()

        # Записываем данные
        writer.writerow(row_data)

    print(f"Данные о погоде в городе {city_name} успешно записаны в {filename}")

if __name__ == "__main__":
    # test weather API
    load_dotenv("../.env")
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("Ошибка: API_KEY не найден в переменных окружения")
    else:
        city = "Moscow"
        save_weather_to_csv(api_key=api_key, city=city)
