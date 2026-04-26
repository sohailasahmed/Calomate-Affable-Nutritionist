from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserProfileForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from datetime import date
import requests
from django.conf import settings
from .models import UserProfile, WaterIntake, DailySteps
from core.services import get_personal_target
from datetime import date

API_KEY = settings.API_KEY

@login_required
def account(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    today = date.today()

    if profile.last_tracker_reset != today:
        profile.water_glasses = 0
        profile.steps = 0
        profile.sleep_hours = 0
        profile.last_tracker_reset = today
        profile.save()

    if request.method == "POST":

        # Add water button
        if "add_water" in request.POST:
            profile.water_glasses += 1
            profile.save()
            return redirect("account")

        if "add_steps" in request.POST:
            profile.steps += 1000
            profile.save()
            return redirect("account")

        if "add_sleep" in request.POST:
            profile.sleep_hours += 1
            profile.save()
            return redirect("account")

        # Save profile form
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            obj = form.save()
            print("Saved:", obj.profile_pic)
            return redirect("account")
        else:
            print(form.errors)

    else:
        form = UserProfileForm(instance=profile)
    # -------- Calculations --------
    age = None
    bmi = None
    bmi_status = ""
    calories = None

    if profile.dob:
        today = date.today()
        age = today.year - profile.dob.year - (
            (today.month, today.day) < (profile.dob.month, profile.dob.day)
        )

    total_inches = (profile.feet * 12) + profile.inches
    height_m = total_inches * 0.0254

    if height_m > 0 and profile.weight_kg > 0:
        bmi = round(profile.weight_kg / (height_m ** 2), 2)

        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Normal"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

    if age and profile.gender:
        if profile.gender.lower() == "male":
            calories = int(10 * profile.weight_kg + 6.25 * (height_m*100) - 5 * age + 5)
        else:
            calories = int(10 * profile.weight_kg + 6.25 * (height_m*100) - 5 * age - 161)

    recommendations = []

    prompt = f"""
    User profile:
    Goal: {profile.goal}
    BMI: {bmi}
    BMI Status: {bmi_status}
    Calories Needed: {calories}
    Medical Conditions: {profile.medical_conditions}

    Give 3 short personalized daily health recommendations.
    Focus on meals, activity, and safety.
    """

    try:
        res = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a nutrition expert. Keep answers short and practical."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )

        data = res.json()

        if "choices" in data:
            text = data["choices"][0]["message"]["content"]
            recommendations = [
                line.replace("-", "").strip()
                for line in text.split("\n")
                if line.strip()
            ]
    except:
        recommendations = [
            "Eat balanced meals.",
            "Stay active daily.",
            "Drink enough water."
        ]

    today = date.today()

    water, created = WaterIntake.objects.get_or_create(
        user=request.user,
        date=today
    )

    if request.method == "POST" and "add_water" in request.POST:
        water.glasses += 1
        water.save()

    steps_obj, created = DailySteps.objects.get_or_create(
    user=request.user,
    date=today
    )

    if request.method == "POST" and "save_steps" in request.POST:
        try:
            entered_steps = int(request.POST.get("steps", 0))
            if entered_steps >= 0:
                steps_obj.steps = entered_steps
                steps_obj.save()
        except:
            pass

    calories_burned = int(steps_obj.steps * 0.04)
    water_percent = min(int((profile.water_glasses / 8) * 100), 100)
    steps_percent = min(int((profile.steps / 10000) * 100), 100)
    sleep_percent = min(int((profile.sleep_hours / 8) * 100), 100)

    target = get_personal_target(request.user)

    context = {
        "form": form,
        "age": age,
        "bmi": bmi,
        "bmi_status": bmi_status,
        "calories": calories,
        "recommendations": recommendations,
        "water_glasses": water.glasses,
        "profile": profile,
        "water_percent": water_percent,
        "sleep_percent": sleep_percent,
        "steps": steps_obj.steps,
        "steps_percent": steps_percent,
        "recommended_target": target,
        "calories_burned": calories_burned,
    }

    return render(request, "account.html", context)

@login_required
def report(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_report.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, y, "Calomate Health Report")

    y -= 50
    p.setFont("Helvetica", 12)

    p.drawString(50, y, f"Username: {request.user.username}")
    y -= 25
    p.drawString(50, y, f"City: {profile.city}")

    y -= 25
    p.drawString(50, y, f"Height: {profile.feet} ft {profile.inches} in")

    y -= 25
    p.drawString(50, y, f"Weight: {profile.weight_kg} kg")

    y -= 25
    p.drawString(50, y, f"Gender: {profile.gender}")

    y -= 25
    p.drawString(50, y, f"Goal: {profile.goal}")

    y -= 25
    p.drawString(50, y, f"Target Weight: {profile.target_weight}")

    y -= 25
    p.drawString(50, y, f"Medical Conditions: {profile.medical_conditions}")

    y -= 50
    p.drawString(50, y, "Generated by Calomate")

    p.showPage()
    p.save()

    return response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})