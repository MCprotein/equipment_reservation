from django.urls import path, include
from .views import base_views, blog_views, edit_views, ajax_views, my_views

app_name = 'reservation'

urlpatterns = [
    path('blog/<int:blog_id>', blog_views.detail, name='detail'),
    path('new/<str:equipment_type>/', edit_views.new, name='new'),
    path('check/', ajax_views.check, name='check'),
    path('index/<str:category_name>', blog_views.index, name='index'),
    path('create/', my_views.create, name='create'),
    path('edit/<int:reservation_id>', edit_views.edit, name='edit'),
    path('update/<int:reservation_id>', edit_views.update, name='update'),
    path('delete/<int:reservation_id>', edit_views.delete, name='delete'),
    path('my/', my_views.myreservation, name='myreservation'),
    path('', base_views.home, name='home'),
]