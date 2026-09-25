"""
Streamlit page for listing all players.

Retrieves and displays a list of registered players in a table, excluding sensitive data like passwords.

Endpoint used:
    GET /player
"""

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Player list")
logger = get_page_logger("list_players")


players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)

        if "id_player" in df.columns:
            df["URL"] = df["id_player"].apply(lambda x: f"/player_stats?player_id={x}")
        else:
            st.error("La colonne 'id_player' est introuvable dans les données de l'API.")

        if "URL" in df.columns:
            cols = list(df.columns)
            cols.remove("URL")
            cols.append("URL")
            df = df[cols]

        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "URL": st.column_config.LinkColumn("Stats Page", display_text="View Stats")
            },
            use_container_width=True,
        )
    else:
        logger.info("No players found.")
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")
