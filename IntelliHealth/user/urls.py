from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('get_user_info/', get_user_info, name='get_user_info'),
    path('add_record/', add_record, name='add_record'),
    path('search_record/', search_record, name='search_record'),
]
