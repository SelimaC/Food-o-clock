from inflection import singularize
import unidecode
import re
from textblob import TextBlob
from nltk.corpus import stopwords


stopWords = set(stopwords.words('english'))

stop = ['cups', 'cup', 'oz', 'pound', 'pounds', 'lb', 'x', 'garnish', 'garnishes', 'teaspoon', 'teaspoons', 'tablespoon', 'optional',
        'tablespoons', 'tsp', 'tbs','hard', 'medium', 'large', 'stick', 'package', 'container', 'dash', 'pinch', 'frozen','bunch', 'piece', 'pieces', 'skinless','boneless',
        'grated', 'drop', 'drops','quartered', 'half', 'halved','ounces', 'ounce','halves','delicious',
        'diameter','step','ml','*' 'recipe', 'strip', 'strips', 'inch', 'cms', 'inches', 'fresh', 'dry', 'thick', 'thin', 'slice', 'slices', 'c', 'sprigs',
        'jumbo', 'can','pkg','quarter','cloves','version','tbsp','additional', 'cans','tenders', 'small','plain' 'bottle', 'beating','bottles','glass', 'glasses', 'huge', 'chopped', 'bone-in', 'skin-on', 'chunks']

foodfile = open("basicfood.txt", "r")
allow = foodfile.read().split('\n')
foodfile.close()

file = open("stopfoods10.txt", "r")
stopfoods = file.read().split('\n')
file.close()

tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for ss in stopfoods:
    stopWords.add(ss)

for s in stop:
    stopWords.add(s)

# Standardize a list of ingredients
def standardize(ingredients):
    recipe = []
    for flag,ing in ingredients:
        temp = ''
        # print(ing)
        # ing = '1 1/4 cups all-purpose flour (about 5 1/2 ounces)'
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
        ing = ing.replace("*", "")
        ing = ing.replace("+", "")
        ing = ing.replace("-", "")
        ing = ing.replace(".", "")
        ing = ing.replace(":", "")
        ing = ing.replace("(", "")
        ing = ing.split("http")[0]

        wi = TextBlob(ing)

        tagbag = wi.tags

        for pos in tagbag:
            if (pos[1] in tags) or (singularize(pos[0]) in allow):
                if singularize(pos[0]) not in stopWords:
                    temp = temp + " " + singularize(pos[0])
        temp = re.sub(r"^\s+", "", temp)
        temp = re.sub(r"\s+$", "", temp)

        if temp != "":
            recipe.append((flag,temp))

    return recipe

query='Potato salad +salmon -onions'
parts = query.split(' ')
ingredients = []
title = []
for p in parts:
    if '+' in p:
        i = p.split('+')
        ingredients.append((True, i[1]))
    elif '-' in p:
        i = p.split('-')
        ingredients.append((False, i[1]))
    else:
        title.append(p)
for i in ingredients:
    print(str(i[0]) +  " " + str(i[1]))
ingredients=standardize(ingredients)
for i in ingredients:
    print(str(i[0]) +  " " + str(i[1]))

print(' '.join(title))