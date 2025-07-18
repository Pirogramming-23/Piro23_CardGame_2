from django.shortcuts import render, redirect
from .models import Game
from users.models import User
import random
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

# Create your views here.
def games_create(request, upk):
    users = User.objects.exclude(id=upk) #수정할 곳!
    numbers = random.sample(range(1, 11), 5)
    if request.method == "POST":
        Game.objects.create(
            attacker=User.objects.get(id=upk), #여기는 유저 넣는곳!!! #수정할 곳!! 중요..!
            defender=User.objects.get(username = request.POST["defender"]),
            attacker_card = int(request.POST["card"]),
            rule = random.choice([True, False]),
            is_over = False,
        )
        return redirect("games_list") #게임 전적 페이지 url넣는 곳 # 수정할 곳!!!
    return render(request, "games_create.html", {"users":users, "numbers":numbers})


def counter_attack(request, upk, gpk):
    game = Game.objects.get(id=gpk)
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
        return redirect("games_list") #게임 전적 페이지 url넣는 곳 # 수정할 곳!!!
    return render(request, "counter_attack.html", {"numbers":numbers})

def games_result(request, upk, gpk):
    game = Game.objects.get(id=gpk)
    user = User.objects.get(id=upk) #수정필요
    return render(request, "games_result.html", {"game":game, "user":user}) 

def games_list(request):
    user = get_object_or_404(User, id)
    games = Game.objects.filter(attacker=user) | Game.objects.filter(defender=user)
    games = games.order_by('-id')

    ongoing_list = []
    counter_list = []
    finished_list = []

    for game in games:
        if game.attacker == user and not game.defender_card and not getattr(game, 'is_over', False):
            ongoing_list.append(game)
        elif game.defender == user and not game.defender_card and not getattr(game, 'is_over', False):
            counter_list.append(game)
        else:
            finished_list.append(game)

    context = {
        'user': user,
        'ongoing_list': ongoing_list,
        'counter_list': counter_list,
        'finished_list': finished_list,
    }
    return render(request, 'games_list.html', context) 

@require_POST
def cancel_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, attacker=request.user, defender_card__isnull=True, is_over=False)
    game.delete()
    return redirect('games_list') 