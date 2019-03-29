from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from inflection import singularize

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
        print( wn.synsets(word, tag))
        return wn.synsets(word, tag)[0]
    except:
        return None


def title_similarity(phrase1, phrase2):

    phrase1 = pos_tag(word_tokenize(phrase1))
    phrase2 = pos_tag(word_tokenize(phrase2))

    synset1 = []
    synset2 = []

    for word in phrase1:
        syn = getsynset(*word)
        if syn:
            synset1.append(getsynset(*word))

    for word in phrase2:
        syn = getsynset(*word)
        if syn:
            synset2.append(getsynset(*word))

    score, count = 0.0, 0

    for synset in synset1:
        sym = [synset.path_similarity(ss) for ss in synset2]
        sym = [x for x in sym if x is not None]
        if len(sym) > 0:
            best_score = max([x for x in sym if x is not None])

            if best_score is not None:
                score = score + best_score
                count += 1

        # Average the values
    score /= count
    return score
'''
#Plug in the real query and title lists in the lists below.
'''
query = 'Mexican Corns on the Cob (Elote)'


titles = ['Chips corn with capers', 'potato roast', 'quinoa salad', 'veggie salad with roast potato skins']

scores = []
for title in titles:
    sim1 = title_similarity(title, query)
    sim2 = title_similarity(query, title)
    scores.append(float((sim1+sim2) / 2))

print(singularize('Corns'))



