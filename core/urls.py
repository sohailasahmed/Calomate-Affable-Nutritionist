
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static

from users.views import register, account, report
from chatbot.views import chat

# Temporary keep current home view import
from .views import home


# Public Landing Page
def about(request):
    return render(request, 'about.html')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Public
    path('', about, name='about'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

    # Private Pages
    path('home/', home, name='home'),
    path('account/', account, name='account'),
    path('report/', report, name='report'),

    # Apps
    path('diet/', include('diet.urls')),
    path('chat/', chat, name='chat'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)