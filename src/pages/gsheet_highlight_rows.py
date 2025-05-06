"""Page for highlighting rows in Google Sheets."""

import collections
import json
import random
from typing import cast

import gspread
import gspread_formatting
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def format_sheet() -> None:
    """Formats a Google Sheets document by highlighting rows based on a specific column's values."""
    with st.status("Extracting data...", expanded=True) as status:
        try:
            worksheet = get_worksheet()
            df = pd.DataFrame(worksheet.get_all_records())
            st.write("Data extracted")

            status.update(label="Grouping data and generating colors...")
            color_groups = generate_color_groups(df)
            st.write("Data grouped and colors generated")

            status.update(label="Generating color ranges...")
            max_column_letter = chr(ord("A") + worksheet.col_count - 1)
            color_ranges = generate_color_ranges(color_groups, max_column_letter)
            st.write("Color ranges generated")

            status.update(label="Applying formatting...")
            apply_formatting(worksheet, color_ranges)
            st.write("Formatting applied")

            status.update(label="Formatting completed successfully!", state="complete", expanded=False)
        except Exception:
            status.update(label="An error occurred while processing the sheet.", state="error", expanded=False)
            raise


def get_worksheet() -> gspread.Worksheet:
    """Returns a gspread worksheet object based on the provided credentials and document URL."""
    credentials_file: UploadedFile = st.session_state["credentials_file"]
    credentials = json.loads(credentials_file.getvalue().decode("utf-8"))
    client = gspread.service_account_from_dict(credentials)

    sheet = client.open_by_url(st.session_state["document_url"])
    return sheet.worksheet(st.session_state["worksheet_name"])


def get_random_color() -> str:
    """Returns a random hex color code."""
    return "#" + "".join(random.choice("89ABCDEF") for _ in range(6))


def generate_color_groups(df: pd.DataFrame) -> dict[str, list[int]]:
    """Groups data and generates unique colors for each group.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be grouped.

    Returns:
        dict[str, list[int]]: A dictionary where keys are unique colors and values are lists of row indices.

    """
    unique_colors = set()
    group_colors = {}
    group_column: str = st.session_state["group_column"]

    for group in df[group_column].unique():
        while True:
            color = get_random_color()
            if color not in unique_colors:
                unique_colors.add(color)
                group_colors[group] = color
                break

    color_groups = collections.defaultdict(list)
    for idx, row in df.iterrows():
        color = group_colors[row[group_column]]
        idx = cast(int, idx)
        color_groups[color].append(idx + 2)

    return color_groups


def generate_color_ranges(
    color_groups: dict[str, list[int]], max_column_letter: str
) -> list[tuple[str, gspread_formatting.CellFormat]]:
    """Generates color ranges for batch updating in Google Sheets.

    Args:
        color_groups (dict[str, list[int]]): Groups of colors and their corresponding row indices.
        max_column_letter (str): The letter of the last column in the worksheet.

    Returns:
        list[tuple[str, gspread_formatting.CellFormat]]: A list of tuples where each tuple
            contains a cell range and its format.

    """
    color_ranges = []

    for color, rows in color_groups.items():
        cell_format = gspread_formatting.CellFormat(backgroundColor=gspread_formatting.Color.fromHex(color))

        start_row = rows[0]
        end_row = start_row
        for current_row in rows[1:]:
            if current_row == end_row + 1:
                end_row = current_row
            else:
                color_ranges.append((f"A{start_row}:{max_column_letter}{end_row}", cell_format))
                start_row = current_row
                end_row = current_row

        color_ranges.append((f"A{start_row}:{max_column_letter}{end_row}", cell_format))

    return color_ranges


def apply_formatting(
    worksheet: gspread.Worksheet, color_ranges: list[tuple[str, gspread_formatting.CellFormat]]
) -> None:
    """Applies formatting to the worksheet using batch updates.

    Args:
        worksheet (gspread.Worksheet): The worksheet to apply formatting to.
        color_ranges (list[tuple[str, gspread_formatting.CellFormat]]): Cell ranges and their formats.

    """
    with gspread_formatting.batch_updater(worksheet.spreadsheet) as batch:
        for cell_range, cell_format in color_ranges:
            batch.format_cell_range(worksheet, cell_range, cell_format)  # pylint: disable=E1101


@st.dialog("Example of result")
def show_example() -> None:
    """Shows example of result."""
    st.write("This is an example of how the rows will be highlighted based on the values in `Metric` column.")
    st.image("images/example_gsheet_highlight_rows.png")


@st.dialog("How to get Google Sheets credentials")
def show_credentials_info() -> None:
    """Shows information on how to get credentials."""
    st.write("To get the Google Sheets credentials, follow these steps:")
    st.write(
        "1. Go to the [Google Cloud Console](https://console.cloud.google.com/).\n"
        "2. Create a new project or select an existing one.\n"
        "3. Enable the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) "
        "for your project.\n"
        "4. Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) "
        "and create service account credentials.\n"
        "5. Download the JSON file and upload it here."
    )
    st.write(
        "For more detailed instructions, see "
        "[Google Cloud documentation](https://cloud.google.com/iam/docs/service-accounts-create)."
    )


if __name__ == "__main__":
    st.title("🎨 Google Sheets - Highlight Rows")
    st.write(
        "This tool allows you to highlight rows in a Google Sheets document based on a specific column's values. "
        "You can use this to visually group data in your spreadsheet."
    )
    st.write("Please note that the colors are generated randomly, but each group will have its own unique color.")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Example of result", icon="🖼", on_click=show_example, use_container_width=True)
    with col2:
        st.button(
            "How to get Google Sheets credentials", icon="🔑", on_click=show_credentials_info, use_container_width=True
        )

    with st.form(key="gsheet_highlight_rows", border=True):
        st.file_uploader(
            "Upload your Google Sheets JSON credentials",
            help="Your service account JSON file. If you don't have it, see the instructions above.",
            type=["json"],
            key="credentials_file",
        )
        st.text_input(
            "Document URL",
            help="The URL of the Google Sheets document you want to format. Make sure you have edit access.",
            key="document_url",
        )
        st.text_input(
            "Worksheet name",
            help="The name of the worksheet you want to format. This is the tab name at the bottom of the sheet.",
            key="worksheet_name",
        )
        st.text_input(
            "Group column",
            help="The name of the column you want to group by. This column will determine the colors of the rows.",
            key="group_column",
        )
        submitted = st.form_submit_button("Format", type="primary")

    if submitted:
        if (
            not st.session_state["credentials_file"]
            or not st.session_state["document_url"]
            or not st.session_state["worksheet_name"]
            or not st.session_state["group_column"]
        ):
            st.warning("Please fill in all fields.", icon="⚠️")
        else:
            format_sheet()
