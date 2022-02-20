from django.urls import path, include
from .views import *

urlpatterns = [
    path('blog/<int:blog_id>', detail, name='detail'),
    path('new/<str:equipment_type>/', new, name='new'),
    path('check/', check, name='check'),
    path('index/<str:category_name>', index, name='index'),
    path('create/', create, name='create'),
    path('edit/<int:reservation_id>', edit, name='edit'),
    path('update/<int:reservation_id>', update, name='update'),
    path('delete/<int:reservation_id', delete, name='delete'),
    path('my/', myreservation, name='myreservation'),
    path('', home, name='home'),
]