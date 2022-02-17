from django.urls import path, include
from .views import *

app_name = 'reservation'

urlpatterns = [
    path('new/<str:equipment_type>', new, name='reservation_new'),
    path('', home, name='home'),
]