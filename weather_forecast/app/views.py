import requests
import os
from dotenv import load_dotenv

from django.shortcuts import render
import datetime

def index(request):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.get('city2', None)
    else:
        return render(request, "index.html")

def fetch_weather_and_forecast(current_weather_url, forecast_url, api_key, city):
    response = request.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast = response.get(forecast_url.format(lat, lon, api_key)).json()