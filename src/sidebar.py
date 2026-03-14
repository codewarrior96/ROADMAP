"""
Premium app sidebar: single coherent surface.
Structure: brand → profile card (avatar + photo icon) → quick actions → nav → footer.
"""
from __future__ import annotations

import base64
import html as html_module

import streamlit as st

from .design_system import get_role_theme, generate_avatar_initials
from .navigation_manager import (
    get_active_section,
    set_active_section,
    SECTION_IDS,
    SECTION_LABELS,
    SECTION_LABEL_TO_ID,
)
from .auth_manager import logout_user


def _escape(text: str) -> str:
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


def _inject_sidebar_styles(theme: dict) -> None:
    primary = theme["primary"]
    css = f"""
<style>
/* ===== New premium sidebar system ===== */
[data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(180deg, #0b1220 0%, #0f172a 50%, #111827 100%) !important;
}}
.sb-brand {{
    padding: 0.75rem 0 0.85rem 0;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid rgba(71,85,105,0.35);
}}
.sb-brand-text {{
    font-size: 1.125rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}}
.sb-brand-icon {{ opacity: 0.9; margin-right: 0.35rem; }}

.sb-profile-card {{
    background: rgba(30,41,59,0.4);
    border: 1px solid rgba(71,85,105,0.4);
    border-radius: 12px;
    padding: 0.9rem 0.95rem;
    margin-bottom: 0.9rem;
}}
.sb-avatar-row {{
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 0.25rem;
    margin-bottom: 0.6rem;
}}
.sb-avatar-wrap {{
    position: relative;
    width: 56px;
    height: 56px;
    flex-shrink: 0;
}}
.sb-avatar {{
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    background: {primary}22;
    border: 2px solid {primary}35;
    overflow: hidden;
}}
.sb-avatar img {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}}
.sb-avatar-btn-wrap {{
    position: absolute;
    bottom: -4px;
    right: -4px;
}}
.sb-avatar-btn-wrap .stButton > button {{
    width: 24px !important;
    min-width: 24px !important;
    height: 24px !important;
    padding: 0 !important;
    font-size: 0.7rem !important;
    border-radius: 50% !important;
    background: rgba(30,41,59,0.95) !important;
    border: 1px solid rgba(71,85,105,0.7) !important;
    color: #e2e8f0 !important;
}}
.sb-avatar-btn-wrap .stButton > button:hover {{
    background: rgba(51,65,85,0.95) !important;
    border-color: {primary}50 !important;
}}
.sb-name {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
    text-align: center;
}}
.sb-role {{
    font-size: 0.75rem;
    color: {primary};
    font-weight: 500;
    margin-bottom: 0.35rem;
    text-align: center;
}}
.sb-plan {{
    font-size: 0.6875rem;
    color: #64748b;
    margin-bottom: 0.45rem;
    text-align: center;
}}
.sb-stage {{
    background: rgba(71,85,105,0.3);
    border-radius: 8px;
    padding: 0.55rem 0.7rem;
}}
.sb-stage-label {{
    font-size: 0.5625rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 0.1rem;
}}
.sb-stage-name {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {primary};
}}
.sb-stage-desc {{
    font-size: 0.6875rem;
    font-weight: 400;
    color: #94a3b8;
    margin-top: 0.2rem;
    line-height: 1.3;
}}

.sb-section {{
    margin-top: 0.9rem;
    margin-bottom: 0.45rem;
}}
.sb-section-label {{
    font-size: 0.5625rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-bottom: 0.35rem;
    padding-left: 0.25rem;
}}
.sb-actions-row {{
    display: flex;
    gap: 0.35rem;
}}
.sb-actions-row .stButton > button {{
    flex: 1;
    font-size: 0.75rem !important;
    padding: 0.38rem 0.5rem !important;
    border-radius: 8px !important;
    background: rgba(71,85,105,0.35) !important;
    border: 1px solid rgba(71,85,105,0.5) !important;
    color: #94a3b8 !important;
}}
.sb-actions-row .stButton > button:hover {{
    background: rgba(71,85,105,0.5) !important;
    border-color: {primary}35 !important;
    color: #e2e8f0 !important;
}}

.sb-nav .stRadio > div {{
    gap: 0.25rem !important;
}}
.sb-nav .stRadio > label {{
    font-size: 0.5625rem !important;
    color: #64748b !important;
}}
.sb-nav .stRadio > div > label {{
    font-size: 0.8125rem !important;
    padding: 0.5rem 0.65rem !important;
    border-radius: 8px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #94a3b8 !important;
}}
.sb-nav .stRadio > div > label:hover {{
    background: rgba(71,85,105,0.35) !important;
    color: #e2e8f0 !important;
}}
.sb-nav .stRadio > div > label[data-checked="true"] {{
    background: {primary}20 !important;
    border-color: {primary}35 !important;
    color: #f1f5f9 !important;
}}

.sb-footer {{
    margin-top: 1.25rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(71,85,105,0.35);
}}
.sb-footer .stButton > button {{
    font-size: 0.8125rem !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 8px !important;
    background: transparent !important;
    border: 1px solid rgba(248,113,113,0.35) !important;
    color: #fca5a5 !important;
}}
.sb-footer .stButton > button:hover {{
    background: rgba(248,113,113,0.08) !important;
    border-color: rgba(248,113,113,0.5) !important;
}}

.sb-upload-area {{
    margin-bottom: 0.5rem;
    padding: 0.5rem 0;
}}
.sb-upload-area .stFileUploader {{
    font-size: 0.75rem;
}}
@media (max-width: 640px) {{
    .sb-profile-card {{ padding: 0.75rem; }}
    .sb-avatar {{ width: 48px; height: 48px; font-size: 1rem; }}
    .sb-avatar-wrap {{ width: 48px; height: 48px; }}
}}
</style>
"""
    st.sidebar.markdown(css, unsafe_allow_html=True)


