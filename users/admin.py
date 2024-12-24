from django.contrib import admin

from users.models import User, Referral


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'email', 'first_name', 'last_name', 'self_referral', 'user_referral', 'sms_code']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['id', 'referral']
