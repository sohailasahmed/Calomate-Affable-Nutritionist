from django.shortcuts import render, redirect
from .forms import MealForm
from .models import Meal
from users.models import Profile
import json
from datetime import date
from django.contrib.auth.decorators import login_required
from collections import defaultdict

@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('dashboard')
    else:
        form = MealForm()

    return render(request, 'diet/add_meal.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    meals = Meal.objects.filter(user=request.user, date=today)
    try:
        profile = Profile.objects.get(user=request.user)

        weight = profile.weight
        height = profile.height
        age = profile.age

        # Simple BMR formula
        calories_needed = 10 * weight + 6.25 * height - 5 * age + 5

        # Adjust based on goal
        if profile.goal == 'loss':
            calories_needed -= 300
        elif profile.goal == 'gain':
            calories_needed += 300

    except:
        calories_needed = 2000  # fallback default

    total_calories = 0
    food_totals = defaultdict(int)

    for meal in meals:
        cal = meal.total_calories()
        total_calories += cal
        food_totals[meal.food.name] += cal

    food_names = list(food_totals.keys())
    calories = list(food_totals.values())

    total = sum(calories)

    percentages = []
    for c in calories:
        if total > 0:
            percentages.append((c / total) * 100)
        else:
            percentages.append(0)
# ------------------
    meal_group = {
        "breakfast": 0,
        "lunch": 0,
        "dinner": 0
    }

    for meal in meals:
        meal_group[meal.meal_type] += meal.total_calories()

    meal_types = list(meal_group.keys())
    meal_calories = list(meal_group.values())

# -------------------
    difference = calories_needed - total_calories

    suggestions = []

    if difference > 0:
        # User can eat more
        if difference < 200:
            suggestions = ["Eat fruits", "Have a small snack like nuts"]
        elif difference < 500:
            suggestions = ["Add 1 boiled egg", "Eat a sandwich", "Drink milk"]
        else:
            suggestions = ["Have rice with curry", "Add chicken meal", "Full meal recommended"]

    else:
        # User exceeded
        suggestions = ["Avoid heavy meals now", "Drink water", "Go for a walk"]
# --------------------
    exercises = []

    if difference > 300:
        exercises = ["Light walking (10 mins)", "Stretching", "Yoga"]
    elif difference > 0:
        exercises = ["Brisk walking (20 mins)", "Cycling", "Light jogging"]
    else:
        exercises = ["Running (30 mins)", "HIIT workout", "Gym training"]
# ----------------------------
    #feedback
    if difference > 0:
        feedback = f"You can eat {difference} more calories 👍"
    elif difference == 0:
        feedback = "Perfect! You met your goal 🎯"
    else:
        feedback = f"You exceeded by {abs(difference)} calories ⚠️"
# -------------------------------
    return render(request, 'diet/dashboard.html', {
        'meals': meals,
        'total_calories': total_calories,
        'food_names': json.dumps(food_names),
        'calories': json.dumps(calories),
        'percentages': json.dumps(percentages),
        'meal_types': json.dumps(meal_types),
        'meal_calories': json.dumps(meal_calories),
        'suggestions': suggestions,
        'exercises': exercises,
        'feedback': feedback,
        'calories_needed': int(calories_needed),
        'today': today
    })