from django.contrib.auth.decorators import login_required
from foodoclock.forms.PreferredCurrencyForm import PreferredCurrencyForm
from foodoclock.models.CryptoCurrency import CryptoCurrency
from foodoclock.models.Currency import Currency
from foodoclock.models.ExchangeRate import ExchangeRate
from foodoclock.models.Wallet import Wallet
from django.shortcuts import redirect, render


@login_required
def exchange(request):

    wallet = Wallet.getWalletByUser(request.user)
    entries = ExchangeRate.objects.all()
    rows = []

    for e in entries:
        rows.append((e.cryptoCurrency, e.currency, e.rate))

    form = PreferredCurrencyForm(request.POST)

    if request.method == 'POST':
        if request.POST.get('pref'):
            form.fields["preferredCurrency"].initial = wallet.preferredCurrency

            if form.is_valid():
                    preferredCurrency = form.cleaned_data.get('preferredCurrency')
                    wallet.preferredCurrency = preferredCurrency
                    wallet.save()

                    return redirect('exchangerate')
        elif request.POST.get('exc'):
            form = PreferredCurrencyForm()
            form.fields["preferredCurrency"].initial = wallet.preferredCurrency

            flag = False;
            try:
                cryptoCurrency = CryptoCurrency.objects.get(code=request.POST.get('cryptoCurrency'))
                flag = True
            except CryptoCurrency.DoesNotExist:
                flag = False

            try:
                currency = Currency.objects.get(code=request.POST.get('currency'))
                flag = True
            except Currency.DoesNotExist:
                flag = False

            try:
                exchangeRate = entries.get(cryptoCurrency=cryptoCurrency, currency=currency)
                flag = True
            except ExchangeRate.DoesNotExist:
                flag = False

            if flag:
                exchangeRate.rate = request.POST.get('rate')
                exchangeRate.save()
            return redirect('exchangerate')

    else:
        form = PreferredCurrencyForm()
        form.fields["preferredCurrency"].initial = wallet.preferredCurrency

    return render(request, '../templates/exchangerate.html', {'form': form, 'rows': rows})
