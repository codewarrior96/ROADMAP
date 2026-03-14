"""
YolHaritam Premium Design System
Role-aware visual styling, dynamic headings, and premium UI components
"""
from __future__ import annotations

import base64
import html as html_module
from pathlib import Path
from typing import Dict, Tuple
import streamlit as st


def _escape(text: str) -> str:
    """Escape for safe injection into HTML so no raw tags are shown as text."""
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


# Refined dark theme: cyan/electric blue primary, soft violet secondary, controlled green success.
# Glow used sparingly for emphasis only.
ROLE_THEMES: Dict[str, Dict[str, str]] = {
    "ai_engineer": {
        "primary": "#22d3ee",
        "secondary": "#a78bfa",
        "accent": "#818cf8",
        "gradient_start": "rgba(34,211,238,0.12)",
        "gradient_end": "rgba(167,139,250,0.08)",
        "glow": "rgba(34,211,238,0.08)",
        "success": "#10b981",
        "label": "AI Engineer Yolculuğu",
    },
    "data_analyst": {
        "primary": "#06b6d4",
        "secondary": "#a78bfa",
        "accent": "#22d3ee",
        "gradient_start": "rgba(6,182,212,0.12)",
        "gradient_end": "rgba(167,139,250,0.08)",
        "glow": "rgba(6,182,212,0.08)",
        "success": "#10b981",
        "label": "Data Analyst Yolculuğu",
    },
    "frontend_developer": {
        "primary": "#0ea5e9",
        "secondary": "#a78bfa",
        "accent": "#38bdf8",
        "gradient_start": "rgba(14,165,233,0.12)",
        "gradient_end": "rgba(167,139,250,0.08)",
        "glow": "rgba(14,165,233,0.08)",
        "success": "#10b981",
        "label": "Frontend Developer Yolculuğu",
    },
    "data_scientist": {
        "primary": "#38bdf8",
        "secondary": "#a78bfa",
        "accent": "#22d3ee",
        "gradient_start": "rgba(56,189,248,0.12)",
        "gradient_end": "rgba(167,139,250,0.08)",
        "glow": "rgba(56,189,248,0.08)",
        "success": "#10b981",
        "label": "Data Scientist Yolculuğu",
    },
    "default": {
        "primary": "#22d3ee",
        "secondary": "#a78bfa",
        "accent": "#818cf8",
        "gradient_start": "rgba(34,211,238,0.1)",
        "gradient_end": "rgba(167,139,250,0.06)",
        "glow": "rgba(34,211,238,0.06)",
        "success": "#10b981",
        "label": "Kariyer Yolculuğu",
    },
}


def get_role_theme(role_id: str | None) -> Dict[str, str]:
    if role_id is None:
        return ROLE_THEMES["default"]
    role_key = role_id.lower().replace(" ", "_").replace("-", "_")
    return ROLE_THEMES.get(role_key, ROLE_THEMES["default"])


def get_dynamic_title(role_display_name: str | None) -> Tuple[str, str]:
    if role_display_name:
        title = f"{role_display_name} Yolculuğu"
        subtitle = "Seçtiğin role ulaşmak için kişiselleştirilmiş öğrenme ve kariyer rotan"
    else:
        title = "Kariyer Yolculuğun"
        subtitle = "Hedef rolüne ulaşmak için kişiselleştirilmiş öğrenme yol haritası"
    return title, subtitle


