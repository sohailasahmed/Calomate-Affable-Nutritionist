import csv
from diet.models import Food

with open('diet/foods_1000.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    added = 0

    for row in reader:
        name = row['name'].strip()
        calories = float(row['calories_per_100g'])

        obj, created = Food.objects.get_or_create(
            name=name,
            defaults={'calories_per_100g': calories}
        )

        if created:
            added += 1

print(f"{added} foods imported successfully")