from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from src.data_loader import load_all
from src.algorithm import analyze_gaps, GapAnalysisResult
from src.planner import build_weekly_plan, WeekPlan
from src.explainer import generate_deterministic_explanation, generate_explanation_with_llm
from src.ui_helpers import (
    render_app_header,
    render_profile_page,
    render_gap_analysis_page,
    render_roadmap_page,
    render_onboarding_page,
    render_dashboard_page,
    render_login_header,
)
from src.design_system import inject_global_styles, get_role_theme, generate_avatar_initials
import base64


def init_session_state() -> None:
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "weekly_plan" not in st.session_state:
        st.session_state["weekly_plan"] = None
    if "explanation" not in st.session_state:
        st.session_state["explanation"] = None
    if "selected_role_id" not in st.session_state:
        st.session_state["selected_role_id"] = None
    if "weekly_hours" not in st.session_state:
        st.session_state["weekly_hours"] = 8.0
    if "num_weeks" not in st.session_state:
        st.session_state["num_weeks"] = 4
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if "has_onboarded" not in st.session_state:
        st.session_state["has_onboarded"] = True
    if "login_error" not in st.session_state:
        st.session_state["login_error"] = ""
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "Kullanıcı"
    if "user_avatar" not in st.session_state:
        st.session_state["user_avatar"] = None
    if "career_goal" not in st.session_state:
        st.session_state["career_goal"] = ""
    if "growth_stage" not in st.session_state:
        st.session_state["growth_stage"] = None
    if "growth_stage_description" not in st.session_state:
        st.session_state["growth_stage_description"] = None
    if "active_plan_name" not in st.session_state:
        st.session_state["active_plan_name"] = None
    if "show_profile_edit" not in st.session_state:
        st.session_state["show_profile_edit"] = False
    if "show_avatar_panel" not in st.session_state:
        st.session_state["show_avatar_panel"] = False
    if "avatar_path" not in st.session_state:
        st.session_state["avatar_path"] = None
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Kontrol Paneli"


