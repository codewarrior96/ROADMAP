from __future__ import annotations

import html as html_module
from dataclasses import dataclass
from typing import Dict, List, Any

import streamlit as st

from .algorithm import GapAnalysisResult, SkillGap
from .data_loader import Skill
from .planner import WeekPlan
from .design_system import get_role_theme


def _escape(text: str) -> str:
    """Escape for safe injection into HTML; prevents raw tags showing as text."""
    if not text:
        return ""
    return html_module.escape(str(text), quote=True)


@dataclass
class JourneyNode:
    id: str
    title: str
    status: str  # completed, active, next, locked
    estimated_hours: float
    difficulty: int
    summary: str
    related_skills: List[str]
    tips: List[str]
    mini_task: str
    reason: str


def _compute_readiness_percentage(gap_result: GapAnalysisResult) -> int:
    if not gap_result.skill_gaps:
        return 95
    total_required = sum(g.required_level for g in gap_result.skill_gaps)
    total_current = sum(g.current_level for g in gap_result.skill_gaps)
    if total_required == 0:
        return 95
    return min(95, max(5, int((total_current / total_required) * 100)))


def _compute_readiness_label(pct: int) -> str:
    if pct >= 75:
        return "İleri Seviye"
    elif pct >= 50:
        return "Orta Seviye"
    elif pct >= 30:
        return "Başlangıç+"
    else:
        return "Başlangıç"


def _get_tips_for_skill(skill_name: str, category: str) -> List[str]:
    tips_map = {
        "Python": ["Önce temel sözdizimi ve veri yapılarını öğren.", "Küçük scriptler yazarak pratik yap."],
        "Pandas": ["Veri okuma ve temizleme işlemlerinden başla.", "groupby ve merge fonksiyonlarına odaklan."],
        "SQL": ["SELECT, WHERE, JOIN ile başla.", "Gerçek veri setleriyle sorgu pratiği yap."],
        "Git": ["Commit, push, pull akışını öğren.", "Küçük bir proje ile branch kullanmayı dene."],
        "JavaScript": ["DOM manipülasyonunu anla.", "Event handling ile küçük uygulamalar yaz."],
        "React": ["Bileşen mantığını kavra.", "State ve props arasındaki farkı öğren."],
        "Machine Learning": ["Denetimli/denetimsiz öğrenme farkını anla.", "Scikit-learn ile basit modeller dene."],
        "Statistics": ["Ortalama, medyan, standart sapma ile başla.", "Dağılım grafiklerini yorumlamayı öğren."],
    }
    for key, tips in tips_map.items():
        if key.lower() in skill_name.lower():
            return tips
    if "Veri" in category:
        return ["Veri ile çalışırken temizlik ve doğrulama kritik.", "Küçük veri setleriyle başla."]
    if "Frontend" in category:
        return ["Görsel sonucu hemen görebilmek motivasyonu artırır.", "Responsive tasarım mantığını kavra."]
    return ["Temel kavramları not alarak öğren.", "Küçük uygulamalarla pekiştir."]


