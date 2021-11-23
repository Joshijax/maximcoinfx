# Generated by Django 3.2.8 on 2021-11-23 15:36

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_invest_plan_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invest_plan',
            name='amountto',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='USD', max_digits=14),
        ),
    ]