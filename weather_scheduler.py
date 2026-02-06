import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.absolute()))

from weather import fetch_weather, save_weather_data

def run_weather_collection():
    """Run weather data collection every minute."""
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        raise ValueError("API_KEY not found in .env file")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting weather collection scheduler...")
    print("Press Ctrl+C to stop")
    
    execution_count = 0
    while True:
        try:
            execution_count += 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{timestamp}] Execution #{execution_count}")
            
            # Fetch weather
            weather_data = fetch_weather(api_key=api_key)
            
            # Save to CSV
            csv_path = Path(__file__).parent / "weather.csv"
            save_weather_data(weather_data, csv_file=str(csv_path))
            
            print(f"[{timestamp}] ✓ Task completed successfully!")
            
            # Wait 60 seconds before next execution
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sleeping for 60 seconds...")
            time.sleep(60)
            
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler stopped by user")
            sys.exit(0)
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    from dotenv import load_dotenv
    run_weather_collection()
