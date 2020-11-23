from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search/', views.new_search, name='new_search'),
    path('car_details/<path:name>',
         views.car_details, name='car_details'),
]
