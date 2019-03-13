from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from foodoclock.models.Wallet import Wallet


@login_required
def ajaxTransactions(request):
    wallet = Wallet.getWalletByUser(request.user)

    if request.GET['orderDesc'] == "true":
        desc = True
    else:
        desc = False

    transactions = wallet.getTransactions(desc)
    data = []
    for t in transactions:
        data.append({
            'code':             t.code,
            'date':             t.date.strftime("%b %d, %Y"),
            'amount':           t.amount.__str__(),
            'inputWallet':      t.inputWallet.code,
            'outputWallet':     t.outputWallet.code,
            'cryptoCurrency':    t.cryptoCurrency.__str__()
        })
    return JsonResponse({'transactions': data})
