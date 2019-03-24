from inflection import singularize
import unidecode
import re
from textblob import TextBlob
from nltk.corpus import stopwords

ingredients_set = []
stopWords = set(stopwords.words('english'))

stop = ['cups', 'cup', 'oz', 'pound', 'pounds', 'lb', 'x', 'garnish', 'garnishes', 'teaspoon', 'teaspoons', 'tablespoon', 'optional',
        'tablespoons', 'tsp', 'tbs','hard', 'medium', 'large', 'stick', 'package', 'container', 'dash', 'pinch', 'frozen','bunch', 'piece', 'pieces', 'skinless','boneless',
        'grated', 'drop', 'drops','quartered', 'half', 'halved','ounces', 'ounce','halves','delicious',
        'diameter','step','ml','*' 'recipe', 'strip', 'strips', 'inch', 'cms', 'inches', 'fresh', 'dry', 'thick', 'thin', 'slice', 'slices', 'c', 'sprigs',
        'jumbo', 'can','pkg','quarter','cloves','version','tbsp','additional', 'cans','tenders', 'small','plain' 'bottle', 'beating','bottles','glass', 'glasses', 'huge', 'chopped', 'bone-in', 'skin-on', 'chunks']

foodfile = open("basicfood.txt", "r")
allow = foodfile.read().split('\n')
tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for s in stop:
    stopWords.add(s)

migration = []

# Standardize a list of ingredients
def standardize(ingredients):
    recipe = []
    for ing in ingredients:
        temp = ''

        ing = ing.lower()
        ing = unidecode.unidecode(ing)

        ing = ing.split(" or ")[0]
        ing = re.sub(r" ?\([^)]+\)", "", ing)
        ing = re.sub(r"([0-9]*-ounces)+", "", ing)
        ing = re.sub(r"([0-9]*-ounce)+", "", ing)
        ing = re.sub(r"([0-9]*-inches)+", "", ing)
        ing = re.sub(r"([0-9]*-inch)+", "", ing)
        ing = re.sub(r"([0-9]*)+", "", ing)
        ing = re.sub(r"(-)+", "", ing)
        ing = re.sub(r"(/)+", "", ing)
        commasplit = re.split(r"\,", ing)
        ing = commasplit[0]
        ing = ing.split(" or ")[0]
        ing = ing.split("http")[0]

        wi = TextBlob(ing)

        tagbag = wi.tags

        for pos in tagbag:
            if (pos[1] in tags) or (singularize(pos[0]) in allow):
                if pos[0] not in stopWords:
                    temp = temp + " " + singularize(pos[0])
        temp = re.sub(r"^\s+", "", temp)
        temp = re.sub(r"\s+$", "", temp)

        if temp != "":
            recipe.append(temp)
            ingredients_set.append(temp)


    return list(set(recipe))


import sqlite3
conn = sqlite3.connect('Recipes.db')
c = conn.cursor()



# Prepare the data for migration to website's database

print("Meal table \n")
for row in c.execute('SELECT * FROM Meal'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['meal_type'] = row[2]
        recipe['preparation_time'] = 0 if row[3] is None else int(row[3].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])

        migration.append(recipe)

print("Diet table \n")
for row in c.execute('SELECT * FROM Diet'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['diet'] = row[2]
        recipe['preparation_time'] = 0 if row[3] is None else int(row[3].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])

        migration.append(recipe)

print("Cuisine table \n")
for row in c.execute('SELECT * FROM Cusine'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['cuisine'] = row[3]
        recipe['preparation_time'] = 0 if row[2] is None else int(row[2].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])

        migration.append(recipe)


print("Common dishes table \n")
for row in c.execute('SELECT * FROM Common_dish'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['meal_type'] = row[2]
        recipe['preparation_time'] = 0 if row[3] is None else int(row[3].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])
        recipe['cuisine'] = row[10]

        migration.append(recipe)

conn.close()
print(len(migration))


diets = [] # ['Diabetic Recipes', 'Gluten Free Recipes', 'Healthy Recipes', 'Low Calorie Recipes', 'Low Fat Recipes', 'Vegan Recipes', 'Vegetarian Recipes']
meals = [] # ['Appetizers & Snacks Recipes', 'Breakfast & Brunch Recipes', 'Dessert Recipes', 'Dinner Recipes', 'Drink Recipes']
cuisines = [] # ['Indian Recipes', 'Asian Recipes', 'Italian Recipes', 'Mexican Recipes', 'Southern Recipes']


# Copy data to website database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
for cuisine in cuisines:
    print(cuisine)
    try:
        sql = '''INSERT INTO foodoclock_cuisine (cuisine) VALUES(?)'''
        c.execute(sql, (cuisine,))
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])  # column name is not unique
    conn.commit()

for meal in meals:
    try:
        sql = '''INSERT INTO foodoclock_mealtype (type) VALUES (?)'''
        c.execute(sql, (meal, ))
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])  # column name is not unique
    conn.commit()


for diet in diets:
    try:
        sql = '''INSERT INTO foodoclock_diet (diet) VALUES (?)'''
        c.execute(sql, (diet,))
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])  # column name is not unique
    conn.commit()


ingredients_to_save = set([x for x in ingredients_set if ingredients_set.count(x) > 1])
print(len(ingredients_to_save))
for ingredient in ingredients_to_save:
    try:
        sql = '''INSERT INTO foodoclock_ingredient (name) VALUES (?)'''
        c.execute(sql, (ingredient,))
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])  # column name is not unique
    conn.commit()

conn.close()

print('done')
