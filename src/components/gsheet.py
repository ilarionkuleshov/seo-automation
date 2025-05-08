import json
from typing import Callable

import gspread
import streamlit as st


def gsheet_selector() -> Callable[[], gspread.Worksheet] | None:
    """Component to select a Google Sheets document and worksheet.

    Returns:
        Callable[[], gspread.Worksheet]: A function that loads and returns the worksheet.
        None: If the user does not upload a credentials file.

    """
    credentials_file = st.file_uploader(
        "Upload your Google Sheets JSON credentials",
        help="Your service account JSON file. If you don't have it, see the instructions on home page.",
        type="json",
    )
    document_url = st.text_input(
        "Document URL",
        help="The URL of the Google Sheets document. Make sure you have edit access.",
    )
    worksheet_name = st.text_input(
        "Worksheet name",
        help="The name of the worksheet. This is the tab name at the bottom of the document.",
    )
    if not credentials_file:
        return None

    def get_worksheet() -> gspread.Worksheet:
        credentials = json.loads(credentials_file.getvalue().decode("utf-8"))
        client = gspread.service_account_from_dict(credentials)
        sheet = client.open_by_url(document_url)
        return sheet.worksheet(worksheet_name)

    return get_worksheet
