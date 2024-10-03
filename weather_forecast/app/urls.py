from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cities'),
    path('weather/', views.weather, name='weather'),
]