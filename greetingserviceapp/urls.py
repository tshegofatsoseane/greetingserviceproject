from django.urls import path
from .views import greet_visitor

urlpatterns = [
    path('hello', greet_visitor),
]
