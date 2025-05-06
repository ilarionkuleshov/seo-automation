"""Main entry point for the Streamlit app."""

import streamlit as st

# with st.sidebar:
#     st.title("SEO Tools")


page = st.navigation(
    [
        st.Page(
            page="pages/gsheet_highlight_rows.py",
            title="Google Sheets - Highlight Rows",
            icon="🎨",
            url_path="/gsheet-highlight-rows",
            default=True,
        ),
    ]
)
page.run()
