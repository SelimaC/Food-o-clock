from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe
from foodoclock.models.MealType import MealType
from foodoclock.models.Cuisine import Cuisine
from foodoclock.models.UserDetails import UserDetails
from foodoclock.models.Ingredient import Ingredient
from inflection import singularize
import unidecode
from random import shuffle
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

@login_required
def home(request):

    # Retrieve user preferences
    user_data = UserDetails.getDetailByUser(request.user)

    # Data to populate advanced filters
    cuisines = Cuisine.objects.all()
    meals = MealType.objects.all()
    sort_options = ['Sort by', 'Title', 'Time', 'Rating']

    # Search query has been performed
    if request.POST and request.POST['query']:
        query = request.POST['query']

        parsed_query = query_parser(query)
        recipes = retrieve_results(parsed_query)

    else:
        query = ""
        # Get all recipes
        recipes = Recipe.objects.all().order_by('?')

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


def sort_results(results):
    pass


def filter_results(results, filters):
    pass