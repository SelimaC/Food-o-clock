from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from foodoclock.models.UserDetails import UserDetails


@login_required
def home(request):
    details = UserDetails.getDetailByUser(request.user)

    return render(request, '../templates/home.html')
