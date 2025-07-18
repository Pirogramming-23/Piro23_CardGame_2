from django.urls import path
from .views import *

app_name = "Game"

urlpatterns = [
    path('games/<int:pk>',detail,name='detail'),
]