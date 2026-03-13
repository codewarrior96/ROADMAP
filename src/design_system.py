"""
YolHaritam Premium Design System
Role-aware visual styling, dynamic headings, and premium UI components
"""
from __future__ import annotations

from typing import Dict, Tuple
import streamlit as st


ROLE_THEMES: Dict[str, Dict[str, str]] = {
    "ai_engineer": {
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "accent": "#a855f7",
        "gradient_start": "rgba(99,102,241,0.4)",
        "gradient_end": "rgba(139,92,246,0.3)",
        "glow": "rgba(99,102,241,0.2)",
        "label": "AI Engineer Yolculuğu",
    },
    "data_analyst": {
        "primary": "#10b981",
        "secondary": "#14b8a6",
        "accent": "#06b6d4",
        "gradient_start": "rgba(16,185,129,0.4)",
        "gradient_end": "rgba(20,184,166,0.3)",
        "glow": "rgba(16,185,129,0.2)",
        "label": "Data Analyst Yolculuğu",
    },
    "frontend_developer": {
        "primary": "#06b6d4",
        "secondary": "#0ea5e9",
        "accent": "#3b82f6",
        "gradient_start": "rgba(6,182,212,0.4)",
        "gradient_end": "rgba(14,165,233,0.3)",
        "glow": "rgba(6,182,212,0.2)",
        "label": "Frontend Developer Yolculuğu",
    },
    "data_scientist": {
        "primary": "#3b82f6",
        "secondary": "#10b981",
        "accent": "#22d3ee",
        "gradient_start": "rgba(59,130,246,0.4)",
        "gradient_end": "rgba(16,185,129,0.3)",
        "glow": "rgba(59,130,246,0.2)",
        "label": "Data Scientist Yolculuğu",
    },
    "default": {
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "accent": "#a855f7",
        "gradient_start": "rgba(99,102,241,0.35)",
        "gradient_end": "rgba(139,92,246,0.25)",
        "glow": "rgba(99,102,241,0.15)",
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

    css = f"""
<style>
/* ===== YolHaritam Premium Design System ===== */

/* Global Background Enhancement */
.stApp {{
    background: linear-gradient(180deg, 
        #0a0f1a 0%, 
        #0f1629 30%,
        #111827 60%,
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
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, {theme['glow']}, transparent),
        radial-gradient(ellipse 60% 40% at 80% 60%, rgba(139,92,246,0.08), transparent),
        radial-gradient(ellipse 50% 30% at 20% 80%, rgba(59,130,246,0.06), transparent);
    pointer-events: none;
    z-index: 0;
}}

/* Main Content Area */
.main .block-container {{
    position: relative;
    z-index: 1;
    max-width: 1200px !important;
    padding-top: 2rem !important;
}}

/* ===== Premium Typography ===== */
h1, h2, h3, h4, h5, h6 {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif !important;
    letter-spacing: -0.02em;
}}

h1 {{
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

h2 {{
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}}

h3 {{
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}}

p, .stMarkdown {{
    color: #94a3b8 !important;
    line-height: 1.7 !important;
}}

/* Caption styling */
.stCaption p {{
    color: #64748b !important;
    font-size: 0.9rem !important;
}}

/* ===== Sidebar Premium Styling ===== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, 
        rgba(15,23,42,0.98) 0%, 
        rgba(15,23,42,0.95) 100%
    ) !important;
    border-right: 1px solid rgba(51,65,85,0.5) !important;
}}

[data-testid="stSidebar"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 200px;
    background: radial-gradient(ellipse at top, {theme['glow']}, transparent);
    pointer-events: none;
}}

[data-testid="stSidebar"] .stRadio > label {{
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b !important;
}}

[data-testid="stSidebar"] .stRadio > div {{
    gap: 0.3rem !important;
}}

[data-testid="stSidebar"] .stRadio > div > label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 0.6rem !important;
    padding: 0.7rem 1rem !important;
    transition: all 0.2s ease !important;
    color: #94a3b8 !important;
}}

[data-testid="stSidebar"] .stRadio > div > label:hover {{
    background: rgba(51,65,85,0.4) !important;
    border-color: rgba(99,102,241,0.3) !important;
}}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {{
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']}) !important;
    border-color: {theme['primary']}66 !important;
    color: #f1f5f9 !important;
}}

[data-testid="stSidebar"] h1 {{
    font-size: 1.4rem !important;
    margin-bottom: 1.5rem !important;
}}

[data-testid="stSidebar"] hr {{
    border-color: rgba(51,65,85,0.4) !important;
    margin: 1.5rem 0 !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    background: transparent !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    color: #f87171 !important;
    border-radius: 0.6rem !important;
    padding: 0.6rem !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(239,68,68,0.1) !important;
    border-color: rgba(239,68,68,0.5) !important;
}}

/* ===== Premium Card Containers ===== */
.yh-card {{
    background: linear-gradient(135deg, 
        rgba(15,23,42,0.9) 0%, 
        rgba(30,41,59,0.8) 100%
    );
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 
        0 4px 6px -1px rgba(0,0,0,0.3),
        0 2px 4px -2px rgba(0,0,0,0.2),
        inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}}

.yh-card:hover {{
    border-color: rgba(99,102,241,0.4);
    box-shadow: 
        0 10px 15px -3px rgba(0,0,0,0.3),
        0 4px 6px -4px rgba(0,0,0,0.2),
        0 0 0 1px rgba(99,102,241,0.1);
}}

.yh-card-highlight {{
    background: linear-gradient(135deg, 
        {theme['gradient_start']} 0%, 
        {theme['gradient_end']} 100%
    );
    border-color: {theme['primary']}66;
}}

/* ===== Hero Section ===== */
.yh-hero {{
    background: linear-gradient(135deg, 
        {theme['gradient_start']} 0%, 
        {theme['gradient_end']} 100%
    );
    border: 1px solid {theme['primary']}55;
    border-radius: 1.2rem;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}

.yh-hero::before {{
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, {theme['glow']}, transparent 70%);
    pointer-events: none;
}}

.yh-hero::after {{
    content: "";
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, {theme['secondary']}15, transparent 70%);
    pointer-events: none;
}}

.yh-hero-brand {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: {theme['primary']};
    font-weight: 600;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}}

.yh-hero-title {{
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
    line-height: 1.2;
}}

.yh-hero-subtitle {{
    font-size: 1rem;
    color: #cbd5e1;
    max-width: 600px;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}}

.yh-hero-badges {{
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}}

.yh-hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 2rem;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    color: #e2e8f0;
}}

.yh-hero-badge-icon {{
    font-size: 1rem;
}}

.yh-hero-badge-value {{
    font-weight: 600;
    color: {theme['primary']};
}}

/* ===== Metric Cards ===== */
.yh-metric {{
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 0.9rem;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s ease;
}}

.yh-metric:hover {{
    border-color: {theme['primary']}55;
    transform: translateY(-2px);
}}

.yh-metric-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
}}

.yh-metric-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
}}

/* ===== Section Titles ===== */
.yh-section-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

.yh-section-icon {{
    font-size: 1.2rem;
}}

/* ===== Form Elements ===== */
.stSelectbox > div > div {{
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(51,65,85,0.6) !important;
    border-radius: 0.7rem !important;
}}

.stSelectbox > div > div:focus-within {{
    border-color: {theme['primary']} !important;
    box-shadow: 0 0 0 2px {theme['primary']}33 !important;
}}

.stNumberInput > div > div > input {{
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(51,65,85,0.6) !important;
    border-radius: 0.7rem !important;
    color: #f1f5f9 !important;
}}

.stTextInput > div > div > input {{
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(51,65,85,0.6) !important;
    border-radius: 0.7rem !important;
    color: #f1f5f9 !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {theme['primary']} !important;
    box-shadow: 0 0 0 2px {theme['primary']}33 !important;
}}

/* ===== Slider Styling ===== */
.stSlider > div > div > div > div {{
    background: {theme['primary']} !important;
}}

.stSlider > div > div > div[data-baseweb="slider"] > div {{
    background: rgba(51,65,85,0.6) !important;
}}

/* ===== Button Styling ===== */
.stButton > button {{
    background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
    border: none !important;
    border-radius: 0.7rem !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px -2px {theme['primary']}55 !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px -2px {theme['primary']}66 !important;
}}

/* ===== Dataframe / Table ===== */
.stDataFrame {{
    border-radius: 0.8rem !important;
    overflow: hidden !important;
}}

[data-testid="stDataFrame"] > div {{
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(51,65,85,0.5) !important;
    border-radius: 0.8rem !important;
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

/* ===== Dashboard Card Grid ===== */
.yh-dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.yh-dashboard-card {{
    background: linear-gradient(135deg, 
        rgba(15,23,42,0.9) 0%, 
        rgba(30,41,59,0.8) 100%
    );
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 1rem;
    padding: 1.4rem;
    transition: all 0.2s ease;
}}

.yh-dashboard-card:hover {{
    border-color: {theme['primary']}44;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.4);
}}

.yh-dashboard-card-header {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.8rem;
}}

.yh-dashboard-card-icon {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border-radius: 0.6rem;
    font-size: 1.1rem;
}}

.yh-dashboard-card-title {{
    font-size: 0.9rem;
    font-weight: 600;
    color: #e2e8f0;
}}

.yh-dashboard-card-content {{
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
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

/* ===== Progress Indicators ===== */
.yh-progress-bar {{
    height: 8px;
    background: rgba(30,41,59,0.8);
    border-radius: 4px;
    overflow: hidden;
    margin: 0.5rem 0;
}}

.yh-progress-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    transition: width 0.5s ease;
}}

/* ===== User Profile Card (Sidebar) ===== */
.yh-profile-card {{
    background: linear-gradient(135deg, 
        rgba(30,41,59,0.8) 0%, 
        rgba(15,23,42,0.9) 100%
    );
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 1rem;
    padding: 1.2rem;
    margin-bottom: 1rem;
    text-align: center;
}}

.yh-profile-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    margin: 0 auto 0.8rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
    border: 3px solid {theme['primary']}66;
    box-shadow: 0 4px 15px -3px {theme['primary']}44;
}}

.yh-profile-avatar img {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}}

.yh-profile-name {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
}}

.yh-profile-role {{
    font-size: 0.8rem;
    color: {theme['primary']};
    font-weight: 600;
    margin-bottom: 0.8rem;
}}

.yh-profile-readiness {{
    background: rgba(15,23,42,0.6);
    border-radius: 0.6rem;
    padding: 0.6rem;
    margin-bottom: 0.8rem;
}}

.yh-profile-readiness-label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-bottom: 0.3rem;
}}

.yh-profile-readiness-value {{
    font-size: 1.4rem;
    font-weight: 700;
    color: {theme['primary']};
}}

.yh-profile-progress {{
    height: 6px;
    background: rgba(30,41,59,0.8);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 0.4rem;
}}

.yh-profile-progress-fill {{
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    transition: width 0.5s ease;
}}

.yh-profile-buttons {{
    display: flex;
    gap: 0.5rem;
    margin-top: 0.8rem;
}}

.yh-profile-btn {{
    flex: 1;
    background: rgba(51,65,85,0.4);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 0.5rem;
    padding: 0.5rem;
    font-size: 0.7rem;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}}

.yh-profile-btn:hover {{
    background: rgba(51,65,85,0.6);
    border-color: {theme['primary']}44;
    color: #e2e8f0;
}}

/* ===== Welcome Section ===== */
.yh-welcome {{
    margin-bottom: 1.5rem;
}}

.yh-welcome-greeting {{
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
}}

.yh-welcome-message {{
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.6;
}}

/* ===== AI Recommendation Panel ===== */
.yh-ai-panel {{
    background: linear-gradient(135deg, 
        rgba(139,92,246,0.15) 0%, 
        rgba(99,102,241,0.1) 100%
    );
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 1rem;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}}

.yh-ai-panel::before {{
    content: "";
    position: absolute;
    top: -50%;
    right: -30%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(139,92,246,0.2), transparent 70%);
    pointer-events: none;
}}

.yh-ai-panel-header {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}}

.yh-ai-panel-icon {{
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    border-radius: 0.6rem;
    font-size: 1.2rem;
}}

.yh-ai-panel-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
}}

.yh-ai-panel-badge {{
    font-size: 0.65rem;
    background: rgba(139,92,246,0.3);
    color: #c4b5fd;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    margin-left: auto;
}}

.yh-ai-panel-content {{
    position: relative;
    z-index: 1;
}}

.yh-ai-next-step {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #a78bfa;
    margin-bottom: 0.3rem;
}}

.yh-ai-skill-name {{
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.8rem;
}}

.yh-ai-explanation {{
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 1rem;
}}

.yh-ai-stats {{
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}}

.yh-ai-stat {{
    text-align: center;
}}

.yh-ai-stat-value {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #a78bfa;
}}

.yh-ai-stat-label {{
    font-size: 0.7rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.yh-ai-action-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    border: none;
    border-radius: 0.6rem;
    padding: 0.7rem 1.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px -2px rgba(139,92,246,0.4);
}}

.yh-ai-action-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px -2px rgba(139,92,246,0.5);
}}

/* ===== Career Goal Card ===== */
.yh-goal-card {{
    background: linear-gradient(135deg, 
        rgba(16,185,129,0.12) 0%, 
        rgba(20,184,166,0.08) 100%
    );
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 1rem;
    padding: 1.4rem;
}}

.yh-goal-header {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.8rem;
}}

.yh-goal-icon {{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(16,185,129,0.4), rgba(20,184,166,0.3));
    border-radius: 0.6rem;
    font-size: 1.1rem;
}}

.yh-goal-title {{
    font-size: 0.9rem;
    font-weight: 600;
    color: #10b981;
}}

.yh-goal-text {{
    font-size: 1rem;
    color: #e2e8f0;
    line-height: 1.6;
}}

/* ===== Responsive Adjustments ===== */
@media (max-width: 768px) {{
    .yh-hero {{
        padding: 1.5rem;
    }}
    
    .yh-hero-title {{
        font-size: 1.5rem;
    }}
    
    .yh-hero-badges {{
        flex-direction: column;
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
            badge_items.append(f'<span class="yh-hero-badge"><span class="yh-hero-badge-icon">🎯</span> Hedef: <span class="yh-hero-badge-value">{role_display_name}</span></span>')
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
    <div class="yh-hero-title">{title}</div>
    <div class="yh-hero-subtitle">{subtitle}</div>
    {badges_html}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_login_screen() -> None:
    """Render premium login screen with AI network background."""
    login_css = """
<style>
/* ===== AI NETWORK BACKGROUND - APPLIED IMMEDIATELY ===== */
[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 60% 40% at 90% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 40%),
        radial-gradient(ellipse 50% 30% at 10% 70%, rgba(59, 130, 246, 0.08) 0%, transparent 35%),
        linear-gradient(180deg, #030712 0%, #0f172a 30%, #1e1b4b 60%, #0f172a 85%, #030712 100%) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        radial-gradient(circle at 15% 25%, rgba(99, 102, 241, 0.08) 0%, transparent 12%),
        radial-gradient(circle at 85% 15%, rgba(139, 92, 246, 0.06) 0%, transparent 10%),
        radial-gradient(circle at 25% 75%, rgba(59, 130, 246, 0.05) 0%, transparent 15%),
        radial-gradient(circle at 75% 85%, rgba(168, 85, 247, 0.04) 0%, transparent 12%),
        radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.03) 0%, transparent 25%),
        radial-gradient(circle at 35% 35%, rgba(6, 182, 212, 0.04) 0%, transparent 8%),
        radial-gradient(circle at 65% 65%, rgba(124, 58, 237, 0.05) 0%, transparent 10%);
}

