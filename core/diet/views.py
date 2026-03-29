from django.shortcuts import render, redirect
from .forms import MealForm
from .models import Meal
from django.contrib.auth.decorators import login_required

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
    meals = Meal.objects.filter(user=request.user)

    total_calories = 0
    food_names = []
    calories = []

    for meal in meals:
        cal = meal.total_calories()
        total_calories += cal

        food_names.append(meal.food.name)
        calories.append(cal)

    return render(request, 'diet/dashboard.html', {
        'meals': meals,
        'total_calories': total_calories,
        'food_names': food_names,
        'calories': calories
    })