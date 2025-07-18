from django.urls import path
from .views import *

app_name = "games"

urlpatterns = [
    path('<int:pk>',detail,name='detail'),
    path('delete/<int:pk>',delete,name="delete"),
    path('ranking',ranking,name="ranking"),
    path("<int:upk>/create/", games_create),
    path("<int:upk>/<int:gpk>/cnt_attack", counter_attack),
    path("<int:upk>/<int:gpk>/result", games_result),
]