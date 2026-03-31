from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    MEAL_TYPES=[('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner')]
    meal_type=models.CharField(max_length=20,choices=MEAL_TYPES,default='breakfast')

    def total_calories(self):
        return self.food.calories * self.quantity