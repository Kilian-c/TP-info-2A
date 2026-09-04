import secrets
from abc import ABC, abstractmethod

from backend.src.business_object.game import Game
from backend.src.business_object.player import Player


class GameMode(ABC):
    """Base class for game modes."""

    @abstractmethod
    def play(self, p1: Player, p2: Player) -> Game:
        """Play a game between two players."""
        raise NotImplementedError


class DiceMode(GameMode):
    """Game mode where both players roll a die."""

    def play(self, p1: Player, p2: Player) -> Game:
        roll1 = secrets.randbelow(6) + 1
        roll2 = secrets.randbelow(6) + 1

        winner = None
        if roll1 > roll2:
            winner = p1
        elif roll2 > roll1:
            winner = p2

        return Game(
            player1=p1,
            player2=p2,
            description=f"{roll1}-{roll2}",
            winner=winner,
        )


class CoinFlipMode(GameMode):
    """Game mode based on a coin flip."""

    def play(self, p1: Player, p2: Player, choice: str = "heads") -> Game:
        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        return Game(
            player1=p1,
            player2=p2,
            description=result,
            winner=winner,
        )
