import re
from inflection import singularize
import unidecode
from textblob import TextBlob
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import random
"""
stop = ['cups','nonfat','spicy','crushed','grated','food','cube','torn','big','small','pint','top','serve','thigh','shoulder','leg','breast','wing','fine','quality','gram','clove','box','nonstick','stick','non','link','use','brand','philadelphia','instant','ready','tasty','easy','link','bulk','huge',
        'old','heart','skirt','new','style','leaf','leafe','heavy', 'striped','firm','whole','thumbsized','mediumsize','litre','liter','smallsize','largesize','light','bag','bags','tub','tubs','vegetable','sharp','ground','cup', 'oz', 'pound', 'pounds', 'lb', 'x', 'garnish', 'garnishes', 'teaspoon', 'teaspoons', 'tablespoon', 'optional','kg','gms','g','extra','warm','cold','lean','recipe','filling','*','precook','shredded','shred',
        'quart','tablespoons', 'tsp', 'tbs','hard', 'medium', 'large', 'stick', 'package', 'section','block','fat-free','flat','cm','tb','season','tin','mexican','leftover','gm','part','skim','confectioner','squeeze','crunchy','raw','uncooked','ripe','choice','chef','professional','refrigerated',
        'container', 'dash', 'pinch', 'frozen','bunch', 'piece', 'pieces', 'skinless','boneless','bar','premium','supreme','fatfree','doublecut','peeled','cap','petite','clove','cloves','handful','good','market','shop','fat','free','envelope','secret','quick','fast','store','round','shape','organic','pod','blanched',
        'grated','skirt','drop', 'drops','quartered', 'half', 'halved','ounces', 'ounce','halves','delicious','longgrain','t','splash','rotisserie','course','leaf','leaves','pinch','crispy','coarse','jar','head','gr','fajitum', 'size','young','tip','partskim',
        'diameter','step','ml','boiling','tender','recipe', 'strip', 'strips', 'inch', 'cms', 'inches', 'fresh', 'dry', 'thick', 'thin', 'slice', 'slices', 'c','sprig', 'sprigs','l','ltr','deep','frying','stalk','homemade','scoop','favourite','baby','goodquality','topping',
        'jumbo', 'can','pkg','quarter','cloves','version','tbsp','additional', 'cans','tenders', 'small','plain', 'bottle', 'beating','bottles','glass', 'glasses', 'huge', 'chopped','boneless','bonein', 'bone-in', 'skin-on','chunk', 'chunks']

stopss=[]

stop=list(set(stop))

for s in stop:
    stopss.append(singularize(s))
"""
def simpletag(tag):

    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None

def getsynset(word, tag):
    tag = simpletag(tag)
    if tag is None:
        return None
    try:
        return wn.synsets(word, tag)[0]
    except:
        return None

print("done")
foodfile = open("basicfood.txt", "r")
allow = foodfile.read().split('\n')
foodfile.close()

foodfiles = open("stopfoodwords.txt", "r")
stopWords = foodfiles.read().split('\n')
foodfiles.close()

file = open("stopfoods10.txt", "r")
stopfoods = file.read().split('\n')
file.close()

stopWords = set(stopWords)

tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for ss in stopfoods:
    stopWords.add(ss)


ingredients_set = []
migration = []
token_set = []

# Standardize a list of ingredients
def standardize(ingredients):
    recipe = []
    for ing in ingredients:
        temp = ''

        ing = ing.lower()
        ing = unidecode.unidecode(ing)

        ing = ing.split(" or ")[0]
        ing = re.sub(r"[\(\[].*?[\)\]]", " ", ing)
        ing = re.sub(r"([0-9]*-ounces)+", " ", ing)
        ing = re.sub(r"([0-9]*-ounce)+", " ", ing)
        ing = re.sub(r"([0-9]*-inches)+", " ", ing)
        ing = re.sub(r"([0-9]*-inch)+", " ", ing)
        ing = re.sub(r"([0-9])+", " ", ing)
        ing = re.sub(r"(-)+", " ", ing)
        ing = re.sub(r"(/)+", " ", ing)
        ing = ing.split(",")[0]
        ing = ing.replace("*", " ")
        ing = ing.replace("%", " ")

        ing = ing.replace("+", " ")
        ing = ing.replace("-", " ")
        ing = ing.replace(".", " ")
        ing = ing.replace(":", " ")
        ing = ing.replace("(", " ")
        ing = ing.split("http")[0]

        wi = TextBlob(ing)
        tagbag = wi.tags

        for pos in tagbag:
            if (pos[1] in tags) or (singularize(pos[0]) in allow):
                if singularize(pos[0]) not in stopWords:

                    temp = temp + " " + singularize(pos[0])
        temp = temp.strip()

        if temp:
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
        recipe['ingredients_list'] = row[5]
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['meal_type'] = row[2]
        recipe['preparation_time'] = 0 if row[3] is None else int(row[3].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])

        recipe['tokens'] = []
        tokens = pos_tag(word_tokenize(recipe['title']))
        for t in tokens:
            if t[0]!="":
                if t[1].startswith('N') or t[1].startswith('V') or t[1].startswith('J') or t[1].startswith('R'):
                    recipe['tokens'].append(singularize(t[0].lower()))
                    token_set.append(singularize(t[0].lower()))

        flag = True
        for m in migration:
            if m['title'] == recipe['title'] or m['link'] == recipe['link']:
                flag = False
                break
        if flag:
            migration.append(recipe)

