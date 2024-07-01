from django.http import JsonResponse
import requests 
import os
from dotenv import load_dotenv

def get_location(ip):
    """
    fetch location of user IP address using ip-api.

    Args:
    ip (str): The IP address of the client.

    Returns:
    str: city matching the IP address or 'Unknown' if it's not found.
    """
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        return response.json().get('city', 'Unknown')
    except:
        return 'Unknown'
    
def get_temperature(city):
    """
    Get the temp of the location using OpenWeather API

    Args:
    city (str): location to fetch the temp.

    Returns:
    float: The temp or None if not found.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
        response.raise_for_status()
        weather_data = response.json()
        return weather_data['main'].get('temp')
    except (requests.RequestException, KeyError):
        return None

def greet_visitor(request):
    """
    Greet visitor by his/her name and show IP address, location, and temperature of location.

    Args:
    request (HttpRequest): request object.

    Returns:
    JsonResponse: The greeting, the IP address & location, and the temperature as json response.
    """
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = request.META.get('REMOTE_ADDR')
    location = get_location(client_ip)
    temperature = get_temperature(location)

    if temperature is not None:
        greeting = f"Hello, {visitor_name}!, the temperature is {temperature:.2f} degrees Celsius in {location}"
    else:
        greeting = f"Hello, {visitor_name}!"

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!"
    }
    return JsonResponse(response, json_dumps_params={'indent': 4})
