import streamlit as st

import components


def main() -> None:
    """Displays the home page."""
    st.title("SEO Tools")
    st.write(
        "A suite of SEO tools, including automation for Google Sheets and keyword clustering features (coming soon)."
    )

    st.subheader("Google Sheets")
    components.card_grid(
        [
            {
                "image": "src/images/previews/gsheet_highlight_rows.svg",
                "page": "pages/gsheet_highlight_rows.py",
                "label": "Highlight Rows",
                "icon": "🎨",
                "description": "Highlight rows in a Google Sheets document based on the values of a specific column.",
            },
        ]
    )


if __name__ == "__main__":
    main()
