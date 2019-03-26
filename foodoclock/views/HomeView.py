from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe
from foodoclock.models.MealType import MealType
from foodoclock.models.Cuisine import Cuisine
from foodoclock.models.UserDetails import UserDetails
from django.http import JsonResponse
from foodoclock.models.Ingredient import Ingredient
from inflection import singularize
import unidecode
from django.core import serializers
import re
from textblob import TextBlob
from nltk.corpus import stopwords
import re
from inflection import singularize
import unidecode
from textblob import TextBlob

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


@login_required
def home(request):

    # Retrieve user preferences
    user_data = UserDetails.getDetailByUser(request.user)

    # Data to populate advanced filters
    cuisines = Cuisine.objects.all()
    meals = MealType.objects.all()
    sort_options = [('Sort by', True), ('Title', False), ('Time',False), ('Rating', False)]


    # Search query has been performed
    if 'query' in request.POST:
        if request.POST and request.POST['query']:
            query = request.POST['query']

            parsed_query = query_parser(query)
            recipes = retrieve_results(parsed_query)
        else:
            query = ""
            # Get all recipes
            recipes = Recipe.objects.all().order_by('?')
    else:
        query = ""
        # Get all recipes
        recipes = Recipe.objects.all().order_by('?')


    sort = request.POST.get('sort', None)
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

    filter_cuisine = request.POST.get('cuisine', None)
    if filter_cuisine is not None:
        pass
    filter_meal = request.POST.get('meal', None)
    if filter_meal is not None:
        pass
    filter_difficulty = request.POST.get('difficulty', None)
    if filter_difficulty is not None:
        pass

    # Prepare some data to be displayed in search results
    for r in recipes:
        r.ingredients_display = eval(r.ingredients_list)
        r.rating_display = int(r.rating)
    total = len(recipes)

    # Prepare paginator for search results
    paginator = Paginator(recipes, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    rows = paginator.get_page(page)

    # Render results
    return render(request, '../templates/home.html',
                      {'page': 1, 'rows': rows, 'total': total, 'sort': sort_options, 'cuisine': cuisines,
                       'meals': meals, 'query': query})


# Parse user query
def query_parser(query_string):
    query = {}
    query['ingredients'] = []
    query['title'] = ""
    query['diet'] = []
    query['cuisine'] = ""
    query['meal_type'] = ""
    query['sort'] = ""

    parts = query_string.split(' ')
    title = []
    ingredients = []
    for p in parts:
        if '+' in p:
            i = p.split('+')
            ingredients.append((True, i[1]))
        elif '-' in p:
            i = p.split('-')
            ingredients.append((False, i[1]))
        else:
            title.append(p)
    query['ingredients'] = standardize(ingredients)
    query['title'] = ' '.join(title)

    return query


def standardize(ingredients):
    recipe = []
    for flag,ing in ingredients:
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
            recipe.append((flag,temp))

    return recipe


# Retrieve results
def retrieve_results(filters):
    ingredients = []
    not_ingredients = []
    for i in filters['ingredients']:
        if i[0]:
            ingredients.append(i[1])
        else:
            not_ingredients.append(i[1])
    ingredients_ids = Ingredient.getIngredientsByNames(ingredients)
    not_ingredients_ids = Ingredient.getIngredientsByNames(not_ingredients)
    return Recipe.getRecipesMatchingIngredients(not_ingredients_ids,ingredients_ids)


def rank_results(results):
    pass


def sort_results(results, sort_option):

    if sort_option == 'Title':
        return results.order_by('title')

    if sort_option == 'Time':
        return results.extra(
            select={'fieldsum':'preparation_time + cook_time'},
            order_by=('fieldsum',)
        )

    if sort_option == 'Rating':
        return results.order_by('-rating')

    return results



def filter_results(results, filters):
    pass