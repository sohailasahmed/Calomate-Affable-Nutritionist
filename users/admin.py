from django.contrib import admin
from .models import UserProfile, WaterIntake, DailySteps

admin.site.register(UserProfile)
admin.site.register(WaterIntake)
admin.site.register(DailySteps)