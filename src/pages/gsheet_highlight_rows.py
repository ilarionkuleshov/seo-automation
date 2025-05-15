import collections
import random
from typing import cast

import gspread
import gspread_formatting
import pandas as pd
import streamlit as st

import components
import utils


def main() -> None:
    """Displays page for highlighting rows in Google Sheets."""
    st.title("🎨 Highlight Rows")
    st.write(
        "This tool allows you to highlight rows in a Google Sheets document based on the values of a specific column. "
        "You can use this to visually group data in your spreadsheet."
    )
    st.write("Please note that the colors are generated randomly, but each group will have its own unique color.")
    components.example_image(
        "This is an example of how the rows will be highlighted based on the values in `Metric` column.",
        "src/images/examples/gsheet_highlight_rows.png",
    )

    with st.form(key="gsheet_highlight_rows"):
        worksheet_func = components.gsheet_selector()
        group_column = st.text_input(
            "Group column",
            help="The name of the column you want to group by. This column will determine the colors of the rows.",
        )
        submitted = st.form_submit_button("Highlight", type="primary")

    if submitted:
        if not worksheet_func or not group_column:
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
                        "name": "Data grouping and color generation",
                        "func": generate_color_groups,
                    },
                    {"name": "Range generation", "func": generate_color_ranges},
                    {"name": "Applying formatting", "func": apply_formatting},
                ],
                context={"group_column": group_column, "columns": [group_column]},
            )


@components.return_stage_context("color_groups")
def generate_color_groups(df: pd.DataFrame, group_column: str) -> dict[str, list[int]]:
    """Groups data and generates unique colors for each group.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be grouped.
        group_column (str): The name of the column to group by.

    Returns:
        dict[str, list[int]]: A dictionary where keys are unique colors and values are lists of row indices.

    """
    unique_colors = set()
    group_colors = {}

    for group in df[group_column].unique():
        while True:
            color = "#" + "".join(random.choice("89ABCDEF") for _ in range(6))
            if color not in unique_colors:
                unique_colors.add(color)
                group_colors[group] = color
                break

    color_groups = collections.defaultdict(list)
    for idx, row in df.iterrows():
        color = group_colors[row[group_column]]
        idx = cast(int, idx)
        # Add 2 to the index to account for the header row and 1-based indexing in Google Sheets.
        color_groups[color].append(idx + 2)

    return color_groups


@components.return_stage_context("color_ranges")
def generate_color_ranges(color_groups: dict[str, list[int]]) -> list[tuple[str, gspread_formatting.CellFormat]]:
    """Generates color ranges for batch updating in Google Sheets.

    Args:
        color_groups (dict[str, list[int]]): Groups of colors and their corresponding row indices.

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
                color_ranges.append((f"{start_row}:{end_row}", cell_format))
                start_row = current_row
                end_row = current_row

        color_ranges.append((f"{start_row}:{end_row}", cell_format))

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
        batch.format_cell_ranges(worksheet, color_ranges)  # pylint: disable=E1101


if __name__ == "__main__":
    main()
