import json

import requests
import streamlit as st
from cryptography.fernet import Fernet
from google_auth_oauthlib.flow import Flow
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg  # pylint: disable=E0611
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx as _get_script_run_ctx,
)
from streamlit_cookies_controller import CookieController


def get_user() -> dict[str, str] | None:
    """Retrieves the user information from cookies or Google OAuth flow.

    Returns:
        dict[str, str] | None: The user information if available, otherwise None.

    """
    user = CookieController().get("user")
    if user:
        return decrypt_user(user)

    if "code" in st.query_params:
        flow = get_google_auth_flow()
        try:
            token = flow.fetch_token(code=st.query_params["code"])
        except Exception:  # pylint: disable=W0718
            st.warning(
                "The app needs you to give all the Google permissions it requests. "
                "Otherwise, the app won't be able to work with your Google Sheets documents. "
                "The app doesn't ask for more permissions than it needs - only the necessary ones.",
                icon="⚠️",
            )
            return None
        finally:
            st.query_params.clear()

        user = get_user_info(token["access_token"])
        if not user:
            st.warning(
                "Something went wrong while trying to get your user information. Please try again.",
                icon="⚠️",
            )
            return None

        user["refresh_token"] = token["refresh_token"]
        CookieController().set(
            name="user",
            value=encrypt_user(user),
            max_age=token["refresh_token_expires_in"] - 200,
            secure=True,
        )
        return user

    return None


def logout() -> None:
    """Logs out the user by removing the user cookie."""
    CookieController().remove("user", secure=True)


def login() -> None:
    """Initiates the Google OAuth flow for user authentication."""
    flow = get_google_auth_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    context = _get_script_run_ctx()
    if context is not None:
        msg = ForwardMsg()
        msg.auth_redirect.url = auth_url
        context.enqueue(msg)


def encrypt_user(user: dict[str, str]) -> str:
    """Returns the encrypted user information as a string.

    Args:
        user (dict[str, str]): The user information to encrypt.

    """
    user_json = json.dumps(user)
    fernet = Fernet(st.secrets["cookies_fernet_key"])
    return fernet.encrypt(user_json.encode()).decode()


def decrypt_user(user: str) -> dict[str, str]:
    """Returns the decrypted user information as a dictionary.

    Args:
        user (str): The encrypted user information to decrypt.

    """
    fernet = Fernet(st.secrets["cookies_fernet_key"])
    user_json = fernet.decrypt(user).decode()
    return json.loads(user_json)


def get_user_info(access_token: str) -> dict[str, str] | None:
    """Retrieves user information from Google API using the access token.

    Args:
        access_token (str): The access token to authenticate the request.

    Returns:
        dict[str, str] | None: The user information if available, otherwise None.

    """
    response = requests.get(
        url="https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=60,
    )
    if response.status_code == 200:
        data = response.json()
        return {
            "email": data["email"],
            "name": data["name"],
        }
    return None


def get_google_auth_flow() -> Flow:
    """Returns Google OAuth flow object for authentication."""
    return Flow.from_client_config(
        json.loads(st.secrets["google_oauth_client_config"]),
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
        redirect_uri=st.secrets["app_url"],
    )
