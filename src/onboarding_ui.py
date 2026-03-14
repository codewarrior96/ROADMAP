"""
YolHaritam onboarding: premium career journey entry experience.
Modular render functions, growth stage (no readiness %), chip-based skill levels.
"""
from __future__ import annotations

import html as html_module
from typing import Dict, List, Tuple, Any

import streamlit as st

from .data_loader import Skill, Role
from .design_system import get_role_theme, generate_avatar_initials, inject_global_styles, render_section_header


def _escape(text: str) -> str:
    """Escape for safe injection into HTML; prevents raw tags showing as text."""
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


# ---- Discrete skill level options (no sliders) ----
SKILL_LEVEL_OPTIONS = [
    ("hic_baslamadim", "Hiç Başlamadım"),
    ("temel_bilgim_var", "Temel Bilgim Var"),
    ("pratik_yaptim", "Pratik Yaptım"),
    ("kucuk_projeler", "Küçük Projeler Geliştirdim"),
    ("guclu_hissediyorum", "Güçlü Hissediyorum"),
]
SKILL_LEVEL_KEYS = [o[0] for o in SKILL_LEVEL_OPTIONS]

# Map level key -> 0..5 for algorithm
SKILL_LEVEL_TO_NUMERIC: Dict[str, int] = {
    "hic_baslamadim": 0,
    "temel_bilgim_var": 1,
    "pratik_yaptim": 2,
    "kucuk_projeler": 3,
    "guclu_hissediyorum": 4,
}

# Growth stages (replace percentage readiness)
GROWTH_STAGES = [
    ("kesif", "Keşif Aşaması", "Yeni alanlara adım atıyorsun. Küçük adımlarla ilerleyerek güven kazanacaksın."),
    ("temel", "Temel Oluşturma", "Temellerin şekilleniyor. Düzenli ilerlemeyle bir üst gelişim aşamasına geçebilirsin."),
    ("duzenli", "Düzenli Gelişim", "Tutarlı bir ilerleme kaydediyorsun. Proje odaklı çalışmalarla derinleşebilirsin."),
    ("proje", "Proje Üretim Aşaması", "Projelerle kendini kanıtlıyorsun. Bir sonraki aşama için profesyonelleşmeye odaklan."),
    ("profesyonel", "Profesyonelleşme", "Hedef role yaklaşıyorsun. İleri seviye konular ve portfolyo ile fark yaratabilirsin."),
]

# Human-centered tempo and duration
TEMPO_OPTIONS = [
    ("light", "Hafif Tempo", "4–6 saat", 5.0),
    ("balanced", "Dengeli Tempo", "8–10 saat", 9.0),
    ("intense", "Yoğun Tempo", "12+ saat", 14.0),
]
DURATION_OPTIONS = [(4, "4 Hafta"), (8, "8 Hafta"), (12, "12 Hafta")]

# Category display names (optional grouping labels)
CATEGORY_LABELS: Dict[str, str] = {
    "Genel": "Temel Yetkinlikler",
    "Programlama": "Yazılım Geliştirme",
    "Profesyonel Pratikler": "Profesyonel Pratikler",
    "Matematik": "Veri ve Analitik Düşünce",
    "Veri Bilimi": "Veri ve Analitik Düşünce",
    "Veri Tabanları": "Veri ve Analitik Düşünce",
    "Yapay Zeka": "AI / Data Odaklı Beceriler",
    "Frontend": "Yazılım Geliştirme",
}
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


def skill_level_key_to_numeric(key: str) -> int:
    """Map discrete level key to 0–4 for gap analysis."""
    return SKILL_LEVEL_TO_NUMERIC.get(key, 0)


def get_growth_stage_from_levels(current_levels: Dict[str, int]) -> Tuple[str, str, str]:
    """Derive growth stage id, label, and description from skill levels (0–4)."""
    if not current_levels:
        return GROWTH_STAGES[0][0], GROWTH_STAGES[0][1], GROWTH_STAGES[0][2]
    avg = sum(current_levels.values()) / len(current_levels)
    if avg < 1.0:
        idx = 0
    elif avg < 2.0:
        idx = 1
    elif avg < 3.0:
        idx = 2
    elif avg < 4.0:
        idx = 3
    else:
        idx = 4
    stage = GROWTH_STAGES[idx]
    return stage[0], stage[1], stage[2]


def get_profile_summary(
    role_display_name: str,
    active_plan_name: str,
    growth_stage_label: str,
) -> str:
    """Generate short personalized summary for sidebar."""
    return f"{role_display_name} hedefine ilerlerken {active_plan_name} ile gelişim aşamasındasın."


