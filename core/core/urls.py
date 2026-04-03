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
from django.shortcuts import render
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from diet.models import Meal
import json

@login_required
def home(request):
    today = date.today()

    # 🔥 Weekly data
    week_data = []
    week_labels = []

    for i in range(7):
        day = today - timedelta(days=i)
        meals = Meal.objects.filter(user=request.user, date=day)
        total = sum(m.total_calories() for m in meals)

        week_labels.append(day.strftime("%A"))
        week_data.append(total)

    # 🔥 Monthly data
    month_data = []
    month_labels = []

    for i in range(30):
        day = today - timedelta(days=i)
        meals = Meal.objects.filter(user=request.user, date=day)
        total = sum(m.total_calories() for m in meals)

        month_labels.append(day.strftime("%d %b"))
        month_data.append(total)

    context = {
        "week_labels": json.dumps(week_labels[::-1]),
        "week_data": json.dumps(week_data[::-1]),
        "month_labels": json.dumps(month_labels[::-1]),
        "month_data": json.dumps(month_data[::-1]),
    }

    return render(request, 'home.html', context)
'''def home(request):
    from django.shortcuts import render
    return render(request, 'home.html')'''

def about(request):
    return render(request, 'about.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔓 Public page
    path('', about),

    # 🔐 Private page
    path('home/', home),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

    path('chat/', chat, name='chat'),
    path('diet/', include('diet.urls')),
]