print("Diet table \n")
for row in c.execute('SELECT * FROM Diet'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['ingredients_list'] = row[5]
        recipe['title'] = row[0]
        recipe['cook_time'] = 0 if row[1] is None else int(row[1].split(' ')[0])
        recipe['diet'] = row[2]
        recipe['preparation_time'] = 0 if row[3] is None else int(row[3].split(' ')[0])
        recipe['corpus'] = row[4]
        recipe['link'] = row[6]
        recipe['meta_description'] = row[7]
        recipe['image_url'] = row[8]
        recipe['rating'] = 0 if row[9] is None else int(row[9])

        recipe['tokens'] = []
        tokens = pos_tag(word_tokenize(recipe['title']))
        for t in tokens:
            if t[0] != "":
                if t[1].startswith('N') or t[1].startswith('V') or t[1].startswith('J') or t[1].startswith('R'):
                    recipe['tokens'].append(singularize(t[0].lower()))
                    token_set.append(singularize(t[0].lower()))

        flag= True
        for m in migration:
            if m['title']==recipe['title'] or m['link']==recipe['link']:
                flag=False
                break
        if flag:
            migration.append(recipe)

print("Cuisine table \n")
for row in c.execute('SELECT * FROM Cusine'):
        text = eval(row[5])
        ingredients = standardize(text)


        recipe = {}
        recipe['ingredients_list'] = row[5]
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

        recipe['tokens'] = []
        tokens = pos_tag(word_tokenize(recipe['title']))
        for t in tokens:
            if t[0] != "":
                if t[1].startswith('N') or t[1].startswith('V') or t[1].startswith('J') or t[1].startswith('R'):
                    recipe['tokens'].append(singularize(t[0].lower()))
                    token_set.append(singularize(t[0].lower()))

        flag = True
        for m in migration:
            if m['title'] == recipe['title'] or m['link'] == recipe['link']:
                flag = False
                break
        if flag:
            migration.append(recipe)


print("Common dishes table \n")
for row in c.execute('SELECT * FROM Common_dish'):
        text = eval(row[5])
        ingredients = standardize(text)

        recipe = {}
        recipe['ingredients'] = ingredients
        recipe['ingredients_list'] = row[5]
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

        recipe['tokens'] = []
        tokens = pos_tag(word_tokenize(recipe['title']))
        for t in tokens:
            if t[0] != "":
                if t[1].startswith('N') or t[1].startswith('V') or t[1].startswith('J') or t[1].startswith('R'):
                    recipe['tokens'].append(singularize(t[0].lower()))
                    token_set.append(singularize(t[0].lower()))

        flag = True
        for m in migration:
            if m['title'] == recipe['title'] or m['link'] == recipe['link']:
                flag = False
                break
        if flag:
            migration.append(recipe)

conn.close()
print(len(migration))


diets = ['Diabetic Recipes', 'Gluten Free Recipes', 'Healthy Recipes', 'Low Calorie Recipes', 'Low Fat Recipes', 'Vegan Recipes', 'Vegetarian Recipes']
meals = ['Appetizers & Snacks Recipes', 'Breakfast & Brunch Recipes', 'Desserts Recipes', 'Dinner Recipes', 'Drinks Recipes']
cuisines = ['Indian Recipes', 'Asian Recipes', 'Italian Recipes', 'Mexican Recipes', 'Southern Recipes']


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

print("Saving ingredients")
print(len(ingredients_set))
ingredients_to_save = set(ingredients_set)
print(len(ingredients_to_save))
for ingredient in ingredients_to_save:
    try:
        sql = '''INSERT INTO foodoclock_ingredient (name) VALUES (?)'''
        c.execute(sql, (ingredient,))
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])  # column name is not unique
    conn.commit()

