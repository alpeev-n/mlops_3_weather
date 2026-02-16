import os
import time
from datetime import datetime
from dotenv import load_dotenv
from weather import save_weather_to_csv

# Загружаем API ключ
load_dotenv(".env")
api_key = os.getenv("API_KEY")

if not api_key:
    print("ERROR: API key not found!")
    exit(1)

print("=" * 60)
print("Starting weather data collection")
print("Duration: 10 minutes (10 requests, 1 per minute)")
print("=" * 60)

for i in range(1, 11):
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{current_time}] Request {i}/10...")

    try:
        result = save_weather_to_csv(api_key=api_key, csv_path="weather.csv", city="Moscow")
        print(f"  ✓ Data saved to {result}")

        # Показываем последнюю добавленную строку
        with open(result, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 1:
                last_line = lines[-1].strip()
                print(f"  → {last_line}")

        if i < 10:
            print(f"  ⏳ Waiting 60 seconds until next request...")
            time.sleep(60)  # Ждём 1 минуту
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("Collection completed!")
print("Check weather.csv for all collected data")
print("=" * 60)