def inject_global_styles(role_id: str | None = None) -> None:
    theme = get_role_theme(role_id)
    success = theme.get("success", "#10b981")

    css = f"""
<style>
/* ===== YolHaritam Design System: DataCamp + Notion + Premium SaaS ===== */
/* Visual system constants: card radius 12px; card padding 1.25rem 1.5rem; section spacing 2rem; section title 1rem/600/mb 1rem; caption 0.8125rem; metric label 0.6875rem; pill radius 999px */

/* Global: rich dark navy / blue-black, calm and premium */
.stApp {{
    background: linear-gradient(180deg, 
        #0b1220 0%, 
        #0f172a 25%,
        #111827 55%,
        #0f172a 100%
    ) !important;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(ellipse 70% 40% at 50% -15%, {theme['glow']}, transparent 55%);
    pointer-events: none;
    z-index: 0;
}}

/* Main: intentional reading flow, alignment */
.main .block-container {{
    position: relative;
    z-index: 1;
    max-width: 1120px !important;
    padding: 2rem 1.5rem 3rem !important;
}}

/* ===== Typography: clear hierarchy, editorial feel ===== */
h1, h2, h3, h4, h5, h6 {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif !important;
    letter-spacing: -0.02em;
    color: #f1f5f9 !important;
}}

h1 {{
    font-size: 1.875rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    color: #f1f5f9 !important;
}}

h2 {{
    font-size: 1.375rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    line-height: 1.35 !important;
}}

h3 {{
    font-size: 1.125rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    line-height: 1.4 !important;
}}

p, .stMarkdown {{
    color: #94a3b8 !important;
    line-height: 1.6 !important;
    font-size: 0.9375rem !important;
}}

.stCaption p {{
    color: #64748b !important;
    font-size: 0.8125rem !important;
    line-height: 1.5 !important;
}}

/* ===== Sidebar: premium AI workspace, calm and minimal ===== */
[data-testid="stSidebar"] {{
    background: rgba(15,23,42,0.97) !important;
    border-right: 1px solid rgba(71,85,105,0.4) !important;
}}

[data-testid="stSidebar"] .stRadio > label {{
    font-size: 0.6875rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b !important;
}}

[data-testid="stSidebar"] .stRadio > div {{
    gap: 0.25rem !important;
}}

[data-testid="stSidebar"] .stRadio > div > label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 0.5rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.2s ease !important;
    color: #94a3b8 !important;
}}

[data-testid="stSidebar"] .stRadio > div > label:hover {{
    background: rgba(51,65,85,0.35) !important;
    border-color: rgba(71,85,105,0.5) !important;
}}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {{
    background: {theme['gradient_start']} !important;
    border-color: {theme['primary']}40 !important;
    color: #f1f5f9 !important;
}}
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"]:hover,
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"]:focus,
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"]:active {{
    background: {theme['gradient_start']} !important;
    border-color: {theme['primary']}40 !important;
    color: #f1f5f9 !important;
}}

[data-testid="stSidebar"] h1 {{
    font-size: 1.25rem !important;
    margin-bottom: 1.25rem !important;
    font-weight: 600 !important;
}}

[data-testid="stSidebar"] hr {{
    border-color: rgba(71,85,105,0.35) !important;
    margin: 1.25rem 0 !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    background: transparent !important;
    border: 1px solid rgba(248,113,113,0.35) !important;
    color: #fca5a5 !important;
    border-radius: 0.5rem !important;
    padding: 0.55rem !important;
    font-size: 0.8125rem !important;
    transition: all 0.2s ease !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(248,113,113,0.08) !important;
    border-color: rgba(248,113,113,0.5) !important;
}}

/* ===== Card system: consistent radius, spacing, subtle depth ===== */
.yh-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.03);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}

.yh-card:hover {{
    border-color: {theme['primary']}35;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.03);
}}

.yh-card-highlight {{
    background: {theme['gradient_start']};
    border-color: {theme['primary']}40;
}}

/* ===== Hero: structured, calm, content-first ===== */
.yh-hero {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-bottom: 2rem;
    position: relative;
}}

.yh-hero-brand {{
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {theme['primary']};
    font-weight: 600;
    margin-bottom: 0.4rem;
}}

.yh-hero-title {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
    line-height: 1.25;
}}

.yh-hero-subtitle {{
    font-size: 0.9375rem;
    color: #94a3b8;
    max-width: 560px;
    line-height: 1.6;
}}

.yh-hero-badges {{
    display: flex;
    gap: 0.75rem;
    margin-top: 1.25rem;
    flex-wrap: wrap;
}}

.yh-hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 999px;
    padding: 0.4rem 0.85rem;
    font-size: 0.8125rem;
    color: #e2e8f0;
}}

.yh-hero-badge-icon {{
    font-size: 0.9rem;
}}

.yh-hero-badge-value {{
    font-weight: 600;
    color: {theme['primary']};
}}

/* ===== Metric cards (same radius/border as .yh-card, compact padding) ===== */
.yh-metric {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
    transition: border-color 0.2s ease;
}}

.yh-metric:hover {{
    border-color: {theme['primary']}35;
}}

.yh-metric-value {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
}}

.yh-metric-label {{
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
}}

/* ===== Section titles: clear hierarchy (unified across dashboard) ===== */
.yh-section-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.yh-section-icon {{
    font-size: 1.1rem;
}}

/* ===== Form Elements ===== */
.stSelectbox > div > div {{
    background: rgba(30,41,59,0.6) !important;
    border: 1px solid rgba(71,85,105,0.5) !important;
    border-radius: 8px !important;
}}

.stSelectbox > div > div:focus-within {{
    border-color: {theme['primary']} !important;
    box-shadow: 0 0 0 2px {theme['primary']}25 !important;
}}

.stNumberInput > div > div > input {{
    background: rgba(30,41,59,0.6) !important;
    border: 1px solid rgba(71,85,105,0.5) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}}

.stTextInput > div > div > input {{
    background: rgba(30,41,59,0.6) !important;
    border: 1px solid rgba(71,85,105,0.5) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {theme['primary']} !important;
    box-shadow: 0 0 0 2px {theme['primary']}25 !important;
}}

/* ===== Slider Styling ===== */
.stSlider > div > div > div > div {{
    background: {theme['primary']} !important;
}}

.stSlider > div > div > div[data-baseweb="slider"] > div {{
    background: rgba(51,65,85,0.6) !important;
}}

/* ===== Buttons: deliberate, controlled states ===== */
.stButton > button {{
    background: {theme['primary']} !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.25rem !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    color: white !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.25) !important;
}}

.stButton > button:hover {{
    filter: brightness(1.08) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important;
}}

/* ===== Dataframe / Table ===== */
.stDataFrame {{
    border-radius: 0.8rem !important;
    overflow: hidden !important;
    max-width: 100% !important;
}}

[data-testid="stDataFrame"] > div {{
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(51,65,85,0.5) !important;
    border-radius: 0.8rem !important;
    overflow-x: auto !important;
}}

/* Responsive table container - prevent overflow on narrow screens */
[data-testid="stDataFrame"] .stDataFrame {{
    min-width: 0 !important;
}}

/* ===== Expander ===== */
.streamlit-expanderHeader {{
    background: rgba(30,41,59,0.6) !important;
    border: 1px solid rgba(51,65,85,0.5) !important;
    border-radius: 0.7rem !important;
    color: #cbd5e1 !important;
}}

.streamlit-expanderHeader:hover {{
    border-color: rgba(99,102,241,0.4) !important;
}}

/* ===== Warning / Info / Success ===== */
.stAlert {{
    border-radius: 0.7rem !important;
}}

/* ===== Plotly Chart Container ===== */
[data-testid="stPlotlyChart"] {{
    background: rgba(15,23,42,0.5) !important;
    border: 1px solid rgba(51,65,85,0.4) !important;
    border-radius: 0.8rem !important;
    padding: 0.5rem !important;
}}

/* ===== Dashboard Card Grid (unified section spacing 2rem) ===== */
.yh-dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
}}

.yh-dashboard-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}

.yh-dashboard-card:hover {{
    border-color: {theme['primary']}35;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.yh-dashboard-card-header {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
}}

.yh-dashboard-card-icon {{
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1rem;
}}

.yh-dashboard-card-title {{
    font-size: 0.875rem;
    font-weight: 600;
    color: #e2e8f0;
}}

.yh-dashboard-card-content {{
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.55;
}}

.yh-dashboard-card-content strong {{
    color: #f1f5f9;
}}

/* ===== Quick Access Links ===== */
.yh-quick-links {{
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}}

.yh-quick-link {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(30,41,59,0.6);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 2rem;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    color: #94a3b8;
    text-decoration: none;
    transition: all 0.2s ease;
}}

.yh-quick-link:hover {{
    background: rgba(51,65,85,0.6);
    border-color: {theme['primary']}44;
    color: #e2e8f0;
}}

/* ===== Login Screen ===== */
.yh-login-container {{
    max-width: 400px;
    margin: 4rem auto;
    text-align: center;
}}

.yh-login-logo {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.yh-login-title {{
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}}

.yh-login-subtitle {{
    font-size: 1rem;
    color: #64748b;
    margin-bottom: 2rem;
}}

/* ===== Progress: controlled green / primary, no glow ===== */
.yh-progress-bar {{
    height: 6px;
    background: rgba(30,41,59,0.8);
    border-radius: 3px;
    overflow: hidden;
    margin: 0.4rem 0;
}}

.yh-progress-fill {{
    height: 100%;
    border-radius: 3px;
    background: {theme['primary']};
    transition: width 0.4s ease;
}}

/* ===== Sidebar profile: premium workspace anchor ===== */
.yh-profile-card {{
    background: rgba(30,41,59,0.4);
    border: 1px solid rgba(71,85,105,0.4);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: center;
}}

.yh-profile-avatar {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    margin: 0 auto 0.6rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: {theme['gradient_start']};
    border: 2px solid {theme['primary']}35;
    overflow: hidden;
}}

.yh-profile-avatar img {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}}

.yh-profile-name {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.15rem;
}}

.yh-profile-role {{
    font-size: 0.75rem;
    color: {theme['primary']};
    font-weight: 500;
    margin-bottom: 0.6rem;
}}

.yh-profile-readiness {{
    background: rgba(15,23,42,0.5);
    border-radius: 8px;
    padding: 0.5rem;
    margin-bottom: 0.6rem;
}}

.yh-profile-readiness-label {{
    font-size: 0.625rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 0.2rem;
}}

.yh-profile-readiness-value {{
    font-size: 1.125rem;
    font-weight: 700;
    color: {theme['primary']};
}}

.yh-profile-progress {{
    height: 4px;
    background: rgba(30,41,59,0.8);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 0.35rem;
}}

.yh-profile-progress-fill {{
    height: 100%;
    border-radius: 2px;
    background: {theme['primary']};
    transition: width 0.4s ease;
}}

.yh-profile-buttons {{
    display: flex;
    gap: 0.4rem;
    margin-top: 0.6rem;
}}

.yh-profile-btn {{
    flex: 1;
    background: rgba(71,85,105,0.35);
    border: 1px solid rgba(71,85,105,0.5);
    border-radius: 6px;
    padding: 0.4rem;
    font-size: 0.6875rem;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}}

.yh-profile-btn:hover {{
    background: rgba(71,85,105,0.5);
    border-color: {theme['primary']}35;
    color: #e2e8f0;
}}

/* ===== Welcome: calm, readable ===== */
.yh-welcome {{
    margin-bottom: 1.25rem;
}}

.yh-welcome-greeting {{
    font-size: 1.375rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.25rem;
}}

.yh-welcome-message {{
    font-size: 0.9375rem;
    color: #94a3b8;
    line-height: 1.55;
}}

/* ===== AI Recommendation: smart, productized, no clutter ===== */
.yh-ai-panel {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}}

.yh-ai-panel-header {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
}}

.yh-ai-panel-icon {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {theme['gradient_start']};
    border-radius: 8px;
    font-size: 1rem;
}}

.yh-ai-panel-title {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: #e2e8f0;
}}

.yh-ai-panel-badge {{
    font-size: 0.625rem;
    background: rgba(167,139,250,0.2);
    color: #c4b5fd;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    margin-left: auto;
    font-weight: 500;
}}

.yh-ai-next-step {{
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {theme['secondary']};
    margin-bottom: 0.25rem;
}}

.yh-ai-skill-name {{
    font-size: 1.125rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}}

.yh-ai-explanation {{
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.55;
    margin-bottom: 0.75rem;
}}

.yh-ai-stats {{
    display: flex;
    gap: 1.25rem;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
}}

.yh-ai-stat {{
    text-align: left;
}}

.yh-ai-stat-value {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: {theme['primary']};
}}

.yh-ai-stat-label {{
    font-size: 0.625rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.yh-ai-action-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: {theme['primary']};
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.25rem;
    font-size: 0.8125rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}

.yh-ai-action-btn:hover {{
    filter: brightness(1.08);
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}}

/* ===== Career Goal Card: success accent, consistent card ===== */
.yh-goal-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}}

.yh-goal-header {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}}

.yh-goal-icon {{
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(16,185,129,0.2);
    border-radius: 8px;
    font-size: 1rem;
}}

.yh-goal-title {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {success};
}}

.yh-goal-text {{
    font-size: 0.9375rem;
    color: #e2e8f0;
    line-height: 1.55;
}}

/* ===== Responsive: preserve hierarchy and spacing ===== */
@media (max-width: 768px) {{
    .main .block-container {{
        padding: 1.5rem 1rem 2rem !important;
    }}
    .yh-hero {{
        padding: 1.25rem 1.5rem;
    }}
    .yh-hero-title {{
        font-size: 1.25rem;
    }}
    .yh-hero-badges {{
        gap: 0.5rem;
    }}
    .yh-profile-buttons {{
        flex-direction: column;
    }}
}}

</style>
"""
    st.markdown(css, unsafe_allow_html=True)


