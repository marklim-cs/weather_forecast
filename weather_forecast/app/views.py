import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

from django.shortcuts import render
from django.template import loader
import datetime

def index(request):
    return render(request, "index.html")

def weather(request):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&cnt=5&appid={}&units=metric"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None) #get() allows to provide a default value, works for optional fields

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

        return render(request, "weather.html", context)
    else:
        return render(request, "weather.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_current = {
        "city": city, 
        "temperature": round(response['main']['temp']),
        "description": response['weather'][0]['description'], 
        "icon": response['weather'][0]['icon'],
    }

    daily_forecast = []
    daily_data_grouped = defaultdict(list)

    #group the data by day 
    for daily_data in forecast_response['list'][1:10]:
        day = datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A")
        daily_data_grouped[day].append(daily_data)

        print(daily_data_grouped)

    #exctract min and max temp
    for day, data_list in list(daily_data_grouped.items())[1:5]:
        min_temp = min(data['main']['temp_min'] for data in data_list)
        max_temp = max(data['main']['max_temp'] for data in data_list)

        descriptions = (data['weather'][0]['description'] for data in data_list)
        most_frequent_description = count_element_frequency(descriptions)

        icons = (data['weather'][0]['icon'] for data in data_list)
        most_frequent_icon = count_element_frequency(icons)


        daily_forecast.append({
            "day": day, 
            "min_temp": min_temp, 
            "max_temp": max_temp,
            "description": most_frequent_description,
            "icon": most_frequent_icon,
        })

    print("Current Weather Data:", weather_current)
    print("Daily Forecast Data:", daily_forecast)

    return weather_current, daily_forecast


def count_element_frequency(array):
    array = array
    frequency_dict = {}

    for element in array:
        if element in frequency_dict:
            frequency_dict[element] += 1
        else:
            frequency_dict[element] = 1

    max_key = max(frequency_dict, key=frequency_dict.get)
    return max_key