/* Neural network grid pattern */
.login-network {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.login-network::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        linear-gradient(90deg, transparent 0%, transparent 49.5%, rgba(99, 102, 241, 0.03) 50%, transparent 50.5%, transparent 100%),
        linear-gradient(0deg, transparent 0%, transparent 49.5%, rgba(139, 92, 246, 0.02) 50%, transparent 50.5%, transparent 100%);
    background-size: 80px 80px;
}

/* Glowing AI nodes */
.login-node {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.9) 0%, rgba(139, 92, 246, 0.6) 40%, transparent 70%);
    animation: node-pulse 4s ease-in-out infinite;
}

.login-node::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 4px;
    height: 4px;
    margin: -2px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 10px #6366f1, 0 0 20px #8b5cf6;
}

.login-node:nth-child(1) { top: 12%; left: 8%; width: 120px; height: 120px; animation-delay: 0s; }
.login-node:nth-child(2) { top: 8%; left: 75%; width: 80px; height: 80px; animation-delay: 1s; }
.login-node:nth-child(3) { top: 65%; left: 5%; width: 100px; height: 100px; animation-delay: 0.5s; }
.login-node:nth-child(4) { top: 70%; left: 85%; width: 90px; height: 90px; animation-delay: 1.5s; }
.login-node:nth-child(5) { top: 35%; left: 90%; width: 60px; height: 60px; animation-delay: 2s; }
.login-node:nth-child(6) { top: 85%; left: 40%; width: 70px; height: 70px; animation-delay: 0.8s; }

