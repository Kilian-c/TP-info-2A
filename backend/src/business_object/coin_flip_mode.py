import random

from business_object.game_mode import GameMode
from business_object.player import Player
from service.game import Game


class CoinFlipMode(GameMode):
    def play(self, player1: Player, player2: Player) -> Game:
        winner = random.choice([player1, player2])

        description = f"Coinflip game played between {player1.username} and {player2.username}."
        return Game(
            id_game=None,
            player1=player1,
            player2=player2,
            game_mode="coinflip",
            winner=winner,
            description=description,
        )
