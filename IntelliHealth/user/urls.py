from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('add_record/', add_record, name='add_record'),
]