print("Saving tokens")
print(len(token_set))
token_to_save = set(token_set)
print(len(token_to_save))
for token in token_to_save:
    flag = True
    ids = c.execute('SELECT id FROM foodoclock_titletoken WHERE token = ?', (token,))

    if c.fetchone() != None:
        flag = False

    if flag:
        try:
            sql = '''INSERT INTO foodoclock_titletoken (token) VALUES (?)'''
            c.execute(sql, (token,))
        except sqlite3.IntegrityError as e:
            print('sqlite error: ', e.args[0])  # column name is not unique
        conn.commit()

#Recover ids
cuisine_ids={}
for cuisine in cuisines:
    ids=c.execute('SELECT id FROM foodoclock_cuisine WHERE cuisine =?', (cuisine,))
    for i in ids:
        id = i
    cuisine_ids[cuisine] = id[0]


meals_ids = {}
for meal in meals:
    ids = c.execute('SELECT id FROM foodoclock_mealtype WHERE type =?', (meal,))
    for i in ids:
        id = i
    meals_ids[meal] = id[0]

diets_ids = {}
for diet in diets:
    ids = c.execute('SELECT id FROM foodoclock_diet WHERE diet =?', (diet,))
    for i in ids:
        id = i
    diets_ids[diet] = id[0]

if True:
    for r in migration:
        if 'diet' in r:
            diet=diets_ids[r['diet']]
        else:
            diet=None
        if 'cuisine' in r:
            cuisine=cuisine_ids[r['cuisine']]
        else:
            cuisine=None
        if 'meal_type' in r:
            meal=meals_ids[r['meal_type']]
        else:
            meal=None

        recipe=(r['title'], r['link'], r['corpus'], r['meta_description'], r['preparation_time'],
                cuisine, diet, meal, 0, r['image_url'], r['cook_time'], r['rating'])
        try:
            sql = '''INSERT INTO foodoclock_recipe (title,link,corpus,meta_description,preparation_time,cuisine_id,diet_id,meal_type_id,click,image_url,cook_time,rating, ingredients_list) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            c.execute(sql, (r['title'], r['link'], r['corpus'], r['meta_description'], r['preparation_time'],
                cuisine, diet, meal, random.randint(1,20001), r['image_url'], r['cook_time'], r['rating'], r['ingredients_list']))
        except sqlite3.IntegrityError as e:
            print('sqlite error: ', e.args[0])  # column name is not unique
        conn.commit()


# Ingredient binding
if True:
    for r in migration:
        print(r['title'])
        for i in r['ingredients']:
            print(i)
            recipe_ids = c.execute('SELECT auto_increment_id FROM foodoclock_recipe WHERE title = ? AND ingredients_list=? AND link=?' , (r['title'],r['ingredients_list'],r['link'] ,))
            for id in recipe_ids:
                r_id=id
            ing_id = c.execute('SELECT id FROM foodoclock_ingredient WHERE name = ?' , (i,))
            for id in ing_id:
                i_id=id
            print(r_id)
            print(i_id)
            try:
                sql = '''INSERT INTO foodoclock_recipe_ingredients (recipe_id, ingredient_id) VALUES(?,?)'''
                c.execute(sql, ( r_id[0],i_id[0],))
            except sqlite3.IntegrityError as e:
                print('sqlite error: ', e.args[0])  # column name is not unique
            #keyboard.wait("enter")
            conn.commit()



# Token binding
if True:
    for r in migration:
        print(r['title'])
        for i in r['tokens']:
            print(i)
            recipe_ids = c.execute('SELECT auto_increment_id FROM foodoclock_recipe WHERE title = ? AND link=?' , (r['title'],r['link'] ,))
            for id in recipe_ids:
                r_id=id
            token_ids = c.execute('SELECT id FROM foodoclock_titletoken WHERE token = ?' , (i,))
            for id in token_ids:
                t_id=id
            print(r_id)
            print(t_id)
            try:
                sql = '''INSERT INTO foodoclock_recipe_title_tokens (recipe_id, titletoken_id) VALUES(?,?)'''
                c.execute(sql, ( r_id[0],t_id[0],))
            except sqlite3.IntegrityError as e:
                print('sqlite error: ', e.args[0])  # column name is not unique
            #keyboard.wait("enter")
            conn.commit()


conn.close()

print('done')