def _active_plan_from_role(role: Role) -> str:
    """Derive active plan label from role (e.g. first category or role name)."""
    return f"{role.display_name} Yol Haritası"


def _get_selected_level_key(skill_id: str) -> str:
    return st.session_state.get(f"onboard_skill_{skill_id}", "hic_baslamadim")


def _build_current_levels_from_session(role: Role) -> Dict[str, int]:
    """Build current_levels dict from session_state skill level keys."""
    current_levels: Dict[str, int] = {}
    for skill_id in role.skills.keys():
        key = _get_selected_level_key(skill_id)
        current_levels[skill_id] = skill_level_key_to_numeric(key)
    return current_levels


def render_onboarding_profile_panel(
    user_name: str,
    role_display_name: str,
    active_plan_name: str,
    growth_stage_id: str,
    growth_stage_label: str,
    growth_stage_description: str,
    profile_summary: str,
    theme: Dict[str, str],
    avatar_url: str | None = None,
) -> None:
    """Left column: premium profile card with avatar, target, active plan, growth stage badge, summary."""
    if avatar_url:
        avatar_content = f'<img src="{avatar_url}" alt="Avatar">'
    else:
        initials = generate_avatar_initials(user_name)
        avatar_content = f'<span style="color: #f1f5f9; font-weight: 700;">{initials}</span>'

    css = f"""
<style>
.yh-onboard-profile {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.2rem;
}}
.yh-onboard-avatar {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto 0.75rem auto;
    background: {theme['gradient_start']};
    border: 2px solid {theme['primary']}35;
    overflow: hidden;
}}
.yh-onboard-avatar img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }}
.yh-onboard-name {{ font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem; text-align: center; }}
.yh-onboard-meta {{ font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.35rem; }}
.yh-onboard-meta-value {{ color: #e2e8f0; font-weight: 600; }}
.yh-onboard-stage {{
    background: linear-gradient(135deg, {theme['primary']}18, {theme['secondary']}12);
    border: 1px solid {theme['primary']}35;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
}}
.yh-onboard-stage-label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.25rem; }}
.yh-onboard-stage-name {{ font-size: 0.95rem; font-weight: 600; color: {theme['primary']}; }}
.yh-onboard-stage-desc {{ font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem; line-height: 1.4; }}
.yh-onboard-summary {{ font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(51,65,85,0.5); }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

    safe_name = _escape(user_name)
    safe_role = _escape(role_display_name)
    safe_plan = _escape(active_plan_name)
    safe_stage = _escape(growth_stage_label)
    safe_stage_desc = _escape(growth_stage_description)
    safe_summary = _escape(profile_summary)
    html = f"""
<div class="yh-onboard-profile">
    <div class="yh-onboard-avatar">{avatar_content}</div>
    <div class="yh-onboard-name">{safe_name}</div>
    <div class="yh-onboard-meta">Ana Kariyer Hedefi <span class="yh-onboard-meta-value">— {safe_role}</span></div>
    <div class="yh-onboard-meta">Aktif Plan <span class="yh-onboard-meta-value">— {safe_plan}</span></div>
    <div class="yh-onboard-stage">
        <div class="yh-onboard-stage-label">Gelişim Aşaması</div>
        <div class="yh-onboard-stage-name">{safe_stage}</div>
        <div class="yh-onboard-stage-desc">{safe_stage_desc}</div>
    </div>
    <div class="yh-onboard-summary">{safe_summary}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_onboarding_top_controls(
    roles: Dict[str, Role],
    theme: Dict[str, str],
) -> Tuple[str, float, int]:
    """
    Target role, weekly tempo (chips), plan duration (chips).
    Returns (selected_role_id, weekly_hours, num_weeks).
    """
    role_options = {r.display_name: r.id for r in roles.values()}
    role_names = sorted(role_options.keys())
    default_idx = 0
    if "onboard_role" in st.session_state and st.session_state["onboard_role"] in role_names:
        default_idx = role_names.index(st.session_state["onboard_role"])

    col_role, col_tempo, col_duration = st.columns(3)

    with col_role:
        st.markdown("**Hedef Rol**")
        role_name = st.selectbox(
            "Hedef Rol",
            options=role_names,
            index=default_idx,
            label_visibility="collapsed",
            key="onboard_role",
        )

    with col_tempo:
        st.markdown("**Haftalık Tempo**")
        tempo_idx = st.session_state.get("onboard_tempo_radio", 1)
        new_tempo = st.radio(
            "Tempo",
            options=range(len(TEMPO_OPTIONS)),
            index=min(tempo_idx, len(TEMPO_OPTIONS) - 1),
            format_func=lambda i: TEMPO_OPTIONS[i][1] + " · " + TEMPO_OPTIONS[i][2],
            label_visibility="collapsed",
            key="onboard_tempo_radio",
            horizontal=False,
        )
        weekly_hours = TEMPO_OPTIONS[new_tempo][3]

    with col_duration:
        st.markdown("**Plan Süresi**")
        dur_idx = st.session_state.get("onboard_duration_radio", 0)
        duration_weeks_idx = st.radio(
            "Süre",
            options=range(len(DURATION_OPTIONS)),
            index=min(dur_idx, len(DURATION_OPTIONS) - 1),
            format_func=lambda i: DURATION_OPTIONS[i][1],
            label_visibility="collapsed",
            key="onboard_duration_radio",
            horizontal=False,
        )
        num_weeks = DURATION_OPTIONS[duration_weeks_idx][0]

    selected_role_id = role_options[role_name]
    return selected_role_id, weekly_hours, num_weeks


