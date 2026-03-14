from __future__ import annotations

import html as html_module
from typing import Dict, Tuple, Any, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import networkx as nx

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
    render_login_left_panel,
    render_login_center_logo,
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
from .navigation_manager import set_active_section


def render_app_header(role_id: str | None = None, role_display_name: str | None = None) -> None:
    inject_global_styles(role_id)


def render_login_header() -> None:
    inject_global_styles(None)
    render_login_screen()


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


def _safe_html(text: str) -> str:
    """Escape for safe injection into HTML; prevents raw tags showing as text."""
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


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
    role_names_sorted = sorted(role_options.keys())
    # Placeholder so we never force a role when none is selected; single source of truth from session.
    ROLE_PLACEHOLDER = "— Rol seçin —"
    options_with_placeholder = [ROLE_PLACEHOLDER] + role_names_sorted
    saved_role_id = st.session_state.get("selected_role_id")
    if saved_role_id and saved_role_id in roles:
        default_role_name = roles[saved_role_id].display_name
        default_index = options_with_placeholder.index(default_role_name)
    else:
        default_role_name = ROLE_PLACEHOLDER
        default_index = 0

    selected_role_id = role_options.get(default_role_name) if default_role_name != ROLE_PLACEHOLDER else None
    selected_role = roles[selected_role_id] if selected_role_id else None
    theme = get_role_theme(selected_role_id)
    # Theme injected once in app.py from canonical selected_role_id; do not inject here to avoid accent flip on re-click.

    # ===== Design system: DataCamp + Notion + premium SaaS =====
    page_css = f"""
<style>
/* ===== Control bar: clean, structured ===== */
.control-bar {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.control-group {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}}
.control-icon-box {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1rem;
    flex-shrink: 0;
}}
.control-info {{
    min-width: 0;
}}
.control-label {{
    font-size: 0.625rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-bottom: 0.05rem;
}}
.control-divider {{
    width: 1px;
    height: 28px;
    background: rgba(71,85,105,0.4);
    flex-shrink: 0;
}}

/* ===== Hero card: content-first, calm ===== */
.hero-card {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}}
.hero-content {{
    position: relative;
}}
.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid {theme['primary']}35;
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.6875rem;
    color: {theme['primary']};
    font-weight: 600;
    margin-bottom: 0.75rem;
}}
.hero-title {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    line-height: 1.25;
}}
.hero-subtitle {{
    font-size: 0.9375rem;
    color: #94a3b8;
    max-width: 540px;
    line-height: 1.6;
    margin-bottom: 1.25rem;
}}
.hero-pills {{
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
}}
.hero-pill {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 999px;
    padding: 0.5rem 1rem;
    transition: border-color 0.2s ease;
}}
.hero-pill:hover {{
    border-color: {theme['primary']}35;
}}
.hero-pill-icon {{
    font-size: 1rem;
}}
.hero-pill-content {{
    display: flex;
    flex-direction: column;
}}
.hero-pill-label {{
    font-size: 0.625rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
}}
.hero-pill-value {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {theme['primary']};
}}

/* ===== Readiness: progress-oriented, clear hierarchy ===== */
.readiness-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.75rem;
    position: relative;
}}
.readiness-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: {theme['primary']};
    border-radius: 12px 0 0 12px;
}}
.readiness-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}}
.readiness-info {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
}}
.readiness-icon-box {{
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1.25rem;
}}
.readiness-text {{
    display: flex;
    flex-direction: column;
}}
.readiness-label {{
    font-size: 0.625rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-bottom: 0.15rem;
}}
.readiness-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
}}
.readiness-score {{
    text-align: right;
}}
.readiness-percentage {{
    font-size: 2.25rem;
    font-weight: 700;
    color: {theme['primary']};
    line-height: 1;
}}
.readiness-score-label {{
    font-size: 0.6875rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.readiness-bar-wrapper {{
    margin-bottom: 1rem;
}}
.readiness-bar-bg {{
    width: 100%;
    height: 8px;
    background: rgba(30,41,59,0.8);
    border-radius: 4px;
    overflow: hidden;
}}
.readiness-bar-fill {{
    height: 100%;
    border-radius: 4px;
    background: {theme['primary']};
    transition: width 0.4s ease;
}}
.readiness-message {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(71,85,105,0.4);
    border-radius: 8px;
}}
.readiness-message-icon {{
    font-size: 1.1rem;
}}
.readiness-message-text {{
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.5;
}}

/* ===== Category container: modular, consistent card ===== */
.category-container {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
    transition: border-color 0.2s ease;
}}
.category-container:hover {{
    border-color: {theme['primary']}30;
}}
.category-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(71,85,105,0.35);
}}
.category-icon {{
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1.2rem;
}}
.category-info {{
    flex: 1;
}}
.category-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.15rem;
}}
.category-desc {{
    font-size: 0.75rem;
    color: #64748b;
}}
.category-badge {{
    background: rgba(34,211,238,0.15);
    color: {theme['primary']};
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.6875rem;
    font-weight: 600;
    border: 1px solid {theme['primary']}25;
}}

/* ===== Skill cards: consistent with card system ===== */
.skill-card {{
    background: rgba(30,41,59,0.45);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    transition: border-color 0.2s ease;
}}
.skill-card:hover {{
    border-color: {theme['primary']}30;
}}
.skill-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}}
.skill-info {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.skill-icon {{
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(71,85,105,0.4);
    border: 1px solid rgba(71,85,105,0.5);
    border-radius: 8px;
    font-size: 1rem;
}}
.skill-name {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: #f1f5f9;
}}
.skill-difficulty {{
    font-size: 0.625rem;
    background: {theme['primary']}18;
    color: {theme['primary']};
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    font-weight: 600;
}}
.skill-level-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}}
.skill-level-label {{
    font-size: 0.75rem;
    color: #94a3b8;
}}
.skill-level-value {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {theme['primary']};
}}
.skill-progress-bg {{
    width: 100%;
    height: 6px;
    background: rgba(30,41,59,0.8);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}}
.skill-progress-fill {{
    height: 100%;
    border-radius: 3px;
    background: {theme['primary']};
    transition: width 0.4s ease;
}}
.skill-helper {{
    font-size: 0.6875rem;
    color: #64748b;
}}

/* ===== AI insight: smart, productized list rows ===== */
.ai-panel {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1.5rem 0;
}}
.ai-header {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
}}
.ai-icon {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1.1rem;
}}
.ai-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
}}
.ai-subtitle {{
    font-size: 0.8125rem;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    padding-left: 0.5rem;
    border-left: 2px solid {theme['primary']}40;
}}
.ai-items {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}
.ai-item {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(71,85,105,0.4);
    border-radius: 8px;
    transition: border-color 0.2s ease;
}}
.ai-item:hover {{
    border-color: {theme['primary']}30;
}}
.ai-rank {{
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['primary']};
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    color: #fff;
}}
.ai-skill-name {{
    flex: 1;
    font-size: 0.875rem;
    font-weight: 600;
    color: #e2e8f0;
}}
.ai-skill-level {{
    font-size: 0.6875rem;
    color: #64748b;
    background: rgba(71,85,105,0.4);
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
}}

/* ===== CTA: focused, no decorative animation ===== */
.cta-card {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-top: 1.75rem;
    text-align: center;
}}
.cta-content {{
    position: relative;
}}
.cta-icon {{
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
    display: block;
}}
.cta-title {{
    font-size: 1.375rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}}
.cta-subtitle {{
    font-size: 0.9375rem;
    color: #94a3b8;
    margin-bottom: 1.5rem;
    max-width: 440px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
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
            options=options_with_placeholder,
            index=min(default_index, len(options_with_placeholder) - 1),
            label_visibility="collapsed",
            key="role_select_main"
        )

    if role_name == ROLE_PLACEHOLDER:
        role_name = None
    if role_name and role_name in role_options:
        selected_role_id = role_options[role_name]
        selected_role = roles[selected_role_id]
    else:
        selected_role_id = None
        selected_role = list(roles.values())[0] if roles else None

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

    theme = get_role_theme(selected_role_id)

    # ===== SECTION 2: PREMIUM HERO CARD =====
    safe_role_name = _safe_html(selected_role.display_name) if selected_role else "—"
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
                    <span class="hero-pill-value">{safe_role_name}</span>
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
        <span class="readiness-message-text">{_safe_html(hint_text)}</span>
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
            safe_cat = _safe_html(category)
            safe_desc = _safe_html(cat_desc)

            st.markdown(f"""
