import random

from business_object.game_mode import GameMode
from business_object.player import Player
from service.game import Game


class DiceMode(GameMode):
    def play(self, player1: Player, player2: Player) -> Game:
        score1 = random.randint(1, 6)
        score2 = random.randint(1, 6)

        if score1 > score2:
            winner = player1
        elif score1 < score2:
            winner = player2
        else:
            winner = None

        description = f"{player1.username} rolled {score1}, {player2.username} rolled {score2}."

        return Game(
            id_game=None,
            player1=player1,
            player2=player2,
            game_mode="dice",
            winner=winner,
            description=description,
        )