def render_onboarding_hero_card(
    role_display_name: str,
    tempo_label: str,
    duration_weeks: int,
    theme: Dict[str, str],
) -> None:
    """Hero card: title, description, three info capsules (Hedef Rol, Plan Süresi, Haftalık Tempo)."""
    css = f"""
<style>
.yh-onboard-hero {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}}
.yh-onboard-hero-title {{ font-size: 1.375rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem; }}
.yh-onboard-hero-desc {{ font-size: 0.9375rem; color: #94a3b8; line-height: 1.55; max-width: 560px; margin-bottom: 1.25rem; }}
.yh-onboard-capsules {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
.yh-onboard-capsule {{
    background: rgba(15,23,42,0.5);
    border: 1px solid {theme['primary']}30;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    color: #e2e8f0;
}}
.yh-onboard-capsule strong {{ color: {theme['primary']}; margin-right: 0.35rem; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    html = f"""
<div class="yh-onboard-hero">
    <div class="yh-onboard-hero-title">Sana Özel Öğrenme Rotanı Oluştur</div>
    <div class="yh-onboard-hero-desc">
        Seçtiğin hedefe, mevcut becerilerine ve ayırabildiğin zamana göre kişiselleştirilmiş bir öğrenme planı hazırlıyoruz. Mevcut durumunu alan bazlı işaretle, sistem senin için en uygun rotayı üretsin.
    </div>
    <div class="yh-onboard-capsules">
        <span class="yh-onboard-capsule"><strong>Hedef Rol</strong> {_escape(role_display_name)}</span>
        <span class="yh-onboard-capsule"><strong>Plan Süresi</strong> {duration_weeks} Hafta</span>
        <span class="yh-onboard-capsule"><strong>Haftalık Tempo</strong> {_escape(tempo_label)}</span>
    </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_onboarding_skill_assessment(
    selected_role: Role,
    skills: Dict[str, Skill],
    theme: Dict[str, str],
) -> None:
    """Grouped skill cards with discrete level selection (chips / selectbox). No sliders."""
    # Group by category
    skill_categories: Dict[str, List[Tuple[str, Skill]]] = {}
    for skill_id in selected_role.skills.keys():
        skill = skills[skill_id]
        cat = skill.category
        if cat not in skill_categories:
            skill_categories[cat] = []
        skill_categories[cat].append((skill_id, skill))

    css = f"""
<style>
.yh-onboard-skill-section {{ margin-bottom: 1.5rem; }}
.yh-onboard-skill-cat {{ font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; }}
.yh-onboard-skill-card {{
    background: rgba(30,41,59,0.45);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}}
.yh-onboard-skill-card:hover {{ border-color: {theme['primary']}30; }}
.yh-onboard-skill-title {{ font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.25rem; }}
.yh-onboard-skill-desc {{ font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.6rem; }}
.yh-onboard-level-options {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
.yh-onboard-chip {{
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.8rem;
    border: 1px solid rgba(51,65,85,0.8);
    background: rgba(30,41,59,0.5);
    color: #94a3b8;
    cursor: pointer;
}}
.yh-onboard-chip.selected {{
    border-color: {theme['primary']};
    background: {theme['primary']}18;
    color: {theme['primary']};
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

    for category in sorted(skill_categories.keys()):
        cat_skills = skill_categories[category]
        group_label = CATEGORY_LABELS.get(category, category)
        icon = CATEGORY_ICONS.get(category, "📌")
        safe_label = _escape(group_label)
        st.markdown(f"<div class='yh-onboard-skill-cat'>{icon} {safe_label}</div>", unsafe_allow_html=True)

        for skill_id, skill in cat_skills:
            current_key = _get_selected_level_key(skill_id)
            safe_skill_name = _escape(skill.display_name)
            st.markdown(f"""
