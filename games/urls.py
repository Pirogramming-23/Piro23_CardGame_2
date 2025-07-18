from django.urls import path
from .views import *

app_name = "Game"

urlpatterns = [
    path('<int:pk>',detail,name='detail'),
    path("create/", games_create),
    path("<int:pk>/cnt_attack", counter_attack),
    path("<int:pk>/result", games_result),
]


