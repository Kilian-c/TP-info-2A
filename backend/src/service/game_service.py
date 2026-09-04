from backend.src.business_object.gamemodefactory import get_mode

from dao.player_dao import PlayerDao  # type: ignore


class GameService:
    def play(self, id_player, id_opponent, game_mode: str, **kwargs):
        # Find players by id -> the code does not change
        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        # Get rules
        mode = get_mode(game_mode)

        # Play the game following rules
        # Eventualy add extra parameters like choice (included in kwargs)
        game = mode.play(p1, p2, **kwargs)

        # Update Players object in the database (not this week)
        PlayerDao().update(p1)
        PlayerDao().update(p2)

        return game
