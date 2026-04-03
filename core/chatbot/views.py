import requests
from django.shortcuts import render
from diet.models import Meal
from users.models import Profile
from datetime import date
from django.contrib.auth.decorators import login_required
from django.conf import settings

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

            try:
                profile = Profile.objects.get(user=request.user)
                calories_needed = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5

                if profile.goal == 'loss':
                    calories_needed -= 300
                elif profile.goal == 'gain':
                    calories_needed += 300

            except:
                calories_needed = 2000

            difference = calories_needed - total_calories

            # 🔥 STEP 2: LOCAL SMART LOGIC (faster + free)
            if "eat" in user_input.lower():
                if difference > 300:
                    response_text = "You can have a full meal like rice, chicken, or roti with curry."
                elif difference > 0:
                    response_text = "You can have a light snack like fruits or nuts."
                else:
                    response_text = "You have exceeded your calories. Try lighter food or walk."

            elif "calorie" in user_input.lower():
                response_text = f"You consumed {total_calories} kcal today. Target is {int(calories_needed)} kcal."

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