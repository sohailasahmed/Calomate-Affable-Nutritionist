import requests
from django.shortcuts import render
from diet.models import Meal
from users.models import UserProfile
from datetime import date
from django.contrib.auth.decorators import login_required
from django.conf import settings
from core.services import get_personal_target


API_KEY = settings.API_KEY
@login_required
def chat(request):
    response_text = ""

    if request.method == "POST":
        user_input = request.POST.get("message")

        # 🔥 STEP 1: Get user data
        if request.user.is_authenticated:
            today = date.today()
            meals = Meal.objects.filter(user=request.user, date=today)
            total_calories = sum(m.total_calories() for m in meals)

            # try:
            #     profile = UserProfile.objects.filter(user=request.user).first()


            #     if profile and profile.dob and profile.gender:
            #         age = today.year - profile.dob.year - (
            #             (today.month, today.day) < (profile.dob.month, profile.dob.day)
            #         )

            #         height_cm = ((profile.feet * 12) + profile.inches) * 2.54
            #         weight = profile.weight_kg

            #         if profile.gender.lower() == "male":
            #             calories_needed = int(10 * weight + 6.25 * height_cm - 5 * age + 5)
            #         else:
            #             calories_needed = int(10 * weight + 6.25 * height_cm - 5 * age - 161)

            #         # Goal adjustment
            #         if profile.goal == "loss":
            #                 calories_needed -= 300
            #         elif profile.goal == "gain":
            #                 calories_needed += 300

            # except:
            #     calories_needed = 2000
            
            target = get_personal_target(request.user)
            difference = target - total_calories
            # 🔥 STEP 2: LOCAL SMART LOGIC (faster + free)
            if any(word in user_input.lower() for word in ["eat", "recommend", "suggest", "suggestion"]):
                if difference > 300:
                    response_text = "You can have a full meal like rice, chicken, or roti with curry."
                elif difference > 0:
                    response_text = "You can have a light snack like fruits or nuts."
                else:
                    response_text = "You have exceeded your calories. Try lighter food or walk."

            elif "protein" in user_input:
                response_text = "Good protein sources: eggs, chicken, paneer, dal."

            elif "calories" in user_input and "my" in user_input:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                response_text = f"You consumed {total_calories} kcal today. Target is {int(target)} kcal."

            else:
                # 🔥 STEP 3: CALL API
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
                                {"role": "system", "content": "You are a nutrition expert. Give safe, short answers."},
                                {"role": "user", "content": user_input}
                            ]
                        }
                    )

                    data = res.json()

                    if "choices" in data:
                        response_text = data["choices"][0]["message"]["content"]
                    elif "error" in data:
                        response_text = "API Error: " + data["error"]["message"]
                    else:
                        response_text = "Unexpected response"

                except Exception as e:
                    response_text = "Error: " + str(e)

        else:
            response_text = "Please login to get personalized suggestions."

    return render(request, 'chatbot/chat.html', {'response': response_text})