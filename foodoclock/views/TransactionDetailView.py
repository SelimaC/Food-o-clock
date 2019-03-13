from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from foodoclock.models.Transaction import Transaction


@login_required
def transactionDetail(request, transactionCode):
    transaction = Transaction.objects.get(code=transactionCode)

    return render(request, '../templates/transactionDetail.html', {'transaction': transaction})
