import json
import numpy as np
import sklearn.feature_selection
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import metrics

cuisine = ['italian', 'british', 'southern', 'vietnamese', 'greek', 'french', 'southwestern', 'kid-friendly', 'hawaiian', 'asian', 'korean', 'japanese', 'thai', 'cuban', 'irish', 'brazilian', 'american', 'barbecue', 'cajun'
, 'russian', 'filipino', 'jamaican', 'german', 'hungarian', 'portuguese', 'indian', 'spanish', 'chinese', 'mediterranean', 'mexican', 'moroccan']

with open('traindata1.json', "r", encoding="utf8") as read_file:
    train1 = json.load(read_file)

with open('traindata2.json', "r", encoding="utf8") as read_file:
    train2 = json.load(read_file)

with open('testdata1.json', "r", encoding="utf8") as read_file:
    test1 = json.load(read_file)

with open('testdata2.json', "r", encoding="utf8") as read_file:
    test2 = json.load(read_file)


foodfile = open("ingredients.txt", "r")
ing = foodfile.read().split('\n')
foodfile.close()

#ing = ing[0:3000]

print(len(train1))
print(len(train2))
print(len(test1))
print(len(test2))
print(len(ing))
train = []
test = []
trainlabel =[]
testlabel = []
label = []
features = []

for i in range(len(train1)):
    f = np.zeros(len(ing))
    for j in train1[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    features.append(f)
    del f
    trainlabel.append(cuisine.index(train1[i]['cuisine']))
    label.append(cuisine.index(train1[i]['cuisine']))

del train1
print("done")

for i in range(len(train2)):
    f = np.zeros(len(ing))
    for j in train2[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    train.append(f)
    features.append(f)
    del f
    trainlabel.append(cuisine.index(train2[i]['cuisine']))
    label.append(cuisine.index(train2[i]['cuisine']))

del train2
print("done")


for i in range(len(test1)):
    f = np.zeros(len(ing))
    for j in test1[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    test.append(f)
    features.append(f)
    del f
    testlabel.append(cuisine.index(test1[i]['cuisine']))
    label.append(cuisine.index(test1[i]['cuisine']))

del test1
print("done")

for i in range(len(test2)):
    f = np.zeros(len(ing))
    for j in test2[i]['ingredients']:
        if j in ing:
            f[ing.index(j)] = 1
    test.append(f)
    features.append(f)
    del f
    testlabel.append(cuisine.index(test2[i]['cuisine']))
    label.append(cuisine.index(test2[i]['cuisine']))

del test2
print("done")

print(len(train))
print(len(test))


mi = sklearn.feature_selection.mutual_info_classif(features, label, discrete_features=True)
mi_ing = list(range(len(ing)))

plt.plot(mi_ing, mi)
plt.title("Mutual Information")
plt.xlabel("Ingredient Id")
plt.ylabel("MI Score")
plt.show()

clf = svm.SVC(kernel='linear')

clf.fit(train, trainlabel)
y_pred = clf.predict(test)


print("Accuracy:",metrics.accuracy_score(testlabel, y_pred))

print("Precision:",metrics.precision_score(testlabel, y_pred))

print("Recall:",metrics.recall_score(testlabel, y_pred))
