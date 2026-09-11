from business_object.game import Game
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDao(metaclass=Singleton):
    """Class containing methods to access Games in the database."""

    @log
    @log
    def create(self, game: Game) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO project.game (id_player1, id_player2, game_mode, id_winner, detail) VALUES "
                        "(%(id_player1)s, %(id_player2)s, %(game_mode)s, %(id_winner)s, %(detail)s) "
                        "RETURNING id_game;",
                        {
                            "id_player1": game.player1.id_player if game.player1 else None,
                            "id_player2": game.player2.id_player if game.player2 else None,
                            "game_mode": game.game_mode,
                            "id_winner": game.winner.id_player if game.winner else None,
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
    def find_by_id(self, id_game: int) -> Game | None:
        """Find a game by its id.

        Args:
            id_game (int): The ID of the game to find

        Returns:
            Game | None: Game matching the given id, or None
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM project.game WHERE id_game = %(id_game)s;",
                        {"id_game": id_game},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        if not res:
            return None

        # Note: res["id_player1"], res["id_player2"] et res["id_winner"] sont des IDs.
        # Si votre couche métier attend de vrais objets Player, vous devrez les charger via PlayerDao.
        return Game(
            id_game=res["id_game"],
            player1=res["id_player1"],
            player2=res["id_player2"],
            game_mode=res["game_mode"],
            winner=res["id_winner"],
            description=res["detail"],
            timestamp=res["timestamp"],
        )

    @log
    def find_all_by_player(self, id_player: int) -> list[Game]:
        """Find all games involving a specific player (as player1 or player2).

        Args:
            id_player (int): The ID of the player

        Returns:
            list[Game]: List of Game objects involving the player
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM project.game "
                        "WHERE id_player1 = %(id_player)s OR id_player2 = %(id_player)s;",
                        {"id_player": id_player},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        games_list = []
        if res:
            for row in res:
                game = Game(
                    id_game=row["id_game"],
                    player1=row["id_player1"],
                    player2=row["id_player2"],
                    game_mode=row["game_mode"],
                    winner=row["id_winner"],
                    description=row["detail"],
                    timestamp=row["timestamp"],
                )
                games_list.append(game)

        return games_list