def main() -> None:
    load_dotenv(override=False)
    st.set_page_config(
        page_title="YolHaritam",
        page_icon="🧭",
        layout="wide",
    )

    init_session_state()

    data = load_all()
    skills = data["skills"]
    roles = data["roles"]
    modules = data.get("modules", [])

    # 1) Giriş ekranı
    if not st.session_state.get("is_authenticated", False):
        render_login_header()

        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            if st.session_state.get("login_error"):
                st.error(st.session_state["login_error"])

            username = st.text_input("E-posta", value="demo@YolHaritam.com", placeholder="ornek@email.com")
            password = st.text_input("Şifre", type="password", value="123456", placeholder="••••••")

            if st.button("Giriş Yap", use_container_width=True, type="primary"):
                if username.strip().lower() in ("demo@yolharitam.com", "demo@yolharitam.com", "demo") and password == "123456":
                    st.session_state["is_authenticated"] = True
                    st.session_state["login_error"] = ""
                    st.rerun()
                else:
                    st.session_state["login_error"] = "Geçersiz kullanıcı adı/e-posta veya şifre."

            st.markdown("""
<div class="yh-login-demo">
    Demo hesabı: <strong>demo@YolHaritam.com</strong> / <strong>123456</strong>
</div>
""", unsafe_allow_html=True)
        return

    # 2) Onboarding akışı (ilk girişte)
    if not st.session_state.get("has_onboarded", False):
        (
            selected_role_id,
            weekly_hours,
            duration_weeks,
            current_levels,
            submitted,
        ) = render_onboarding_page(roles, skills, modules)

        if submitted:
            st.session_state["selected_role_id"] = selected_role_id
            st.session_state["weekly_hours"] = weekly_hours
            st.session_state["num_weeks"] = duration_weeks

            role = roles[selected_role_id]
            gap_result: GapAnalysisResult = analyze_gaps(
                role=role,
                skills=skills,
                current_levels=current_levels,
            )
            weeks: list[WeekPlan] = build_weekly_plan(
                gap_result=gap_result,
                skills=skills,
                weekly_hours=weekly_hours,
                num_weeks=duration_weeks,
            )

            explanation = generate_explanation_with_llm(role, gap_result, weeks)
            if not explanation:
                explanation = generate_deterministic_explanation(role, gap_result, weeks)

            st.session_state["analysis_result"] = gap_result
            st.session_state["weekly_plan"] = weeks
            st.session_state["explanation"] = explanation
            st.session_state["has_onboarded"] = True

            st.success("Onboarding tamamlandı ve ilk yol haritanız oluşturuldu. Kontrol Paneli'ne yönlendiriliyorsunuz.")
            st.rerun()

        return

    # 3) Giriş yapmış ve onboarding'i tamamlamış kullanıcılar için ana gezinme
    selected_role_id = st.session_state.get("selected_role_id")
    inject_global_styles(selected_role_id)

    st.sidebar.markdown("""
<div style="padding: 0.5rem 0 1rem 0;">
    <div style="font-size: 1.4rem; font-weight: 700; background: linear-gradient(135deg, #f1f5f9, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🧭 YolHaritam
    </div>
</div>
""", unsafe_allow_html=True)

    user_name = st.session_state.get("user_name", "Kullanıcı")
    user_avatar = st.session_state.get("user_avatar")
    analysis_result = st.session_state.get("analysis_result")

    role_display_name = None
    readiness_pct = None

    if selected_role_id and selected_role_id in roles:
        role_display_name = roles[selected_role_id].display_name

    if analysis_result and analysis_result.skill_gaps:
        total_required = sum(g.required_level for g in analysis_result.skill_gaps)
        total_current = sum(g.current_level for g in analysis_result.skill_gaps)
        if total_required > 0:
            readiness_pct = min(95, max(5, int((total_current / total_required) * 100)))

    # ===== AVATAR COMPONENT WITH EDIT BADGE =====
    theme = get_role_theme(selected_role_id)

    # Generate avatar content
    if user_avatar:
        avatar_content = f'<img src="{user_avatar}" alt="Avatar">'
    else:
        initials = generate_avatar_initials(user_name)
        avatar_content = f'<span style="color: #f1f5f9; font-weight: 700;">{initials}</span>'

    role_text = role_display_name or "Henüz seçilmedi"
    growth_stage = st.session_state.get("growth_stage")
    growth_stage_description = st.session_state.get("growth_stage_description", "")

    # Profile card with avatar - CSS and HTML (Growth Stage instead of readiness bar)
    profile_css = f"""
<style>
.yh-profile-card {{
    background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,41,59,0.8) 100%);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 1rem;
    padding: 1.2rem 1rem;
    margin-bottom: 0.8rem;
    text-align: center;
}}
.yh-avatar-container {{
    position: relative;
    width: 72px;
    height: 72px;
    margin: 0 auto 0.8rem auto;
}}
.yh-profile-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border: 3px solid {theme['primary']}66;
    box-shadow: 0 4px 15px -3px {theme['primary']}44;
    overflow: hidden;
}}
.yh-profile-avatar img {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}}
.yh-avatar-badge {{
    position: absolute;
    bottom: 0;
    right: 0;
    width: 22px;
    height: 22px;
    background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
    border: 2px solid rgba(15,23,42,0.95);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    cursor: pointer;
}}
.yh-profile-name {{
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
}}
.yh-profile-role {{
    font-size: 0.8rem;
    color: {theme['primary']};
    margin-bottom: 0.6rem;
}}
.yh-profile-stage {{
    background: linear-gradient(135deg, {theme['primary']}18, {theme['secondary']}12);
    border: 1px solid {theme['primary']}44;
    border-radius: 0.6rem;
    padding: 0.6rem 0.8rem;
    text-align: left;
}}
.yh-profile-stage-label {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 0.2rem;
}}
.yh-profile-stage-name {{
    font-size: 0.85rem;
    font-weight: 600;
    color: {theme['primary']};
}}
.yh-profile-stage-desc {{
    font-size: 0.75rem;
    color: #94a3b8;
    margin-top: 0.35rem;
    line-height: 1.35;
}}
/* Avatar edit button styling */
.avatar-edit-trigger {{
    margin-top: -4px;
    margin-bottom: 4px;
}}
.avatar-edit-trigger .stButton > button {{
    background: transparent !important;
    border: none !important;
    padding: 2px 8px !important;
    font-size: 0.7rem !important;
    color: {theme['primary']} !important;
    opacity: 0.8;
}}
.avatar-edit-trigger .stButton > button:hover {{
    opacity: 1;
    text-decoration: underline;
}}
/* Compact upload panel */
.avatar-upload-panel {{
    background: rgba(15,23,42,0.95);
    border: 1px solid {theme['primary']}44;
    border-radius: 0.6rem;
    padding: 0.8rem;
    margin-bottom: 0.5rem;
}}
.avatar-upload-panel-title {{
    font-size: 0.75rem;
    color: #94a3b8;
    margin-bottom: 0.5rem;
    text-align: center;
}}
</style>
"""
    st.sidebar.markdown(profile_css, unsafe_allow_html=True)

    # Profile card HTML (Growth Stage badge; no percentage readiness)
    active_plan = st.session_state.get("active_plan_name") or (f"{role_display_name} Yol Haritası" if role_display_name else "—")
    stage_block = ""
    if growth_stage:
        stage_block = f"""
    <div class="yh-profile-stage">
        <div class="yh-profile-stage-label">Gelişim Aşaması</div>
        <div class="yh-profile-stage-name">{growth_stage}</div>
        <div class="yh-profile-stage-desc">{growth_stage_description}</div>
    </div>
"""
    else:
        stage_block = f"""
    <div class="yh-profile-stage">
        <div class="yh-profile-stage-label">Gelişim Aşaması</div>
        <div class="yh-profile-stage-name">—</div>
        <div class="yh-profile-stage-desc">Hedef ve Profil sayfasından beceri durumunu işaretle.</div>
    </div>
"""
    profile_html = f"""
<div class="yh-profile-card">
    <div class="yh-avatar-container">
        <div class="yh-profile-avatar">{avatar_content}</div>
        <div class="yh-avatar-badge">📷</div>
    </div>
    <div class="yh-profile-name">{user_name}</div>
    <div class="yh-profile-role">{role_text}</div>
    <div class="yh-profile-meta" style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem;">Aktif Plan — {active_plan}</div>
    {stage_block}
</div>
"""
    st.sidebar.markdown(profile_html, unsafe_allow_html=True)

    # Small text button to trigger avatar upload
    if st.sidebar.button("Fotoğraf değiştir", key="avatar_edit_btn", use_container_width=True):
        st.session_state["show_avatar_panel"] = not st.session_state.get("show_avatar_panel", False)

    # Compact avatar upload panel
    if st.session_state.get("show_avatar_panel", False):
        st.sidebar.markdown('<div class="avatar-upload-panel"><div class="avatar-upload-panel-title">Profil fotoğrafı yükle</div></div>', unsafe_allow_html=True)

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

        col_cancel, col_remove = st.sidebar.columns(2)
        with col_cancel:
            if st.button("İptal", key="avatar_cancel_btn", use_container_width=True):
                st.session_state["show_avatar_panel"] = False
                st.rerun()
        with col_remove:
            if user_avatar:
                if st.button("Kaldır", key="avatar_remove_btn", use_container_width=True):
                    st.session_state["user_avatar"] = None
                    st.session_state["show_avatar_panel"] = False
                    st.rerun()

    # Profile edit buttons
    col_edit, col_goal = st.sidebar.columns(2)
    with col_edit:
        if st.button("✏️ Profil", use_container_width=True, key="edit_profile_btn"):
            st.session_state["show_profile_edit"] = not st.session_state.get("show_profile_edit", False)
    with col_goal:
        if st.button("🎯 Hedef", use_container_width=True, key="change_goal_btn"):
            st.session_state["show_profile_edit"] = not st.session_state.get("show_profile_edit", False)

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

    st.sidebar.markdown("---")

    page_options = ["Kontrol Paneli", "Hedef ve Profil", "Beceri Boşluğu Analizi", "Öğrenme Yol Haritası"]
    current_page = st.session_state.get("current_page", "Kontrol Paneli")
    current_index = page_options.index(current_page) if current_page in page_options else 0

    def on_page_change():
        st.session_state["current_page"] = st.session_state["_nav_selection"]

    page = st.sidebar.radio(
        "Gezinti",
        options=page_options,
        index=current_index,
        label_visibility="collapsed",
        key="_nav_selection",
        on_change=on_page_change,
    )

    # Sync page variable with current_page state
    page = st.session_state.get("current_page", "Kontrol Paneli")

    st.sidebar.markdown("---")

    if st.sidebar.button("Çıkış Yap", use_container_width=True):
        st.session_state["is_authenticated"] = False
        st.session_state["has_onboarded"] = False
        st.session_state["login_error"] = ""
        st.session_state["analysis_result"] = None
        st.session_state["weekly_plan"] = None
        st.session_state["explanation"] = None
        st.session_state["selected_role_id"] = None
        st.session_state["user_name"] = "Kullanıcı"
        st.session_state["user_avatar"] = None
        st.session_state["career_goal"] = ""
        st.session_state["growth_stage"] = None
        st.session_state["growth_stage_description"] = None
        st.session_state["active_plan_name"] = None
        st.session_state["show_profile_edit"] = False
        st.session_state["show_avatar_panel"] = False
        st.session_state["avatar_path"] = None
        st.session_state["current_page"] = "Kontrol Paneli"
        st.rerun()

    if page == "Kontrol Paneli":
        render_dashboard_page(roles, skills, modules)

    elif page == "Hedef ve Profil":
        new_role_id, weekly_hours, duration_weeks, current_levels, submitted = render_profile_page(
            roles, skills, modules
        )

        st.session_state["selected_role_id"] = new_role_id
        st.session_state["weekly_hours"] = weekly_hours
        st.session_state["num_weeks"] = duration_weeks

        if submitted:
            role = roles[new_role_id]
            gap_result: GapAnalysisResult = analyze_gaps(
                role=role,
                skills=skills,
                current_levels=current_levels,
            )
            weeks: list[WeekPlan] = build_weekly_plan(
                gap_result=gap_result,
                skills=skills,
                weekly_hours=weekly_hours,
                num_weeks=duration_weeks,
            )

            explanation = generate_explanation_with_llm(role, gap_result, weeks)
            if not explanation:
                explanation = generate_deterministic_explanation(role, gap_result, weeks)

            st.session_state["analysis_result"] = gap_result
            st.session_state["weekly_plan"] = weeks
            st.session_state["explanation"] = explanation
            from src.onboarding_ui import get_growth_stage_from_levels
            _, growth_label, growth_desc = get_growth_stage_from_levels(current_levels)
            st.session_state["growth_stage"] = growth_label
            st.session_state["growth_stage_description"] = growth_desc
            st.session_state["active_plan_name"] = f"{role.display_name} Yol Haritası"

            st.success("Yol haritanız oluşturuldu! Yol Haritası sayfasına yönlendiriliyorsunuz...")
            st.session_state["current_page"] = "Öğrenme Yol Haritası"
            st.rerun()

    elif page == "Beceri Boşluğu Analizi":
        gap_result = st.session_state.get("analysis_result")
        render_gap_analysis_page(gap_result, skills)

    elif page == "Öğrenme Yol Haritası":
        weeks = st.session_state.get("weekly_plan")
        explanation = st.session_state.get("explanation")
        gap_result = st.session_state.get("analysis_result")
        render_roadmap_page(weeks, explanation, gap_result, skills)


if __name__ == "__main__":
    main()

