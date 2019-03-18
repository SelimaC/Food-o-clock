from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cuisine import Cuisine

@login_required
def home(request):

    recipes= Recipe.objects.all()
    total=len(recipes)
    sort_options=['Sort by', 'Title', 'Preparation time']
    for r in recipes:
        r.ingredients_list=r.ingredients.all()

    paginator = Paginator(recipes, 10)  # Show 10 contacts per page

    cuisines=Cuisine.objects.all()
    meals=MealType.objects.all()
    page = request.GET.get('page')
    rows = paginator.get_page(page)


    if request.POST:
        term= request.POST['term']
        return render(request, '../templates/home.html',
                      {'page': 1, 'rows': rows, 'total': total, 'sort': sort_options, 'cuisine': cuisines,
                       'meals': meals, 'term':term})

    else:
        return render(request, '../templates/home.html', {'page': 1,'rows': rows,'total':total, 'sort':sort_options,'cuisine':cuisines,'meals':meals})
