# Generated by Django 3.1.2 on 2021-03-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoinInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.TextField()),
                ('balance', models.TextField()),
                ('initial', models.TextField()),
                ('change', models.DecimalField(decimal_places=2, max_digits=5)),
                ('coins', models.DecimalField(decimal_places=6, max_digits=12)),
            ],
        ),
    ]
