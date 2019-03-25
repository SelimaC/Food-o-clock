import json
#import unicode
import nltk
import glob
import spacy
import keyboard
import random
import re
from inflection import singularize
import sklearn
import unidecode
from textblob import TextBlob
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))
print(type(stopWords))

stop = ['cups', 'striped','firm','whole','thumbsized','mediumsize','litre','liter','smallsize','largesize','light','bag','bags','tub','tubs','vegetable','sharp','ground','cup', 'oz', 'pound', 'pounds', 'lb', 'x', 'garnish', 'garnishes', 'teaspoon', 'teaspoons', 'tablespoon', 'optional','kg','gms','g','extra','warm','cold','lean','recipe','filling','*','precook','shredded','shred',
        'quart','tablespoons', 'tsp', 'tbs','hard', 'medium', 'large', 'stick', 'package', 'container', 'dash', 'pinch', 'frozen','bunch', 'piece', 'pieces', 'skinless','boneless','bar','premium','supreme','fatfree','doublecut','peeled','cap','petite','clove','cloves','handful',
        'grated', 'drop', 'drops','quartered', 'half', 'halved','ounces', 'ounce','halves','delicious','longgrain','t. ','splash','rotisserie','course','leaf','leaves','pinch','crispy','c.','coarse','jar','head','gr','fajitum', 'size','young','tip','partskim',
        'diameter','step','ml','*', 'recipe', 'strip', 'strips', 'inch', 'cms', 'inches', 'fresh', 'dry', 'thick', 'thin', 'slice', 'slices', 'c','sprig', 'sprigs','l','ltr','deep','frying','stalk','homemade','scoop','favourite','baby','goodquality','topping',
        'jumbo', 'can','pkg','quarter','cloves','version','tbsp','additional', 'cans','tenders', 'small','plain', 'bottle', 'beating','bottles','glass', 'glasses', 'huge', 'chopped','boneless','bonein', 'bone-in', 'skin-on','chunk', 'chunks']

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

output = []
traindata = []
trainlabel = []
unique = []
filenames = glob.glob('D:\\metadata27638\\*.json')
random.shuffle(filenames)
nlp = spacy.load('en_core_web_sm')
for file in filenames:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FILE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~` \n")
    with open(file, "r",  encoding="utf8") as read_file:
        data = json.load(read_file)
        trainlabel.append(data['attributes']['cuisine'][0])
        recipe = []
        for ing in data['ingredientLines']:
            temp = ''
            #print(ing)
            #ing = '1 1/4 cups all-purpose flour (about 5 1/2 ounces)'
            ing = ing.lower()
            ing = unidecode.unidecode(ing)

            ing = ing.split(" or ")[0]
            ing = re.sub(r" ?\([^)]+\)", " ", ing)
            ing = re.sub(r"([0-9]*-ounces)+", " ", ing)
            ing = re.sub(r"([0-9]*-ounce)+", " ", ing)
            ing = re.sub(r"([0-9]*-inches)+", " ", ing)
            ing = re.sub(r"([0-9]*-inch)+", " ", ing)
            ing = re.sub(r"([0-9]*)+", " ", ing)
            ing = re.sub(r"(-)+", " ", ing)
            ing = re.sub(r"(/)+", " ", ing)
            commasplit = re.split(r"\,", ing)
            ing = commasplit[0]
            ing = ing.replace("*", " ")
            ing = ing.replace("+", " ")
            ing = ing.replace("-", " ")
            ing = ing.replace(".", " ")
            ing = ing.replace(":", " ")
            ing = ing.replace("(", " ")
            ing = ing.split("http")[0]

            wi = TextBlob(ing)

            tagbag = wi.tags

            for pos in  tagbag:
                if (pos[1] in tags) or (singularize(pos[0]) in allow):
                    if singularize(pos[0]) not in stopWords:
                        temp = temp + " " + singularize(pos[0])
            temp = re.sub(r"^\s+", "", temp)
            temp = re.sub(r"\s+$", "", temp)
            print(temp)
            if temp == "":
                recipe.append(temp)
            #print("----------------------------")
        output.append({"cuisine": data["attributes"]["cuisine"][0], "ingredients": list(set(recipe))})
        #traindata.append(list(set(recipe)))

    read_file.close()

with open('output.json', 'w') as json_file:
    json.dump(output, json_file)
