"""Main entry point for the Streamlit app."""

import streamlit as st
from streamlit_cookies_controller import CookieController

import auth


def main() -> None:
    """Main function to run the Streamlit app."""
    st.logo(image="src/images/logo.svg", icon_image="src/images/logo_icon.svg", size="large")
    setup_cookies()
    page = st.navigation(
        {
            "": [
                st.Page(
                    page="pages/home.py",
                    title="Home",
                    icon="🏡",
                    default=True,
                )
            ],
            "Google Sheets": [
                st.Page(
                    page="pages/gsheet_highlight_rows.py",
                    title="Highlight Rows",
                    icon="🎨",
                    url_path="/gsheet-highlight-rows",
                ),
                st.Page(
                    page="pages/gsheet_detect_language.py",
                    title="Detect Language",
                    icon="🔍",
                    url_path="/gsheet-detect-language",
                ),
            ],
        }
    )
    user = auth.get_user()
    with st.sidebar:
        if user:
            with st.popover(user["name"], use_container_width=True, icon="👤"):
                st.write("You are logged in as", user["email"])
                st.button("Logout", icon="🚫", on_click=auth.logout, use_container_width=True)
        else:
            st.button("Login", icon="🔑", on_click=auth.login, use_container_width=True)
    st.session_state["user"] = user
    page.run()


def setup_cookies() -> None:
    """Sets up cookies for the app."""
    if not CookieController().getAll():
        st.stop()
    st.html(
        """<style>
            div[data-testid='element-container']:has(
                iframe[title='streamlit_cookies_controller.cookie_controller.cookie_controller']
            ) {
                display: none;
            }
        </style>"""
    )


if __name__ == "__main__":
    main()
