from django.urls import path
from diet.views import add_meal, dashboard

urlpatterns = [
    path('add-meal/', add_meal, name='add_meal'),
    path('dashboard/', dashboard, name='dashboard'),
]