def render_premium_header(
    role_display_name: str | None = None,
    readiness_pct: int | None = None,
    weekly_hours: float | None = None,
    num_weeks: int | None = None,
    role_id: str | None = None,
) -> None:
    theme = get_role_theme(role_id)
    title, subtitle = get_dynamic_title(role_display_name)

    badges_html = ""
    if role_display_name or readiness_pct is not None or weekly_hours is not None:
        badge_items = []
        if role_display_name:
            badge_items.append(f'<span class="yh-hero-badge"><span class="yh-hero-badge-icon">🎯</span> Hedef: <span class="yh-hero-badge-value">{_escape(role_display_name)}</span></span>')
        if readiness_pct is not None:
            badge_items.append(f'<span class="yh-hero-badge"><span class="yh-hero-badge-icon">📊</span> Hazırbulunuşluk: <span class="yh-hero-badge-value">{readiness_pct}%</span></span>')
        if weekly_hours is not None:
            badge_items.append(f'<span class="yh-hero-badge"><span class="yh-hero-badge-icon">⏰</span> <span class="yh-hero-badge-value">{weekly_hours:.0f}</span> saat/hafta</span>')
        if num_weeks is not None:
            badge_items.append(f'<span class="yh-hero-badge"><span class="yh-hero-badge-icon">📅</span> <span class="yh-hero-badge-value">{num_weeks}</span> hafta</span>')

        badges_html = f'<div class="yh-hero-badges">{"".join(badge_items)}</div>'

    html = f"""
<div class="yh-hero">
    <div class="yh-hero-brand">YolHaritam</div>
    <div class="yh-hero-title">{_escape(title)}</div>
    <div class="yh-hero-subtitle">{_escape(subtitle)}</div>
    {badges_html}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def _get_login_bg_image_data_url() -> str | None:
    """If assets/images/ai-network.* (or ai_network.*) exists, return data URL for CSS background; else None."""
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        "ai-network.png", "ai-network.jpg", "ai-network.webp",
        "ai_network.png", "ai_network.jpg", "ai_network.webp",
    ]
    for name in candidates:
        path = base_dir / "assets" / "images" / name
        if path.exists():
            try:
                data = path.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
                mime = "png" if name.endswith(".png") else "webp" if name.endswith(".webp") else "jpeg"
                return f"data:image/{mime};base64,{b64}"
            except Exception:
                pass
    return None


def _get_login_logo_data_url() -> tuple[str | None, str]:
    """Load login center logo from assets/images. Prefer myway-icon.png."""
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        "myway-icon.png",
        "logo-icon.png",
        "logo.png", "logo.jpg", "logo.webp",
        "myway.png",
    ]
    for name in candidates:
        path = base_dir / "assets" / "images" / name
        if path.exists():
            try:
                data = path.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
                mime = "png" if name.endswith(".png") else "webp" if name.endswith(".webp") else "jpeg"
                return f"data:image/{mime};base64,{b64}", mime
            except Exception:
                pass
    return None, ""


def get_login_logo_data_url() -> str | None:
    """Public helper for login logo as data URL, or None if missing."""
    data_url, _ = _get_login_logo_data_url()
    return data_url


def render_login_screen() -> None:
    """Inject login-page CSS and marker only. Layout and card are rendered by app.py."""
    login_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500&family=Syne:wght@700;800&display=swap');

/* ===== LOGIN PAGE: hide Streamlit header ===== */
body:has(#login-page-marker) [data-testid="stHeader"],
body:has(#login-page-marker) header[data-testid="stHeader"] {
    display: none !important;
}

/* ===== Background: #070d1a + grid lines + glow orbs ===== */
body:has(#login-page-marker) .main {
    background: #070d1a !important;
    background-image:
        repeating-linear-gradient(0deg, transparent, transparent 59px, rgba(0,200,255,0.04) 59px, rgba(0,200,255,0.04) 60px),
        repeating-linear-gradient(90deg, transparent, transparent 59px, rgba(0,200,255,0.04) 59px, rgba(0,200,255,0.04) 60px) !important;
    position: relative !important;
}
body:has(#login-page-marker) .main::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 30%, rgba(0,200,255,0.12) 0%, transparent 50%),
        radial-gradient(ellipse 60% 80% at 80% 70%, rgba(10,240,200,0.08) 0%, transparent 50%);
    animation: login-orb-drift 12s ease-in-out infinite alternate;
}
@keyframes login-orb-drift {
    0% { opacity: 0.7; transform: translate(0, 0); }
    100% { opacity: 1; transform: translate(3%, -2%); }
}
@keyframes login-card-in {
    0% { opacity: 0; transform: translateY(32px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes login-slide-up {
    0% { opacity: 0; transform: translateY(24px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* ===== Card: 460px, centered, glass ===== */
body:has(#login-page-marker) .main .block-container {
    position: relative;
    z-index: 1;
    max-width: 460px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 48px 44px 40px !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    background: rgba(13,22,40,0.85) !important;
    border: 1px solid rgba(0,200,255,0.12) !important;
    border-radius: 24px !important;
    backdrop-filter: blur(24px) !important;
    box-shadow: 0 40px 80px rgba(0,0,0,0.5) !important;
    animation: login-slide-up 0.7s cubic-bezier(0.22,1,0.36,1) both;
}

/* ===== Logo section ===== */
.login-card-inner { animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) both; }
.login-card-inner .delay-1 { animation-delay: 0.05s; }
.login-card-inner .delay-2 { animation-delay: 0.1s; }
.login-card-inner .delay-3 { animation-delay: 0.15s; }
.login-card-inner .delay-4 { animation-delay: 0.2s; }
.login-card-inner .delay-5 { animation-delay: 0.25s; }
.login-card-inner .delay-6 { animation-delay: 0.3s; }
.login-card-inner .delay-7 { animation-delay: 0.35s; }
.login-card-inner .delay-8 { animation-delay: 0.4s; }

.login-logo-box {
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    margin: 0 auto 24px auto;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.05s both;
}
.login-logo-box img {
    width: 200px;
    height: auto;
    display: block;
    margin: 0 auto;
    object-fit: contain;
    border-radius: 20px;
    filter: drop-shadow(0 0 25px rgba(0, 240, 255, 0.5));
}
.login-brand-name {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 30px;
    line-height: 1.2;
    background: linear-gradient(90deg, #00c8ff, #0af0c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.1s both;
}
.login-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #5a6a85;
    margin-bottom: 32px;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.15s both;
}

/* ===== Form ===== */
body:has(#login-page-marker) [data-testid="stVerticalBlock"] > div {
    margin-bottom: 0.5rem !important;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.2s both;
}
body:has(#login-page-marker) .stTextInput label {
    font-family: 'DM Sans', sans-serif !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
    color: #5a6a85 !important;
    letter-spacing: 0.5px !important;
}
body:has(#login-page-marker) .stTextInput input {
    font-family: 'DM Sans', sans-serif !important;
    background: #111d30 !important;
    border: 1px solid rgba(0,200,255,0.12) !important;
    border-radius: 14px !important;
    padding: 13px 16px !important;
    color: #e8f0fe !important;
    font-size: 15px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
body:has(#login-page-marker) .stTextInput input:focus {
    border-color: rgba(0,200,255,0.45) !important;
    box-shadow: 0 0 0 3px rgba(0,200,255,0.08) !important;
    outline: none !important;
}
.login-forgot-link {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    color: #00c8ff;
    text-align: right;
    display: block;
    margin-top: 4px;
    margin-bottom: 8px;
    text-decoration: none;
}
.login-forgot-link:hover { color: #0af0c8; }

/* ===== Login button ===== */
body:has(#login-page-marker) .stButton > button[kind="primary"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    color: #04111f !important;
    background: linear-gradient(90deg, #00c8ff, #0af0c8) !important;
    border: none !important;
    border-radius: 14px !important;
    height: 50px !important;
    padding: 0 1.5rem !important;
    margin-top: 0.5rem !important;
    box-shadow: 0 4px 24px rgba(0,200,255,0.25) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.25s both;
}
body:has(#login-page-marker) .stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0,200,255,0.35) !important;
}
body:has(#login-page-marker) .stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ===== Social: divider + 3 buttons ===== */
.login-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 24px 0 20px;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.3s both;
}
.login-divider::before,
.login-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(0,200,255,0.12);
}
.login-divider span {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    color: #5a6a85;
    text-transform: lowercase;
}
.login-social-buttons {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.35s both;
}
.login-social-btn {
    flex: 1;
    min-width: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    background: #111d30;
    border: 1px solid rgba(0,200,255,0.12);
    border-radius: 14px;
    color: #e8f0fe;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.login-social-btn:hover {
    border-color: rgba(0,200,255,0.35);
    background: rgba(0,200,255,0.06);
}
.login-social-btn svg { width: 20px; height: 20px; flex-shrink: 0; }

/* ===== Demo box ===== */
.yh-login-demo {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #e8f0fe;
    line-height: 1.5;
    margin-top: 20px;
    padding: 14px 18px;
    background: rgba(0,200,255,0.05);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 14px;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.4s both;
}
.yh-login-demo .demo-label {
    font-size: 11px;
    text-transform: uppercase;
    color: #00c8ff;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}
.yh-login-demo strong { color: #0af0c8; }

/* ===== Register link ===== */
.login-register {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: #5a6a85;
    text-align: center;
    margin-top: 24px;
    animation: login-card-in 0.6s cubic-bezier(0.22,1,0.36,1) 0.45s both;
}
.login-register a {
    color: #00c8ff;
    text-decoration: none;
}
.login-register a:hover { color: #0af0c8; }

/* Login error */
body:has(#login-page-marker) [data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid rgba(248,113,113,0.35) !important;
    background: rgba(248,113,113,0.08) !important;
    font-family: 'DM Sans', sans-serif !important;
}

@media (max-width: 540px) {
    body:has(#login-page-marker) .main .block-container {
        margin: 1rem !important;
        padding: 32px 24px 28px !important;
        border-radius: 20px !important;
    }
}
</style>
"""
    st.markdown('<div id="login-page-marker" aria-hidden="true" style="position:absolute;left:-9999px;"></div>', unsafe_allow_html=True)
    st.markdown(login_css, unsafe_allow_html=True)


