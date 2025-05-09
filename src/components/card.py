from typing import TypedDict

import streamlit as st


class Card(TypedDict):
    """A dictionary representing a card.

    Attributes:
        image (str): The URL of the image to display on the card.
        page (str): Streamlit page link (just python module).
        label (str): The label for page link.
        icon (str): The icon for page link.
        description (str): A short description of the card.

    """

    image: str
    page: str
    label: str
    icon: str
    description: str


def card_grid(cards: list[Card], num_columns: int = 2) -> None:
    """Displays a grid of cards.

    Args:
        cards (list[Card]): A list of card data structures.
        num_columns (int): The number of columns in the grid. Default is 2.

    """
    card_columns = st.columns(num_columns)

    for idx, card in enumerate(cards):
        with card_columns[idx % num_columns]:
            with st.container(border=True):
                st.image(card["image"])
                st.page_link(
                    card["page"],
                    label=f"**{card["label"]}**",
                    icon=card["icon"],
                    use_container_width=True,
                )
                st.write(f"*{card["description"]}*")
