from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from foodoclock.models.UserDetails import UserDetails


@login_required
def show(request):
    details = UserDetails.getDetailByUser(request.user)

    return render(request, '../templates/account_details.html',{'page': 2})
