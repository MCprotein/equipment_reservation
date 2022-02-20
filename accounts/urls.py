from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('confirm/', confirm, name='confirm'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]