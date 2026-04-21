from diet.models import Food

foods = [
# India
("Rice",130),("Roti",297),("Dal",116),("Paneer",265),("Biryani",290),
("Idli",58),("Dosa",168),("Poha",130),("Upma",150),("Samosa",262),

# Pakistan / Middle East
("Kebab",294),("Shawarma",250),("Falafel",333),("Hummus",166),

# China / Japan
("Noodles",138),("Fried Rice",163),("Dumplings",190),("Sushi",143),("Ramen",436),

# Europe
("Pizza",266),("Pasta",131),("Croissant",406),("Lasagna",135),

# USA
("Burger",295),("Sandwich",250),("French Fries",312),("Pancakes",227),

# Africa
("Jollof Rice",180),("Couscous",112),("Injera",166),

# Healthy
("Boiled Egg",155),("Banana",89),("Apple",52),("Milk",42),
("Chicken Breast",165),("Oats",389),("Salad",50),("Soup",70),

# Drinks
("Tea",2),("Coffee",5),("Orange Juice",45)
]

for name, cal in foods:
    Food.objects.get_or_create(
        name=name,
        defaults={'calories_per_100g': cal}
    )

print("Clean foods imported")