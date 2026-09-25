"""
Streamlit page for the stats menu.

Provides navigation to available actions such as displayer the player's details for logged-in users.
"""

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Player Stats")
logger = get_page_logger("player_menu")


player = st.session_state.get("player")

player_id_str = st.query_params.get("player_id")

if player_id_str:
    try:
        player_id = int(player_id_str)
    except ValueError:
        st.error("L'ID du joueur dans l'URL est invalide.")
        st.stop()

    response = api_client.get(f"/player/{player_id}")

    if response and response.get("data"):
        player_data = response.get("data")

        st.subheader(player_data.get("username", "Username inconnu"))

        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="ELO", value=player_data.get("elo", "N/A"))

        with col2:
            st.write(player_data.get("email", "Aucun email fourni"))
            st.checkbox(
                "Fan de Pokémon", value=player_data.get("is_pokemon_fan", False), disabled=True
            )
    else:
        st.error("Impossible de récupérer les informations du joueur.")

    games_response = api_client.get(
        path="/game",
        params={"id_player": player_id},
    )

    if isinstance(games_response, dict):
        games_list = games_response.get("data", [])
    elif isinstance(games_response, list):
        games_list = games_response
    else:
        games_list = []

    if not games_list:
        st.info("Ce joueur n'a joué aucune partie pour le moment.")
    else:
        processed_games = []

        for game in games_list:
            # Récupérer les données des deux joueurs
            player1 = game.get("player1", {})
            player2 = game.get("player2", {})

            if player1.get("id_player") == player_id:
                opponent_username = player2.get("username", "Inconnu")
                opponent_elo = player2.get("elo", "N/A")
            else:
                opponent_username = player1.get("username", "Inconnu")
                opponent_elo = player1.get("elo", "N/A")

            winner = game.get("winner")

            if winner is None:
                result = "Draw"
            elif winner.get("id_player") == player_id:
                result = "Win"
            else:
                result = "Loss"

            game_mode = game.get("game_mode", "Inconnu").capitalize()

            processed_games.append({
                "Game Mode": game_mode,
                "Opponent": opponent_username,
                "Opponent ELO": opponent_elo,
                "Result": result,
            })

        # Création et affichage du DataFrame
        df_games = pd.DataFrame(processed_games)

        st.subheader("Historique des parties")

        st.dataframe(use_container_width=True, hide_index=True)

else:
    st.warning("Aucun ID de joueur spécifié dans l'URL. (Ex: ?player_id=3)")
