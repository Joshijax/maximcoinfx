from django.contrib import admin

from main.models import Invest, Invest_plan, Message, Payment_Method, Referral, Replys, UserType
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Invest_plan)
admin.site.register(UserType)
admin.site.register(Message)
admin.site.register(Replys)
admin.site.register(Payment_Method)
admin.site.register(Referral)

class ProfileInline(admin.StackedInline):
    model = UserType
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class ReplyInline(admin.StackedInline):
    model = Replys
    can_delete = True
    verbose_name_plural = 'reply'
    fk_name = 'rep'

class ReferralInline(admin.StackedInline):
    model = Referral
    can_delete = True
    verbose_name_plural = 'ref'
    fk_name = 'ref'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, ReplyInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)