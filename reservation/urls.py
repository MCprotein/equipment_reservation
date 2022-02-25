from django.urls import path, include
from .views import base_views, blog_views, edit_views, ajax_views, my_views

app_name = 'reservation'

urlpatterns = [

    # blog_views.py
    path('blog/detail/<int:blog_id>/', blog_views.blog_detail, name='blog_detail'),
    path('blog/create/<str:category_name>/', blog_views.blog_create, name='blog_create'),
    path('blog/modify/<int:blog_id>/', blog_views.blog_modify, name='blog_modify'),
    path('blog/delete/<str:category_name>/<int:blog_id>/', blog_views.blog_delete, name='blog_delete'),
    path('blog/index/<str:category_name>/', blog_views.blog_index, name='blog_index'),

    # edit_views.py
    path('new/<str:equipment_type>/', edit_views.new, name='new'),
    path('edit/<int:reservation_id>/', edit_views.edit, name='edit'),
    path('update/<int:reservation_id>/', edit_views.update, name='update'),
    path('delete/<int:reservation_id>/', edit_views.delete, name='delete'),

    # my_views.py
    path('my/', my_views.myreservation, name='myreservation'),
    path('create/', my_views.create, name='create'),

    # ajax_views.py
    path('check/', ajax_views.check, name='check'),

    # base_views.py
    path('', base_views.home, name='home'),
]