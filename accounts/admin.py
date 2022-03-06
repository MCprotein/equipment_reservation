from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'last_name', 'first_name','is_active', 'is_staff']

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

class AccountsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'realname', 'department', 'email']

admin.site.register(Profile, AccountsAdmin)