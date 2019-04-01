import json
import numpy as np
import sklearn.feature_selection
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.naive_bayes import ComplementNB
from sklearn import svm
import keyboard
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

testrecipes = 4793

foodfile = open("select_ing.txt", "r")
ing = foodfile.read().split('\n')
foodfile.close()

cuisine = ['italian', 'british', 'southern', 'vietnamese', 'greek', 'french', 'southwestern', 'kid-friendly', 'hawaiian', 'asian', 'korean', 'japanese', 'thai', 'cuban', 'irish', 'brazilian', 'american', 'barbecue', 'cajun'
, 'russian', 'filipino', 'jamaican', 'german', 'hungarian', 'portuguese', 'indian', 'spanish', 'chinese', 'mediterranean', 'mexican', 'moroccan']

c.execute('UPDATE foodoclock_recipe SET cuisine_id = NULL WHERE cuisine_id not NULL')
conn.commit()

print("nulled")

c.execute('DELETE FROM foodoclock_cuisine')
conn.commit()

print("deleted")

for cus in cuisine:
    c.execute('INSERT INTO foodoclock_cuisine (cuisine) VALUES (?)', (cus.capitalize(),))
    conn.commit()

print("cuisine updated")

for i in ing:

    flag=True
    ids = c.execute('SELECT id FROM foodoclock_ingredient WHERE name = ?', (i,))

    if c.fetchone()!=None:
        flag=False

    if flag:
        try:
            sql = '''INSERT INTO foodoclock_ingredient (name) VALUES (?)'''
            c.execute(sql, (i,))
        except sqlite3.IntegrityError as e:
            print('sqlite error: ', e.args[0])  # column name is not unique
        conn.commit()

print("ingredients updated")


with open('traindata1.json', "r", encoding="utf8") as read_file:
    train1 = json.load(read_file)

with open('traindata2.json', "r", encoding="utf8") as read_file:
    train2 = json.load(read_file)

with open('testdata1.json', "r", encoding="utf8") as read_file:
    test1 = json.load(read_file)

with open('testdata2.json', "r", encoding="utf8") as read_file:
    test2 = json.load(read_file)


#ing = ing[0:3000]

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

#print(len(train))
#print(len(test))

'''
select_ing = []

mi = sklearn.feature_selection.mutual_info_classif(features, label, discrete_features=True)
mi_ing = list(range(len(ing)))

for i in mi_ing:
    if mi[i]>=0.002:
        select_ing.append(ing[i])

print(len(select_ing))

with open('select_ing1.txt', 'w', encoding="ISO-8859-1") as f:
    for item in select_ing:
        if item == select_ing[-1]:
            f.write("%s" % item)
        else:
            f.write("%s\n" % item)
f.close()

select_ing.clear()

for i in mi_ing:
    if mi[i]>=0.005:
        select_ing.append(ing[i])

print(len(select_ing))

with open('select_ing2.txt', 'w', encoding="ISO-8859-1") as f:
    for item in select_ing:
        if item == select_ing[-1]:
            f.write("%s" % item)
        else:
            f.write("%s\n" % item)
f.close()
'''
'''
plt.plot(mi_ing, mi)
plt.title("Mutual Information")
plt.xlabel("Ingredient Id")
plt.ylabel("MI Score")
plt.show()
'''

clf = svm.SVC(gamma = 'scale')
clf.fit(train, trainlabel)

print("fitted")

for i in range(1, testrecipes+1):
    feature_set = c.execute('SELECT name FROM foodoclock_ingredient WHERE id IN (SELECT ingredient_id FROM foodoclock_recipe_ingredients WHERE recipe_id = ?)', (i,))
    ing_id = c.fetchall()
    ings = list(np.reshape(ing_id, (-1)))
    f = np.zeros(len(ing))
    for j in ings:
        if j in ing:
            f[ing.index(j)] = 1
    f = np.reshape(f, (1,-1))
    ans = clf.predict(f)[0]
    del f
    ans = ans + 19 # 19 is the ID offset
    c.execute('UPDATE foodoclock_recipe SET cuisine_id = ? WHERE auto_increment_id = ?', (ans, i, ))
    conn.commit()

print("prediction done")

for i in range(1, testrecipes+1):

    c.execute('SELECT cuisine_id FROM foodoclock_recipe WHERE auto_increment_id = ?', (i,))
    id = c.fetchone()
    ch = int.from_bytes(id[0], byteorder='little')
    c.execute('UPDATE foodoclock_recipe SET cuisine_id = ? WHERE auto_increment_id = ?', (ch, i, ))
    conn.commit()

conn.close()
print("DONE")
'''
print("Accuracy:",clf.score(test, testlabel))

print("Precision:",metrics.precision_score(testlabel, y_pred))

print("Recall:",metrics.recall_score(testlabel, y_pred))
'''