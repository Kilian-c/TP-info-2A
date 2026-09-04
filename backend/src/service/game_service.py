from fastapi import HTTPException

from business_object.game_mode_factory import GameModeFactory
from business_object.scoring_strategy import ScoringStrategy
from dao.player_dao import PlayerDao
from service.game import Game
from utils.log_utils import log


class GameService:
    """Service that manages games."""
    @log
    def play(
      self, id_player: int, id_opponent: int, game_mode: str, **kwargs) -> Game:
        """Executes a game between two players using the specified game mode.

    Args:
        id_player (int): The unique identifier of the first player.
        id_opponent (int): The unique identifier of the opponent.
        game_mode (str): The mode of the game to play (e.g. 'coinflip',
          'dice').
        **kwargs: Additional parameters passed to the game mode execution.

    Returns:
        Game: A Game object containing all match details.

    Raises:
        HTTPException: 400 if the two players are the same.
        HTTPException: 404 if one or both players are not found in the database.
    """
        if id_player == id_opponent:
            raise HTTPException(status_code=400, detail="Two different players required")

        # 1. Get players
        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        # 2. Get the game mode using the factory
        mode = GameModeFactory.get_mode(game_mode)

        # 3. Play the game
        game = mode.play(p1, p2, **kwargs)

        # 4. Update elo of both players using ScoringStrategy
        ScoringStrategy.update_player_ratings(game)

        # Save updated players in the database
        PlayerDao().update(p1)
        PlayerDao().update(p2)

        # 5. Return a Game object
        return game
