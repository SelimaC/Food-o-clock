from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from foodoclock.models.Recipe import Recipe

@login_required
def home(request):

    recipes= Recipe.objects.all()
    total=len(recipes)
    sort_options=['Sort by', 'Title', 'Preparation time']
    for r in recipes:
        r.ingredients_list=r.ingredients.all()

    paginator = Paginator(recipes, 10)  # Show 10 contacts per page


    if request.POST:
        print(request.POST['term'])
        return render(request, '../templates/home.html', {'page': 1})
    else:
        page = request.GET.get('page')
        rows = paginator.get_page(page)
        return render(request, '../templates/home.html', {'page': 1,'rows': rows,'total':total, 'sort':sort_options})
