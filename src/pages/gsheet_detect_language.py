from typing import Iterator

import gspread
import langcodes
import langdetect
import pandas as pd
import streamlit as st

import components
import utils


def main() -> None:
    """Displays page for detecting language in a Google Sheets."""
    st.title("🔍 Detect Language")
    st.markdown(
        "This tool detects the language of the text in a Google Sheets column "
        "and saves the detected language to another column. "
        "The detected language is saved as a string in the format `lang_name (lang_code)`."
    )

    with st.form(key="gsheet_detect_language"):
        worksheet_func = components.gsheet_selector()
        source_column = st.text_input(
            "Source column",
            help="This column will be used as the source for language detection.",
        )
        destination_column = st.text_input(
            "Destination column",
            value="Detected Language",
            help="This column will be used to save the detected language.",
        )
        submitted = st.form_submit_button("Detect", type="primary")

    # pylint: disable=R0801
    if submitted:
        if not worksheet_func or not source_column or not destination_column:
            st.warning("Please make sure you are logged in and have filled in all fields.", icon="⚠️")
        else:
            components.stage_status(
                stages=[
                    {
                        "name": "Retrieving worksheet",
                        "func": components.return_stage_context("worksheet")(worksheet_func),
                    },
                    {
                        "name": "Data extraction",
                        "func": components.return_stage_context("df")(utils.get_data_from_worksheet),
                    },
                    {
                        "name": "Language detection and saving to sheet",
                        "func": detect_language_and_save,
                    },
                ],
                context={
                    "columns": [source_column],
                    "source_column": source_column,
                    "destination_column": destination_column,
                },
            )


def detect_language_and_save(
    worksheet: gspread.Worksheet, df: pd.DataFrame, source_column: str, destination_column: str
) -> None:
    """Detects the language of the text in the source column and saves it to the destination column.

    Args:
        worksheet (gspread.Worksheet): The Google Sheets worksheet.
        df (pd.DataFrame): The DataFrame containing the data from the worksheet.
        source_column (str): The name of the source column to detect language from.
        destination_column (str): The name of the destination column to save detected language.

    """
    worksheet.add_cols(1)
    destination_column_idx = len(worksheet.row_values(1)) + 1
    worksheet.update_cell(1, destination_column_idx, destination_column)
    counter = 2

    for language in components.progress_status(
        "Language detection and writing to sheet",
        total=len(df),
        func=detect_language,
        context={"data": df[source_column]},
    ):
        worksheet.update_cell(counter, destination_column_idx, language)
        counter += 1


def detect_language(data: pd.Series) -> Iterator[str]:
    """Detects the language of the text in the given data.

    Yields:
        str: The detected language in the format `language_name (language_code)`.

    """
    for text in data:
        lang_code = langdetect.detect(text)
        lang_name = langcodes.Language.get(lang_code).language_name()
        yield f"{lang_name} ({lang_code})"


if __name__ == "__main__":
    main()
