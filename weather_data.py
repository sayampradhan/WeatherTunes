from bs4 import BeautifulSoup
import requests
from opencage.geocoder import OpenCageGeocode

def get_city(latitude, longitude):
    key = 'bde2fa3fd7e0467ca00b407495e3e60b'
    geocoder = OpenCageGeocode(key)
    results = geocoder.reverse_geocode(latitude, longitude)

    if results:
        components = results[0]['components']
        city = components.get('city') or components.get(
            'town') or components.get('village') or components.get('hamlet')
        return city.split()[0]
    return None

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=80f5f6e4a25cc8825ca7b927c10639d7"

    response = requests.get(url)
    response = response.json()

    # Check if the 'weather' key is in the response
    if 'weather' in response:
        sky = ''
        for i in response['weather']:
            sky += i['main']
        return sky
    else:
        # Handle the case where 'weather' is not in the response
        if 'message' in response:
            return f"Error: {response['message']}"
        else:
            return "Error: Unable to retrieve weather data."

