from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('games/', include("games.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('users.urls')),
]