@keyframes node-pulse {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.1); }
}

/* Connection lines between nodes */
.login-connections {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}

.login-line {
    position: absolute;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15), transparent);
    transform-origin: left center;
    animation: line-glow 3s ease-in-out infinite;
}

.login-line:nth-child(1) { top: 15%; left: 12%; width: 200px; transform: rotate(25deg); animation-delay: 0s; }
.login-line:nth-child(2) { top: 20%; left: 60%; width: 180px; transform: rotate(-15deg); animation-delay: 0.5s; }
.login-line:nth-child(3) { top: 68%; left: 10%; width: 250px; transform: rotate(10deg); animation-delay: 1s; }
.login-line:nth-child(4) { top: 75%; left: 55%; width: 200px; transform: rotate(-30deg); animation-delay: 1.5s; }
.login-line:nth-child(5) { top: 40%; left: 5%; width: 150px; transform: rotate(45deg); animation-delay: 0.3s; }
.login-line:nth-child(6) { top: 50%; left: 70%; width: 180px; transform: rotate(-20deg); animation-delay: 0.8s; }

@keyframes line-glow {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.7; }
}

/* Central glow behind login card */
.login-center-glow {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.04) 30%, transparent 60%);
    z-index: 0;
    pointer-events: none;
}

/* Login Header */
.yh-login-header {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    position: relative;
    z-index: 1;
}

