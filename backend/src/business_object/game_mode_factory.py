from business_object.coin_flip_mode import CoinFlipMode
from business_object.dice_mode import DiceMode
from business_object.game_mode import GameMode


class GameModeFactory:
    @staticmethod
    def get_mode(game_mode_name: str) -> GameMode:
        if game_mode_name.lower() == "coinflip":
            return CoinFlipMode()
        elif game_mode_name.lower() == "dice":
            return DiceMode()
        else:
            raise ValueError(f"Unknown game mode: {game_mode_name}")
