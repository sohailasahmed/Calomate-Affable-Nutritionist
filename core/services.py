from collections import defaultdict
from datetime import timedelta
from django.utils import timezone

from users.models import UserProfile
from datetime import date


def get_top_foods(meals):
    food_map = defaultdict(int)

    for meal in meals:
        food_map[meal.food.name] += meal.total_calories()

    top = sorted(food_map.items(), key=lambda x: x[1], reverse=True)[:10]

    return [x[0] for x in top], [x[1] for x in top]


def get_weekly_data(Meal, user, target):
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
        targets.append(target)

    return labels, calories, targets


def get_weekday_data(Meal, user):
    names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    data = []

    for i in range(7):
        meals = Meal.objects.filter(user=user, date__week_day=((i+2) if i<6 else 1))
        total = sum(m.total_calories() for m in meals)
        data.append(total)

    return names, data


def get_monthly_trend(Meal, user):
    today = timezone.localdate()

    labels = []
    data = []

    for i in range(29, -1, -1):
        day = today - timedelta(days=i)

        meals = Meal.objects.filter(user=user, date=day)
        total = sum(m.total_calories() for m in meals)

        labels.append(day.strftime("%d"))
        data.append(total)

    return labels, data


def get_real_streak(Meal, user):
    today = timezone.localdate()
    streak = 0

    while True:
        meals = Meal.objects.filter(user=user, date=today)
        if meals.exists():
            streak += 1
            today -= timedelta(days=1)
        else:
            break

    return streak


def get_kpi_data(Meal, user):
    meals = Meal.objects.filter(user=user)

    total_meals = meals.count()
    total_calories = sum(m.total_calories() for m in meals)

    avg_calories = round(total_calories / 7) if total_calories else 0

    streak = get_real_streak(Meal, user)

    return {
        "total_meals": total_meals,
        "avg_calories": avg_calories,
        "streak": streak,
        "best_day": "Tuesday"
    }


def get_health_score(user, Meal):
    from users.models import UserProfile

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return [50, 50, 50, 50, 50]

    # ---------------------------------
    # 1. Calories Control Score
    # ---------------------------------
    today = timezone.localdate()

    meals = Meal.objects.filter(user=user, date=today)
    total_calories = sum(m.total_calories() for m in meals)

    calorie_score = max(
        0,
        min(100, 100 - abs(total_calories - 2000) / 20)
    )

    # ---------------------------------
    # 2. Consistency Score
    # ---------------------------------
    streak = get_real_streak(Meal, user)
    consistency_score = min(100, streak * 12)

    # ---------------------------------
    # 3. Hydration Score
    # ---------------------------------
    water_score = min(100, profile.water_glasses * 12)

    # ---------------------------------
    # 4. Fitness Score (Steps)
    # ---------------------------------
    fitness_score = min(100, profile.steps / 100)

    # ---------------------------------
    # 5. Sleep Recovery
    # ---------------------------------
    sleep_score = min(100, profile.sleep_hours * 12)

    return [
        round(calorie_score),
        round(consistency_score),
        round(water_score),
        round(fitness_score),
        round(sleep_score),
    ]


def get_weight_chart():
    labels = ['Week1','Week2','Week3','Week4']
    data = [82, 81.4, 80.9, 80.1]
    return labels, data

def get_deficit_chart(Meal, user):
    today = timezone.localdate()

    labels = []
    data = []

    target = 2000

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        meals = Meal.objects.filter(user=user, date=day)
        total = sum(m.total_calories() for m in meals)

        diff = total - target

        labels.append(day.strftime("%a"))
        data.append(diff)

    return labels, data

def get_avg_meal_type_chart(Meal, user):
    meal_types = ["Breakfast", "Lunch", "Dinner", "Snack"]

    labels = []
    data = []

    for meal_type in meal_types:
        meals = Meal.objects.filter(user=user, meal_type=meal_type)

        total = sum(m.total_calories() for m in meals)
        count = meals.count()

        avg = round(total / count) if count else 0

        labels.append(meal_type)
        data.append(avg)

    return labels, data

def get_meals_logged_chart(Meal, user):
    today = timezone.localdate()

    labels = []
    data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        count = Meal.objects.filter(user=user, date=day).count()

        labels.append(day.strftime("%a"))
        data.append(count)

    return labels, data


def get_today_kpi(user, Meal):
    from users.models import UserProfile

    today = timezone.localdate()

    meals = Meal.objects.filter(user=user, date=today)
    calories = sum(m.total_calories() for m in meals)

    try:
        profile = UserProfile.objects.get(user=user)

        water = profile.water_glasses
        steps = profile.steps
        sleep = profile.sleep_hours

    except:
        water = 0
        steps = 0
        sleep = 0

    streak = get_real_streak(Meal, user)

    return {
        "calories": round(calories),
        "water": water,
        "steps": steps,
        "sleep": sleep,
        "streak": streak
    }


def get_personal_target(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except:
        return 2000

    if not profile.dob:
        return 2000

    today = date.today()

    age = today.year - profile.dob.year - (
        (today.month, today.day) < (profile.dob.month, profile.dob.day)
    )

    total_inches = (profile.feet * 12) + profile.inches
    cm = total_inches * 2.54
    weight = profile.weight_kg

    if profile.gender.lower() == "male":
        bmr = 10 * weight + 6.25 * cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * cm - 5 * age - 161

    target = bmr * 1.35   # light activity default

    goal = profile.goal.lower()

    if "lose" in goal:
        target -= 400
    elif "gain" in goal:
        target += 400

    return int(target)