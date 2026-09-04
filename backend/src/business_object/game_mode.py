from abc import ABC, abstractmethod

from business_object.player import Player
from service.game import Game


class GameMode(ABC):
    @abstractmethod
    def play(self, player1: Player, player2: Player) -> Game:
        pass
