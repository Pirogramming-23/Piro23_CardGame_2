from django.urls import path
from .views import *

urlpatterns = [
    path("<int:upk>/create/", games_create),
    path("<int:upk>/<int:gpk>/cnt_attack", counter_attack),
    path("<int:upk>/<int:gpk>/result", games_result),
]