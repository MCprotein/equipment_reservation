from django.contrib import admin
from .models import *
# Register your models here.

class AccountsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

admin.site.register(Profile, AccountsAdmin)