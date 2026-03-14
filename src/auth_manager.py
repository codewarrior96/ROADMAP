"""
Auth state: login, logout, and login check.
On login: set dashboard state and default section; rerun.
On logout: reset app state, set login page; rerun.
"""
from __future__ import annotations

import streamlit as st

from .state_manager import reset_app_state
from .navigation_manager import set_page, set_active_section


def is_logged_in() -> bool:
    """True if the user is authenticated."""
    return st.session_state.get("is_authenticated", False)


def login_user() -> None:
    """
    Call after successful login. Sets logged-in state, opens dashboard
    with default section (journey_summary), then reruns.
    """
    st.session_state["is_authenticated"] = True
    st.session_state["login_error"] = ""
    set_page("dashboard")
    set_active_section("journey_summary")
    st.rerun()


def logout_user() -> None:
    """
    Full logout: clear user-flow state, set page to login, then rerun.
    """
    reset_app_state()
    set_page("login")
    st.rerun()
