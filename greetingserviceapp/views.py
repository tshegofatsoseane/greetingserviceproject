
from dotenv import load_dotenv
import requests 
from django.http import JsonResponse
import os

load_dotenv()

def get_location(ip):
    """
    get ip address

    Args: ip(str) user IP address

    Return str(city) location ip address

    """

    try:
        response=requests.get(f'http://ip-api.com/json/{ip}')
        response.raise_for_status()
        data = response.json()
        city = data.get('city', 'Unknown')
        country = data.get('country', 'Unknown')
        return city, country
    except requests.RequestException:
        return 'Unknown', 'Unknown'
    
def get_temperature(city, country):
    """
    get location temparature

    Args: city(str): location to fetch the temparature for

    Return: float: The location temparature, or None if not found

    """
    api_key=os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return None
    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
        )
        response.raise_for_status()
        weather_data = response.json()
        return weather_data['main'].get('temp')
    except (requests.RequestException, KeyError):
        return None

def greet_visitor(request):
    """
    Greet the visitor by their name, and show their IP address, location and temparature of the city

    Args: request(HttpRequest): request object

    Returns:JsonResponse: The greeting, consisting of a user's name, IP address, location and temparature of the city
    """
    visitor_name=request.GET.get('visitor_name', 'Visitor')
    client_ip=get_client_ip(request)
    city, country = get_location(client_ip)
    temperature = get_temperature(city, country)

    if temperature is not None:
        greeting = f"Hello, {visitor_name}! The temperature is {temperature:.2f} degrees Celsius in {city}."
    else:
        greeting = f"Hello, {visitor_name}!"

    response = {
        "client_ip": client_ip,
        "location": f"{city}",
        "greeting": greeting
    }
    return JsonResponse(response, json_dumps_params={'indent': 4})

def get_client_ip(request):
    """
    get client IP from request, check for the X-Forwarded-For header.

    Args:
    request (HttpRequest): request object.

    Returns:
    str: The client's IP address.
    """
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0].strip()
    else:
        ip=request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip