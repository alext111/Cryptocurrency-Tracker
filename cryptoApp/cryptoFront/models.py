from django.db import models

# Create your models here.
class CoinInfo(models.Model):

    name = models.TextField()
    price = models.TextField()
    balance = models.TextField()
    deposit = models.TextField()
    change = models.DecimalField(max_digits=5,decimal_places=2)
    coins = models.DecimalField(max_digits=12,decimal_places=6)
