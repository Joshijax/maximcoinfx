from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver

# Create your models here.
class UserType(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE,)
    phone = models.CharField(max_length = 100, blank=True)
    balance = MoneyField(max_digits=14, decimal_places=1, default_currency='USD', default=0)
    invested_balance = MoneyField(max_digits=14, decimal_places=1, default_currency='USD', default=0)
    btc_balance = MoneyField(max_digits=14, decimal_places=4, default_currency='USD', default=0.0001)
    eth_balance = MoneyField(max_digits=14, decimal_places=4, default_currency='USD', default=0.0001)
    usdt_balance = MoneyField(max_digits=14, decimal_places=4, default_currency='USD', default=0.0001)
    commision = MoneyField(max_digits=14, decimal_places=1, default_currency='USD', default=2)
    bonus = MoneyField(max_digits=14, decimal_places=1, default_currency='USD', default=2)
    message = models.CharField(max_length = 100, blank=True)
    email_confirm = models.BooleanField(default=False)
    

    
    # url = models.URLField("Website", blank=True)
    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

class Invest(models.Model):
    name = models.CharField(max_length = 100, blank=True)
    
    duration = models.CharField(max_length = 100, blank=True)
    
    # url = models.URLField("Website", blank=True)
    
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Invest_plan(models.Model):
    name = models.CharField(max_length = 100, blank=True)
    amount = MoneyField(max_digits=14, decimal_places=0, default_currency='USD', default=0)
    amountto = MoneyField(max_digits=14, decimal_places=0, default_currency='USD', default=0)
    percent = models.CharField(max_length = 100, blank=True)
    percentr = models.CharField(max_length = 100, blank=True, default='0')
    return_date = models.CharField(max_length = 100, blank=True)
    

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Payment_Method(models.Model):
    name = models.CharField(max_length = 100, blank=True)
    # Message = MoneyField(max_digits=14, decimal_places=1, default_currency='USD')
    Message = models.TextField(max_length = 1000, blank=True)
    
    # url = models.URLField("Website", blank=True)
    
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Message(models.Model):
    message = models.CharField(max_length = 100, blank=True)
    
    # url = models.URLField("Website", blank=True)
    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message

class Replys(models.Model):
    rep = models.ForeignKey(User, related_name="reply", on_delete=models.CASCADE)
    reply = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
class Referral(models.Model):
    ref = models.ForeignKey(User, related_name="ref", on_delete=models.CASCADE)
    ref_user = models.ForeignKey(User, related_name="ref_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.ref.username + ' referred ' + self.ref_user.username

    def __unicode__(self):
        return self.message

@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserType.objects.create(user=instance)
