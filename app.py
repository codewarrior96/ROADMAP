from __future__ import annotations

import html as html_module
import streamlit as st
from dotenv import load_dotenv


def _html_escape(text: str) -> str:
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)

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
    render_login_header,
    render_login_left_panel,
    render_login_center_logo,
)
from src.journey_overview import render_journey_overview_page
from src.design_system import inject_global_styles, get_role_theme, get_login_logo_data_url
from src.sidebar import render_sidebar
from src.state_manager import init_session_state
from src.auth_manager import is_logged_in, login_user, logout_user
from src.navigation_manager import (
    get_page,
    get_active_section,
    set_page,
    set_active_section,
    ensure_valid_section,
)


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

    # Sync role from Hedef ve Profil widget into session before sidebar/theme so first click applies immediately.
    if get_active_section() == "goal_and_profile" and "role_select_main" in st.session_state:
        role_name = st.session_state["role_select_main"]
        if role_name == "— Rol seçin —":
            st.session_state["selected_role_id"] = None
            st.session_state["selected_target_role"] = None
        else:
            role_options = {r.display_name: r.id for r in roles.values()}
            if role_name in role_options:
                rid = role_options[role_name]
                st.session_state["selected_role_id"] = rid
                st.session_state["selected_target_role"] = rid

    # 1) Login screen: centered premium login card
    if not is_logged_in():
        render_login_header()
        logo_src = get_login_logo_data_url()
        logo_img = (
            f'<img src="{logo_src}" alt="YolHaritam" class="login-logo-img">'
            if logo_src
            else ""
        )
        header_html = f"""
<div class="login-card-inner">
  <div class="login-logo-box">{logo_img}</div>
  <h1 class="login-brand-name">YolHaritam</h1>
  <p class="login-tagline">Rotanı keşfet, yolculuğunu planla</p>
</div>
"""
        st.markdown(header_html, unsafe_allow_html=True)
        if st.session_state.get("login_error"):
            st.error(st.session_state["login_error"])
        username = st.text_input("E-posta", value="demo@YolHaritam.com", placeholder="ornek@email.com")
        password = st.text_input("Şifre", type="password", value="123456", placeholder="••••••")
        st.markdown('<a href="#" class="login-forgot-link">Forgot password?</a>', unsafe_allow_html=True)
        if st.button("Giriş Yap", use_container_width=True, type="primary"):
            if username.strip().lower() in ("demo@yolharitam.com", "demo@yolharitam.com", "demo") and password == "123456":
                login_user()
            else:
                st.session_state["login_error"] = "Geçersiz kullanıcı adı/e-posta veya şifre."
        st.markdown(
            """
            <div class="login-divider"><span>or continue with</span></div>
            <div class="login-social-buttons">
            <button type="button" class="login-social-btn" aria-label="Google">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Google
            </button>
            <button type="button" class="login-social-btn" aria-label="GitHub">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .32.21.694.825.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
            GitHub
            </button>
            <button type="button" class="login-social-btn" aria-label="Apple">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
            Apple
            </button>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="yh-login-demo">'
            '<div class="demo-label">Demo Account</div>'
            'E-posta: <strong>demo@YolHaritam.com</strong><br>'
            'Şifre: <strong>123456</strong>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="login-register">Don\'t have an account? <a href="#">Sign Up</a></p>',
            unsafe_allow_html=True,
        )
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
            from src.onboarding_ui import get_growth_stage_from_levels
            _, growth_label, growth_desc = get_growth_stage_from_levels(current_levels)
            st.session_state["growth_stage"] = growth_label
            st.session_state["growth_stage_description"] = growth_desc
            st.session_state["active_plan_name"] = f"{role.display_name} Yol Haritası"
            st.session_state["selected_target_role"] = selected_role_id
            st.session_state["selected_weekly_tempo"] = weekly_hours
            st.session_state["selected_plan_duration"] = duration_weeks
            st.session_state["onboarding_completed"] = True
            st.session_state["main_career_goal"] = st.session_state.get("career_goal", "") or f"Junior seviyeye ulaşıp {role.display_name} olarak çalışmak."
            st.session_state["derived_profile_summary"] = f"{role.display_name} hedefine ilerlerken {growth_label} aşamasındasın."
            set_page("dashboard")
            set_active_section("journey_summary")
            st.success("Planın hazır. Yolculuk özetine yönlendiriliyorsun.")
            st.rerun()

        return

    # 3) Logged in, onboarding done: show dashboard. Only correct section if missing/invalid.
    if get_page() != "dashboard":
        set_page("dashboard")
    selected_role_id = st.session_state.get("selected_role_id")
    if selected_role_id is not None:
        st.session_state["selected_target_role"] = selected_role_id
    if st.session_state.get("weekly_hours") is not None and st.session_state.get("selected_weekly_tempo") is None:
        st.session_state["selected_weekly_tempo"] = st.session_state["weekly_hours"]
    if st.session_state.get("num_weeks") is not None and st.session_state.get("selected_plan_duration") is None:
        st.session_state["selected_plan_duration"] = st.session_state["num_weeks"]
    inject_global_styles(selected_role_id)
    render_sidebar(roles, selected_role_id)

    # Validate section once before routing so invalid/stale ids cannot break rendering.
    section = ensure_valid_section()
    if section == "journey_summary":
        render_journey_overview_page(roles, skills)
    elif section == "goal_and_profile":
        new_role_id, weekly_hours, duration_weeks, current_levels, submitted = render_profile_page(
            roles, skills, modules
        )

        # Idempotent: same role re-selection keeps same state; single canonical key.
        st.session_state["selected_role_id"] = new_role_id
        st.session_state["selected_target_role"] = new_role_id
        st.session_state["weekly_hours"] = weekly_hours
        st.session_state["num_weeks"] = duration_weeks

        if submitted and new_role_id is not None:
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
            set_active_section("learning_roadmap")
            st.rerun()
        elif submitted and new_role_id is None:
            st.warning("Lütfen önce bir hedef rol seçin.")
    elif section == "skill_gap":
        gap_result = st.session_state.get("analysis_result")
        render_gap_analysis_page(gap_result, skills)
    elif section == "learning_roadmap":
        weeks = st.session_state.get("weekly_plan")
        explanation = st.session_state.get("explanation")
        gap_result = st.session_state.get("analysis_result")
        render_roadmap_page(weeks, explanation, gap_result, skills)


if __name__ == "__main__":
    main()

