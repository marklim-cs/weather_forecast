import requests
import os
from dotenv import load_dotenv

from django.shortcuts import render
from django.template import loader
import datetime

def index(request):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}&units=metric"
    #template = loader.get_template('index.html')

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.get('city2', None)

        weather_current1, daily_forecast1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
        if city2:
            weather_current2, daily_forecast2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_current2, daily_forecast2 = None, None

        context = {
            "weather_current1": weather_current1, 
            "daily_forecast1": daily_forecast1, 
            "weather_current2": weather_current2, 
            "daily_forecast2": daily_forecast2, 
        }

        return render(request, "app/index.html", context)
    else:
        return render(request, "app/index.html")

def fetch_weather_and_forecast(city, api_key, forecast_url,current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = response.get(forecast_url.format(lat, lon, api_key)).json()

    weather_current = {
        "city": city, 
        "temperature": round(response['main']['temp']),
        "description": response['weather'][0]['description'], 
        "icon": response['weather'][0]['icon'],
    }

    daily_forecast = []
    for daily_data in forecast_response['list'][:5]:
        daily_forecast.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"), 
            "min_temp": round(daily_data['temp']['min']), 
            "max_temp": round(daily_data['temp']['max']),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon'],
        })

    return weather_current, daily_forecast