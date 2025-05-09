"""Main entry point for the Streamlit app."""

import streamlit as st


def main() -> None:
    """Main function to run the Streamlit app."""
    st.logo(image="src/images/logo.svg", icon_image="src/images/logo_icon.svg", size="large")
    page = st.navigation(
        [
            st.Page(
                page="pages/home.py",
                title="Home",
                icon="🏡",
                default=True,
            ),
            st.Page(
                page="pages/gsheet_highlight_rows.py",
                title="Google Sheets - Highlight Rows",
                icon="🎨",
                url_path="/gsheet-highlight-rows",
            ),
        ]
    )
    page.run()


if __name__ == "__main__":
    main()
