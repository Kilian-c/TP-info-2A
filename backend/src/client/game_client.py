import json
from datetime import UTC, datetime, timezone

import requests
from business_object.game import Game, Player


class GameClient:
    def get_games(self) -> list[Game]:
        r = requests.get(url="http://localhost:5555/")
        r.raise_for_status()
        raw_json = r.json()

        games = []
        for game_dict in raw_json:
            # Handle optional or missing attributes safely
            players = game_dict.get("players_list") or []
            p1_name = players[0] if len(players) > 0 else "Unknown Player 1"
            p2_name = players[1] if len(players) > 1 else "Unknown Player 2"

            player1 = Player(username=p1_name, elo=1000, email="")
            player2 = Player(username=p2_name, elo=1000, email="")

            winner_name = game_dict.get("winner_name")
            winner = None
            if winner_name == player1.username:
                winner = player1
            elif winner_name == player2.username:
                winner = player2
            elif winner_name:
                winner = Player(username=winner_name, elo=1000, email="")

            location = game_dict.get("location_name", "Unknown Location")
            duration = game_dict.get("duration_seconds", 0)
            description = f"Location: {location} | Duration: {duration}s"

            game_id = game_dict.get("id")
            id_game = int(game_id) if game_id is not None else None

            # Create an object
            g = Game(
                player1=player1,
                player2=player2,
                game_mode=game_dict.get("mode_type", "Unknown"),
                winner=winner,
                description=description,
                timestamp=datetime.now(UTC),
                id_game=id_game,
            )

            # If it succeed, add to the list
            if g:
                games.append(g)
        return games
