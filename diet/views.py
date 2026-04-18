from django.shortcuts import render, redirect
from .forms import MealForm
from .models import Meal
from users.models import UserProfile
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

    # ---------------- USER PROFILE ----------------
    profile = UserProfile.objects.filter(user=request.user).first()

    calories_needed = 2000

    if profile and profile.dob and profile.gender:
        age = today.year - profile.dob.year - (
            (today.month, today.day) < (profile.dob.month, profile.dob.day)
        )

        height_cm = ((profile.feet * 12) + profile.inches) * 2.54
        weight = profile.weight_kg

        if profile.gender.lower() == "male":
            calories_needed = int(10 * weight + 6.25 * height_cm - 5 * age + 5)
        else:
            calories_needed = int(10 * weight + 6.25 * height_cm - 5 * age - 161)

        # Goal adjustment
        if profile.goal == "loss":
            calories_needed -= 300
        elif profile.goal == "gain":
            calories_needed += 300

    # ---------------- TOTAL CALORIES ----------------
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

    # ---------------- MEAL TYPE CHART ----------------
    meal_group = {
        "breakfast": 0,
        "lunch": 0,
        "dinner": 0
    }

    for meal in meals:
        meal_group[meal.meal_type] += meal.total_calories()

    meal_types = list(meal_group.keys())
    meal_calories = list(meal_group.values())

    # ---------------- DIFFERENCE ----------------
    difference = calories_needed - total_calories

    # ---------------- FOOD SUGGESTIONS ----------------
    suggestions = []

    if difference > 0:
        if difference < 200:
            suggestions = ["Eat fruits", "Have a small snack like nuts"]
        elif difference < 500:
            suggestions = ["Add boiled eggs", "Drink milk", "Eat sandwich"]
        else:
            suggestions = ["Full meal recommended", "Rice with curry", "Chicken meal"]
    else:
        suggestions = ["Avoid heavy meals now", "Drink water", "Take a walk"]

    # ---------------- EXERCISES ----------------
    exercises = []

    if difference > 300:
        exercises = ["Walking 10 mins", "Stretching", "Yoga"]
    elif difference > 0:
        exercises = ["Brisk walk 20 mins", "Cycling", "Jogging"]
    else:
        exercises = ["Running 30 mins", "HIIT", "Gym Workout"]

    # ---------------- FEEDBACK ----------------
    if difference > 0:
        feedback = f"You can eat {difference} more calories 👍"
    elif difference == 0:
        feedback = "Perfect! You met your goal 🎯"
    else:
        feedback = f"You exceeded by {abs(difference)} calories ⚠️"

    # ----------------progress_percentage---------------
    if calories_needed > 0:
        raw_percent = int((total_calories / calories_needed) * 100)
    else:
        raw_percent = 0

    progress_percent = min(raw_percent, 100)

    # Color logic
    if raw_percent < 80:
        progress_color = "bg-success"
    elif raw_percent <= 100:
        progress_color = "bg-warning"
    else:
        progress_color = "bg-danger"
    # ---------------- SEND TO TEMPLATE ----------------
    return render(request, 'diet/dashboard.html', {
        'meals': meals,
        'today': today,
        'total_calories': total_calories,
        'calories_needed': calories_needed,
        'food_names': json.dumps(food_names),
        'calories': json.dumps(calories),
        'percentages': json.dumps(percentages),
        'meal_types': json.dumps(meal_types),
        'meal_calories': json.dumps(meal_calories),
        'suggestions': suggestions,
        'exercises': exercises,
        'feedback': feedback,
        'progress_percent': progress_percent,
        'raw_percent': raw_percent,
        'progress_color': progress_color,
    })