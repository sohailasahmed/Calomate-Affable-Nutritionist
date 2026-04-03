from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()   # in kg
    height = models.FloatField()   # in cm

    GOALS = [
        ('loss', 'Weight Loss'),
        ('maintain', 'Maintain'),
        ('gain', 'Weight Gain'),
    ]
    goal = models.CharField(max_length=20, choices=GOALS)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)