def render_login_left_panel() -> None:
    """Render the left branding panel with animated AI atmosphere (call inside the left column from app.py)."""
    left_panel_html = """
<div class="login-left-panel">
    <div class="login-bg-image" aria-hidden="true"></div>
    <div class="login-left-bg" aria-hidden="true">
        <div class="login-bg-gradient"></div>
        <div class="login-bg-nodes">
            <span class="login-orb login-orb-1"></span>
            <span class="login-orb login-orb-2"></span>
            <span class="login-orb login-orb-3"></span>
            <span class="login-orb login-orb-4"></span>
            <span class="login-orb login-orb-5"></span>
            <span class="login-orb login-orb-6"></span>
            <span class="login-orb login-orb-7"></span>
            <span class="login-orb login-orb-8"></span>
        </div>
    </div>
    <div class="login-left-overlay"></div>
    <div class="login-left-content">
        <div class="login-brand-subtitle">AI destekli kişisel öğrenme yolculuğun</div>
        <div class="login-brand-desc">
            <p>Beceri boşluklarını analiz et.</p>
            <p>Hedef rolüne göre öğrenme planı oluştur.</p>
            <p>Kariyer yolculuğunu görsel olarak takip et.</p>
        </div>
        <div class="login-brand-bullets">
            <ul>
                <li>Skill Gap Analysis</li>
                <li>AI Learning Roadmap</li>
                <li>Career Journey Dashboard</li>
            </ul>
        </div>
    </div>
</div>
"""
    st.markdown(left_panel_html, unsafe_allow_html=True)


