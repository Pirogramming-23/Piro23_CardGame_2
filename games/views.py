from django.shortcuts import render, redirect
from .models import Game
from users.models import User
import random

# Create your views here.
def games_create(request):
    users = User.objects.all()
    numbers = random.sample(range(1, 11), 5)
    if request.method == "POST":
        Game.objects.create(
            attacker=User.objects.get(username=request.POST["defender"]), #여기는 유저 넣는곳!!! #수정할 곳!! 중요..!
            defender=User.objects.get(username = request.POST["defender"]),
            attacker_card = int(request.POST["card"]),
            rule = random.choice([True, False]),
            is_over = False,
        )
        return redirect("게임 전적 페이지로") #게임 전적 페이지 url넣는 곳 # 수정할 곳!!!
    return render(request, "games_create.html", {"users":users, "numbers":numbers})