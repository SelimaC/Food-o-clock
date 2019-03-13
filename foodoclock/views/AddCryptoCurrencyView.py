from django.contrib.auth.decorators import login_required

from foodoclock.forms.EntryWalletForm import EntryWalletForm
from foodoclock.models.Wallet import Wallet
from django.shortcuts import redirect, render


@login_required
def add(request):
    if request.method == 'POST':
        form = EntryWalletForm(request.POST)
        if form.is_valid():
            cryptocurrency = form.cleaned_data.get('cryptoCurrency')
            amount = form.cleaned_data.get('amount')

            wallet = Wallet.getWalletByUser(request.user)
            wallet.addCryptoCurrency(cryptocurrency, amount)

            return redirect('home')
    else:
        form = EntryWalletForm()
    return render(request, '../templates/add_cryptocurrency.html', {'form': form})