.yh-login-logo {
    width: 72px;
    height: 72px;
    margin: 0 auto 1rem;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    border-radius: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    box-shadow: 
        0 10px 40px -10px rgba(99, 102, 241, 0.5),
        0 0 60px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255,255,255,0.2);
    position: relative;
}

.yh-login-logo::before {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 1.4rem;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.2));
    z-index: -1;
    filter: blur(8px);
}

.yh-login-title {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}

.yh-login-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-bottom: 0;
}

.yh-login-subtitle span {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
}

/* Demo Info */
.yh-login-demo {
    text-align: center;
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid rgba(99, 102, 241, 0.2);
}

.yh-login-demo strong {
    color: #a78bfa;
}

/* Style inputs on login page */
[data-testid="stVerticalBlock"] .stTextInput input {
    background: rgba(15, 23, 42, 0.9) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 0.6rem !important;
    padding: 0.75rem 1rem !important;
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
}

[data-testid="stVerticalBlock"] .stTextInput input:focus {
    border-color: rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15), 0 0 20px rgba(99, 102, 241, 0.1) !important;
}

[data-testid="stVerticalBlock"] .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

[data-testid="stVerticalBlock"] .stTextInput label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* Gradient Login Button */
[data-testid="stVerticalBlock"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
    border: none !important;
    border-radius: 0.6rem !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stVerticalBlock"] .stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}

/* Reduce spacing in login form */
[data-testid="stVerticalBlock"] > div {
    gap: 0.5rem !important;
}
</style>
"""
    st.markdown(login_css, unsafe_allow_html=True)

    # AI Network background elements
    bg_html = """
<div class="login-network"></div>
<div class="login-center-glow"></div>
<div class="login-connections">
    <div class="login-line"></div>
    <div class="login-line"></div>
    <div class="login-line"></div>
    <div class="login-line"></div>
    <div class="login-line"></div>
    <div class="login-line"></div>
</div>
<div class="login-nodes">
    <div class="login-node"></div>
    <div class="login-node"></div>
    <div class="login-node"></div>
    <div class="login-node"></div>
    <div class="login-node"></div>
    <div class="login-node"></div>
</div>
"""
    st.markdown(bg_html, unsafe_allow_html=True)

    # Logo and title header
    header_html = """
<div class="yh-login-header">
    <div class="yh-login-logo">🧭</div>
    <div class="yh-login-title">YolHaritam</div>
    <div class="yh-login-subtitle"><span>AI</span> Career Navigator</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)


