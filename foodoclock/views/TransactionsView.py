from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from foodoclock.models.Wallet import Wallet


@login_required
def transactions(request):
    wallet = Wallet.getWalletByUser(request.user)
    transactionslist = wallet.getTransactions()
    resList = []

    for t in transactionslist:
        formattedDate = t.date.strftime("%b %d, %Y")
        currTuple = t
        currTuple.date = formattedDate
        currTuple.amount = t.amount.__str__()
        resList.append(currTuple)
    existCC = False

    if len(wallet.getCryptoCurrencyList()) != 0:
        existCC = True

    return render(request, '../templates/transactions.html', {'rows': resList, 'existCC': existCC})