def _build_journey_nodes(
    weeks: List[WeekPlan],
    gap_result: GapAnalysisResult,
    skills: Dict[str, Skill],
) -> List[JourneyNode]:
    nodes: List[JourneyNode] = []
    scheduled_skills: List[Any] = []

    for week in weeks:
        for skill in week.skills:
            scheduled_skills.append((week.week_index, skill))

    node_idx = 0
    total_nodes = len(scheduled_skills) + 2

    nodes.append(JourneyNode(
        id="start",
        title="Başlangıç Noktası",
        status="completed",
        estimated_hours=0,
        difficulty=0,
        summary="Yolculuğa başlamak için hedef rolünü ve mevcut seviyeni belirledin.",
        related_skills=[],
        tips=["Hedefini net tut.", "Küçük adımlarla ilerle."],
        mini_task="Hedef rolün için 3 temel gereksinimi yaz.",
        reason="Her yolculuk bir başlangıç noktası gerektirir."
    ))
    node_idx += 1

    for i, (week_idx, skill) in enumerate(scheduled_skills):
        skill_meta = skills.get(skill.skill_id)
        category = skill_meta.category if skill_meta else "Genel"

        if i == 0:
            status = "active"
        elif i == 1:
            status = "next"
        else:
            status = "locked"

        tips = _get_tips_for_skill(skill.display_name, category)

        gap_info = next((g for g in gap_result.skill_gaps if g.skill_id == skill.skill_id), None)
        reason = f"Bu beceri, hedef rolün için {gap_info.role_weight:.1f} ağırlığında ve {gap_info.gap} seviye boşluk var." if gap_info else "Bu beceri rol gereksinimleri arasında yer alıyor."

        nodes.append(JourneyNode(
            id=skill.skill_id,
            title=skill.display_name,
            status=status,
            estimated_hours=skill.estimated_hours,
            difficulty=skill.difficulty,
            summary=f"{week_idx}. hafta odağı. {skill.rationale}",
            related_skills=[skill.display_name],
            tips=tips,
            mini_task=skill.mini_tasks[0] if skill.mini_tasks else "Bu beceri için küçük bir uygulama yap.",
            reason=reason
        ))
        node_idx += 1

    nodes.append(JourneyNode(
        id="milestone",
        title="Kariyer Eşiği",
        status="locked",
        estimated_hours=0,
        difficulty=0,
        summary="Bu noktada temel becerilerini tamamlamış ve role hazır olmaya yaklaşmış olacaksın.",
        related_skills=[],
        tips=["Öğrendiklerini bir portfolyo projesiyle göster.", "Özgeçmişini güncelle."],
        mini_task="Öğrendiğin becerileri gösteren mini bir proje oluştur.",
        reason="Hedef role doğru ilerlemenin somut bir göstergesi."
    ))

    return nodes


def _get_status_color(status: str) -> str:
    """Refined status colors: completed=green, active=cyan, next=violet, locked=cool gray."""
    colors = {
        "completed": "#10b981",
        "active": "#22d3ee",
        "next": "#a78bfa",
        "locked": "#64748b"
    }
    return colors.get(status, "#64748b")


def _get_status_label(status: str) -> str:
    labels = {
        "completed": "Tamamlandı",
        "active": "Aktif",
        "next": "Sıradaki",
        "locked": "Kilitli"
    }
    return labels.get(status, "Beklemede")


def _build_mini_project_suggestion(role_name: str) -> str:
    if "Data Analyst" in role_name:
        return "Açık bir veri seti ile uçtan uca analiz projesi: veri temizleme, görselleştirme ve içgörü raporu."
    if "AI Engineer" in role_name or "AI" in role_name:
        return "Küçük bir ML projesi: veri hazırlama, model eğitimi, değerlendirme metrikleri ve sonuç notu."
    if "Frontend" in role_name:
        return "Tek sayfalık React uygulaması: kullanıcı girişi, filtreleme ve temiz tasarım."
    return "Rol ile ilgili uçtan uca mini proje: temel kavramlar, veri/arayüz ve çıktı."


