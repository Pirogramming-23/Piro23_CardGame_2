from django.db import models
from users.models import User

class Game(models.Model):
    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_attacker')
    defender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_defender')
    attacker_card = models.PositiveIntegerField()
    defender_card = models.PositiveIntegerField(null=True, blank=True)
    rule = models.BooleanField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='games_as_winner')
    loser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='game_as_loser')
    is_over = models.BooleanField(default=False)
