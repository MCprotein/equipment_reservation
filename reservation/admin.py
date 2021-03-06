from django.contrib import admin
from .models import *


# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'equipment_type', 'equipment_date']
    list_filter = ['author', 'equipment_type', 'equipment_date']


admin.site.register(Reservation, ReservationAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'created']
    list_filter = ['id', 'category', 'title', 'created']


admin.site.register(Blog, BlogAdmin)
