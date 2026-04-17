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
from users.views import register, account
from django.contrib.auth import views as auth_views
from chatbot.views import chat
from django.urls import include
from django.shortcuts import render

from collections import defaultdict
from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    from diet.models import Meal

    meals = Meal.objects.filter(user=request.user)

    # -------------------------------
    # 1. Top 10 Foods
    # -------------------------------
    food_map = defaultdict(int)
    quantity_map = defaultdict(int)

    for meal in meals:
        food_map[meal.food.name] += meal.total_calories()
        quantity_map[meal.food.name] += meal.quantity

    sorted_foods = sorted(food_map.items(), key=lambda x: x[1], reverse=True)[:10]

    top_food_labels = [f[0] for f in sorted_foods]
    top_food_data = [f[1] for f in sorted_foods]

    # -------------------------------
    # 2. Scatter Plot
    # -------------------------------
    scatter_data = []

    for name in food_map:
        scatter_data.append({
            "x": quantity_map[name],
            "y": food_map[name]
        })

    # -------------------------------
    # 3. Daily vs Target (Last 7 days)
    # -------------------------------
    today = datetime.today().date()

    daily_labels = []
    daily_calories = []
    target_calories = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_meals = Meal.objects.filter(user=request.user, date=day)

        total = sum(m.total_calories() for m in day_meals)

        daily_labels.append(day.strftime("%a"))
        daily_calories.append(total)
        target_calories.append(2000)

    # -------------------------------
    # 4. Cumulative Trend
    # -------------------------------
    all_meals = Meal.objects.filter(user=request.user).order_by('date')

    date_map = defaultdict(int)

    for meal in all_meals:
        date_map[str(meal.date)] += meal.total_calories()

    running_total = 0
    cumulative_labels = []
    cumulative_data = []

    for d in sorted(date_map.keys()):
        running_total += date_map[d]
        cumulative_labels.append(d)
        cumulative_data.append(running_total)

    return render(request, 'home.html', {
        "top_food_labels": json.dumps(top_food_labels),
        "top_food_data": json.dumps(top_food_data),

        "scatter_data": json.dumps(scatter_data),

        "daily_labels": json.dumps(daily_labels),
        "daily_calories": json.dumps(daily_calories),
        "target_calories": json.dumps(target_calories),

        "cumulative_labels": json.dumps(cumulative_labels),
        "cumulative_data": json.dumps(cumulative_data),
    })

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
    path('account/', account, name='account'),
]