<div class="yh-onboard-skill-card">
    <div class="yh-onboard-skill-title">{safe_skill_name}</div>
    <div class="yh-onboard-skill-desc">Mevcut durumunu seç</div>
</div>
""", unsafe_allow_html=True)
            # Use selectbox for clear selected state (Streamlit doesn't support styled chips as form controls)
            _level_labels = {k: lbl for k, lbl in SKILL_LEVEL_OPTIONS}
            st.selectbox(
                skill.display_name,
                options=SKILL_LEVEL_KEYS,
                index=SKILL_LEVEL_KEYS.index(current_key) if current_key in SKILL_LEVEL_KEYS else 0,
                key=f"onboard_skill_{skill_id}",
                label_visibility="collapsed",
                format_func=lambda k: _level_labels.get(k, k),
            )


def render_onboarding_action_area(submitted_key: str = "onboard_submit") -> bool:
    """Primary and secondary CTAs. Returns True if primary submitted."""
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    col_primary, col_secondary = st.columns([1, 2])
    with col_primary:
        submitted = st.button("Planımı Oluştur", type="primary", use_container_width=True, key=submitted_key)
    with col_secondary:
        st.caption("Beceri alanlarını gözden geçirip mevcut durumunu güncelleyebilirsin.")
    return submitted


def render_onboarding_page(
    roles: Dict[str, Role],
    skills: Dict[str, Skill],
    modules: List[Any] | None = None,
) -> Tuple[str, float, int, Dict[str, int], bool]:
    """
    Premium career journey entry: profile panel (left), controls + hero + skills + action (main).
    No readiness bar; growth stage badge. No sliders; discrete skill levels.
    Returns (selected_role_id, weekly_hours, num_weeks, current_levels, submitted).
    """
    if modules is None:
        modules = []
    role_options = {r.display_name: r.id for r in roles.values()}
    role_names = sorted(role_options.keys())
    default_role_name = role_names[0]
    # Sync role from session so left panel and controls stay consistent
    current_role_name = st.session_state.get("onboard_role", default_role_name)
    if current_role_name not in role_names:
        current_role_name = default_role_name
    selected_role_id = role_options[current_role_name]
    selected_role = roles[selected_role_id]
    theme = get_role_theme(selected_role_id)
    inject_global_styles(selected_role_id)

    # Left = profile panel, Right = main flow (controls, hero, skills, action)
    col_left, col_main = st.columns([1, 3])
    with col_left:
        user_name = st.session_state.get("user_name", "Kullanıcı")
        user_avatar = st.session_state.get("user_avatar")
        current_levels_pre = _build_current_levels_from_session(selected_role)
        growth_stage_id, growth_stage_label, growth_stage_desc = get_growth_stage_from_levels(current_levels_pre)
        active_plan_name = _active_plan_from_role(selected_role)
        role_display_name = selected_role.display_name
        profile_summary = get_profile_summary(role_display_name, active_plan_name, growth_stage_label)
        render_onboarding_profile_panel(
            user_name=user_name,
            role_display_name=role_display_name,
            active_plan_name=active_plan_name,
            growth_stage_id=growth_stage_id,
            growth_stage_label=growth_stage_label,
            growth_stage_description=growth_stage_desc,
            profile_summary=profile_summary,
            theme=theme,
            avatar_url=user_avatar,
        )

    with col_main:
        selected_role_id, weekly_hours, num_weeks = render_onboarding_top_controls(roles, theme)
        selected_role = roles[selected_role_id]
        theme = get_role_theme(selected_role_id)

        tempo_label = next((t[2] for t in TEMPO_OPTIONS if abs(t[3] - weekly_hours) < 2), "8–10 saat")
        render_onboarding_hero_card(selected_role.display_name, tempo_label, num_weeks, theme)

        render_section_header("📊", "Beceri Durumunu İşaretle")
        st.caption("Her alan için mevcut durumunu seç. Slider yok — sadece senin hissettiğin seviye.")

        render_onboarding_skill_assessment(selected_role, skills, theme)

        submitted = render_onboarding_action_area()

    # Build current_levels from session (all skill widgets are in col_main, so state is updated)
    selected_role = roles[selected_role_id]
    current_levels = _build_current_levels_from_session(selected_role)

    if submitted:
        _, growth_stage_label, growth_stage_desc = get_growth_stage_from_levels(current_levels)
        st.session_state["growth_stage"] = growth_stage_label
        st.session_state["growth_stage_description"] = growth_stage_desc
        st.session_state["active_plan_name"] = _active_plan_from_role(selected_role)

    return selected_role_id, weekly_hours, num_weeks, current_levels, submitted
