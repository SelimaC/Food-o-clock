from django.contrib.auth.decorators import login_required
from fuzzywuzzy import fuzz
from django.shortcuts import render
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe
from foodoclock.models.MealType import MealType
from foodoclock.models.Cuisine import Cuisine
from foodoclock.models.Diet import Diet
from foodoclock.models.UserDetails import UserDetails
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from foodoclock.models.Ingredient import Ingredient
from foodoclock.models.TitleToken import TitleToken
import re
from inflection import singularize
import unidecode
from textblob import TextBlob
from operator import attrgetter

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

foodfile = open("basicfood.txt", "r")
allow = foodfile.read().split('\n')
foodfile.close()

with open("stopfoodwords.txt", "r", encoding='utf-8', errors='ignore') as foodfiles:
    stopWords = foodfiles.read().split('\n')
    foodfiles.close()

with open("stopfoods10.txt", "r", encoding='utf-8',errors='ignore') as file:
    stopfoods = file.read().split('\n')
    file.close()

stopWords = set(stopWords)

tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for ss in stopfoods:
    stopWords.add(ss)


@login_required
def home(request):

    # Retrieve user preferences
    user_data = UserDetails.getDetailByUser(request.user)

    # Data to populate advanced filters
    cuisines = Cuisine.objects.all()
    meals = MealType.objects.all()
    diets = Diet.objects.all()
    sort_options = [('Sort by', True), ('Title', False), ('Time',False), ('Rating', False)]

    # Filtering
    filter = {}
    cuisine_filters = []
    diet_filters = []
    meal_filters = []

    if 'cuisine' in request.POST:
        filter['cuisine'] = request.POST.getlist('cuisine')
        cuisine_filters = filter['cuisine']
    if 'meal' in request.POST:
        filter['meal'] = request.POST.getlist('meal')
        meal_filters = filter['meal']
    if 'diet' in request.POST:
        filter['diet'] = request.POST.getlist('diet')
        diet_filters = filter['diet']
    if not request.POST:
        if 'cuisine' in request.GET and len(eval(request.GET.get('cuisine')))>0:
            filter['cuisine'] = eval(request.GET.get('cuisine'))
            cuisine_filters = filter['cuisine']
        if 'meal' in request.GET and len(eval(request.GET.get('meal')))>0:
            filter['meal'] = eval(request.GET.get('meal'))
            meal_filters = filter['meal']
        if 'diet' in request.GET and len(eval(request.GET.get('diet')))>0:
            filter['diet'] = eval(request.GET.get('diet'))
            diet_filters = filter['diet']

    # Search query has been performed
    query = ""

    # Get all recipes

    if 'query' in request.POST or 'q' in request.GET:
        if request.POST and request.POST['query']:
            query = request.POST['query']
        elif request.GET and request.GET.get('q'):
            query = request.GET.get('q')
             
    parsed_query = query_parser(query)

    recipes = retrieve_results(parsed_query, filter)

    # Rank results
    recipes = rank_results(recipes, user_data, parsed_query)

    sort = request.POST.get('sort', None)
    if 's' in request.GET:
        sort = request.GET.get('s')
    if sort is not None:
        recipes=sort_results(recipes, sort)
        if sort == 'Title':
            sort_options = [('Sort by', False), ('Title', True), ('Time', False), ('Rating', False)]
        if sort == 'Sort by':
            sort_options = [('Sort by', True), ('Title', False), ('Time', False), ('Rating', False)]
        if sort == 'Rating':
            sort_options = [('Sort by', False), ('Title', False), ('Time', False), ('Rating', True)]
        if sort == 'Time':
            sort_options = [('Sort by', False), ('Title', False), ('Time', True), ('Rating', False)]

    # Prepare some data to be displayed in search results
    for r in recipes:
        r.ingredients_display = eval(r.ingredients_list)
        r.rating_display = int(r.rating)
        if len(r.meta_description.split()) > 50:
            r.meta_description = ' '.join(r.meta_description.split()[0:50]) + ' ...'
    total = len(recipes)

    # Prepare paginator for search results
    paginator = Paginator(recipes, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    rows = paginator.get_page(page)

    # Render results
    return render(request, '../templates/home.html',
                      {'page': 1, 'rows': rows, 'total': total, 'sort': sort_options, 'cuisine': cuisines,
                       'meals': meals, 'diets': diets, 'query': query, 'sort_selected': sort,
                       'filter_cuisine': cuisine_filters, 'filter_diet': diet_filters,
                       'filter_meal': meal_filters})

# Parse user query
def query_parser(query_string):
    query = {}
    query['ingredients'] = []
    query['title'] = ""
    query['title_tokens'] = []
    if query_string == '':
        return query

    first_plus = query_string.find("+")
    first_minus = query_string.find("-")
    if first_minus != -1 and first_plus != -1:
        end_title = min(first_minus, first_plus)
    elif first_minus != -1:
        end_title = first_minus
    else:
        end_title = first_plus

    if end_title == -1:
        query["title"] = query_string
    elif end_title != 0 :
        query["title"] = query_string[0:end_title-1]

    tokens = pos_tag(word_tokenize(query['title']))
    for t in tokens:
        if t[0] != "":
            if t[1].startswith('N') or t[1].startswith('V') or t[1].startswith('J') or t[1].startswith('R'):
                query['title_tokens'].append(singularize(t[0].lower()))

    if end_title == -1:
        return query

    parts_plus = re.findall(r'\+[a-zA-Z ]*', query_string[end_title:])
    parts_minus = re.findall(r'\-[a-zA-Z ]*', query_string[end_title:])
    ingredients = []

    for p in parts_plus:
        i = p.split('+')
        ingredients.append((True, i[1]))
    for p in parts_minus:
        i = p.split('-')
        ingredients.append((False, i[1]))
    query['ingredients'] = standardize(ingredients)

    return query


# Standardize query ingredients
def standardize(ingredients):
    recipe = []
    for flag, ing in ingredients:
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
            recipe.append((flag,temp))

    return recipe

# Retrieve results
def retrieve_results(query, filters):
    ingredients = []
    not_ingredients = []

    for i in query['ingredients']:
        if i[0]:
            ingredients.append(i[1])
        else:
            not_ingredients.append(i[1])

    ingredients_ids = {}
    for name in ingredients:
        ingredients_ids[name] = Ingredient.getIngredientsByName(name)

    not_ingredients_ids = {}
    for name in not_ingredients:
        not_ingredients_ids[name] = Ingredient.getIngredientsByName(name)

    print(len(ingredients_ids))
    print(len(not_ingredients_ids))
    passed = query

    passed['ingredients'] = ingredients_ids
    passed['not_ingredients'] = not_ingredients_ids

    token_ids = TitleToken.getTokensByNames(query['title_tokens'])

    passed['token_ids'] = token_ids
    if len(filters) != 0:
        for k,v in filters.items():
            passed[k] = v
    return Recipe.getRecipes(passed, ingredients_ids, not_ingredients_ids)


# Rank search results
def rank_results(recipes, user_details, query):
    tot_click = 0
    max_content_score = 0
    max_preference_score = 0

    print(len(recipes))
    for r in recipes:
        if user_details.diet and r.diet == user_details.diet:
            r.user_preference_score = 10
        else:
            r.user_preference_score = 0
        if user_details.cuisine and r.cuisine == user_details.cuisine:
            r.user_preference_score += 5
        else:
            r.user_preference_score = 0
        if query['title'] != "":
            sim = fuzz.ratio(r.title, query['title'])
            r.similarity_score = sim/100
        else:
            r.similarity_score = 0

        if r.similarity_score == 1:
            r.similarity_score *= 2

        r.content_score = r.similarity_score
        tot_click += r.click
        if r.content_score > max_content_score:
            max_content_score = r.content_score
        if r.user_preference_score > max_preference_score:
            max_preference_score = r.user_preference_score

    for r in recipes:
        if max_content_score > 0:
            r.content_score /= max_content_score
        if max_preference_score > 0:
            r.user_preference_score /= max_preference_score
        r.feedback_score = r.click / tot_click + r.rating/5
        r.rank_score = r.content_score + r.user_preference_score + r.feedback_score

    recipes = sorted(recipes, key=attrgetter('content_score', 'feedback_score', 'user_preference_score'), reverse=True)

    return recipes


# Sort search results
def sort_results(results, sort_option):

    if sort_option == 'Title':
        return sorted(results, key=attrgetter('title'))

    if sort_option == 'Time':
        return sorted(results, key=attrgetter('preparation_time, cook_time'))

    if sort_option == 'Rating':
        return sorted(results, key=attrgetter('rating'), reverse=True)

    return results


