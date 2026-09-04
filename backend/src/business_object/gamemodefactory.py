from backend.src.business_object.game_mode import CoinFlipMode, DiceMode, GameMode


class Gamemodefactory:
    @classmethod
    def get_mode(cls, game_mode: str) -> GameMode:
        """
        Returns the corresponding GameMode object.
        Args:
            game_mode (str): The identifier of the game mode (e.g., 'coinflip', 'dice').
        Returns:
            GameMode: An instance of a class implementing GameMode.
        Raises:
            ValueError: If the requested game_mode is not supported.
        """
        if game_mode == "coinflip":
            return CoinFlipMode(game_mode)
        elif game_mode == "dice":
            return DiceMode(game_mode)
