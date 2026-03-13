from __future__ import annotations

from typing import Dict, Tuple, Any, List

import pandas as pd
import plotly.express as px
import streamlit as st

from .algorithm import GapAnalysisResult, gaps_to_table
from .data_loader import Skill, Role, Module
from .planner import WeekPlan, weekly_plan_to_table
from .module_progress import (
    MODULE_STATES,
    get_module_state,
    get_category_progress,
    module_progress_to_skill_levels,
    get_overall_readiness_percentage,
)
from .visual_roadmap import render_visual_roadmap
from .design_system import (
    inject_global_styles,
    render_premium_header,
    render_login_screen,
    render_dashboard_cards,
    render_section_header,
    get_role_theme,
    get_dynamic_title,
    render_sidebar_profile,
    render_welcome_section,
    render_ai_recommendation_panel,
    render_career_goal_card,
    render_todays_task_card,
)


def render_app_header(role_id: str | None = None, role_display_name: str | None = None) -> None:
    inject_global_styles(role_id)


def render_login_header() -> None:
    inject_global_styles(None)
    render_login_screen()


import plotly.graph_objects as go


def _get_level_label(level: int) -> str:
    labels = {
        0: "Hiç Bilmiyorum",
        1: "Farkındalık",
        2: "Temel Bilgi",
        3: "Uygulayabiliyorum",
        4: "İyi Seviye",
        5: "Uzman",
    }
    return labels.get(level, "Temel Bilgi")


def _render_skill_radar_chart(
    skill_names: list,
    skill_values: list,
    role_id: str | None = None,
) -> None:
    """
    Render a premium radar chart showing current skill levels.
    """
    theme = get_role_theme(role_id)

    # Close the polygon by repeating the first value
    values_closed = skill_values + [skill_values[0]]
    names_closed = skill_names + [skill_names[0]]

    fig = go.Figure()

    # Add filled area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=names_closed,
        fill='toself',
        fillcolor=f"rgba({int(theme['primary'][1:3], 16)}, {int(theme['primary'][3:5], 16)}, {int(theme['primary'][5:7], 16)}, 0.25)",
        line=dict(
            color=theme['primary'],
            width=2,
        ),
        name='Mevcut Seviye',
        hovertemplate='%{theta}: %{r}/5<extra></extra>',
    ))

    # Add points
    fig.add_trace(go.Scatterpolar(
        r=skill_values,
        theta=skill_names,
        mode='markers',
        marker=dict(
            color=theme['primary'],
            size=10,
            line=dict(color='white', width=2),
        ),
        name='Beceriler',
        hovertemplate='%{theta}: %{r}/5<extra></extra>',
        showlegend=False,
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[0, 1, 2, 3, 4, 5],
                ticktext=['0', '1', '2', '3', '4', '5'],
                tickfont=dict(color='#64748b', size=10),
                gridcolor='rgba(51, 65, 85, 0.4)',
                linecolor='rgba(51, 65, 85, 0.4)',
            ),
            angularaxis=dict(
                tickfont=dict(color='#e2e8f0', size=11),
                gridcolor='rgba(51, 65, 85, 0.3)',
                linecolor='rgba(51, 65, 85, 0.4)',
            ),
            bgcolor='rgba(15, 23, 42, 0.6)',
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=40, b=40),
        height=350,
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Info text
    avg_level = sum(skill_values) / len(skill_values) if skill_values else 0
    st.caption(f"📊 Ortalama beceri seviyesi: {avg_level:.1f}/5 — Slider'ları hareket ettirdiğinde grafik otomatik güncellenir.")


def _module_state_label(state: str) -> str:
    """Turkish label for module state."""
    labels = {
        "not_started": "Başlamadım",
        "in_progress": "Devam ediyorum",
        "completed": "Tamamladım",
        "applied": "Uyguladım",
    }
    return labels.get(state, state)