def render_login_center_logo() -> None:
    """Render the center column: logo icon (Y symbol only, no crop)."""
    logo_data_url, _ = _get_login_logo_data_url()
    if logo_data_url:
        logo_html = f"""
<div class="login-center">
    <img src="{logo_data_url}" class="login-logo" alt="" />
</div>
"""
    else:
        logo_html = """
<div class="login-center"></div>
"""
    st.markdown(logo_html, unsafe_allow_html=True)


def render_dashboard_cards(
    todays_task: str,
    weekly_progress: str,
    skill_summary: str,
    role_id: str | None = None,
) -> None:
    theme = get_role_theme(role_id)

    safe_task = _escape(todays_task)
    safe_weekly = _escape(weekly_progress)
    safe_skill = _escape(skill_summary)
    html = f"""
<div class="yh-dashboard-grid">
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">📌</div>
            <div class="yh-dashboard-card-title">Bugünün Görevi</div>
        </div>
        <div class="yh-dashboard-card-content">{safe_task}</div>
    </div>
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">📈</div>
            <div class="yh-dashboard-card-title">Haftalık İlerleme</div>
        </div>
        <div class="yh-dashboard-card-content">{safe_weekly}</div>
    </div>
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">🎯</div>
            <div class="yh-dashboard-card-title">Beceri Gelişim Özeti</div>
        </div>
        <div class="yh-dashboard-card-content">{safe_skill}</div>
    </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(icon: str, title: str) -> None:
    html = f"""
