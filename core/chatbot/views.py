import requests
from django.shortcuts import render

API_KEY = "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"

def chat(request):
    response_text = ""

    if request.method == "POST":
        user_input = request.POST.get("message")

        try:
            res = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a nutrition expert. Give safe, short answers."},
                        {"role": "user", "content": user_input}
                    ]
                }
            )

            data = res.json()

            # 🔍 DEBUG PRINT
            print("FULL RESPONSE:", data)

            # ✅ SAFE PARSE
            if "choices" in data:
                response_text = data["choices"][0]["message"]["content"]
            elif "error" in data:
                response_text = "API Error: " + data["error"]["message"]
            else:
                response_text = "Unexpected response from API"

        except Exception as e:
            response_text = "Error: " + str(e)

    return render(request, 'chatbot/chat.html', {'response': response_text})