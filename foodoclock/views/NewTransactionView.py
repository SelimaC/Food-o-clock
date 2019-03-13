from django.contrib.auth.decorators import login_required

from foodoclock.forms.NewTransactionForm import NewTransactionForm
from foodoclock.models.Transaction import Transaction
from foodoclock.models.Wallet import Wallet
from django.shortcuts import redirect, render


@login_required
def newtransaction(request):
    failure = False
    wallet = Wallet.getWalletByUser(request.user)
    if request.method == 'POST':
        form = NewTransactionForm(request.POST)
        form.fields["outputWallet"].queryset = Wallet.objects.exclude(code=wallet.code)
        form.fields["cryptoCurrency"].queryset = wallet.getCryptoCurrencyList()
        if form.is_valid():
            outputWallet = form.cleaned_data.get('outputWallet')
            cryptocurrency = form.cleaned_data.get('cryptoCurrency')
            amount = form.cleaned_data.get('amount')

            result = Transaction.newTransaction(wallet, outputWallet, cryptocurrency, amount)

            if result:
                return redirect('transactions')
            else:
                failure = True

    else:
        form = NewTransactionForm()
        form.fields["outputWallet"].queryset = Wallet.objects.exclude(code=wallet.code)
        form.fields["cryptoCurrency"].queryset = wallet.getCryptoCurrencyList()
    return render(request, '../templates/newtransaction.html', {'form': form, 'failure': failure})
