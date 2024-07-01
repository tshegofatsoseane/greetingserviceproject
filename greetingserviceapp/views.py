from django.http import JsonResponse
import requests 
 
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
    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!"
    }
    return JsonResponse(response, json_dumps_params={'indent': 4})