def render_profile_page(
    roles: Dict[str, Role],
    skills: Dict[str, Skill],
    modules: List[Module] | None = None,
) -> Tuple[str, float, int, Dict[str, int], bool]:
    """
    Premium AI Career Setup Experience - module-based progress (no sliders).
    """
    if modules is None:
        modules = []
    role_options = {r.display_name: r.id for r in roles.values()}
    default_role_name = sorted(role_options.keys())[0]

    saved_role_id = st.session_state.get("selected_role_id")
    if saved_role_id and saved_role_id in roles:
        default_role_name = roles[saved_role_id].display_name

    selected_role_id = role_options.get(default_role_name, list(role_options.values())[0])
    selected_role = roles[selected_role_id]
    theme = get_role_theme(selected_role_id)

    inject_global_styles(selected_role_id)

    # ===== PREMIUM UI SYSTEM CSS =====
    page_css = f"""
<style>
/* ===== GLASSMORPHISM CONTROL BAR ===== */
.control-bar {{
    background: linear-gradient(135deg, rgba(15,23,42,0.85) 0%, rgba(30,41,59,0.75) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 1rem;
    padding: 0.8rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}}
.control-bar::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {theme['primary']}66, transparent);
}}
.control-group {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}}
.control-icon-box {{
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border-radius: 0.6rem;
    font-size: 1.1rem;
    box-shadow: 0 4px 15px {theme['glow']};
    flex-shrink: 0;
}}
.control-info {{
    min-width: 0;
}}
.control-label {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    margin-bottom: 0.1rem;
}}
.control-divider {{
    width: 1px;
    height: 32px;
    background: linear-gradient(180deg, transparent, rgba(99,102,241,0.3), transparent);
    flex-shrink: 0;
}}

/* ===== PREMIUM HERO CARD ===== */
.hero-card {{
    background: linear-gradient(145deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 40%, rgba(15,23,42,0.98) 100%);
    border: 1px solid {theme['primary']}44;
    border-radius: 1.5rem;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}
.hero-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']}, {theme['accent']}, {theme['primary']});
    background-size: 300% 100%;
    animation: gradient-flow 4s ease infinite;
}}
@keyframes gradient-flow {{
    0%, 100% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
}}
.hero-card::after {{
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, {theme['primary']}20 0%, transparent 60%);
    pointer-events: none;
}}
.hero-content {{
    position: relative;
    z-index: 1;
}}
.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(15,23,42,0.6);
    border: 1px solid {theme['primary']}44;
    border-radius: 2rem;
    padding: 0.4rem 1rem;
    font-size: 0.75rem;
    color: {theme['primary']};
    font-weight: 600;
    margin-bottom: 1rem;
}}
.hero-title {{
    font-size: 2.2rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.6rem;
    letter-spacing: -0.03em;
    line-height: 1.2;
}}
.hero-subtitle {{
    font-size: 1.05rem;
    color: #cbd5e1;
    max-width: 550px;
    line-height: 1.7;
    margin-bottom: 1.8rem;
}}
.hero-pills {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}}
.hero-pill {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 3rem;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}}
.hero-pill:hover {{
    border-color: {theme['primary']}55;
    background: rgba(15,23,42,0.9);
}}
.hero-pill-icon {{
    font-size: 1.1rem;
}}
.hero-pill-content {{
    display: flex;
    flex-direction: column;
}}
.hero-pill-label {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
}}
.hero-pill-value {{
    font-size: 0.9rem;
    font-weight: 700;
    color: {theme['primary']};
}}

/* ===== READINESS PROGRESS SECTION ===== */
.readiness-card {{
    background: linear-gradient(145deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.9) 100%);
    border: 1px solid {theme['primary']}33;
    border-radius: 1.2rem;
    padding: 2rem 2.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}}
.readiness-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, {theme['primary']}, {theme['secondary']}, {theme['accent']});
    border-radius: 0 0 0 1.2rem;
}}
.readiness-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
}}
.readiness-info {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
.readiness-icon-box {{
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border-radius: 0.8rem;
    font-size: 1.5rem;
    box-shadow: 0 6px 20px {theme['glow']};
}}
.readiness-text {{
    display: flex;
    flex-direction: column;
}}
.readiness-label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    margin-bottom: 0.2rem;
}}
.readiness-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
}}
.readiness-score {{
    text-align: right;
}}
.readiness-percentage {{
    font-size: 3rem;
    font-weight: 900;
    color: {theme['primary']};
    line-height: 1;
    text-shadow: 0 0 40px {theme['glow']};
}}
.readiness-score-label {{
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}
.readiness-bar-wrapper {{
    margin-bottom: 1.2rem;
}}
.readiness-bar-bg {{
    width: 100%;
    height: 14px;
    background: rgba(30,41,59,0.9);
    border-radius: 7px;
    overflow: hidden;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.4);
}}
.readiness-bar-fill {{
    height: 100%;
    border-radius: 7px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']}, {theme['accent']});
    position: relative;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 20px {theme['glow']};
}}
.readiness-bar-fill::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.4), transparent);
    border-radius: 7px 7px 0 0;
}}
.readiness-bar-fill::before {{
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 30px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
    border-radius: 0 7px 7px 0;
    animation: shimmer 2s infinite;
}}
@keyframes shimmer {{
    0%, 100% {{ opacity: 0; }}
    50% {{ opacity: 1; }}
}}
.readiness-message {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 1rem 1.2rem;
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(51,65,85,0.4);
    border-radius: 0.8rem;
}}
.readiness-message-icon {{
    font-size: 1.3rem;
}}
.readiness-message-text {{
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.5;
}}

/* ===== SKILL CATEGORY CONTAINER ===== */
.category-container {{
    background: linear-gradient(145deg, rgba(15,23,42,0.9) 0%, rgba(30,41,59,0.85) 100%);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 1.2rem;
    padding: 1.8rem;
    margin-bottom: 1.8rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.category-container::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    opacity: 0;
    transition: opacity 0.3s ease;
}}
.category-container:hover {{
    border-color: {theme['primary']}44;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}}
.category-container:hover::before {{
    opacity: 1;
}}
.category-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(51,65,85,0.4);
}}
.category-icon {{
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border-radius: 0.8rem;
    font-size: 1.4rem;
    box-shadow: 0 6px 20px {theme['glow']};
}}
.category-info {{
    flex: 1;
}}
.category-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
}}
.category-desc {{
    font-size: 0.8rem;
    color: #64748b;
}}
.category-badge {{
    background: {theme['primary']}22;
    color: {theme['primary']};
    padding: 0.4rem 0.9rem;
    border-radius: 2rem;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid {theme['primary']}33;
}}

/* ===== SKILL CARDS ===== */
.skill-card {{
    background: linear-gradient(150deg, rgba(30,41,59,0.95) 0%, rgba(15,23,42,0.98) 100%);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 1rem;
    padding: 1.3rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}}
.skill-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}}
.skill-card:hover {{
    border-color: {theme['primary']}55;
    transform: translateY(-4px);
    box-shadow: 0 12px 35px -8px rgba(0,0,0,0.5), 0 0 25px {theme['glow']};
}}
.skill-card:hover::before {{
    transform: scaleX(1);
}}
.skill-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}}
.skill-info {{
    display: flex;
    align-items: center;
    gap: 0.7rem;
}}
.skill-icon {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(51,65,85,0.6), rgba(30,41,59,0.8));
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 0.6rem;
    font-size: 1.1rem;
}}
.skill-name {{
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
}}
.skill-difficulty {{
    font-size: 0.65rem;
    background: {theme['primary']}20;
    color: {theme['primary']};
    padding: 0.3rem 0.7rem;
    border-radius: 2rem;
    font-weight: 600;
    border: 1px solid {theme['primary']}30;
}}
.skill-level-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.7rem;
}}
.skill-level-label {{
    font-size: 0.8rem;
    color: #94a3b8;
}}
.skill-level-value {{
    font-size: 0.9rem;
    font-weight: 700;
    color: {theme['primary']};
}}
.skill-progress-bg {{
    width: 100%;
    height: 8px;
    background: rgba(30,41,59,0.9);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.8rem;
}}
.skill-progress-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    transition: width 0.4s ease;
    box-shadow: 0 0 12px {theme['glow']};
}}
.skill-helper {{
    font-size: 0.72rem;
    color: #64748b;
    font-style: italic;
}}

/* ===== AI INSIGHT SECTION ===== */
.ai-panel {{
    background: linear-gradient(145deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.92) 100%);
    border: 1px solid {theme['primary']}44;
    border-radius: 1.2rem;
    padding: 2rem;
    margin: 2.5rem 0;
    position: relative;
    overflow: hidden;
}}
.ai-panel::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']}, {theme['accent']});
}}
.ai-header {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}}
.ai-icon {{
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border-radius: 0.8rem;
    font-size: 1.4rem;
    box-shadow: 0 6px 20px {theme['glow']};
}}
.ai-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: #f1f5f9;
}}
.ai-subtitle {{
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 1.2rem;
    padding-left: 0.5rem;
    border-left: 2px solid {theme['primary']}55;
}}
.ai-items {{
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}}
.ai-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.2rem;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 0.9rem;
    transition: all 0.25s ease;
}}
.ai-item:hover {{
    border-color: {theme['primary']}44;
    background: rgba(15,23,42,0.9);
    transform: translateX(4px);
}}
.ai-rank {{
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
    border-radius: 50%;
    font-size: 0.85rem;
    font-weight: 800;
    color: #fff;
    box-shadow: 0 4px 12px {theme['glow']};
}}
.ai-skill-name {{
    flex: 1;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e2e8f0;
}}
.ai-skill-level {{
    font-size: 0.75rem;
    color: #64748b;
    background: rgba(51,65,85,0.6);
    padding: 0.3rem 0.7rem;
    border-radius: 2rem;
}}

/* ===== CTA SECTION ===== */
.cta-card {{
    background: linear-gradient(145deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 50%, rgba(15,23,42,0.98) 100%);
    border: 1px solid {theme['primary']}55;
    border-radius: 1.5rem;
    padding: 3rem;
    margin-top: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
.cta-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']}, {theme['accent']}, {theme['primary']});
    background-size: 300% 100%;
    animation: gradient-flow 4s ease infinite;
}}
.cta-card::after {{
    content: '';
    position: absolute;
    bottom: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse, {theme['primary']}25 0%, transparent 60%);
    pointer-events: none;
}}
.cta-content {{
    position: relative;
    z-index: 1;
}}
.cta-icon {{
    font-size: 3.5rem;
    margin-bottom: 1.2rem;
    display: block;
}}
.cta-title {{
    font-size: 1.8rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}}
.cta-subtitle {{
    font-size: 1rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
    max-width: 480px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.7;
}}
</style>
"""
    st.markdown(page_css, unsafe_allow_html=True)

    # ===== SECTION 1: GLASSMORPHISM CONTROL BAR =====
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.3, 1, 1])
    
    with ctrl_col1:
        st.markdown(f"""
<div class="control-group">
    <div class="control-icon-box">🎯</div>
    <div class="control-info">
        <div class="control-label">Hedef Rol</div>
    </div>
</div>
""", unsafe_allow_html=True)
        role_name = st.selectbox(
            "Hedef Rol",
            options=list(role_options.keys()),
            index=list(role_options.keys()).index(default_role_name),
            label_visibility="collapsed",
            key="role_select_main"
        )
    
    with ctrl_col2:
        st.markdown(f"""
<div class="control-group">
    <div class="control-icon-box">⏰</div>
    <div class="control-info">
        <div class="control-label">Haftalık Saat</div>
    </div>
</div>
""", unsafe_allow_html=True)
        weekly_hours = st.number_input(
            "Haftalık Saat",
            min_value=2.0, max_value=40.0,
            value=st.session_state.get("weekly_hours", 8.0),
            step=1.0,
            label_visibility="collapsed",
            key="hours_main"
        )
    
    with ctrl_col3:
        st.markdown(f"""
<div class="control-group">
    <div class="control-icon-box">📅</div>
    <div class="control-info">
        <div class="control-label">Plan Süresi</div>
    </div>
</div>
""", unsafe_allow_html=True)
        duration_weeks = st.number_input(
            "Hafta Sayısı",
            min_value=1, max_value=12,
            value=st.session_state.get("num_weeks", 4),
            step=1,
            label_visibility="collapsed",
            key="weeks_main"
        )

    # Update selected role based on selection
    selected_role_id = role_options[role_name]
    selected_role = roles[selected_role_id]
    theme = get_role_theme(selected_role_id)

    # ===== SECTION 2: PREMIUM HERO CARD =====
    st.markdown(f"""
<div class="hero-card">
    <div class="hero-content">
        <div class="hero-badge">✨ Kişiselleştirilmiş Öğrenme Deneyimi</div>
        <div class="hero-title">AI Kariyer Yolculuğunu Başlat</div>
        <div class="hero-subtitle">Beceri seviyeni belirle ve sana özel öğrenme yol haritanı oluştur. Aşağıdaki becerilerde mevcut durumunu işaretle, sistem sana kişiselleştirilmiş bir gelişim planı hazırlayacak.</div>
        <div class="hero-pills">
            <div class="hero-pill">
                <span class="hero-pill-icon">🎯</span>
                <div class="hero-pill-content">
                    <span class="hero-pill-label">Hedef Rol</span>
                    <span class="hero-pill-value">{selected_role.display_name}</span>
                </div>
            </div>
            <div class="hero-pill">
                <span class="hero-pill-icon">📅</span>
                <div class="hero-pill-content">
                    <span class="hero-pill-label">Plan Süresi</span>
                    <span class="hero-pill-value">{int(duration_weeks)} Hafta</span>
                </div>
            </div>
            <div class="hero-pill">
                <span class="hero-pill-icon">⏰</span>
                <div class="hero-pill-content">
                    <span class="hero-pill-label">Haftalık Çalışma</span>
                    <span class="hero-pill-value">{weekly_hours:.0f} Saat</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    role_skill_ids = list(selected_role.skills.keys())
    # Module-based readiness when modules exist
    if modules:
        readiness_pct = int(get_overall_readiness_percentage(modules, role_skill_ids, st.session_state))
    else:
        total_skills = len(selected_role.skills)
        total_current = sum(st.session_state.get(f"skill_{sid}", 2) for sid in role_skill_ids)
        max_possible = total_skills * 5
        readiness_pct = int((total_current / max_possible) * 100) if max_possible > 0 else 0

    # Readiness hint based on level
    if readiness_pct < 25:
        hint_text = "Başlangıç seviyesindesin. Her yolculuk bir adımla başlar! Düzenli çalışmayla kısa sürede temel yapını güçlendireceksin."
        hint_icon = "💡"
    elif readiness_pct < 50:
        hint_text = "Temel seviyeni oluşturuyorsun. Bu hızla ilerlersen kısa sürede güçlü bir altyapı kazanacaksın."
        hint_icon = "📈"
    elif readiness_pct < 75:
        hint_text = "Güçlü bir temel kurmuşsun. Uzmanlaşmaya doğru ilerliyorsun, hedefe yaklaşıyorsun!"
        hint_icon = "⚡"
    else:
        hint_text = "İleri seviyedesin! Hedef role çok yakınsın, son adımları at ve başarıya ulaş."
        hint_icon = "🌟"

    # ===== SECTION 3: READINESS PROGRESS =====
    st.markdown(f"""
<div class="readiness-card">
    <div class="readiness-top">
        <div class="readiness-info">
            <div class="readiness-icon-box">📊</div>
            <div class="readiness-text">
                <div class="readiness-label">Değerlendirme</div>
                <div class="readiness-title">Mevcut Hazırbulunuşluk</div>
            </div>
        </div>
        <div class="readiness-score">
            <div class="readiness-percentage">{readiness_pct}%</div>
            <div class="readiness-score-label">Tamamlandı</div>
        </div>
    </div>
    <div class="readiness-bar-wrapper">
        <div class="readiness-bar-bg">
            <div class="readiness-bar-fill" style="width: {readiness_pct}%;"></div>
        </div>
    </div>
    <div class="readiness-message">
        <span class="readiness-message-icon">{hint_icon}</span>
        <span class="readiness-message-text">{hint_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # ===== SECTION 4: MODULE-BASED PROGRESS (or legacy skill grid) =====
    category_icons = {
        "Temel Beceriler": "🧠",
        "Programlama": "💻",
        "Veri ve Matematik": "📈",
        "Matematik": "📐",
        "Veri Bilimi": "📊",
        "Yapay Zeka": "🤖",
        "Frontend": "🎨",
        "Genel": "📚",
        "Profesyonel Pratikler": "📂",
        "Veri Tabanları": "🗄️",
    }
    category_descriptions = {
        "Temel Beceriler": "Problem çözme ve analitik düşünce",
        "Programlama": "Kod yazma ve geliştirme becerileri",
        "Veri Bilimi": "Veri analizi ve görselleştirme",
        "Matematik": "Matematiksel temeller",
        "Yapay Zeka": "Yapay zeka ve makine öğrenmesi",
        "Frontend": "Kullanıcı arayüzü geliştirme",
        "Genel": "Genel teknik beceriler",
        "Profesyonel Pratikler": "Versiyon kontrol ve pratikler",
        "Veri Tabanları": "SQL ve veri tabanı temelleri",
    }

    if modules:
        # Group modules by category (only skills in selected role)
        role_skill_set = set(selected_role.skills.keys())
        category_modules: Dict[str, List[Module]] = {}
        for m in modules:
            if m.skill_id not in role_skill_set:
                continue
            skill = skills.get(m.skill_id)
            cat = skill.category if skill else "Genel"
            if cat not in category_modules:
                category_modules[cat] = []
            category_modules[cat].append(m)
        for cat in category_modules:
            category_modules[cat].sort(key=lambda x: (x.order, x.id))

        for category, cat_modules in category_modules.items():
            cat_icon = category_icons.get(category, "📌")
            cat_desc = category_descriptions.get(category, "")
            cat_pct = get_category_progress(category, modules, skills, st.session_state)

            st.markdown(f"""
<div class="category-container">
    <div class="category-header">
        <div class="category-icon">{cat_icon}</div>
        <div class="category-info">
            <div class="category-title">{category}</div>
            <div class="category-desc">{cat_desc}</div>
        </div>
        <div class="category-badge">{cat_pct:.0f}% · {len(cat_modules)} modül</div>
    </div>
    <div class="readiness-bar-bg" style="margin-top: 0.8rem; height: 8px;">
        <div class="readiness-bar-fill" style="width: {cat_pct}%; height: 8px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

            mod_cols = st.columns(2)
            for idx, mod in enumerate(cat_modules):
                col_idx = idx % 2
                with mod_cols[col_idx]:
                    skill = skills.get(mod.skill_id)
                    skill_name = skill.display_name if skill else mod.skill_id
                    current_state = get_module_state(mod.id, st.session_state)
                    st.markdown(f"""
<div class="skill-card">
    <div class="skill-header">
        <div class="skill-info">
            <div class="skill-name">{mod.title}</div>
        </div>
    </div>
    <div class="skill-helper">Beceri: {skill_name}</div>
</div>
""", unsafe_allow_html=True)
                    st.selectbox(
                        "Durum",
                        options=MODULE_STATES,
                        index=MODULE_STATES.index(current_state) if current_state in MODULE_STATES else 0,
                        key=f"module_{mod.id}",
                        label_visibility="collapsed",
                        format_func=_module_state_label,
                    )

        current_levels = module_progress_to_skill_levels(modules, role_skill_ids, st.session_state)
    else:
        # Legacy: skill sliders when no modules
        skill_categories_legacy: Dict[str, List[Tuple[str, Skill]]] = {}
        for skill_id in selected_role.skills.keys():
            skill = skills[skill_id]
            cat = skill.category
            if cat not in skill_categories_legacy:
                skill_categories_legacy[cat] = []
            skill_categories_legacy[cat].append((skill_id, skill))
        skill_icons = {
            "python_basics": "🐍", "git_basics": "📂", "sql_basics": "🗄️",
            "statistics_fundamentals": "📊", "data_analysis": "📉", "data_visualization": "📈",
            "machine_learning": "🤖", "deep_learning": "🧠", "html_css": "🎨",
            "javascript_basics": "⚡", "react_basics": "⚛️", "apis_rest": "🔌",
            "problem_solving": "🧩", "prompt_engineering": "💬",
            "linear_algebra": "📐", "pandas_library": "🐼",
        }
        current_levels = {}
        for category, category_skills in skill_categories_legacy.items():
            cat_icon = category_icons.get(category, "📌")
            st.markdown(f"""
<div class="category-container">
    <div class="category-header">
        <div class="category-icon">{cat_icon}</div>
        <div class="category-info">
            <div class="category-title">{category}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
            skill_cols = st.columns(2)
            for idx, (skill_id, skill) in enumerate(category_skills):
                with skill_cols[idx % 2]:
                    cv = st.session_state.get(f"skill_{skill_id}", 2)
                    st.markdown(f"""
<div class="skill-card">
    <div class="skill-header">
        <div class="skill-name">{skill.display_name}</div>
    </div>
</div>
""", unsafe_allow_html=True)
                    current_levels[skill_id] = st.slider(
                        skill.display_name, 0, 5, cv, key=f"skill_{skill_id}",
                        label_visibility="collapsed",
                    )

    # ===== SECTION 5: AI INSIGHT =====
    skill_values_list = []
    for skill_id in selected_role.skills.keys():
        skill = skills[skill_id]
        val = current_levels.get(skill_id, 0)
        skill_values_list.append((skill_id, skill.display_name, val))

    skill_values_list.sort(key=lambda x: x[2])
    top_3_to_improve = skill_values_list[:3]

    ai_items_html = ""
    for idx, (sid, sname, sval) in enumerate(top_3_to_improve):
        ai_items_html += f"""
<div class="ai-item">
    <div class="ai-rank">{idx + 1}</div>
    <div class="ai-skill-name">{sname}</div>
    <div class="ai-skill-level">Seviye {sval}/5</div>
</div>
"""

    st.markdown(f"""
<div class="ai-panel">
    <div class="ai-header">
        <div class="ai-icon">🤖</div>
        <div class="ai-title">AI Öneri Motoru</div>
    </div>
    <div class="ai-subtitle">Mevcut beceri seviyelerine göre öncelikli odaklanman gereken alanlar:</div>
    <div class="ai-items">
        {ai_items_html}
    </div>
</div>
""", unsafe_allow_html=True)

    # ===== SECTION 6: CTA =====
    st.markdown(f"""
<div class="cta-card">
    <div class="cta-content">
        <span class="cta-icon">🗺️</span>
        <div class="cta-title">Yol Haritanı Oluştur</div>
        <div class="cta-subtitle">Belirlediğin becerilere göre {int(duration_weeks)} haftalık kişiselleştirilmiş öğrenme planın hazırlanacak.</div>
    </div>
</div>
""", unsafe_allow_html=True)

    submitted = st.button("🚀 Yol Haritamı Oluştur", use_container_width=True, type="primary")

    return selected_role_id, float(weekly_hours), int(duration_weeks), current_levels, submitted


def render_onboarding_page(
    roles: Dict[str, Role],
    skills: Dict[str, Skill],
    modules: List[Module] | None = None,
) -> Tuple[str, float, int, Dict[str, int], bool]:
    """
    Premium career journey entry experience (profile panel, growth stage, chip-based skills).
    Delegates to onboarding_ui.
    """
    from .onboarding_ui import render_onboarding_page as render_onboarding_impl
    return render_onboarding_impl(roles, skills, modules)


def render_dashboard_page(
    roles: Dict[str, Role],
    skills: Dict[str, Skill],
    modules: List[Module] | None = None,
) -> None:
    """
    Premium personalized dashboard with welcome, category progress, AI recommendations, career goals.
    """
    from streamlit import session_state as ss

    if modules is None:
        modules = []
    analysis_result: GapAnalysisResult | None = ss.get("analysis_result")
    weeks: List[WeekPlan] | None = ss.get("weekly_plan")
    selected_role_id = ss.get("selected_role_id")
    weekly_hours = ss.get("weekly_hours", 8.0)
    num_weeks = ss.get("num_weeks", 4)
    user_name = ss.get("user_name", "Kullanıcı")
    career_goal = ss.get("career_goal", "")

    role_display_name = None
    readiness_pct = None

    if selected_role_id and selected_role_id in roles:
        role_display_name = roles[selected_role_id].display_name

    if analysis_result and analysis_result.skill_gaps:
        total_required = sum(g.required_level for g in analysis_result.skill_gaps)
        total_current = sum(g.current_level for g in analysis_result.skill_gaps)
        if total_required > 0:
            readiness_pct = min(95, max(5, int((total_current / total_required) * 100)))

    inject_global_styles(selected_role_id)

    render_welcome_section(user_name, role_display_name)

    render_premium_header(
        role_display_name=role_display_name,
        readiness_pct=readiness_pct,
        role_id=selected_role_id,
    )

    col_main, col_ai = st.columns([2, 1])

    with col_main:
        task_text = "Henüz tanımlı bir görev yok. <strong>Hedef ve Profil</strong> sayfasından yol haritanı oluştur."
        if weeks:
            first_week = weeks[0]
            if first_week.skills and first_week.skills[0].mini_tasks:
                task_text = first_week.skills[0].mini_tasks[0]

        render_todays_task_card(task_text, selected_role_id)

        if st.button("📝 Hedef ve Profil sayfasına git", key="task_to_profile_btn"):
            st.session_state["current_page"] = "Hedef ve Profil"
            st.rerun()

        if not career_goal:
            if role_display_name:
                career_goal = f"Junior seviyeye ulaşıp {role_display_name} olarak bir şirkette çalışmak."
            else:
                career_goal = "Hedef rolümü belirleyip kariyer yolculuğuma başlamak."

        render_career_goal_card(career_goal)

        # Category progress from module completion (when modules exist)
        if modules and selected_role_id and selected_role_id in roles:
            role_skill_ids = list(roles[selected_role_id].skills.keys())
            role_skill_set = set(role_skill_ids)
            category_modules: Dict[str, List[Module]] = {}
            for m in modules:
                if m.skill_id not in role_skill_set:
                    continue
                skill = skills.get(m.skill_id)
                cat = skill.category if skill else "Genel"
                if cat not in category_modules:
                    category_modules[cat] = []
                category_modules[cat].append(m)
            if category_modules:
                cat_icons = {"Temel Beceriler": "🧠", "Programlama": "💻", "Veri ve Matematik": "📈", "Matematik": "📐", "Veri Bilimi": "📊", "Yapay Zeka": "🤖", "Frontend": "🎨", "Genel": "📚", "Profesyonel Pratikler": "📂", "Veri Tabanları": "🗄️"}
                overall_pct = int(get_overall_readiness_percentage(modules, role_skill_ids, ss))
                st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
                st.markdown("**📊 Kategori İlerlemesi** (modül durumlarına göre)")
                for cat in sorted(category_modules.keys()):
                    cat_pct = get_category_progress(cat, modules, skills, ss)
                    icon = cat_icons.get(cat, "📌")
                    st.markdown(f"**{icon} {cat}** — {cat_pct:.0f}%")
                    st.progress(cat_pct / 100.0)
                st.caption(f"Genel hazırlık: **{overall_pct}%**")
                st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        weekly_progress = "Henüz oluşturulmuş bir haftalık plan bulunamadı."
        if weeks:
            total_weeks_count = len(weeks)
            active_weeks = sum(1 for w in weeks if w.skills)
            total_hours = sum(w.total_hours for w in weeks)
            weekly_progress = f"<strong>{total_weeks_count} haftalık</strong> planında <strong>{active_weeks}</strong> haftada odaklı çalışma var. Toplam <strong>{total_hours:.0f} saat</strong> öğrenme süresi."

        skill_summary = "Öne çıkan bir beceri boşluğu özeti için henüz veri yok."
        if analysis_result and analysis_result.skill_gaps:
            top_gaps = analysis_result.skill_gaps[:3]
            summary_items = [
                f"<strong>{gap.display_name}</strong>: {gap.current_level} → {gap.required_level}"
                for gap in top_gaps
            ]
            skill_summary = "<br>".join(summary_items)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        progress_card_html = f"""
<div class="yh-dashboard-card">
    <div class="yh-dashboard-card-header">
        <div class="yh-dashboard-card-icon">📈</div>
        <div class="yh-dashboard-card-title">Haftalık İlerleme</div>
    </div>
    <div class="yh-dashboard-card-content">{weekly_progress}</div>
</div>
"""
        st.markdown(progress_card_html, unsafe_allow_html=True)

        skill_card_html = f"""
<div class="yh-dashboard-card">
    <div class="yh-dashboard-card-header">
        <div class="yh-dashboard-card-icon">🎯</div>
        <div class="yh-dashboard-card-title">Beceri Gelişim Özeti</div>
    </div>
    <div class="yh-dashboard-card-content">{skill_summary}</div>
</div>
"""
        st.markdown(skill_card_html, unsafe_allow_html=True)

    with col_ai:
        # Boş durum: henüz haftalık plan yoksa, kullanıcıyı önce profil/ yol haritası oluşturmaya yönlendir
        if not weeks:
            next_skill_name = "Önce yol haritanı oluştur"
            next_skill_hours = 0.0
            next_skill_explanation = (
                "AI tavsiyesini görmek için önce **Hedef ve Profil** sayfasına gidip "
                "\"Yol Haritamı Oluştur\" butonuna tıklayarak kişisel öğrenme planını oluşturmalısın."
            )
        else:
            next_skill_name = "Python Temelleri"
            next_skill_hours = 4.0
            next_skill_explanation = "Temel programlama becerileri, tüm teknik rollerin yapı taşıdır. Değişkenler, döngüler ve fonksiyonlar ile başla."

            if weeks[0].skills:
                first_skill = weeks[0].skills[0]
                next_skill_name = first_skill.display_name
                next_skill_hours = first_skill.estimated_hours
                next_skill_explanation = first_skill.rationale if first_skill.rationale else f"{next_skill_name} becerisi, hedef rolün için kritik öneme sahip."

        render_ai_recommendation_panel(
            skill_name=next_skill_name,
            explanation=next_skill_explanation,
            estimated_hours=next_skill_hours,
            impact="Yüksek",
            role_id=selected_role_id,
        )

        if st.button("🚀 Başla", use_container_width=True, key="ai_start_btn"):
            if not weeks:
                st.info("Önce **Hedef ve Profil** sayfasından yol haritanı oluşturmalısın.")
            else:
                st.info(f"'{next_skill_name}' öğrenme modülü yakında aktif olacak!")

    render_section_header("⚡", "Hızlı Erişim")

    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        if st.button("📊 Beceri Analizi", use_container_width=True, key="qa_analysis"):
            st.session_state["current_page"] = "Beceri Boşluğu Analizi"
            st.rerun()
    with qa_col2:
        if st.button("🗺️ Yol Haritası", use_container_width=True, key="qa_roadmap"):
            st.session_state["current_page"] = "Öğrenme Yol Haritası"
            st.rerun()
    with qa_col3:
        if st.button("🎯 Profil Güncelle", use_container_width=True, key="qa_profile"):
            st.session_state["current_page"] = "Hedef ve Profil"
            st.rerun()


def render_gap_analysis_page(
    gap_result: GapAnalysisResult | None,
    skills: Dict[str, Skill],
) -> None:
    from streamlit import session_state as ss

    selected_role_id = ss.get("selected_role_id")

    if gap_result is None or not gap_result.skill_gaps:
        inject_global_styles(selected_role_id)
        st.warning(
            "Henüz bir analiz bulunmuyor. Önce sol menüden **Hedef ve Profil** sayfasına gidip "
            "*Yol Haritasını Oluştur* butonuna basmalısınız."
        )
        return

    inject_global_styles(selected_role_id)
    render_premium_header(
        role_display_name=gap_result.role.display_name,
        role_id=selected_role_id,
    )

    table_rows = gaps_to_table(gap_result, skills)
    df = pd.DataFrame(table_rows)

    avg_gap = df["Boşluk"].mean() if not df.empty else 0
    high_priority = (df["Öncelik Skoru"] > df["Öncelik Skoru"].median()).sum() if not df.empty else 0

    metrics_html = f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
    <div class="yh-metric">
        <div class="yh-metric-value">{len(df)}</div>
        <div class="yh-metric-label">Toplam Eksik Beceri</div>
    </div>
    <div class="yh-metric">
        <div class="yh-metric-value">{avg_gap:.1f}</div>
        <div class="yh-metric-label">Ortalama Boşluk</div>
    </div>
    <div class="yh-metric">
        <div class="yh-metric-value">{int(high_priority)}</div>
        <div class="yh-metric-label">Yüksek Öncelikli</div>
    </div>
</div>
"""
    st.markdown(metrics_html, unsafe_allow_html=True)

    st.caption(f"Seçilen rol: {gap_result.role.display_name}. Aşağıdaki tablo, mevcut ve hedef seviyeler arasındaki boşlukları özetler.")

    st.dataframe(
        df[
            [
                "Beceri",
                "Kategori",
                "Zorluk (1-5)",
                "Hızlı Kazanım",
                "Mevcut Seviye",
                "Hedef Seviye",
                "Boşluk",
                "Rol Ağırlığı",
                "Öncelik Skoru",
                "Eksik Önkoşullar",
            ]
        ],
        use_container_width=True,
    )

    chart_df = df[["Beceri", "Mevcut Seviye", "Hedef Seviye"]].melt(
        id_vars="Beceri", var_name="Tür", value_name="Seviye"
    )

    theme = get_role_theme(selected_role_id)
    fig = px.bar(
        chart_df,
        x="Beceri",
        y="Seviye",
        color="Tür",
        barmode="group",
        title="Mevcut ve Hedef Beceri Seviyeleri",
        color_discrete_map={
            "Mevcut Seviye": "#64748b",
            "Hedef Seviye": theme["primary"],
        }
    )
    fig.update_layout(
        xaxis_title="Beceri",
        yaxis_title="Seviye",
        legend_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0"),
    )
    fig.update_xaxes(gridcolor="rgba(51,65,85,0.3)")
    fig.update_yaxes(gridcolor="rgba(51,65,85,0.3)")
    st.plotly_chart(fig, use_container_width=True)

    prerequisite_rows = df[df["Eksik Önkoşullar"] != "-"]
    if not prerequisite_rows.empty:
        render_section_header("⚠️", "Önkoşul Uyarıları")
        st.info(
            "Bazı becerilerin verimli öğrenilebilmesi için önce temel konuları çalışman önerilir."
        )
        st.table(prerequisite_rows[["Beceri", "Eksik Önkoşullar"]])


def render_roadmap_page(
    weeks: List[WeekPlan] | None,
    explanation: Dict[str, str] | None,
    gap_result: GapAnalysisResult | None = None,
    skills: Dict[str, Skill] | None = None,
) -> None:
    from streamlit import session_state as ss

    selected_role_id = ss.get("selected_role_id")

    if weeks is None or all(len(w.skills) == 0 for w in weeks):
        inject_global_styles(selected_role_id)
        st.warning(
            "Henüz bir yol haritası oluşturulmadı. Önce sol menüden **Hedef ve Profil** sayfasına gidip "
            "*Yol Haritasını Oluştur* butonuna basmalısınız."
        )
        return

    inject_global_styles(selected_role_id)

    if skills is not None and gap_result is not None:
        render_visual_roadmap(weeks, gap_result, explanation or {}, skills, selected_role_id)

    with st.expander("📋 Detaylı Teknik Görünüm", expanded=False):
        st.caption("Haftalık plan detayları ve özet tablo")
        for week in weeks:
            st.markdown(f"**{week.week_index}. Hafta** — {week.total_hours:.1f} saat")
            if week.skills:
                for skill in week.skills:
                    st.markdown(f"- {skill.display_name} ({skill.estimated_hours:.1f} saat)")

        st.markdown("---")
        df = pd.DataFrame(weekly_plan_to_table(weeks))
        if not df.empty:
            st.dataframe(df, use_container_width=True)