<div class="yh-section-title">
    <span class="yh-section-icon">{_escape(icon)}</span>
    {_escape(title)}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def generate_avatar_initials(name: str) -> str:
    if not name:
        return "👤"
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    elif len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return "👤"


def render_sidebar_profile(
    user_name: str,
    role_display_name: str | None,
    readiness_pct: int | None,
    avatar_url: str | None = None,
    role_id: str | None = None,
) -> None:
    theme = get_role_theme(role_id)

    if avatar_url:
        avatar_content = f'<img src="{avatar_url}" alt="Avatar">'
    else:
        initials = generate_avatar_initials(user_name)
        avatar_content = f'<span style="color: #f1f5f9; font-weight: 700;">{initials}</span>'

    role_text = role_display_name or "Henüz seçilmedi"
    safe_user_name = _escape(user_name)
    safe_role_text = _escape(role_text)
    readiness_value = f"{readiness_pct}%" if readiness_pct is not None else "—"
    progress_width = readiness_pct if readiness_pct is not None else 0

    avatar_edit_css = f"""
<style>
.yh-avatar-wrapper {{
    position: relative;
    width: 64px;
    height: 64px;
    margin: 0 auto 0.6rem auto;
}}
.yh-profile-avatar {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: {theme['gradient_start']};
    border: 2px solid {theme['primary']}35;
    overflow: hidden;
}}
.yh-profile-avatar img {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}}
.yh-avatar-edit-icon {{
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 22px;
    height: 22px;
    background: rgba(30,41,59,0.95);
    border: 1px solid rgba(71,85,105,0.6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    cursor: pointer;
    transition: border-color 0.2s ease, background 0.2s ease;
    box-shadow: 0 1px 4px rgba(0,0,0,0.25);
}}
.yh-avatar-edit-icon:hover {{
    background: rgba(51,65,85,0.9);
    border-color: {theme['primary']}50;
}}
</style>
"""
    st.sidebar.markdown(avatar_edit_css, unsafe_allow_html=True)

    html = (
        "<div class=\"yh-profile-card\">"
        "<div class=\"yh-avatar-wrapper\" id=\"avatar-wrapper\">"
        "<div class=\"yh-profile-avatar\">" + avatar_content + "</div>"
        "<div class=\"yh-avatar-edit-icon\">📷</div>"
        "</div>"
        "<div class=\"yh-profile-name\">" + safe_user_name + "</div>"
        "<div class=\"yh-profile-role\">" + safe_role_text + "</div>"
        "<div class=\"yh-profile-readiness\">"
        "<div class=\"yh-profile-readiness-label\">Hazırbulunuşluk</div>"
        "<div class=\"yh-profile-readiness-value\">" + _escape(readiness_value) + "</div>"
        "<div class=\"yh-profile-progress\">"
        "<div class=\"yh-profile-progress-fill\" style=\"width: " + str(progress_width) + "%;\"></div>"
        "</div></div></div>"
    )
    st.sidebar.markdown(html, unsafe_allow_html=True)


