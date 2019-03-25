from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe
from foodoclock.models.MealType import MealType
from foodoclock.models.Cuisine import Cuisine
from foodoclock.models.UserDetails import UserDetails
from inflection import singularize
import unidecode
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
tags = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'NNP', 'NNPS']
for s in stop:
    stopWords.add(s)

@login_required
def home(request):

    # Retrieve user preferences
    user_data = UserDetails.getDetailByUser(request.user)

    # Get all recipes
    recipes= Recipe.objects.all()
    total=len(recipes)
    sort_options = ['Sort by', 'Title', 'Preparation time']
    for r in recipes:
        r.ingredients_display=eval(r.ingredients_list)
        r.rating_display = int(r.rating)

    paginator = Paginator(recipes, 10)  # Show 10 contacts per page

    cuisines = Cuisine.objects.all()
    meals = MealType.objects.all()
    page = request.GET.get('page')
    rows = paginator.get_page(page)

    if request.POST: # search has been performed
        query = request.POST['query']
        return render(request, '../templates/home.html',
                      {'page': 1, 'rows': rows, 'total': total, 'sort': sort_options, 'cuisine': cuisines,
                       'meals': meals, 'query': query})

    else:
        return render(request, '../templates/home.html', {'page': 1, 'rows': rows, 'total': total,
                        'sort': sort_options, 'cuisine': cuisines,'meals': meals})


def query_parser(query):
    query['ingredients'] = []
    query['title'] = ""
    query['diet'] = []
    query['cuisine'] = ""
    query['meal_type'] = ""
    query['sort'] = ""

    return query


# Standardize a list of ingredients
def standardize(ingredients):
    recipe = []
    for ing in ingredients:
        temp = ''

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
        ing = ing.split(" or ")[0]
        ing = ing.split("http")[0]

        wi = TextBlob(ing)

        tagbag = wi.tags

        for pos in tagbag:
            if (pos[1] in tags) or (singularize(pos[0]) in allow):
                if pos[0] not in stopWords:
                    temp = temp + " " + singularize(pos[0])
        temp = re.sub(r"^\s+", "", temp)
        temp = re.sub(r"\s+$", "", temp)

        if temp != "":
            recipe.append(temp)

    return list(set(recipe))