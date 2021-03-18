from django.shortcuts import render
from cryptoFront.models import CoinInfo
from cryptoFront.utils import CryptoApp

# Create your views here.
def main(request):
    return render(request, 'main.html', None)

def crypto_tables(request):
    #obtain database table values
    coinObj = CoinInfo.objects.all().values()
    context = {
        'coinData': coinObj
    }

    #update button functionality in html crypto_tables
    if request.method == 'POST':
        app = CryptoApp()
        for obj in list(coinObj):
            coin = obj['name']
            app.updatePrice(coin)
            app.updateBalance(coin)
            app.updateChange(coin)

        return render(request, 'crypto_tables.html', context)

    return render(request, 'crypto_tables.html', context)

def deposit_page(request):
    #deposit functionality for html deposit_page
    if request.method == 'POST':
        coin = request.POST.get('deposit_coin', None)
        coin = str(coin)
        amount = request.POST.get('deposit_amount', None)
        amount = float(amount)
        app = CryptoApp()
        app.addCoinRow(coin)
        app.fillEmptyRow(coin)
        app.updatePrice(coin)
        app.updateDeposit(coin, amount)
        app.updateCoins(coin, amount)
        app.updateBalance(coin)
        app.updateChange(coin)

    return render(request, 'deposit_page.html', None)

def withdraw_page(request):
    #withdraw functionality for html withdraw_page
    if request.method == 'POST':
        coin = request.POST.get('withdraw_coin', None)
        coin = str(coin)
        amount = request.POST.get('withdraw_amount', None)
        amount = float(amount) * -1
        app = CryptoApp()
        app.addCoinRow(coin)
        app.fillEmptyRow(coin)
        app.updatePrice(coin)
        app.updateDeposit(coin, amount)
        app.updateCoins(coin, amount)
        app.updateBalance(coin)
        app.updateChange(coin)

    return render(request, 'withdraw_page.html', None)