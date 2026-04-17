from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def account(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
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

    context = {
        "form": form,
        "age": age,
        "bmi": bmi,
        "bmi_status": bmi_status,
        "calories": calories,
    }

    return render(request, "account.html", context)

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