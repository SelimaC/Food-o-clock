import pandas as pd
import numpy as np
import json
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.naive_bayes import ComplementNB
from sklearn import svm
import re
import matplotlib.pyplot as plt
from inflection import singularize
import sklearn
import unidecode
from textblob import TextBlob
#from nltk.corpus import stopwords

foodfile = open("ingredients.txt", "r")
ing = foodfile.read().split('\n')
foodfile.close()


cuisine = ['italian', 'british', 'southern', 'vietnamese', 'greek', 'french', 'southwestern', 'kid-friendly', 'hawaiian', 'asian', 'korean', 'japanese', 'thai', 'cuban', 'irish', 'brazilian', 'american', 'barbecue', 'cajun'
, 'russian', 'filipino', 'jamaican', 'german', 'hungarian', 'portuguese', 'indian', 'spanish', 'chinese', 'mediterranean', 'mexican', 'moroccan']



'''
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

def stan(ing):
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

    return temp

print("start")
data = pd.read_csv("Classification Testing.csv", encoding = "ISO-8859-1") #ISO-8859-1
print(len(data))
testdata = []
testlabel = []
for i in range(len(data)):
    feature = np.zeros(len(ing))
    data['cuisine'][i] = data['cuisine'][i].lower()
    if data['cuisine'][i] == 'vietnamese':
        data['cuisine'][i] = 'asian'
    if data['cuisine'][i] == 'asian recipes':
        data['cuisine'][i] = 'asian'
    if data['cuisine'][i] == 'italian recipes':
        data['cuisine'][i] = 'italian'
    if data['cuisine'][i] == 'southern recipes':
        data['cuisine'][i] = 'southern'
    if data['cuisine'][i] == 'indian recipes':
        data['cuisine'][i] = 'indian'
    if data['cuisine'][i] == 'mexican recipes':
        data['cuisine'][i] = 'mexican'
    if data['cuisine'][i] == 'caribbean':
        data['cuisine'][i] = 'hawaiian'
    if data['cuisine'][i] == 'turkish':
        data['cuisine'][i] = 'mediterranean'


    testlabel.append(cuisine.index(data['cuisine'][i]))
    ing_bag = eval(data['ingredients'][i])
    for tokens in ing_bag:
        fixed = stan(tokens)
        if fixed:
            if fixed in ing:
                feature[ing.index(fixed)] = 1
    testdata.append(feature)
    del feature


del data
'''
print("test features done")
with open('traindata1.json', "r", encoding="utf8") as read_file:
    train1 = json.load(read_file)

with open('traindata2.json', "r", encoding="utf8") as read_file:
    train2 = json.load(read_file)

with open('testdata1.json', "r", encoding="utf8") as read_file:
    test1 = json.load(read_file)

with open('testdata2.json', "r", encoding="utf8") as read_file:
    test2 = json.load(read_file)


train = []
trainlabel =[]
label = []
features = []

for i in range(len(train1)):
    f = np.zeros(len(ing))
    for j in train1[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    #features.append(f)
    del f
    trainlabel.append(cuisine.index(train1[i]['cuisine']))
    #label.append(cuisine.index(train1[i]['cuisine']))

del train1
print("done")

for i in range(len(train2)):
    f = np.zeros(len(ing))
    for j in train2[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    #features.append(f)
    del f
    trainlabel.append(cuisine.index(train2[i]['cuisine']))
    #label.append(cuisine.index(train2[i]['cuisine']))

del train2
print("done")


for i in range(len(test1)):
    f = np.zeros(len(ing))
    for j in test1[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    #features.append(f)
    del f
    trainlabel.append(cuisine.index(test1[i]['cuisine']))
    #label.append(cuisine.index(test1[i]['cuisine']))

del test1
print("done")

for i in range(len(test2)):
    f = np.zeros(len(ing))
    for j in test2[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    #features.append(f)
    del f
    trainlabel.append(cuisine.index(test2[i]['cuisine']))
    #label.append(cuisine.index(test2[i]['cuisine']))

del test2
print("done")
var = []
comp = [4000, 3800, 3500, 3300, 3000, 2700, 2500, 2200,
        2000, 1900, 1700, 1500, 1300, 1000, 990, 950, 930, 900, 850, 830, 800, 760, 740, 700, 650, 600, 580, 550, 500]


pca = PCA(4000)
pca_full = pca.fit(train)
plt.plot(np.cumsum(pca_full.explained_variance_ratio_))
plt.xlabel('# of components')
plt.ylabel('Cumulative explained variance')
plt.show()
'''
clf = svm.SVC(gamma = 'scale')
clf.fit(train, trainlabel)
print("fitted")

ans = clf.predict(testdata)

print("Accuracy:",clf.score(testdata, testlabel))
'''