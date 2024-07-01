from django.http import JsonResponse
import requests 
 
def get_location(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        return response.json().get('city', 'Unknown')
    except:
        return 'Unknown'

def greet_visitor(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = request.META.get('REMOTE_ADDR')
    location = get_location(client_ip)
    response = {
        "clientir": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!"
    }
    return JsonResponse(response)
