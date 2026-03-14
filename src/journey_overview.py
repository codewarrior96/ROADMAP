"""
YolHaritam Journey Overview: premium post-onboarding landing page.
Single coherent continuation of onboarding — no legacy dashboard clutter.
"""
from __future__ import annotations

import html as html_module
from typing import Dict, List, Any, TYPE_CHECKING

import streamlit as st

from .data_loader import Skill, Role
from .design_system import inject_global_styles, get_role_theme, render_section_header
from .algorithm import GapAnalysisResult
from .planner import WeekPlan

if TYPE_CHECKING:
    pass


def _escape(text: str) -> str:
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


# Map numeric level 0-4 to Turkish label for display
LEVEL_LABELS = [
    "Hiç Başlamadım",
    "Temel Bilgim Var",
    "Pratik Yaptım",
    "Küçük Projeler Geliştirdim",
    "Güçlü Hissediyorum",
]
CATEGORY_ICONS: Dict[str, str] = {
    "Genel": "🧠",
    "Programlama": "💻",
    "Profesyonel Pratikler": "📂",
    "Matematik": "📐",
    "Veri Bilimi": "📊",
    "Veri Tabanları": "🗄️",
    "Yapay Zeka": "🤖",
    "Frontend": "🎨",
}
CATEGORY_GROUP_LABELS: Dict[str, str] = {
    "Genel": "Temel Yetkinlikler",
    "Programlama": "Yazılım Geliştirme",
    "Profesyonel Pratikler": "Profesyonel Pratikler",
    "Matematik": "Veri ve Analitik Düşünce",
    "Veri Bilimi": "Veri ve Analitik Düşünce",
    "Veri Tabanları": "Veri ve Analitik Düşünce",
    "Yapay Zeka": "AI / Data Odaklı Beceriler",
    "Frontend": "Yazılım Geliştirme",
}


def _level_label(level: int) -> str:
    idx = max(0, min(level, 4))
    return LEVEL_LABELS[idx]


def render_journey_hero(
    user_name: str,
    role_display_name: str,
    theme: Dict[str, str],
) -> None:
    safe_name = _escape(user_name)
    safe_role = _escape(role_display_name)
    html = f"""
<div class="yh-journey-hero">
    <div class="yh-journey-hero-header">
        <div class="yh-journey-hero-title">Kariyer Yolculuğun</div>
        <div class="yh-journey-hero-badge">🎯 {safe_role}</div>
    </div>
    <div class="yh-journey-hero-subtitle">Hoş geldin, {safe_name}. Bu alan, hedef rolüne giden yolculuğunun özetini ve bir sonraki en iyi adımı gösterir.</div>
</div>
"""
    css = f"""
<style>
.yh-journey-hero {{
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(71,85,105,0.5);
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-bottom: 2rem;
}}
.yh-journey-hero-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}}
.yh-journey-hero-title {{
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}}
.yh-journey-hero-badge {{
    font-size: 0.8125rem;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    border: 1px solid {theme['primary']}40;
    background: rgba(15,23,42,0.9);
    color: {theme['primary']};
    white-space: nowrap;
}}
.yh-journey-hero-subtitle {{
    font-size: 0.9375rem;
    color: #94a3b8;
    line-height: 1.55;
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


def render_journey_overview_card(
    role_display_name: str,
    active_plan_name: str,
    weekly_hours: float,
    num_weeks: int,
    growth_stage: str,
    theme: Dict[str, str],
) -> None:
    safe_role = _escape(role_display_name)
    safe_plan = _escape(active_plan_name)
    safe_stage = _escape(growth_stage)
    tempo = "8–10 saat"
    if weekly_hours <= 6:
        tempo = "4–6 saat"
    elif weekly_hours >= 12:
        tempo = "12+ saat"
    html = f"""
<div class="yh-journey-overview-card">
    <div class="yh-journey-overview-title">Yolculuk Özeti</div>
    <div class="yh-journey-overview-grid">
        <div class="yh-journey-overview-item"><span class="yh-journey-okey">Ana Hedef</span><span class="yh-journey-oval">{safe_role}</span></div>
        <div class="yh-journey-overview-item"><span class="yh-journey-okey">Aktif Plan</span><span class="yh-journey-oval">{safe_plan}</span></div>
        <div class="yh-journey-overview-item"><span class="yh-journey-okey">Haftalık Tempo</span><span class="yh-journey-oval">{tempo}</span></div>
        <div class="yh-journey-overview-item"><span class="yh-journey-okey">Plan Süresi</span><span class="yh-journey-oval">{num_weeks} Hafta</span></div>
        <div class="yh-journey-overview-item"><span class="yh-journey-okey">Gelişim Aşaması</span><span class="yh-journey-oval">{safe_stage}</span></div>
    </div>
</div>
"""
    css = f"""