def render_dashboard_cards(
    todays_task: str,
    weekly_progress: str,
    skill_summary: str,
    role_id: str | None = None,
) -> None:
    theme = get_role_theme(role_id)

    html = f"""
<div class="yh-dashboard-grid">
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">📌</div>
            <div class="yh-dashboard-card-title">Bugünün Görevi</div>
        </div>
        <div class="yh-dashboard-card-content">{todays_task}</div>
    </div>
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">📈</div>
            <div class="yh-dashboard-card-title">Haftalık İlerleme</div>
        </div>
        <div class="yh-dashboard-card-content">{weekly_progress}</div>
    </div>
    <div class="yh-dashboard-card">
        <div class="yh-dashboard-card-header">
            <div class="yh-dashboard-card-icon">🎯</div>
            <div class="yh-dashboard-card-title">Beceri Gelişim Özeti</div>
        </div>
        <div class="yh-dashboard-card-content">{skill_summary}</div>
    </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(icon: str, title: str) -> None:
    html = f"""
<div class="yh-section-title">
    <span class="yh-section-icon">{icon}</span>
    {title}
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
    readiness_value = f"{readiness_pct}%" if readiness_pct is not None else "—"
    progress_width = readiness_pct if readiness_pct is not None else 0

    avatar_edit_css = f"""
<style>
.yh-avatar-wrapper {{
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
.yh-avatar-edit-icon {{
    position: absolute;
    bottom: 0;
    right: 0;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
    border: 2px solid rgba(15,23,42,0.9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
.yh-avatar-edit-icon:hover {{
    transform: scale(1.1);
    box-shadow: 0 4px 12px {theme['primary']}66;
}}
</style>
"""
    st.sidebar.markdown(avatar_edit_css, unsafe_allow_html=True)

    html = f"""
<div class="yh-profile-card">
    <div class="yh-avatar-wrapper" id="avatar-wrapper">
        <div class="yh-profile-avatar">{avatar_content}</div>
        <div class="yh-avatar-edit-icon">📷</div>
    </div>
    <div class="yh-profile-name">{user_name}</div>
    <div class="yh-profile-role">{role_text}</div>
    <div class="yh-profile-readiness">
        <div class="yh-profile-readiness-label">Hazırbulunuşluk</div>
        <div class="yh-profile-readiness-value">{readiness_value}</div>
        <div class="yh-profile-progress">
            <div class="yh-profile-progress-fill" style="width: {progress_width}%;"></div>
        </div>
    </div>
</div>
"""
    st.sidebar.markdown(html, unsafe_allow_html=True)


