from fastapi import HTTPException

from business_object.game import Game
from business_object.game_mode.game_mode_factory import GameModeFactory
from business_object.scoring_strategy import ScoringStrategy
from dao.game_dao import GameDao
from dao.player_dao import PlayerDao
from utils.log_utils import log


class GameService:
    """Service that manages games."""

    @log
    def play(self, id_player: int, id_opponent: int, game_mode: str, **kwargs):
        """Executes a single round of a coin-flip game between two players.

        Args:
            id_player (int): The unique identifier of the first player.
            id_opponent (int): The unique identifier of the opponent.
            game_mode (str): The game mode to play.

        Returns:
            Game: The game object saved in database with updated player ratings.

        Raises:
            HTTPException: 400 if the two players are the same.
            HTTPException: 404 if one or both players are not found in the database.
        """
        if id_player == id_opponent:
            raise HTTPException(status_code=400, detail="Two different players required")

        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        mode = GameModeFactory.get_mode(game_mode)

        # 1. Jouer la partie
        game = mode.play(p1, p2, **kwargs)

        # 2. Sauvegarder la partie en base de données (injecte l'id_game dans l'objet game)
        GameDao().create(game)

        # 3. Mettre à jour les ELO des joueurs et les persister
        ScoringStrategy.update_player_ratings(game)

        PlayerDao().update(p1)
        PlayerDao().update(p2)

        return game

    @log
    def find_by_id(self, id_game: int) -> Game:
        """Find a game by its ID and hydrate associated Player entities.

        Args:
            id_game (int): The unique identifier of the game to find.

        Returns:
            Game: The hydrated Game object.

        Raises:
            HTTPException: 404 if the game is not found.
        """
        game_dao = GameDao()
        player_dao = PlayerDao()

        game = game_dao.find_by_id(id_game)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        # Si le DAO renvoie des IDs bruts pour les joueurs, on charge les objets Player complets
        if isinstance(game.player1, int):
            game.player1 = player_dao.find_by_id(game.player1)
        if isinstance(game.player2, int):
            game.player2 = player_dao.find_by_id(game.player2)
        if isinstance(game.winner, int):
            game.winner = player_dao.find_by_id(game.winner)

        return game

    @log
    def find_all_by_player(self, id_player: int, game_mode: str | None = None) -> list[Game]:
        """Find all games involving a specific player, optionally filtered by game mode.

        Args:
            id_player (int): The ID of the player.
            game_mode (str | None): Optional game mode to filter by.

        Returns:
            list[Game]: List of hydrated Game objects.

        Raises:
            HTTPException: 404 if the player does not exist.
        """
        player_dao = PlayerDao()
        game_dao = GameDao()

        # 1. Vérifier que le joueur existe
        player = player_dao.find_by_id(id_player)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        # 2. Récupérer toutes les parties du joueur
        games = game_dao.find_all_by_player(id_player)

        # 3. Filtrer par mode de jeu si spécifié
        if game_mode is not None:
            games = [g for g in games if g.game_mode == game_mode]

        # 4. Réhydrater les entités Player si la DAO a retourné des IDs bruts
        for game in games:
            if isinstance(game.player1, int):
                game.player1 = player_dao.find_by_id(game.player1)
            if isinstance(game.player2, int):
                game.player2 = player_dao.find_by_id(game.player2)
            if isinstance(game.winner, int):
                game.winner = player_dao.find_by_id(game.winner)

        return games