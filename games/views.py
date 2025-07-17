from django.shortcuts import render, redirect
from .models import Game
from users.models import User
import random

# Create your views here.
def games_create(request):
    users = User.objects.all() #수정할 곳!
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

def counter_attack(request, pk):
    game = Game.objects.get(id=pk)
    numbers = random.sample(range(1, 11), 5)
    if request.method == "POST":
        game.defender_card = int(request.POST["card"])
        if game.rule == True: #rule이 True일 때는 숫자가 더 큰 사람이 이긴다!
            if game.attacker_card > game.defender_card:
                game.winner, game.loser = game.attacker, game.defender
            elif game.attacker_card == game.defender_card: #무승부일 때는 winner와 loser를 None처리 했습니다
                game.winner, game.loser = None, None
            elif game.attacker_card < game.defender_card :
                game.winner, game.loser = game.defender, game.attacker
        else :#rule이 False일 때는 숫자가 더 작은 사람이 이긴다!
            if game.attacker_card > game.defender_card:
                game.winner, game.loser = game.defender, game.attacker
            elif game.attacker_card == game.defender_card:
                game.winner, game.loser = None, None
            elif game.attacker_card < game.defender_card :
                game.winner, game.loser = game.attacker, game.defender
        game.is_over = True
        game.save()
        return redirect("게임 전적 페이지로") #게임 전적 페이지 url넣는 곳 # 수정할 곳!!!
    return render(request, "counter_attack.html", {"numbers":numbers})