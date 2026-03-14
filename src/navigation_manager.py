"""
Navigation state: page (login vs dashboard) and active_section (dashboard tab).
Sidebar only updates active_section; it does not overwrite login or page state.
"""
from __future__ import annotations

import streamlit as st


# Dashboard section ids and their display labels (for sidebar radio).
SECTION_IDS = ["journey_summary", "goal_and_profile", "skill_gap", "learning_roadmap"]
SECTION_LABELS = [
    "Yolculuk Özeti",
    "Hedef ve Profil",
    "Beceri Boşluğu Analizi",
    "Öğrenme Yol Haritası",
]
SECTION_ID_TO_LABEL = dict(zip(SECTION_IDS, SECTION_LABELS))
SECTION_LABEL_TO_ID = dict(zip(SECTION_LABELS, SECTION_IDS))


def set_page(page: str) -> None:
    """Set top-level page: 'login' or 'dashboard'."""
    st.session_state["current_page"] = page


def get_page() -> str:
    """Current top-level page: 'login' or 'dashboard'."""
    return st.session_state.get("current_page", "login")


def set_active_section(section_id: str) -> None:
    """Set dashboard section (e.g. 'journey_summary'). Only affects dashboard content."""
    if section_id in SECTION_IDS:
        st.session_state["active_section"] = section_id


def ensure_valid_section() -> str:
    """
    Ensure active_section exists and is one of the valid SECTION_IDS.
    If missing or invalid, reset to 'journey_summary'.
    Returns the final valid section id.
    """
    current = st.session_state.get("active_section")
    if current not in SECTION_IDS:
        current = "journey_summary"
        st.session_state["active_section"] = current
    return current


def get_active_section() -> str:
    """
    Current dashboard section id (e.g. 'journey_summary').
    Always validated via ensure_valid_section so callers never see an invalid id.
    """
    return ensure_valid_section()


def get_active_section_label() -> str:
    """Display label for current section (e.g. 'Yolculuk Özeti')."""
    return SECTION_ID_TO_LABEL.get(get_active_section(), SECTION_LABELS[0])


def get_section_options() -> list[tuple[str, str]]:
    """List of (section_id, label) for sidebar nav."""
    return list(zip(SECTION_IDS, SECTION_LABELS))
