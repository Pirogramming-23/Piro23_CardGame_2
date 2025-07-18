from django.urls import path
from .views import *
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Game

urlpatterns = [
    path("<int:upk>/create/", games_create),
    path("<int:upk>/<int:gpk>/cnt_attack", counter_attack, name='counter_attack'),
    path("<int:upk>/<int:gpk>/result", games_result, name='games_result'),
    path('list/', games_list, name='games_list'),
    path('cancel/<int:game_id>/', cancel_game, name='cancel_game'),
]