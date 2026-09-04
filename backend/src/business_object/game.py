import datetime

from backend.src.business_object.player import Player


class Game:
    """
    Class representing a Game.
    Attributes:
        id_game (int): The unique identifier for the game.
        player1  (Player): The player 1.
        player2  (Player): The player 2.
        game_mode (str): The game mode.
        winner  (Player): The player's email address.
        description (str): The description of a game.
        timestamp  (datetime): The duration of the game.
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        game_mode: str,
        winner: Player | None,
        description: str,
        timestamp: datetime,
        id_game=None,
    ):
        """Constructor"""
        self.player1 = player1
        self.player2 = player2
        self.game_mode = game_mode
        self.winner = winner
        self.description = description
        self.id_game = id_game

    def __str__(self):
        """Returns a string representation of the game.
        Returns:
            str: A string containing the players and the winner.
        """
        return f"Coinflip between {self.player1} and {self.player2}, winner: {self.winner})"
