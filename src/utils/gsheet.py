import gspread
import pandas as pd


def get_data_from_worksheet(worksheet: gspread.Worksheet, columns: list[str]) -> pd.DataFrame:
    """Returns data from a Google Sheets worksheet.

    Args:
        worksheet (gspread.Worksheet): The worksheet to get data from.
        columns (list[str]): The columns to retrieve.

    """
    all_columns = worksheet.row_values(1)
    column_indexes = [all_columns.index(column) + 1 for column in columns]

    data = {}
    for col_name, col_index in zip(columns, column_indexes):
        data[col_name] = worksheet.col_values(col_index)[1:]

    return pd.DataFrame(data)
