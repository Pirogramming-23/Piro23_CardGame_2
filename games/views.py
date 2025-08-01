from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from users.models import User
import random
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def detail(request,pk):
    game = get_object_or_404(Game, id=pk)
    user = request.user #현재 로그인한 유저
    status = "게임 종료"
    if not game.is_over:
        if user == game.attacker: #공격자 입장
            status = "진행중"
        elif user == game.defender and game.defender_card is None: #수비자 입장 (반격 아직 안 한 상태)
            status = "반격 가능"
        else: # 공격자도 수비자도 아닌 유저
            status = "진행중"
    context = {
        'game':game,
        'status':status,
        'is_attacker' : user == game.attacker,
        'is_defender' : user == game.defender,
    }
    return render(request,'detail.html',context)

# 유저는 자신이 공격한 게임(상대가 반격하지 않은 경우에 한해) 삭제 가능
def delete(request,pk):
    game = get_object_or_404(Game, id=pk)
    if request.user == game.attacker and game.defender_card is None:
        game.delete()
    return redirect('games:games_list', upk=request.user.pk) 


def ranking(request):
    users = User.objects.all().order_by('-user_score')[:3]
    context ={
        'users':users
    }
    return render(request,'ranking.html',context)


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
        # return redirect("게임 전적 페이지로") #게임 전적 페이지 url넣는 곳 # 수정할 곳!!!
        return redirect('games:games_list', upk=request.user.pk) 
    return render(request, "games_create.html", {"users":users, "numbers":numbers})

def counter_attack(request, upk, gpk):
    user = User.objects.get(id=upk)
    game = Game.objects.get(id=gpk)
    numbers = random.sample(range(1, 11), 5)
    if request.method == "POST":
        game.defender_card = int(request.POST["card"])
        if game.rule == True: #rule이 True일 때는 숫자가 더 큰 사람이 이긴다!
            if game.attacker_card > game.defender_card:
                game.winner, game.loser = game.attacker, game.defender
                game.winner.user_score += game.attacker_card
                game.loser.user_score -= game.defender_card
                game.winner.save()
                game.loser.save()
            elif game.attacker_card == game.defender_card: #무승부일 때는 winner와 loser를 None처리 했습니다
                game.winner, game.loser = None, None
            elif game.attacker_card < game.defender_card :
                game.winner, game.loser = game.defender, game.attacker
                game.winner.user_score += game.defender_card
                game.loser.user_score -= game.attacker_card
                game.winner.save()
                game.loser.save()

        else :#rule이 False일 때는 숫자가 더 작은 사람이 이긴다!
            if game.attacker_card > game.defender_card:
                game.winner, game.loser = game.defender, game.attacker
                game.winner.user_score += game.defender_card
                game.loser.user_score -= game.attacker_card
                game.winner.save()
                game.loser.save()
            elif game.attacker_card == game.defender_card:
                game.winner, game.loser = None, None
            elif game.attacker_card < game.defender_card :
                game.winner, game.loser = game.attacker, game.defender
                game.winner.user_score += game.attacker_card
                game.loser.user_score -= game.defender_card
                game.winner.save()
                game.loser.save()
        game.is_over = True
        game.save()
        return redirect('games:detail', pk=game.pk) 
    return render(request, "counter_attack.html", {"numbers":numbers})

def games_result(request, upk, gpk):
    game = Game.objects.get(id=gpk)
    user = User.objects.get(id=upk) #수정필요
    return render(request, "games_result.html", {"game":game, "user":user})


def games_list(request,upk):
    # user = request.user
    user = User.objects.get(id=upk) #수정할 곳!
    games = Game.objects.filter(attacker=user) | Game.objects.filter(defender=user)
    games = games.order_by('-id')

    ongoing_list = []
    counter_list = []
    finished_list = []

    for game in games:
        # 1. 진행중: 내가 공격자이고, defender_card가 None(상대가 아직 반격X)
        if game.attacker == user and not game.defender_card and not getattr(game, 'is_over', False):
            ongoing_list.append(game)
        # 2. 반격대기: 내가 수비자이고, defender_card가 None(내가 아직 반격X)
        elif game.defender == user and not game.defender_card and not getattr(game, 'is_over', False):
            counter_list.append(game)
        # 3. 종료: defender_card가 있고, is_over가 True이거나 winner/loser가 있으면 종료
        else:
            finished_list.append(game)

    context = {
        'user': user,
        'ongoing_list': ongoing_list,
        'counter_list': counter_list,
        'finished_list': finished_list,
    }
    return render(request, 'games_list.html', context) 