def render_sidebar(
    roles: dict,
    selected_role_id: str | None,
) -> None:
    """
    Render the full app sidebar: brand, profile card (with avatar photo action),
    quick actions, navigation, footer. Reads/writes session state as needed.
    """
    theme = get_role_theme(selected_role_id)
    _inject_sidebar_styles(theme)

    user_name = st.session_state.get("user_name", "Kullanıcı")
    user_avatar = st.session_state.get("user_avatar")
    role_obj = roles.get(selected_role_id) if selected_role_id else None
    role_display_name = role_obj.display_name if role_obj else None
    role_text = role_display_name or "Henüz seçilmedi"
    active_plan = st.session_state.get("active_plan_name") or (f"{role_display_name} Yol Haritası" if role_display_name else "—")
    growth_stage = st.session_state.get("growth_stage") or "—"
    growth_stage_description = st.session_state.get("growth_stage_description") or "Hedef ve Profil sayfasından beceri durumunu işaretle."

    # —— 1) Top brand ——
    st.sidebar.markdown(
        '<div class="sb-brand">'
        '<span class="sb-brand-text"><span class="sb-brand-icon">🧭</span>YolHaritam</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # —— 2) Compact profile card (avatar + photo icon attached) ——
    if user_avatar:
        avatar_content = f'<img src="{user_avatar}" alt="Avatar">'
    else:
        initials = generate_avatar_initials(user_name)
        avatar_content = f'<span>{_escape(initials)}</span>'

    safe_name = _escape(user_name)
    safe_role = _escape(role_text)
    safe_plan = _escape(active_plan)
    safe_stage = _escape(growth_stage)
    safe_stage_desc = _escape(growth_stage_description)

    col_card, col_photo = st.sidebar.columns([5, 1])
    with col_card:
        st.markdown(
            "<div class=\"sb-profile-card\">"
            "<div class=\"sb-avatar-row\">"
            "<div class=\"sb-avatar-wrap\">"
            "<div class=\"sb-avatar\">" + avatar_content + "</div>"
            "</div>"
            "</div>"
            "<div class=\"sb-name\">" + safe_name + "</div>"
            "<div class=\"sb-role\">" + safe_role + "</div>"
            "<div class=\"sb-plan\">Aktif Plan — " + safe_plan + "</div>"
            "<div class=\"sb-stage\">"
            "<div class=\"sb-stage-label\">Gelişim Aşaması</div>"
"<div class=\"sb-stage-name\">" + safe_stage + "</div>"
        "<div class=\"sb-stage-desc\">" + safe_stage_desc + "</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with col_photo:
        if st.button("📷", key="avatar_edit_btn", help="Profil fotoğrafı değiştir"):
            st.session_state["show_avatar_panel"] = not st.session_state.get("show_avatar_panel", False)
            st.rerun()

    # Upload panel (only when triggered from avatar icon)
    if st.session_state.get("show_avatar_panel", False):
        st.sidebar.markdown('<div class="sb-upload-area">', unsafe_allow_html=True)
        uploaded_file = st.sidebar.file_uploader(
            "Fotoğraf seç",
            type=["png", "jpg", "jpeg"],
            key="avatar_file_upload",
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            avatar_bytes = uploaded_file.read()
            avatar_b64 = base64.b64encode(avatar_bytes).decode()
            mime_type = uploaded_file.type
            st.session_state["user_avatar"] = f"data:{mime_type};base64,{avatar_b64}"
            st.session_state["show_avatar_panel"] = False
            st.rerun()
        if user_avatar and st.button("Kaldır", key="avatar_remove_btn", use_container_width=True):
            st.session_state["user_avatar"] = None
            st.session_state["show_avatar_panel"] = False
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # —— 3) Quick actions ——
    st.sidebar.markdown('<div class="sb-section"><div class="sb-section-label">Hızlı İşlemler</div></div>', unsafe_allow_html=True)
    ac1, ac2 = st.sidebar.columns(2)
    with ac1:
        if st.button("Profil", key="edit_profile_btn", use_container_width=True):
            st.session_state["show_profile_edit"] = not st.session_state.get("show_profile_edit", False)
            st.rerun()
    with ac2:
        if st.button("Hedef", key="change_goal_btn", use_container_width=True):
            st.session_state["show_profile_edit"] = not st.session_state.get("show_profile_edit", False)
            st.rerun()

    if st.session_state.get("show_profile_edit", False):
        with st.sidebar.expander("Profil Düzenle", expanded=True):
            new_name = st.text_input("Adın", value=user_name, key="profile_name_input")
            new_goal = st.text_area(
                "Kariyer Hedefin",
                value=st.session_state.get("career_goal", ""),
                placeholder="Örn: Junior AI Engineer olarak bir teknoloji şirketinde çalışmak",
                key="profile_goal_input",
            )
            if st.button("Kaydet", key="save_profile_btn"):
                st.session_state["user_name"] = new_name
                st.session_state["career_goal"] = new_goal
                st.session_state["show_profile_edit"] = False
                st.rerun()

    # —— 4) Navigation (updates active_section only; does not touch login or page) ——
    st.sidebar.markdown('<div class="sb-section"><div class="sb-section-label">Gezinti</div></div>', unsafe_allow_html=True)
    section = get_active_section()
    if section not in SECTION_IDS:
        section = "journey_summary"
        set_active_section(section)
    current_index = SECTION_IDS.index(section)

    def on_nav_change():
        selected_label = st.session_state.get("_nav_selection")
        section_id = SECTION_LABEL_TO_ID.get(selected_label, "journey_summary")
        set_active_section(section_id)

    st.sidebar.markdown('<div class="sb-nav">', unsafe_allow_html=True)
    st.sidebar.radio(
        "Sayfa",
        options=SECTION_LABELS,
        index=current_index,
        label_visibility="collapsed",
        key="_nav_selection",
        on_change=on_nav_change,
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # —— 5) Footer ——
    st.sidebar.markdown('<div class="sb-footer">', unsafe_allow_html=True)
    if st.sidebar.button("Çıkış Yap", use_container_width=True, key="sidebar_logout_btn"):
        logout_user()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
