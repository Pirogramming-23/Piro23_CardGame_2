from django.urls import path
from .views import *

urlpatterns = [
    path("create/", games_create),
    path("<int:pk>/cnt_attack", counter_attack),
    path("<int:pk>/result", games_result),
]