from django.shortcuts import render
from cryptoFront.models import CoinInfo

# Create your views here.
def main(request):
    return render(request, 'main.html', None)

def crypto_tables(request):
    coinObj = CoinInfo.objects.all().values()
    print(CoinInfo.objects.all().exists())
    print(coinObj)
    context = {
        'coinData': coinObj
    }

    return render(request, 'crypto_tables.html', context)

