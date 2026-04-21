from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories_per_100g = models.FloatField(default=100)

    def __str__(self):
        return self.name


class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.FloatField(default=100)

    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES,
        default='breakfast'
    )

    date = models.DateField(auto_now_add=True)

    def total_calories(self):
        return round(
            (self.food.calories_per_100g * self.quantity) / 100, 2
        )

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"