<style>
.yh-journey-overview-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 2rem;
}}
.yh-journey-overview-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
    letter-spacing: 0.03em;
}}
.yh-journey-overview-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.6rem 1.25rem;
}}
.yh-journey-overview-item {{
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}
.yh-journey-okey {{
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
}}
.yh-journey-oval {{
    font-size: 0.9375rem;
    font-weight: 600;
    color: {theme['primary']};
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


def render_skill_snapshot(
    gap_result: GapAnalysisResult | None,
    skills: Dict[str, Skill],
    theme: Dict[str, str],
) -> None:
    if not gap_result or not gap_result.skill_gaps:
        summary = st.session_state.get("derived_profile_summary", "").strip()
        if summary:
            st.markdown(f"**Beceri özeti** — {summary}")
        else:
            st.markdown("**Beceri özeti** — Henüz beceri değerlendirmesi yok. Hedef ve Profil sayfasından plan oluştur.")
        return
    by_category: Dict[str, List[Any]] = {}
    for gap in gap_result.skill_gaps:
        cat = gap.category
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(gap)
    for category in sorted(by_category.keys()):
        group_label = CATEGORY_GROUP_LABELS.get(category, category)
        icon = CATEGORY_ICONS.get(category, "📌")
        st.markdown(f"**{icon} {group_label}**")
        items = []
        for gap in by_category[category]:
            label = _level_label(gap.current_level)
            items.append(f"{_escape(gap.display_name)}: {_escape(label)}")
        st.caption(", ".join(items))
        st.markdown("")


def render_next_step_card(
    weeks: List[WeekPlan] | None,
    theme: Dict[str, str],
) -> None:
    if not weeks or not any(w.skills for w in weeks):
        html = f"""
<div class="yh-journey-next-card">
    <div class="yh-journey-next-title">Sonraki Adım</div>
    <div class="yh-journey-next-body">Yol haritanı oluşturmak için <strong>Hedef ve Profil</strong> sayfasına git ve &quot;Yol Haritamı Oluştur&quot; butonuna tıkla.</div>
</div>
"""
    else:
        first_skill = None
        for w in weeks:
            if w.skills:
                first_skill = w.skills[0]
                break
        if not first_skill:
            return
        name = _escape(first_skill.display_name)
        hours = first_skill.estimated_hours
        reason = _escape(first_skill.rationale or f"{first_skill.display_name} becerisi hedef rolün için kritik.")
        html = f"""
<div class="yh-journey-next-card">
    <div class="yh-journey-next-title">Önerilen İlk Odak</div>
    <div class="yh-journey-next-skill">{name}</div>
    <div class="yh-journey-next-reason">{reason}</div>
    <div class="yh-journey-next-meta">Tahmini {hours:.1f} saat · Yüksek etki</div>
</div>
"""
    css = f"""
<style>
.yh-journey-next-card {{
    background: linear-gradient(135deg, {theme['primary']}18 0%, {theme['secondary']}12 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 1rem;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
}}
.yh-journey-next-title {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.4rem; }}
.yh-journey-next-skill {{ font-size: 1.1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.5rem; }}
.yh-journey-next-reason {{ font-size: 0.9rem; color: #94a3b8; line-height: 1.5; margin-bottom: 0.5rem; }}
.yh-journey-next-body {{ font-size: 0.9rem; color: #94a3b8; line-height: 1.5; }}
.yh-journey-next-meta {{ font-size: 0.8rem; color: {theme['primary']}; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


# Default fallbacks when state is missing (e.g. first load or legacy session)
_DEFAULT_GROWTH_STAGE = "Temel Oluşturma"
_DEFAULT_GROWTH_DESC = "Temellerin şekilleniyor. Düzenli ilerlemeyle bir üst gelişim aşamasına geçebilirsin."


def render_journey_overview_page(
    roles: Dict[str, Role],
    skills: Dict[str, Skill],
) -> None:
    ss = st.session_state
    # Use same keys as onboarding / Hedef ve Profil; sync aliases.
    selected_role_id = ss.get("selected_role_id") or ss.get("selected_target_role")
    if selected_role_id and selected_role_id not in roles:
        selected_role_id = None
    if not selected_role_id and roles:
        selected_role_id = next(iter(roles.keys()))
        ss["selected_role_id"] = selected_role_id
        ss["selected_target_role"] = selected_role_id
    # Theme injected once in app.py from canonical selected_role_id; avoid double-inject to prevent accent flip.
    theme = get_role_theme(selected_role_id)

    user_name = ss.get("user_name", "Kullanıcı")
    role_display_name = roles[selected_role_id].display_name if selected_role_id and selected_role_id in roles else (list(roles.values())[0].display_name if roles else "—")
    active_plan_name = ss.get("active_plan_name") or (f"{role_display_name} Yol Haritası" if role_display_name != "—" else "Kişiselleştirilmiş Yol Haritası")
    weekly_hours = ss.get("weekly_hours") or ss.get("selected_weekly_tempo") or 8.0
    num_weeks = ss.get("num_weeks") or ss.get("selected_plan_duration") or 4
    growth_stage = ss.get("growth_stage") or _DEFAULT_GROWTH_STAGE
    if not ss.get("derived_profile_summary") and role_display_name != "—":
        ss["derived_profile_summary"] = f"{role_display_name} hedefine ilerlerken {growth_stage} aşamasındasın."
    gap_result: GapAnalysisResult | None = ss.get("analysis_result")
    weeks: List[WeekPlan] | None = ss.get("weekly_plan")

    render_journey_hero(user_name, role_display_name, theme)
    render_journey_overview_card(
        role_display_name=role_display_name,
        active_plan_name=active_plan_name,
        weekly_hours=weekly_hours,
        num_weeks=num_weeks,
        growth_stage=growth_stage,
        theme=theme,
    )
    render_section_header("📊", "Beceri Özeti")
    render_skill_snapshot(gap_result, skills, theme)
    render_section_header("🎯", "Önerilen Sonraki Adım")
    render_next_step_card(weeks, theme)

