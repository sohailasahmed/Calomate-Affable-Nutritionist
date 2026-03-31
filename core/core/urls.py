"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import register
from django.contrib.auth import views as auth_views
from chatbot.views import chat
from django.urls import include
from diet.models import Meal
import json
from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        meals=Meal.objects.filter(user=request.user)
        labels=[]
        data=[]
        for meal in meals:
            labels.append(meal.food.name)
            data.append(meal.total_calories())

        context = {
            "labels": json.dumps(labels),
            "data": json.dumps(data),
            "total_calories": sum(data),
            "meals_count": len(data)
        }
    else:
        context={}

    return render(request, 'home.html', context)

'''def home(request):
    from django.shortcuts import render
    return render(request, 'home.html')'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('register/', register, name='register'),
    path('chat/', chat, name='chat'),
    path('diet/',include('diet.urls')),
]