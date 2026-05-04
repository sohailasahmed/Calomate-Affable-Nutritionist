
# 🥗 Calomate – AI-Powered Nutrition & Fitness Tracker

Calomate is a full-stack web application built with Django that helps users track their daily calorie intake, analyze eating habits, and receive intelligent diet suggestions. It combines meal logging, analytics, and an AI chatbot into a single platform to promote healthier lifestyle decisions.

---

## 🚀 Features

* 🔐 User Authentication (Register/Login/Logout)
* 🍽️ Meal Logging System (Add, Delete, Track Meals)
* 📊 Interactive Dashboard with real-time calorie tracking
* 📈 Analytics using charts (daily & weekly trends)
* 🤖 AI Chatbot for diet suggestions and Q&A
* 🌙 Dark Mode UI for better user experience
* 📱 Fully Responsive Design (Bootstrap)
* 🔒 Secure environment-based configuration
* ☁️ Deployment-ready (PostgreSQL + WhiteNoise + Gunicorn)

---

## 🛠️ Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Database

* SQLite (Development)
* PostgreSQL (Production)

### Tools & Libraries

* Chart.js
* Gunicorn
* WhiteNoise
* python-dotenv

### Deployment

* Render

---

## 📂 Project Structure

```
project_root/
│
├── core/                # Project settings & URLs
├── users/               # Authentication & profiles
├── diet/                # Meal management
├── home/                # Charts & insights
├── chatbot/             # AI assistant
│
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploads
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/calomate.git
cd calomate
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
API_KEY=your_api_key (Your AI chatbot API Key)
```

---

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Run Server

```bash
python manage.py runserver
```

👉 Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
gunicorn core.wsgi:application
```

---

## 🔐 Environment Variables

| Variable      | Description           |
| ------------- | --------------------- |
| SECRET_KEY    | Django secret key     |
| DEBUG         | Debug mode            |
| ALLOWED_HOSTS | Allowed domains       |
| DATABASE_URL  | PostgreSQL connection |
| API_KEY       | AI chatbot key        |

---

## 📊 Key Functionalities

### ✔ Meal Tracking

Users can log meals with calorie values and maintain daily records.

### ✔ Dashboard

Displays:

* Total calories
* Remaining calories
* Daily summary

### ✔ Analytics

* Visual charts for trends
* Helps understand eating habits

### ✔ AI Chatbot

* Answers health-related queries
* Provides diet suggestions

---

## 🧪 Testing

* Unit Testing (modules)
* Integration Testing (module interaction)
* System Testing (full app)
* UI Testing (responsiveness)

---

## 📈 Future Enhancements

* 📱 Mobile App (Android/iOS)
* ⌚ Wearable device integration
* 🧠 Advanced AI recommendations
* 🔔 Notifications & reminders
* 🌍 Multi-language support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Push and create PR

---

## 📜 License

This project is for educational purposes.

---

## 👨‍💻 Author

Sohail Ahmed
CSE (Software Engineering) Graduate
Let's Connect https://www.linkedin.com/in/sohailasahmed/

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share!

---

<!-- * I'll Add live link (after deployment) -->

* https://github.com/sohailasahmed/Calomate-Affable-Nutritionist
