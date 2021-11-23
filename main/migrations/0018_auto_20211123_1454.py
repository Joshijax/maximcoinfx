# Generated by Django 3.2.8 on 2021-11-23 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_auto_20211123_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertype',
            name='ref',
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ref', to=settings.AUTH_USER_MODEL)),
                ('ref_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ref_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