def render_welcome_section(user_name: str, role_display_name: str | None) -> None:
    safe_name = _escape(user_name)
    greeting = f"👋 Hoş geldin, {safe_name}"
    if role_display_name:
        message = _escape(role_display_name) + " yolculuğuna kaldığın yerden devam ediyorsun."
    else:
        message = "Kariyer yolculuğuna başlamak için hedef rolünü seç."
    html = f"""
<div class="yh-welcome">
    <div class="yh-welcome-greeting">{greeting}</div>
    <div class="yh-welcome-message">{message}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_ai_recommendation_panel(
    skill_name: str,
    explanation: str,
    estimated_hours: float,
    impact: str = "Yüksek",
    role_id: str | None = None,
) -> None:
    theme = get_role_theme(role_id)

    safe_skill = _escape(skill_name)
    safe_explanation = _escape(explanation)
    safe_impact = _escape(impact)
    hours_str = f"{estimated_hours:.1f}"
    html = (
        "<div class=\"yh-ai-panel\">"
        "<div class=\"yh-ai-panel-header\">"
        "<div class=\"yh-ai-panel-icon\">🤖</div>"
        "<div class=\"yh-ai-panel-title\">AI Tavsiyesi</div>"
        "<span class=\"yh-ai-panel-badge\">Kişiselleştirilmiş</span>"
        "</div>"
        "<div class=\"yh-ai-panel-content\">"
        "<div class=\"yh-ai-next-step\">Sonraki Adım</div>"
        "<div class=\"yh-ai-skill-name\">" + safe_skill + "</div>"
        "<div class=\"yh-ai-explanation\">" + safe_explanation + "</div>"
        "<div class=\"yh-ai-stats\">"
        "<div class=\"yh-ai-stat\">"
        "<div class=\"yh-ai-stat-value\">" + hours_str + " saat</div>"
        "<div class=\"yh-ai-stat-label\">Tahmini Süre</div>"
        "</div>"
        "<div class=\"yh-ai-stat\">"
        "<div class=\"yh-ai-stat-value\">" + safe_impact + "</div>"
        "<div class=\"yh-ai-stat-label\">Etki</div>"
        "</div>"
        "</div></div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_career_goal_card(goal_text: str) -> None:
    safe_text = _escape(goal_text)
    html = f"""
<div class="yh-goal-card">
    <div class="yh-goal-header">
        <div class="yh-goal-icon">🎯</div>
        <div class="yh-goal-title">Kariyer Hedefin</div>
    </div>
    <div class="yh-goal-text">{safe_text}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_todays_task_card(task_text: str, role_id: str | None = None) -> None:
    theme = get_role_theme(role_id)

    html = f"""
<div class="yh-dashboard-card" style="border-color: {theme['primary']}44;">
    <div class="yh-dashboard-card-header">
        <div class="yh-dashboard-card-icon">📌</div>
        <div class="yh-dashboard-card-title">Bugünün Görevi</div>
    </div>
    <div class="yh-dashboard-card-content">{_escape(task_text)}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
