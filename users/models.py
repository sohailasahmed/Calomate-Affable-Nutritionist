from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    city = models.CharField(max_length=100, blank=True)

    feet = models.IntegerField(default=5)
    inches = models.IntegerField(default=6)

    weight_kg = models.FloatField(default=60)

    dob = models.DateField(blank=True, null=True)

    gender = models.CharField(max_length=20, blank=True)

    goal = models.CharField(max_length=20, blank=True)

    target_weight = models.FloatField(blank=True, null=True)

    medical_conditions = models.TextField(blank=True)

    water_glasses = models.IntegerField(default=0)
    steps = models.IntegerField(default=0)
    sleep_hours = models.FloatField(default=0)

    last_tracker_reset = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    glasses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class DailySteps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.steps}"