def render_career_roadmap(
    weeks: List[WeekPlan],
    gap_result: GapAnalysisResult | None,
    explanation: Dict[str, str] | None,
    skills: Dict[str, Skill],
    role_id: str | None = None,
) -> None:
    if gap_result is None or not weeks:
        st.warning("Henüz bir yol haritası oluşturulmadı.")
        return

    role = gap_result.role
    theme = get_role_theme(role_id)
    readiness_pct = _compute_readiness_percentage(gap_result)
    readiness_label = _compute_readiness_label(readiness_pct)
    journey_nodes = _build_journey_nodes(weeks, gap_result, skills)
    mini_project = _build_mini_project_suggestion(role.display_name)

    total_hours = sum(w.total_hours for w in weeks)
    total_weeks = len(weeks)

    success = theme.get("success", "#10b981")
    css = f"""
<style>
.cr-container {{ max-width: 1000px; margin: 0 auto; padding: 0 0 2rem 0; }}
.cr-hero {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}30;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-bottom: 2rem;
}}
.cr-hero-title {{ font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: {theme['primary']}; margin-bottom: 0.35rem; }}
.cr-hero-role {{ font-size: 1.375rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem; }}
.cr-hero-stats {{ display: flex; gap: 1.5rem; margin: 0.75rem 0; flex-wrap: wrap; }}
.cr-stat {{ text-align: center; }}
.cr-stat-value {{ font-size: 1.5rem; font-weight: 700; color: #f1f5f9; }}
.cr-stat-label {{ font-size: 0.6875rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }}
.cr-progress-bar {{ height: 6px; background: rgba(30,41,59,0.8); border-radius: 3px; overflow: hidden; margin: 0.75rem 0 0.4rem 0; max-width: 360px; }}
.cr-progress-fill {{ height: 100%; border-radius: 3px; transition: width 0.4s ease; }}
.cr-hero-summary {{ font-size: 0.875rem; color: #94a3b8; line-height: 1.55; max-width: 560px; }}

.cr-section {{ margin-bottom: 2rem; }}
.cr-section:last-child {{ margin-bottom: 0; }}
.cr-section-title {{ font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}

/* Timeline: clearer vertical flow and alignment */
.cr-journey {{ position: relative; padding-left: 3rem; margin-top: 0.25rem; }}
.cr-journey::before {{
    content: "";
    position: absolute;
    left: 15px;
    top: 20px;
    bottom: 20px;
    width: 2px;
    background: linear-gradient(to bottom, {success} 0%, {theme['primary']} 25%, {theme['secondary']} 60%, #475569 100%);
    border-radius: 1px;
}}

.cr-node {{ position: relative; margin-bottom: 1rem; }}
.cr-node:last-child {{ margin-bottom: 0; }}
.cr-node-header {{
    display: flex;
    align-items: center;
    gap: 0.85rem;
    cursor: pointer;
    padding: 0.9rem 1.15rem;
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    transition: border-color 0.2s ease, background 0.2s ease;
}}
.cr-node-header:hover {{
    border-color: {theme['primary']}35;
}}
/* Dot aligned to card vertical center */
.cr-node-dot {{
    position: absolute;
    left: -2.5rem;
    top: 50%;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 2px solid;
    background: #0f172a;
    z-index: 2;
}}
.cr-node-content {{ flex: 1; min-width: 0; }}
.cr-node-title {{ font-size: 0.9375rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.25rem; line-height: 1.35; }}
.cr-node-meta {{ font-size: 0.75rem; color: #94a3b8; display: flex; gap: 0.75rem; flex-wrap: wrap; }}
.cr-node-status {{
    font-size: 0.625rem;
    padding: 0.28rem 0.55rem;
    border-radius: 999px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    flex-shrink: 0;
}}
.cr-node-expand {{ font-size: 0.875rem; color: #64748b; transition: transform 0.2s; flex-shrink: 0; }}

.cr-node-details {{
    display: none;
    margin-top: 0.5rem;
    margin-left: 0;
    padding: 1rem 1.25rem;
    background: rgba(30,41,59,0.35);
    border: 1px solid rgba(71,85,105,0.3);
    border-radius: 12px;
}}
.cr-node-details.open {{ display: block; }}
.cr-detail-section {{ margin-bottom: 0.85rem; }}
.cr-detail-section:last-child {{ margin-bottom: 0; }}
.cr-detail-label {{ font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: {theme['primary']}; margin-bottom: 0.3rem; }}
.cr-detail-text {{ font-size: 0.8125rem; color: #94a3b8; line-height: 1.55; }}
.cr-detail-list {{ padding-left: 1rem; margin: 0.2rem 0 0 0; }}
.cr-detail-list li {{ font-size: 0.8125rem; color: #94a3b8; margin-bottom: 0.2rem; }}

/* Status clarity: subtle distinction (same meaning, clearer visuals) */
.cr-node--completed .cr-node-dot {{ background: {success}; border-color: {success}; }}
.cr-node--active .cr-node-dot {{ background: {theme['primary']}22; border-color: {theme['primary']}; box-shadow: 0 0 0 2px {theme['primary']}30; }}
.cr-node--next .cr-node-dot {{ background: rgba(167,139,250,0.15); border-color: {theme['secondary']}; }}
.cr-node--locked .cr-node-dot {{ background: #1e293b; border-color: #475569; }}

.cr-action-card {{
    background: {theme['gradient_start']};
    border: 1px solid {theme['primary']}35;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}}
.cr-action-label {{ font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: {theme['primary']}; margin-bottom: 0.35rem; }}
.cr-action-title {{ font-size: 1.0625rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.5rem; }}
.cr-action-stats {{ display: flex; gap: 1.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }}
.cr-action-stat {{ }}
.cr-action-stat-val {{ font-size: 0.9375rem; font-weight: 600; color: {theme['primary']}; }}
.cr-action-stat-lbl {{ font-size: 0.6875rem; color: #64748b; }}
.cr-action-reason {{ font-size: 0.8125rem; color: #94a3b8; line-height: 1.55; }}

.cr-projection {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
.cr-proj-card {{
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(71,85,105,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s ease;
}}
.cr-proj-card:hover {{ border-color: {theme['primary']}30; }}
.cr-proj-time {{ font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.06em; color: {theme['primary']}; margin-bottom: 0.4rem; }}
.cr-proj-text {{ font-size: 0.875rem; color: #e2e8f0; line-height: 1.5; }}

.cr-toggle {{ display: none; }}
.cr-toggle:checked + .cr-node-header + .cr-node-details {{ display: block; }}
.cr-toggle:checked + .cr-node-header .cr-node-expand {{ transform: rotate(180deg); }}
</style>
"""

    role_summary = f"Hedef rolün için toplam {len(gap_result.skill_gaps)} eksik beceri tespit edildi. "
    if readiness_pct >= 50:
        role_summary += "Temel yapın güçlü, odaklanarak hızlı ilerleme sağlayabilirsin."
    else:
        role_summary += "Önce temelleri güçlendirmen, sonraki adımları kolaylaştıracak."

    dynamic_title = _escape(f"{role.display_name} Yolculuğu")
    safe_readiness_label = _escape(readiness_label)
    safe_role_summary = _escape(role_summary)

    progress_style = f"width: {readiness_pct}%; background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});"
    hero_html = (
        "<div class=\"cr-hero\">"
        "<div class=\"cr-hero-title\">YolHaritam</div>"
        "<div class=\"cr-hero-role\">" + dynamic_title + "</div>"
        "<div class=\"cr-hero-stats\">"
        "<div class=\"cr-stat\"><div class=\"cr-stat-value\">" + safe_readiness_label + "</div><div class=\"cr-stat-label\">Mevcut Konum</div></div>"
        "<div class=\"cr-stat\"><div class=\"cr-stat-value\">" + str(readiness_pct) + "%</div><div class=\"cr-stat-label\">Hazırbulunuşluk</div></div>"
        "<div class=\"cr-stat\"><div class=\"cr-stat-value\">" + f"{total_hours:.0f}" + " saat</div><div class=\"cr-stat-label\">Toplam Süre</div></div>"
        "<div class=\"cr-stat\"><div class=\"cr-stat-value\">" + str(total_weeks) + " hafta</div><div class=\"cr-stat-label\">Plan Süresi</div></div>"
        "</div>"
        "<div class=\"cr-progress-bar\"><div class=\"cr-progress-fill\" style=\"" + progress_style + "\"></div></div>"
        "<div class=\"cr-hero-summary\">" + safe_role_summary + "</div>"
        "</div>"
    )

    journey_html_parts = []
    for i, node in enumerate(journey_nodes):
        color = _get_status_color(node.status)
        status_label = _get_status_label(node.status)
        status_bg = f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.2)"

        meta_items = []
        if node.estimated_hours > 0:
            meta_items.append(f"⏱️ {node.estimated_hours:.1f} saat")
        if node.difficulty > 0:
            meta_items.append(f"📊 Zorluk {node.difficulty}/5")
        meta_html = _escape(" · ".join(meta_items)) if meta_items else ""

        tips_html = "".join(f"<li>{_escape(tip)}</li>" for tip in node.tips)
        skills_html = _escape(", ".join(node.related_skills) if node.related_skills else "—")

        safe_title = _escape(node.title)
        safe_reason = _escape(node.reason)
        safe_summary = _escape(node.summary)
        safe_mini = _escape(node.mini_task)
        safe_status = _escape(status_label)

        node_html = (
            "<div class=\"cr-node cr-node--" + node.status + "\">"
            "<input type=\"checkbox\" class=\"cr-toggle\" id=\"node-" + str(i) + "\">"
            "<label class=\"cr-node-header\" for=\"node-" + str(i) + "\">"
            "<div class=\"cr-node-dot\" style=\"border-color: " + color + ";\"></div>"
            "<div class=\"cr-node-content\">"
            "<div class=\"cr-node-title\">" + safe_title + "</div>"
            "<div class=\"cr-node-meta\">" + meta_html + "</div>"
            "</div>"
            "<span class=\"cr-node-status\" style=\"background: " + status_bg + "; color: " + color + ";\">" + safe_status + "</span>"
            "<span class=\"cr-node-expand\">▼</span>"
            "</label>"
            "<div class=\"cr-node-details\">"
            "<div class=\"cr-detail-section\"><div class=\"cr-detail-label\">Bu adım neden önemli?</div><div class=\"cr-detail-text\">" + safe_reason + "</div></div>"
            "<div class=\"cr-detail-section\"><div class=\"cr-detail-label\">Özet</div><div class=\"cr-detail-text\">" + safe_summary + "</div></div>"
            "<div class=\"cr-detail-section\"><div class=\"cr-detail-label\">Eğitici İpuçları</div><ul class=\"cr-detail-list\">" + tips_html + "</ul></div>"
            "<div class=\"cr-detail-section\"><div class=\"cr-detail-label\">Mini Görev</div><div class=\"cr-detail-text\">" + safe_mini + "</div></div>"
            "</div>"
            "</div>"
        )
        journey_html_parts.append(node_html)

    journey_inner = "".join(journey_html_parts)
    journey_html = (
        "<div class=\"cr-section\">"
        "<div class=\"cr-section-title\">🗺️ Öğrenme Yolculuğu</div>"
        "<div class=\"cr-journey\">" + journey_inner + "</div>"
        "</div>"
    )

    first_active = next((n for n in journey_nodes if n.status == "active"), None)
    action_html = ""
    if first_active:
        safe_action_title = _escape(first_active.title)
        safe_action_reason = _escape(first_active.reason)
        action_hours = f"{first_active.estimated_hours:.1f}"
        action_html = (
            "<div class=\"cr-section\">"
            "<div class=\"cr-section-title\">🎯 Sonraki En Doğru Adım</div>"
            "<div class=\"cr-action-card\">"
            "<div class=\"cr-action-label\">Şu an odaklanman gereken</div>"
            "<div class=\"cr-action-title\">" + safe_action_title + "</div>"
            "<div class=\"cr-action-stats\">"
            "<div class=\"cr-action-stat\"><div class=\"cr-action-stat-val\">" + action_hours + " saat</div><div class=\"cr-action-stat-lbl\">Tahmini Süre</div></div>"
            "<div class=\"cr-action-stat\"><div class=\"cr-action-stat-val\">Yüksek</div><div class=\"cr-action-stat-lbl\">Etki</div></div>"
            "</div>"
            "<div class=\"cr-action-reason\">" + safe_action_reason + "</div>"
            "</div></div>"
        )

    proj_4w = _escape("Temel teknik yapı güçlenir, ilk pratikler yapılır.")
    proj_8w = _escape(f"{role.display_name} için ilk küçük proje üretilebilir.")
    proj_12w = _escape("Junior seviyede proje geliştirme güveni artar.")
    projection_html = (
        "<div class=\"cr-section\">"
        "<div class=\"cr-section-title\">🔮 Kariyer Projeksiyonu</div>"
        "<div class=\"cr-projection\">"
        "<div class=\"cr-proj-card\"><div class=\"cr-proj-time\">4 Hafta Sonra</div><div class=\"cr-proj-text\">" + proj_4w + "</div></div>"
        "<div class=\"cr-proj-card\"><div class=\"cr-proj-time\">8 Hafta Sonra</div><div class=\"cr-proj-text\">" + proj_8w + "</div></div>"
        "<div class=\"cr-proj-card\"><div class=\"cr-proj-time\">12 Hafta Sonra</div><div class=\"cr-proj-text\">" + proj_12w + "</div></div>"
        "</div></div>"
    )

    full_html = css + "<div class=\"cr-container\">" + hero_html + journey_html + action_html + projection_html + "</div>"
    st.markdown(full_html, unsafe_allow_html=True)


def render_visual_roadmap(
    weeks: List[WeekPlan],
    gap_result: GapAnalysisResult | None,
    explanation: Dict[str, str] | None,
    skills: Dict[str, Skill],
    role_id: str | None = None,
) -> None:
    render_career_roadmap(weeks, gap_result, explanation, skills, role_id)