def render_welcome_section(user_name: str, role_display_name: str | None) -> None:
    greeting = f"👋 Hoş geldin, {user_name}"

    if role_display_name:
        message = f"{role_display_name} yolculuğuna kaldığın yerden devam ediyorsun."
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

    html = f"""
<div class="yh-ai-panel">
    <div class="yh-ai-panel-header">
        <div class="yh-ai-panel-icon">🤖</div>
        <div class="yh-ai-panel-title">AI Tavsiyesi</div>
        <span class="yh-ai-panel-badge">Kişiselleştirilmiş</span>
    </div>
    <div class="yh-ai-panel-content">
        <div class="yh-ai-next-step">Sonraki Adım</div>
        <div class="yh-ai-skill-name">{skill_name}</div>
        <div class="yh-ai-explanation">{explanation}</div>
        <div class="yh-ai-stats">
            <div class="yh-ai-stat">
                <div class="yh-ai-stat-value">{estimated_hours:.1f} saat</div>
                <div class="yh-ai-stat-label">Tahmini Süre</div>
            </div>
            <div class="yh-ai-stat">
                <div class="yh-ai-stat-value">{impact}</div>
                <div class="yh-ai-stat-label">Etki</div>
            </div>
        </div>
    </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_career_goal_card(goal_text: str) -> None:
    html = f"""
<div class="yh-goal-card">
    <div class="yh-goal-header">
        <div class="yh-goal-icon">🎯</div>
        <div class="yh-goal-title">Kariyer Hedefin</div>
    </div>
    <div class="yh-goal-text">{goal_text}</div>
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
    <div class="yh-dashboard-card-content">{task_text}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
