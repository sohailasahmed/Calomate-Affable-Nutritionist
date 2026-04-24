import json
from collections import defaultdict
from datetime import timedelta
from django.utils import timezone


def get_top_foods(meals):
    food_map = defaultdict(int)
    quantity_map = defaultdict(int)

    for meal in meals:
        food_map[meal.food.name] += meal.total_calories()
        quantity_map[meal.food.name] += meal.quantity

    sorted_foods = sorted(food_map.items(), key=lambda x: x[1], reverse=True)[:10]

    labels = [item[0] for item in sorted_foods]
    data = [item[1] for item in sorted_foods]

    scatter = []

    for name in food_map:
        scatter.append({
            "x": quantity_map[name],
            "y": food_map[name]
        })

    return labels, data, scatter


def get_weekly_data(Meal, user):
    today = timezone.localdate()

    labels = []
    calories = []
    targets = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        meals = Meal.objects.filter(user=user, date=day)
        total = sum(m.total_calories() for m in meals)

        labels.append(day.strftime("%a"))
        calories.append(total)
        targets.append(2000)

    return labels, calories, targets


def get_cumulative_data(Meal, user):
    meals = Meal.objects.filter(user=user).order_by("date")

    date_map = defaultdict(int)

    for meal in meals:
        date_map[str(meal.date)] += meal.total_calories()

    running = 0
    labels = []
    data = []

    for d in sorted(date_map.keys()):
        running += date_map[d]
        labels.append(d)
        data.append(running)

    return labels, data