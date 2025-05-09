import streamlit as st

import components


def main() -> None:
    """Displays the home page."""
    st.title("SEO Tools")
    st.write(
        "A suite of SEO tools, including automation for Google Sheets and keyword clustering features (coming soon)."
    )

    st.subheader("Google Sheets Tools")
    components.card_grid(
        [
            {
                "image": "src/images/preview_gsheet_highlight_rows.svg",
                "page": "pages/gsheet_highlight_rows.py",
                "label": "Highlight Rows",
                "icon": "🎨",
                "description": "Highlight rows in a Google Sheets document based on the values of a specific column.",
            },
        ]
    )
    # st.button(
    #     "How to get Google Sheets credentials",
    #     icon="🔑",
    #     use_container_width=True,
    #     on_click=show_credentials_info,
    # )


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
    main()
