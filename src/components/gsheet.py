import json
from typing import Callable

import gspread
import streamlit as st
from google.oauth2.credentials import Credentials


def gsheet_selector() -> Callable[[], gspread.Worksheet] | None:
    """Component to select a Google Sheets document and worksheet.

    Returns:
        Callable[[], gspread.Worksheet]: A function that loads and returns the worksheet.
        None: If the user does not upload a credentials file.

    """
    document_url = st.text_input(
        "Document URL",
        help="The URL of the Google Sheets document. Make sure you have edit access.",
    )
    worksheet_name = st.text_input(
        "Worksheet name",
        help="The name of the worksheet. This is the tab name at the bottom of the document.",
    )
    if not st.session_state["user"]:
        return None

    def get_worksheet() -> gspread.Worksheet:
        google_oauth_client_config = json.loads(st.secrets["google_oauth_client_config"])
        credentials = Credentials(
            token=None,
            refresh_token=st.session_state["user"]["refresh_token"],
            token_uri=google_oauth_client_config["web"]["token_uri"],
            client_id=google_oauth_client_config["web"]["client_id"],
            client_secret=google_oauth_client_config["web"]["client_secret"],
        )
        client = gspread.Client(credentials)
        sheet = client.open_by_url(document_url)
        return sheet.worksheet(worksheet_name)

    return get_worksheet
