from business_object.game import Game
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDao(metaclass=Singleton):
    """Class containing methods to access games in the database."""

    @log
    def create(self, game) -> bool:
        """Create a game in the database.
        Args:
            Game to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO game(id_player1, id_player2, game_mode, id_winner, detail) VALUES "
                        "(%(id_player1)s, %(id_player2)s, %(game_mode)s, %(id_winner)s, %(detail)s) "
                        "RETURNING id_game;",
                        {
                            "id_player1": game.player1.id_player,
                            "id_player2": game.player2.id_player,
                            "game_mode": game.game_mode,
                            "id_winner": game.winner.id_player,
                            "detail": game.description,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            game.id_game = res["id_game"]
            created = True

        return created

    @log
    def find_by_id(self, id_game: int) -> Game:
        """Find a game by their id.
        Args:
            id_game (int): The ID of the game to find
        Returns:
            Game matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM game                       "
                        " WHERE id_game = %(id_game)s;   ",
                        {"id_game": id_game},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        game = None
        if res:
            game = Game(
                id_player1=res["id_player1"],
                id_player2=res["id_player2"],
                game_mode=res["game_mode"],
                id_winner=res["id_winner"],
                detail=res["detail"],
                id_game=res["id_game"],
            )

        return game