<div class="category-container">
    <div class="category-header">
        <div class="category-icon">{cat_icon}</div>
        <div class="category-info">
            <div class="category-title">{safe_cat}</div>
            <div class="category-desc">{safe_desc}</div>
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
                    safe_title = _safe_html(mod.title)
                    safe_skill_name = _safe_html(skill_name)
                    st.markdown(f"""
<div class="skill-card">
    <div class="skill-header">
        <div class="skill-info">
            <div class="skill-name">{safe_title}</div>
        </div>
    </div>
    <div class="skill-helper">Beceri: {safe_skill_name}</div>
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
            safe_cat = _safe_html(category)
            st.markdown(f"""
<div class="category-container">
    <div class="category-header">
        <div class="category-icon">{cat_icon}</div>
        <div class="category-info">
            <div class="category-title">{safe_cat}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
            skill_cols = st.columns(2)
            for idx, (skill_id, skill) in enumerate(category_skills):
                with skill_cols[idx % 2]:
                    cv = st.session_state.get(f"skill_{skill_id}", 2)
                    safe_skill_name = _safe_html(skill.display_name)
                    st.markdown(f"""
<div class="skill-card">
    <div class="skill-header">
        <div class="skill-name">{safe_skill_name}</div>
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

    ai_item_parts = []
    for idx, (sid, sname, sval) in enumerate(top_3_to_improve):
        safe_sname = _safe_html(sname)
        ai_item_parts.append(
            "<div class=\"ai-item\">"
            "<div class=\"ai-rank\">" + str(idx + 1) + "</div>"
            "<div class=\"ai-skill-name\">" + safe_sname + "</div>"
            "<div class=\"ai-skill-level\">Seviye " + str(sval) + "/5</div>"
            "</div>"
        )
    ai_items_inner = "".join(ai_item_parts)
    ai_panel_html = (
        "<div class=\"ai-panel\">"
        "<div class=\"ai-header\">"
        "<div class=\"ai-icon\">🤖</div>"
        "<div class=\"ai-title\">AI Öneri Motoru</div>"
        "</div>"
        "<div class=\"ai-subtitle\">Mevcut beceri seviyelerine göre öncelikli odaklanman gereken alanlar:</div>"
        "<div class=\"ai-items\">" + ai_items_inner + "</div>"
        "</div>"
    )
    st.markdown(ai_panel_html, unsafe_allow_html=True)

    # ===== SECTION 6: CTA =====
    cta_weeks = int(duration_weeks)
    cta_html = (
        "<div class=\"cta-card\">"
        "<div class=\"cta-content\">"
        "<span class=\"cta-icon\">🗺️</span>"
        "<div class=\"cta-title\">Yol Haritanı Oluştur</div>"
        "<div class=\"cta-subtitle\">Belirlediğin becerilere göre " + str(cta_weeks) + " haftalık kişiselleştirilmiş öğrenme planın hazırlanacak.</div>"
        "</div></div>"
    )
    st.markdown(cta_html, unsafe_allow_html=True)

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
        task_text = "Henüz tanımlı bir görev yok. Hedef ve Profil sayfasından yol haritanı oluştur."
        if weeks:
            first_week = weeks[0]
            if first_week.skills and first_week.skills[0].mini_tasks:
                task_text = first_week.skills[0].mini_tasks[0]

        render_todays_task_card(task_text, selected_role_id)

        if st.button("📝 Hedef ve Profil sayfasına git", key="task_to_profile_btn"):
            set_active_section("goal_and_profile")
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
            weekly_progress = f"{total_weeks_count} haftalık planda {active_weeks} haftada odaklı çalışma var. Toplam {total_hours:.0f} saat öğrenme süresi."

        skill_summary = "Öne çıkan bir beceri boşluğu özeti için henüz veri yok."
        if analysis_result and analysis_result.skill_gaps:
            top_gaps = analysis_result.skill_gaps[:3]
            summary_items = [
                f"{gap.display_name}: {gap.current_level} → {gap.required_level}"
                for gap in top_gaps
            ]
            skill_summary = " · ".join(summary_items)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        safe_weekly = _safe_html(weekly_progress)
        safe_summary = _safe_html(skill_summary)
        progress_card_html = f"""
<div class="yh-dashboard-card">
    <div class="yh-dashboard-card-header">
        <div class="yh-dashboard-card-icon">📈</div>
        <div class="yh-dashboard-card-title">Haftalık İlerleme</div>
    </div>
    <div class="yh-dashboard-card-content">{safe_weekly}</div>
</div>
"""
        st.markdown(progress_card_html, unsafe_allow_html=True)

        skill_card_html = f"""
<div class="yh-dashboard-card">
    <div class="yh-dashboard-card-header">
        <div class="yh-dashboard-card-icon">🎯</div>
        <div class="yh-dashboard-card-title">Beceri Gelişim Özeti</div>
    </div>
    <div class="yh-dashboard-card-content">{safe_summary}</div>
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
            set_active_section("skill_gap")
            st.rerun()
    with qa_col2:
        if st.button("🗺️ Yol Haritası", use_container_width=True, key="qa_roadmap"):
            set_active_section("learning_roadmap")
            st.rerun()
    with qa_col3:
        if st.button("🎯 Profil Güncelle", use_container_width=True, key="qa_profile"):
            set_active_section("goal_and_profile")
            st.rerun()


def _build_skill_dependency_figure(
    gap_result: GapAnalysisResult,
    skills: Dict[str, Skill],
    theme: Dict[str, str],
) -> go.Figure | None:
    """
    Build a read-only Plotly figure for skill dependency graph.
    Uses only gap_result and skills; no state or logic changes.
    Node states: learned (prereq not in gap list), gap, prerequisite (same as learned), locked (gap with missing prereqs).
    """
    gap_ids = {g.skill_id for g in gap_result.skill_gaps}
    gaps_by_id = {g.skill_id: g for g in gap_result.skill_gaps}
    nodes_set: set[str] = set(gap_ids)
    for g in gap_result.skill_gaps:
        skill = skills.get(g.skill_id)
        if skill:
            for p in skill.prerequisites:
                if p in skills:
                    nodes_set.add(p)
    if not nodes_set:
        return None

    G = nx.DiGraph()
    G.add_nodes_from(nodes_set)
    for sid in nodes_set:
        skill = skills.get(sid)
        if not skill:
            continue
        for p in skill.prerequisites:
            if p in nodes_set:
                G.add_edge(p, sid)

    # Hierarchical layout: level = max predecessor level + 1, roots at 0
    level_of: Dict[str, int] = {}
    for _ in range(len(nodes_set) + 1):
        for n in G.nodes():
            preds = list(G.predecessors(n))
            if not preds:
                level_of[n] = 0
            else:
                level_of[n] = 1 + max(level_of.get(p, 0) for p in preds)
    levels: Dict[int, List[str]] = {}
    for n, lev in level_of.items():
        levels.setdefault(lev, []).append(n)
    max_level = max(levels.keys()) if levels else 0
    # Position: x = level (left to right), y = spread within level
    pos: Dict[str, Tuple[float, float]] = {}
    for lev in range(max_level + 1):
        nodes_in_level = levels.get(lev, [])
        for i, n in enumerate(nodes_in_level):
            num = len(nodes_in_level)
            y = (i - (num - 1) / 2) * 1.2 if num > 1 else 0
            pos[n] = (float(lev), y)

    node_list = list(G.nodes())
    node_x = [pos[n][0] for n in node_list]
    node_y = [pos[n][1] for n in node_list]
    primary = theme.get("primary", "#22d3ee")
    success = theme.get("success", "#10b981")

    def _state(sid: str) -> str:
        if sid not in gaps_by_id:
            return "learned"
        g = gaps_by_id[sid]
        if g.missing_prerequisites:
            return "locked"
        return "gap"

    state_colors = {
        "learned": success,
        "prerequisite": "#64748b",
        "gap": primary,
        "locked": "#475569",
    }
    node_color = [state_colors.get(_state(n), "#64748b") for n in node_list]
    node_names = [skills[n].display_name if n in skills else n for n in node_list]

    edge_x: List[float] = []
    edge_y: List[float] = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color="rgba(71,85,105,0.6)"),
        hoverinfo="none",
        mode="lines",
    )
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_names,
        textposition="top center",
        textfont=dict(size=11, color="#e2e8f0"),
        hoverinfo="text",
        hovertext=[f"{name} ({_state(n)})" for name, n in zip(node_names, node_list)],
        marker=dict(
            size=28,
            color=node_color,
            line=dict(width=2, color="#1e293b"),
            symbol="circle",
        ),
    )
    layout = go.Layout(
        title=dict(text="Beceri Bağımlılık Grafiği", font=dict(color="#e2e8f0", size=16)),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(showgrid=True, gridcolor="rgba(51,65,85,0.25)", zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(51,65,85,0.25)", zeroline=False, showticklabels=False),
        margin=dict(b=40, t=50, l=40, r=40),
        height=400,
    )
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig


def _category_badge_color(category: str) -> str:
    """Stable badge color per category for table; display only."""
    palette = {
        "veri": "rgba(34,211,238,0.25)",
        "data": "rgba(34,211,238,0.25)",
        "frontend": "rgba(167,139,250,0.25)",
        "backend": "rgba(34,197,94,0.2)",
        "genel": "rgba(71,85,105,0.4)",
        "yazılım": "rgba(99,102,241,0.25)",
    }
    key = (category or "genel").strip().lower()
    return palette.get(key, "rgba(71,85,105,0.4)")


def _render_gap_skill_table(df: pd.DataFrame, primary: str) -> None:
    """Render enhanced skill gap table: same data, priority color scale, category and prereq as pills."""
    if df.empty:
        return
    priority_vals = df["Öncelik Skoru"]
    p_min, p_max = float(priority_vals.min()), float(priority_vals.max())
    p_range = (p_max - p_min) or 1.0

    headers = [
        "Beceri", "Kategori", "Zorluk (1-5)", "Hızlı Kazanım",
        "Mevcut Seviye", "Hedef Seviye", "Boşluk", "Rol Ağırlığı",
        "Öncelik Skoru", "Eksik Önkoşullar",
    ]
    thead = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>"
    rows = []
    for _, row in df.iterrows():
        p = float(row["Öncelik Skoru"])
        norm = (p - p_min) / p_range
        # Background: low = slate, high = primary tint (restrained)
        r, g, b = 34, 211, 238
        alpha = 0.08 + 0.18 * norm
        bg = f"rgba({r},{g},{b},{alpha:.2f})"
        priority_style = f"background:{bg};"
        cat = str(row["Kategori"])
        cat_color = _category_badge_color(cat)
        cat_esc = html_module.escape(cat)
        prereq_text = str(row["Eksik Önkoşullar"])
        if prereq_text == "-" or not prereq_text.strip():
            prereq_html = "—"
        else:
            parts = [p.strip() for p in prereq_text.split(",") if p.strip()]
            prereq_html = " ".join(
                f'<span class="gap-pill" style="background:rgba(71,85,105,0.5);color:#94a3b8;">{html_module.escape(part)}</span>'
                for part in parts
            )
        cells = [
            html_module.escape(str(row["Beceri"])),
            f'<span class="gap-pill" style="background:{cat_color};color:#e2e8f0;">{cat_esc}</span>',
            str(int(row["Zorluk (1-5)"])),
            str(row["Hızlı Kazanım"]),
            str(int(row["Mevcut Seviye"])),
            str(int(row["Hedef Seviye"])),
            str(int(row["Boşluk"])),
            f"{row['Rol Ağırlığı']:.2f}",
            f'<span class="gap-priority-cell" style="{priority_style}">{p:.2f}</span>',
            prereq_html,
        ]
        rows.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    tbody = "<tbody>" + "".join(rows) + "</tbody>"
    table_html = f'<div class="gap-skill-table-wrap"><table class="gap-skill-table">{thead}{tbody}</table></div>'
    st.markdown(table_html, unsafe_allow_html=True)


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
    theme = get_role_theme(selected_role_id)
    primary = theme.get("primary", "#22d3ee")

    # Scoped styles for Skill Gap Analysis only (no logic/state changes)
    gap_css = f"""
<style>
/* Skill Gap Analysis: visual refinement only */
body:has(#gap-analysis-marker) .yh-metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
}}
body:has(#gap-analysis-marker) .yh-metric.yh-metric-priority {{
    border-left: 3px solid {primary}66;
    background: rgba(34,211,238,0.04);
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] {{
    margin-top: 0.25rem;
    margin-bottom: 2rem;
    border-radius: 10px;
    overflow: hidden;
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] table {{
    border-collapse: separate;
    border-spacing: 0;
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] th {{
    padding: 0.65rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] td {{
    padding: 0.6rem 0.75rem;
    vertical-align: middle;
    font-size: 0.8125rem;
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] tbody tr {{
    border-bottom: 1px solid rgba(71,85,105,0.25);
}}
body:has(#gap-analysis-marker) [data-testid="stDataFrame"] td {{
    font-variant-numeric: tabular-nums;
}}
body:has(#gap-analysis-marker) .gap-analysis-caption {{
    margin-bottom: 1rem;
    color: #94a3b8;
    font-size: 0.8125rem;
    line-height: 1.5;
}}
body:has(#gap-analysis-marker) [data-testid="stVerticalBlock"] > div:has([data-testid="stPlotlyChart"]) {{
    margin-bottom: 2rem;
}}
/* Prerequisite: info box and table spacing */
body:has(#gap-analysis-marker) div[data-testid="stTable"] {{
    margin-top: 1rem;
}}
body:has(#gap-analysis-marker) div[data-testid="stTable"] table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    overflow: hidden;
    font-size: 0.8125rem;
}}
body:has(#gap-analysis-marker) div[data-testid="stTable"] th {{
    padding: 0.6rem 0.85rem;
    text-align: left;
    font-weight: 600;
    background: rgba(30,41,59,0.6);
}}
body:has(#gap-analysis-marker) div[data-testid="stTable"] td {{
    padding: 0.6rem 0.85rem;
    border-bottom: 1px solid rgba(71,85,105,0.2);
}}
body:has(#gap-analysis-marker) div[data-testid="stTable"] tr:last-child td {{
    border-bottom: none;
}}
/* Top Priority Skills cards */
body:has(#gap-analysis-marker) .gap-priority-cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}}
body:has(#gap-analysis-marker) .gap-priority-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    transition: border-color 0.2s ease;
}}
body:has(#gap-analysis-marker) .gap-priority-card:hover {{
    border-color: {primary}40;
}}
body:has(#gap-analysis-marker) .gap-priority-card-name {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}}
body:has(#gap-analysis-marker) .gap-priority-card-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #94a3b8;
}}
body:has(#gap-analysis-marker) .gap-priority-card-badge {{
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    font-size: 0.6875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}
/* Enhanced skill table */
body:has(#gap-analysis-marker) .gap-skill-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
    font-size: 0.8125rem;
}}
body:has(#gap-analysis-marker) .gap-skill-table th {{
    padding: 0.65rem 0.75rem;
    text-align: left;
    font-weight: 600;
    background: rgba(30,41,59,0.7);
    color: #e2e8f0;
    border-bottom: 1px solid rgba(71,85,105,0.4);
}}
body:has(#gap-analysis-marker) .gap-skill-table td {{
    padding: 0.6rem 0.75rem;
    vertical-align: middle;
    border-bottom: 1px solid rgba(71,85,105,0.2);
    color: #e2e8f0;
}}
body:has(#gap-analysis-marker) .gap-skill-table-wrap {{
    overflow-x: auto;
    margin-bottom: 2rem;
}}
body:has(#gap-analysis-marker) .gap-skill-table tbody tr:hover td {{
    background: rgba(51,65,85,0.2);
}}
body:has(#gap-analysis-marker) .gap-skill-table .gap-pill {{
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    font-size: 0.6875rem;
    margin: 0.1rem 0.15rem 0.1rem 0;
    white-space: nowrap;
}}
body:has(#gap-analysis-marker) .gap-skill-table .gap-priority-cell {{
    border-radius: 4px;
    font-variant-numeric: tabular-nums;
    font-weight: 600;
}}
/* Prerequisite explanation panel */
body:has(#gap-analysis-marker) .gap-prereq-panel {{
    background: rgba(30,41,59,0.4);
    border: 1px solid rgba(71,85,105,0.4);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-panel-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-block {{
    margin-bottom: 1.25rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-block:last-child {{
    margin-bottom: 0;
}}
body:has(#gap-analysis-marker) .gap-prereq-foundation {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {primary};
    margin-bottom: 0.35rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-depends {{
    font-size: 0.8125rem;
    color: #94a3b8;
    margin-bottom: 0.25rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-skills {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
}}
body:has(#gap-analysis-marker) .gap-prereq-skill-pill {{
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    background: rgba(71,85,105,0.5);
    border: 1px solid rgba(71,85,105,0.6);
    color: #e2e8f0;
}}
</style>
"""
    st.markdown('<div id="gap-analysis-marker" aria-hidden="true" style="position:absolute;left:-9999px;"></div>', unsafe_allow_html=True)
    st.markdown(gap_css, unsafe_allow_html=True)

    table_rows = gaps_to_table(gap_result, skills)
    df = pd.DataFrame(table_rows)

    avg_gap = df["Boşluk"].mean() if not df.empty else 0
    high_priority = (df["Öncelik Skoru"] > df["Öncelik Skoru"].median()).sum() if not df.empty else 0

    metrics_html = f"""
<div class="yh-metrics-grid">
    <div class="yh-metric">
        <div class="yh-metric-value">{len(df)}</div>
        <div class="yh-metric-label">Toplam Eksik Beceri</div>
    </div>
    <div class="yh-metric">
        <div class="yh-metric-value">{avg_gap:.1f}</div>
        <div class="yh-metric-label">Ortalama Boşluk</div>
    </div>
    <div class="yh-metric yh-metric-priority">
        <div class="yh-metric-value">{int(high_priority)}</div>
        <div class="yh-metric-label">Yüksek Öncelikli</div>
    </div>
</div>
"""
    st.markdown(metrics_html, unsafe_allow_html=True)

    st.markdown(
        f'<p class="gap-analysis-caption">Seçilen rol: {html_module.escape(gap_result.role.display_name)}. '
        "Aşağıdaki tablo, mevcut ve hedef seviyeler arasındaki boşlukları özetler.</p>",
        unsafe_allow_html=True,
    )

    # Top Priority Skills panel (top 5 by priority score; same data, no new logic)
    top_n = min(5, len(df))
    if top_n > 0:
        top_df = df.nlargest(top_n, "Öncelik Skoru")
        cards_html_parts = []
        for _, row in top_df.iterrows():
            cat_esc = html_module.escape(str(row["Kategori"]))
            name_esc = html_module.escape(str(row["Beceri"]))
            cards_html_parts.append(
                f'<div class="gap-priority-card">'
                f'<div class="gap-priority-card-name">{name_esc}</div>'
                f'<div class="gap-priority-card-meta">'
                f'<span>Boşluk: {int(row["Boşluk"])}</span>'
                f'<span>Öncelik: {row["Öncelik Skoru"]:.1f}</span>'
                f'<span class="gap-priority-card-badge" style="background:rgba(34,211,238,0.2);color:{primary};">{cat_esc}</span>'
                f'</div></div>'
            )
        st.markdown(
            '<div class="gap-priority-cards">' + "".join(cards_html_parts) + "</div>",
            unsafe_allow_html=True,
        )

    # Enhanced skill table (same columns and data; priority scale, category and prereq as badges)
    _render_gap_skill_table(df, primary)

    # Keep full data available for chart (same df)

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

    # Read-only Skill Dependency Graph (visualization only; no logic/state changes)
    dep_fig = _build_skill_dependency_figure(gap_result, skills, theme)
    if dep_fig is not None:
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        render_section_header("🔗", "Beceri Bağımlılık Grafiği")
        st.caption("Beceriler arasındaki önkoşul ilişkileri. Yeşil: önkoşul (tamamlanmış/bağımlılık), cyan: eksik beceri, koyu: önkoşulu eksik.")
        st.plotly_chart(dep_fig, use_container_width=True)

    # Prerequisite explanation panel: "Önce öğrenmen gereken temeller" (grouped by foundation skill)
    prereq_to_dependents: Dict[str, List[str]] = {}
    for gap in gap_result.skill_gaps:
        for prereq_id in gap.missing_prerequisites:
            prereq_to_dependents.setdefault(prereq_id, []).append(gap.display_name)
    if prereq_to_dependents:
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        render_section_header("📚", "Önce öğrenmen gereken temeller")
        st.caption("Aşağıdaki becerileri tamamladıktan sonra ilgili gelişmiş becerilere daha verimli çalışabilirsin.")
        panel_parts = []
        for prereq_id, dependents in sorted(prereq_to_dependents.items(), key=lambda x: (x[0], 0)):
            prereq_skill = skills.get(prereq_id)
            foundation_name = prereq_skill.display_name if prereq_skill else prereq_id
            foundation_esc = html_module.escape(foundation_name)
            dep_esc = [html_module.escape(d) for d in dependents]
            pills = "".join(
                f'<span class="gap-prereq-skill-pill">{d}</span>' for d in dep_esc
            )
            panel_parts.append(
                f'<div class="gap-prereq-block">'
                f'<div class="gap-prereq-foundation">{foundation_esc}</div>'
                f'<div class="gap-prereq-depends">Bu beceri şunlar için gerekli:</div>'
                f'<div class="gap-prereq-skills">{pills}</div>'
                f'</div>'
            )
        st.markdown(
            '<div class="gap-prereq-panel">' + "".join(panel_parts) + "</div>",
            unsafe_allow_html=True,
        )


def _learning_analytics_from_weeks(
    weeks: List[WeekPlan],
) -> Tuple[Dict[str, float], float, str, float, str, int]:
    """
    Derive learning analytics from the same weekly plan data (no new logic).
    Returns: (hours_by_skill, total_hours, top_skill_name, top_skill_hours, hardest_name, hardest_difficulty).
    """
    hours_by_skill: Dict[str, float] = {}
    total_hours = 0.0
    hardest_name, hardest_difficulty = "", 0
    for week in weeks:
        for skill in week.skills:
            hours_by_skill[skill.display_name] = hours_by_skill.get(skill.display_name, 0.0) + skill.estimated_hours
            total_hours += skill.estimated_hours
            if skill.difficulty >= hardest_difficulty:
                hardest_difficulty = skill.difficulty
                hardest_name = skill.display_name
    if not hours_by_skill:
        return {}, 0.0, "", 0.0, hardest_name or "—", hardest_difficulty
    top_skill_name = max(hours_by_skill.keys(), key=lambda k: hours_by_skill[k])
    top_skill_hours = hours_by_skill[top_skill_name]
    return hours_by_skill, total_hours, top_skill_name, top_skill_hours, hardest_name or "—", hardest_difficulty


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

    # Learning analytics panel (same data as weekly plan; visualization only)
    hours_by_skill, total_planned, top_skill_name, top_skill_hours, hardest_name, hardest_difficulty = _learning_analytics_from_weeks(
        weeks
    )
    theme = get_role_theme(selected_role_id)
    primary = theme.get("primary", "#22d3ee")

    with st.expander("📊 Öğrenme Analitiği", expanded=False):
        st.caption("Haftalık plana göre süre dağılımı ve özet metrikler")
        if not hours_by_skill:
            st.info("Planlanmış beceri bulunmuyor.")
        else:
            col_chart, col_cards = st.columns([1, 1])
            with col_chart:
                labels = list(hours_by_skill.keys())
                values = list(hours_by_skill.values())
                palette = [primary, "#64748b", "#475569", "#334155", "#06b6d4", "#0ea5e9"]
                colors = [palette[i % len(palette)] for i in range(len(labels))]
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=labels,
                            values=values,
                            hole=0.55,
                            textinfo="label+percent",
                            textposition="outside",
                            hovertemplate="%{label}<br>%{value:.1f} saat (%{percent})<extra></extra>",
                            marker=dict(
                                colors=colors,
                                line=dict(width=2, color="#0f172a"),
                            ),
                        )
                    ],
                    layout=go.Layout(
                        showlegend=False,
                        margin=dict(t=20, b=20, l=20, r=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=320,
                        font=dict(color="#94a3b8", size=12),
                        annotations=[
                            dict(
                                text=f"<b>{total_planned:.1f}h</b>",
                                x=0.5,
                                y=0.5,
                                font=dict(size=22, color="#e2e8f0"),
                                showarrow=False,
                            )
                        ],
                    ),
                )
                fig.update_traces(texttemplate="%{label}<br>%{percent}")
                st.plotly_chart(fig, use_container_width=True)
            with col_cards:
                card_radius = "12px"
                card_style = (
                    "background: rgba(30,41,59,0.5); border: 1px solid rgba(71,85,105,0.45); "
                    f"border-radius: {card_radius}; padding: 1rem 1.25rem; margin-bottom: 0.75rem;"
                )
                top_skill_esc = html_module.escape(top_skill_name)
                hardest_esc = html_module.escape(hardest_name)
                cards_html = f"""
<div style="{card_style}">
    <div style="font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.25rem;">En çok süre ayrılan</div>
    <div style="font-size: 0.9375rem; font-weight: 600; color: #f1f5f9;">{top_skill_esc}</div>
    <div style="font-size: 0.75rem; color: {primary}; margin-top: 0.2rem;">{top_skill_hours:.1f} saat</div>
</div>
<div style="{card_style}">
    <div style="font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.25rem;">En zor beceri</div>
    <div style="font-size: 0.9375rem; font-weight: 600; color: #f1f5f9;">{hardest_esc}</div>
    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem;">Zorluk {hardest_difficulty}/5</div>
</div>
<div style="{card_style} margin-bottom: 0;">
    <div style="font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.25rem;">Toplam planlanan süre</div>
    <div style="font-size: 1.25rem; font-weight: 700; color: {primary};">{total_planned:.1f} saat</div>
</div>
"""
                st.markdown(cards_html, unsafe_allow_html=True)

