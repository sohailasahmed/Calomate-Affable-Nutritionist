from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from diet.models import Meal
import json

from .services import (
    get_top_foods,
    get_weekly_data,
    get_cumulative_data
)


@login_required
def home(request):
    meals = Meal.objects.filter(user=request.user)

    top_labels, top_data, scatter = get_top_foods(meals)

    daily_labels, daily_calories, targets = get_weekly_data(
        Meal, request.user
    )

    cumulative_labels, cumulative_data = get_cumulative_data(
        Meal, request.user
    )

    context = {
        "top_food_labels": json.dumps(top_labels),
        "top_food_data": json.dumps(top_data),
        "scatter_data": json.dumps(scatter),

        "daily_labels": json.dumps(daily_labels),
        "daily_calories": json.dumps(daily_calories),
        "target_calories": json.dumps(targets),

        "cumulative_labels": json.dumps(cumulative_labels),
        "cumulative_data": json.dumps(cumulative_data),
    }

    return render(request, "home.html", context)