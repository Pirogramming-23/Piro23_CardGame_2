from django.shortcuts import render,redirect
from .models import Game

# Create your views here.
def detail(request,pk):
    game = Game.objects.get(id=pk)
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
    return render(request,'games/detail.html',context)

# 유저는 자신이 공격한 게임(상대가 반격하지 않은 경우에 한해) 삭제 가능
def delete(request,pk):
    game = Game.objects.get(id=pk)
    if request.user == game.attacker and game.defender is None:
        game.delete()
    return redirect('games:main')