from django.urls import path
from . import views
from diet.views import add_meal, dashboard

urlpatterns = [
    path('add-meal/', add_meal, name='add_meal'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-food/', views.add_custom_food, name='add_custom_food'),
    path('delete-meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
]
