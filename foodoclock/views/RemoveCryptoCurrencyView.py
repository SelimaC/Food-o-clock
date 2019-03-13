from django.contrib.auth.decorators import login_required

from foodoclock.forms.EntryWalletForm import EntryWalletForm
from foodoclock.models.Wallet import Wallet
from django.shortcuts import redirect, render

@login_required
def remove(request):
    wallet = Wallet.getWalletByUser(request.user)
    if request.method == 'POST':
        form = EntryWalletForm(request.POST)
        form.fields["cryptoCurrency"].queryset = wallet.getCryptoCurrencyList()
        if form.is_valid():
            cryptoCurrency = form.cleaned_data.get('cryptoCurrency')
            amount = form.cleaned_data.get('amount')

            wallet.removeCryptoCurrency(cryptoCurrency, amount)

            return redirect('home')
    else:
        form = EntryWalletForm()
        form.fields["cryptoCurrency"].queryset = wallet.getCryptoCurrencyList()
    return render(request, '../templates/remove_cryptocurrency.html', {'form': form})
