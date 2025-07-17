from django.urls import path
from .views import *

app_name = "Game"

urlpatterns = [
    path('detail/<int:pk>',detail,name='detail'),
    path('delete/<int:pk>',delete,name="delete"),
]