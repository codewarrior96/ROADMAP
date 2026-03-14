"""
Centralized session state: defaults, init, and full reset for logout.
Avatar state (show_avatar_panel, user_avatar) is isolated and not cleared by reset_app_state.
"""
from __future__ import annotations

import streamlit as st


# Default values for app session state (used at startup and for reference).
DEFAULTS = {
    "analysis_result": None,
    "weekly_plan": None,
    "explanation": None,
    "selected_role_id": None,
    "weekly_hours": 8.0,
    "num_weeks": 4,
    "is_authenticated": False,
    "has_onboarded": True,
    "login_error": "",
    "user_name": "Kullanıcı",
    "user_avatar": None,
    "career_goal": "",
    "growth_stage": None,
    "growth_stage_description": None,
    "active_plan_name": None,
    "selected_target_role": None,
    "selected_weekly_tempo": None,
    "selected_plan_duration": None,
    "onboarding_completed": False,
    "main_career_goal": "",
    "derived_profile_summary": "",
    "show_profile_edit": False,
    "show_avatar_panel": False,
    "avatar_path": None,
    "current_page": "login",
    "active_section": "journey_summary",
}


def init_session_state() -> None:
    """Initialize all session state keys at app startup. Only sets missing keys."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_app_state() -> None:
    """
    Full logout cleanup: clear user-flow state. Keeps has_onboarded True so
    re-login opens dashboard (no onboarding again). Avatar UI state is reset
    so sidebar is clean.
    """
    st.session_state["is_authenticated"] = False
    st.session_state["has_onboarded"] = True
    st.session_state["login_error"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["weekly_plan"] = None
    st.session_state["explanation"] = None
    st.session_state["selected_role_id"] = None
    st.session_state["user_name"] = "Kullanıcı"
    st.session_state["career_goal"] = ""
    st.session_state["growth_stage"] = None
    st.session_state["growth_stage_description"] = None
    st.session_state["active_plan_name"] = None
    st.session_state["selected_target_role"] = None
    st.session_state["selected_weekly_tempo"] = None
    st.session_state["selected_plan_duration"] = None
    st.session_state["onboarding_completed"] = False
    st.session_state["main_career_goal"] = ""
    st.session_state["derived_profile_summary"] = ""
    st.session_state["show_profile_edit"] = False
    st.session_state["current_page"] = "login"
    st.session_state["active_section"] = "journey_summary"
    # Avatar state intentionally not cleared here (isolated)
    # show_avatar_panel and user_avatar are left as-is or can be reset if desired
    st.session_state["show_avatar_panel"] = False
    st.session_state["user_avatar"] = None
    st.session_state["avatar_path"] = None
