import json
#import unicode
import nltk
import glob
import spacy
import keyboard
import random
import re
from inflection import pluralize
from textblob_aptagger import PerceptronTagger
import csv
import unidecode
from textblob import TextBlob
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))
print(type(stopWords))

stop = ['cups', 'cup', 'oz', 'pound', 'pounds', 'lb', 'x', 'garnish', 'garnishes', 'teaspoon', 'teaspoons', 'tablespoon', 'optional',
        'tablespoons', 'tsp', 'tbs','hard', 'medium', 'large', 'stick', 'package', 'container', 'dash', 'pinch', 'frozen','bunch', 'piece', 'pieces', 'skinless','boneless',
        'grated', 'drop', 'drops','quartered', 'half', 'halved','ounces', 'ounce','halves','delicious',
        'diameter','step','ml','*' 'recipe', 'strip', 'strips', 'inch', 'cms', 'inches', 'fresh', 'dry', 'thick', 'thin', 'slice', 'slices', 'c', 'sprigs',
        'jumbo', 'can','pkg','quarter','cloves','version','tbsp','additional', 'cans','tenders', 'small','plain' 'bottle', 'beating','bottles','glass', 'glasses', 'huge', 'chopped', 'bone-in', 'skin-on', 'chunks']

foodfile = open("your_file.txt", "r")
allow = foodfile.read().split('\n')

for word in allow:
    allow.append(pluralize(word))

with open('basicfood.txt', 'w') as f:
    for item in allow:
        if item == allow[-1]:
            f.write("%s" % item)
        else:
            f.write("%s\n" % item)
f.close()

tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']


for s in stop:
    stopWords.add(s)

traindata = []
filenames = glob.glob('D:\\metadata27638\\*.json')
random.shuffle(filenames)
nlp = spacy.load('en_core_web_sm')
for file in filenames:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FILE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~` \n")
    with open(file, "r",  encoding="utf8") as read_file:
        data = json.load(read_file)
        recipe = []
        for ing in data['ingredientLines']:
            temp = ''
            print(ing)
            #ing = '1 1/4 cups all-purpose flour (about 5 1/2 ounces)'
            ing = ing.lower()
            ing = unidecode.unidecode(ing)
            print("<<<<<")
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


            wi = TextBlob(ing)

            tagbag = wi.tags

            for pos in  tagbag:
                if (pos[1] in tags) or (pos[0] in allow):
                    if pos[0] not in stopWords:
                        temp = temp + " " + pos[0]
            temp = re.sub(r"^\s+", "", temp)
            temp = re.sub(r"\s+$", "", temp)
            #count = count + len(wi.noun_phrases)
            #print(temp)
            recipe.append(temp)
            #print("----------------------------")

        traindata.append(list(set(recipe)))



    keyboard.wait("enter")

    read_file.close()