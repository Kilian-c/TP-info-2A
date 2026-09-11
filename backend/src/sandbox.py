# uv run --project backend python backend/src/sandbox.py
from business_object.game import Game
from business_object.player import Player
from dao.game_dao import GameDao
from utils.env_variables import load_environment_variables

load_environment_variables()  # Required to load the variables needed (env) to connect to the database

p1 = Player("timothé", 1200, "a@a.com", id_player=8)
p2 = Player("kilian", 1200, "b@b.com", id_player=9)

"""
PlayerDao().create(p1)
PlayerDao().create(p2)
"""
game = Game(p1, p2, "coin_flip", p1, "test", "", 15)

id = GameDao().create(game)
print(id)
game2 = GameDao().find_by_id(id_game=15)


"""
from service.game_service import GameService
from utils.env_variables import display_values, load_environment_variables
from utils.log_utils import initialize_logs

# Initialization
initialize_logs("Webservice")

load_environment_variables()
display_values()


g = GameService().play(3, 5, "coinflip", choice="tails")
print(g)

print(f"{g.player1.username} : new elo -> {g.player1.elo}")
print(f"{g.player2.username} : new elo -> {g.player2.elo}")

g2 = GameService().play(3, 5, "dice")
print(g2)

print(f"{g2.player1.username} : new elo -> {g2.player1.elo}")
print(f"{g2.player2.username} : new elo -> {g2.player2.elo}")
"""
