from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render


@login_required
def list(request):

    return render(request, '../templates/favourites.html')
