from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from foodoclock.models.Wallet import Wallet


@login_required
def home(request):
    wallet = Wallet.getWalletByUser(request.user)
    total = wallet.getTotal()
    entries = wallet.getEntries()
    preferredCurrencyCode =  wallet.preferredCurrency.code;

    rows = []
    for e in entries:
        rows.append((e.cryptoCurrency.code + " - " + e.cryptoCurrency.name, e.amount))

    return render(request, '../templates/home.html', {'total': total, 'preferredCurrencyCode': preferredCurrencyCode, 'rows': rows})
