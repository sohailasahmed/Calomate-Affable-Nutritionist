from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from diet.models import Meal
import json

from .services import (
    get_top_foods,
    get_weekly_data,
    get_weekday_data,
    get_monthly_trend,
    get_kpi_data,
    get_meals_logged_chart,
    get_today_kpi,
    get_personal_target
)


@login_required
def home(request):
    meals = Meal.objects.filter(user=request.user)

    # Existing Charts
    top_labels, top_data = get_top_foods(meals)
    target = get_personal_target(request.user)

    daily_labels, daily_calories, target_calories = get_weekly_data(
        Meal, request.user, target
    )


    weekday_labels, weekday_data = get_weekday_data(
        Meal, request.user
    )

    month_labels, month_data = get_monthly_trend(
        Meal, request.user
    )

    # NEW Chart
    logged_labels, logged_data = get_meals_logged_chart(
        Meal, request.user
    )

    # KPI Sections
    kpi = get_kpi_data(Meal, request.user)

    today_kpi = get_today_kpi(
        request.user,
        Meal
    )

    context = {
        "top_food_labels": json.dumps(top_labels),
        "top_food_data": json.dumps(top_data),

        "daily_labels": json.dumps(daily_labels),
        "daily_calories": json.dumps(daily_calories),
        "target_calories": json.dumps(target_calories),

        "weekday_labels": json.dumps(weekday_labels),
        "weekday_data": json.dumps(weekday_data),

        "month_labels": json.dumps(month_labels),
        "month_data": json.dumps(month_data),

        "logged_labels": json.dumps(logged_labels),
        "logged_data": json.dumps(logged_data),

        "kpi": kpi,
        "today_kpi": today_kpi,
        "recommended_target": target,
    }

    return render(request, "home.html", context)