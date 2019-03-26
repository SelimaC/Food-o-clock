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

print("done")
foodfile = open("basicfood.txt", "r")
allow = foodfile.read().split('\n')
foodfile.close()
print(allow)
file = open("stopfoods10.txt", "r")
stopfoods = file.read().split('\n')
file.close()

tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for ss in stopfoods:
    stopWords.add(ss)

for s in stopss:
    stopWords.add(s)

for s in stop:
    stopWords.add(s)

stopfoodwords=list(stopWords)
with open('stopfoodwords.txt', 'w') as f:
    for item in stopfoodwords:
        if item == stopfoodwords[-1]:
            f.write("%s" % item.lower())
        else:
            f.write("%s\n" % item.lower())
f.close()

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
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            #ing = ing.split(" or ")[0]
            ing = ing.split(" or ")[0]
            #ing = ing.split(" (")[0]
            ing = re.sub(r"[\(\[].*?[\)\]]", " ", ing)
            #print(ing)
            ing = re.sub(r"([0-9]*-ounces)+", " ", ing)
            #print(ing)
            ing = re.sub(r"([0-9]*-ounce)+", " ", ing)
            #print(ing)
            ing = re.sub(r"([0-9]*-inches)+", " ", ing)
            #print(ing)
            ing = re.sub(r"([0-9]*-inch)+", " ", ing)
            #print(ing)
            ing = re.sub(r"([0-9])+", " ", ing)
            #print(ing)
            ing = re.sub(r"(-)+", " ", ing)
            #print(ing)
            ing = re.sub(r"(/)+", " ", ing)
            #print(ing)
            ing = ing.split(",")[0]
            #print(ing)
            ing = ing.replace("*", " ")
            ing = ing.replace("%", " ")

            #print(ing)
            ing = ing.replace("+", " ")
            #print(ing)
            ing = ing.replace("-", " ")
            #print(ing)
            ing = ing.replace(".", " ")
            #print(ing)
            ing = ing.replace(":", " ")
            #print(ing)
            ing = ing.replace("(", " ")
            #print(ing)
            ing = ing.split("http")[0]
            #print(ing)
            #print("\n")

            #keyboard.wait("enter")

            wi = TextBlob(ing)
            tagbag = wi.tags

            for pos in  tagbag:
                if (pos[1] in tags) or (singularize(pos[0]) in allow):
                    if singularize(pos[0]) not in stopWords:

                        #print(singularize(pos[0]))
                        temp = temp + " " + singularize(pos[0])
            temp = temp.strip()
            #print("\n")
            #print(temp)
            #keyboard.wait("enter")
            if temp:
                #print("ooo")
                recipe.append(temp)
            #print("----------------------------")
        output.append({"cuisine": data["attributes"]["cuisine"][0], "ingredients": list(set(recipe))})
        #traindata.append(list(set(recipe)))

    read_file.close()

with open('yummlyfood.json', 'w') as json_file:
    json.dump(output, json_file)
