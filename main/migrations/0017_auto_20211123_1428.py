# Generated by Django 3.2.8 on 2021-11-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_usertype_email_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertype',
            name='ref',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='email_confirm',
            field=models.BooleanField(default=False),
        ),
    ]
