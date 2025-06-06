from fastapi import FastAPI
import socket
import requests
from datetime import datetime
import pytz
import os

API_VERSION = os.getenv("APP_VERSION", "dev")
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI server for weather!"}


@app.get("/api/health")
def health_check():
    try:
        # Check if weather API is reachable
        test_url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=23.8103&longitude=90.4125"
            "&current_weather=true"
        )
        response = requests.get(test_url, timeout=5)

        # Check HTTP response status
        if response.status_code == 200:
            return {"status": "ok", "weather_api": "reachable"}
        else:
            return {"status": "degraded", "weather_api": "unreachable", "code": response.status_code}

    except Exception as e:
        return {"status": "error", "weather_api": "unreachable", "error": str(e)}


@app.get("/api/hello")
def get_hello():
    # Get hostname
    hostname = socket.gethostname()

    # setting up date-time
    dhaka_tz = pytz.timezone("Asia/Dhaka")
    dhaka_time = datetime.now(dhaka_tz).strftime("%Y-%m-%d %H:%M:%S")

    # Weather API (Open-Meteo)
    latitude = 23.8103
    longitude = 90.4125

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current_weather=true"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia%2FDhaka"
    )

    try:
        response = requests.get(weather_url)
        weather_data = response.json()

        # Current temperature
        temperature = weather_data["current_weather"]["temperature"]

        # Daily forecast
        dates = weather_data["daily"]["time"]
        max_temps = weather_data["daily"]["temperature_2m_max"]
        min_temps = weather_data["daily"]["temperature_2m_min"]

        forecast = []
        for i in range(len(dates)):
            forecast.append({
                "date": dates[i],
                "temp_max": max_temps[i],
                "temp_min": min_temps[i]
            })

    except Exception as e:
        temperature = "N/A"
        forecast = []

    return {
        "hostname": hostname,
        "datetime": dhaka_time,
        "version": "v1.0",
        "weather": {
            "dhaka": {
                "temperature": temperature,
                "temp_unit": "°C",
                "forecast": forecast  # Add forecast here
            }
        }

    }

