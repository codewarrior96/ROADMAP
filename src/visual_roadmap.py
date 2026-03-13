from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

import streamlit as st

from .algorithm import GapAnalysisResult, SkillGap
from .data_loader import Skill
from .planner import WeekPlan
from .design_system import get_role_theme


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
    colors = {
        "completed": "#22c55e",
        "active": "#3b82f6",
        "next": "#a855f7",
        "locked": "#6b7280"
    }
    return colors.get(status, "#6b7280")


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

    css = f"""
<style>
.cr-container {{ max-width: 1000px; margin: 0 auto; }}
.cr-hero {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}66;
    border-radius: 1.2rem;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}
.cr-hero::before {{
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, {theme['glow']}, transparent 70%);
    pointer-events: none;
}}
.cr-hero-title {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: {theme['primary']}; margin-bottom: 0.4rem; }}
.cr-hero-role {{ font-size: 1.6rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.6rem; }}
.cr-hero-stats {{ display: flex; gap: 2rem; margin: 1rem 0; flex-wrap: wrap; }}
.cr-stat {{ text-align: center; }}
.cr-stat-value {{ font-size: 1.8rem; font-weight: 700; color: #f1f5f9; }}
.cr-stat-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }}
.cr-progress-bar {{ height: 8px; background: rgba(30,41,59,0.8); border-radius: 4px; overflow: hidden; margin: 1rem 0 0.5rem 0; max-width: 400px; }}
.cr-progress-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s ease; }}
.cr-hero-summary {{ font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; max-width: 600px; }}

.cr-section {{ margin-bottom: 2rem; }}
.cr-section-title {{ font-size: 1.1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}

.cr-journey {{ position: relative; padding-left: 3rem; }}
.cr-journey::before {{
    content: "";
    position: absolute;
    left: 18px;
    top: 20px;
    bottom: 20px;
    width: 3px;
    background: linear-gradient(to bottom, #22c55e 0%, {theme['primary']} 30%, {theme['secondary']} 70%, #6b7280 100%);
    border-radius: 2px;
}}

.cr-node {{
    position: relative;
    margin-bottom: 0.8rem;
}}
.cr-node-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
    padding: 0.9rem 1.2rem;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 0.9rem;
    transition: all 0.2s ease;
}}
.cr-node-header:hover {{
    background: rgba(30,41,59,0.8);
    border-color: {theme['primary']}88;
}}
.cr-node-dot {{
    position: absolute;
    left: -2.5rem;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 3px solid;
    background: #0f172a;
    z-index: 2;
}}
.cr-node-content {{ flex: 1; }}
.cr-node-title {{ font-size: 0.95rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.15rem; }}
.cr-node-meta {{ font-size: 0.75rem; color: #94a3b8; display: flex; gap: 1rem; flex-wrap: wrap; }}
.cr-node-status {{
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.cr-node-expand {{ font-size: 1.2rem; color: #64748b; transition: transform 0.2s; }}

.cr-node-details {{
    display: none;
    margin-top: 0.5rem;
    margin-left: 0;
    padding: 1rem 1.2rem;
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(51,65,85,0.4);
    border-radius: 0.8rem;
}}
.cr-node-details.open {{ display: block; }}
.cr-detail-section {{ margin-bottom: 0.8rem; }}
.cr-detail-section:last-child {{ margin-bottom: 0; }}
.cr-detail-label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: {theme['primary']}; margin-bottom: 0.3rem; }}
.cr-detail-text {{ font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; }}
.cr-detail-list {{ padding-left: 1.2rem; margin: 0.2rem 0 0 0; }}
.cr-detail-list li {{ font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.2rem; }}

.cr-action-card {{
    background: linear-gradient(135deg, {theme['gradient_start']} 0%, {theme['gradient_end']} 100%);
    border: 1px solid {theme['primary']}66;
    border-radius: 1rem;
    padding: 1.4rem 1.6rem;
}}
.cr-action-label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: {theme['primary']}; margin-bottom: 0.4rem; }}
.cr-action-title {{ font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.6rem; }}
.cr-action-stats {{ display: flex; gap: 2rem; margin-bottom: 0.8rem; flex-wrap: wrap; }}
.cr-action-stat {{ }}
.cr-action-stat-val {{ font-size: 1rem; font-weight: 600; color: {theme['primary']}; }}
.cr-action-stat-lbl {{ font-size: 0.7rem; color: #94a3b8; }}
.cr-action-reason {{ font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; }}

.cr-projection {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}}
.cr-proj-card {{
    background: rgba(30,41,59,0.6);
    border: 1px solid rgba(51,65,85,0.5);
    border-radius: 0.9rem;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s ease;
}}
.cr-proj-card:hover {{
    border-color: {theme['primary']}44;
    transform: translateY(-2px);
}}
.cr-proj-time {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: {theme['primary']}; margin-bottom: 0.4rem; }}
.cr-proj-text {{ font-size: 0.9rem; color: #e2e8f0; line-height: 1.5; }}

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

    dynamic_title = f"{role.display_name} Yolculuğu"

    hero_html = f"""
<div class="cr-hero">
    <div class="cr-hero-title">YolHaritam</div>
    <div class="cr-hero-role">{dynamic_title}</div>
    <div class="cr-hero-stats">
        <div class="cr-stat">
            <div class="cr-stat-value">{readiness_label}</div>
            <div class="cr-stat-label">Mevcut Konum</div>
        </div>
        <div class="cr-stat">
            <div class="cr-stat-value">{readiness_pct}%</div>
            <div class="cr-stat-label">Hazırbulunuşluk</div>
        </div>
        <div class="cr-stat">
            <div class="cr-stat-value">{total_hours:.0f} saat</div>
            <div class="cr-stat-label">Toplam Süre</div>
        </div>
        <div class="cr-stat">
            <div class="cr-stat-value">{total_weeks} hafta</div>
            <div class="cr-stat-label">Plan Süresi</div>
        </div>
    </div>
    <div class="cr-progress-bar">
        <div class="cr-progress-fill" style="width: {readiness_pct}%; background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});"></div>
    </div>
    <div class="cr-hero-summary">{role_summary}</div>
</div>
"""

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
        meta_html = " · ".join(meta_items) if meta_items else ""

        tips_html = "".join(f"<li>{tip}</li>" for tip in node.tips)
        skills_html = ", ".join(node.related_skills) if node.related_skills else "—"

        node_html = f"""
<div class="cr-node">
    <input type="checkbox" class="cr-toggle" id="node-{i}">
    <label class="cr-node-header" for="node-{i}">
        <div class="cr-node-dot" style="border-color: {color};"></div>
        <div class="cr-node-content">
            <div class="cr-node-title">{node.title}</div>
            <div class="cr-node-meta">{meta_html}</div>
        </div>
        <span class="cr-node-status" style="background: {status_bg}; color: {color};">{status_label}</span>
        <span class="cr-node-expand">▼</span>
    </label>
    <div class="cr-node-details">
        <div class="cr-detail-section">
            <div class="cr-detail-label">Bu adım neden önemli?</div>
            <div class="cr-detail-text">{node.reason}</div>
        </div>
        <div class="cr-detail-section">
            <div class="cr-detail-label">Özet</div>
            <div class="cr-detail-text">{node.summary}</div>
        </div>
        <div class="cr-detail-section">
            <div class="cr-detail-label">Eğitici İpuçları</div>
            <ul class="cr-detail-list">{tips_html}</ul>
        </div>
        <div class="cr-detail-section">
            <div class="cr-detail-label">Mini Görev</div>
            <div class="cr-detail-text">{node.mini_task}</div>
        </div>
    </div>
</div>
"""
        journey_html_parts.append(node_html)

    journey_html = f"""
<div class="cr-section">
    <div class="cr-section-title">🗺️ Öğrenme Yolculuğu</div>
    <div class="cr-journey">
        {"".join(journey_html_parts)}
    </div>
</div>
"""

    first_active = next((n for n in journey_nodes if n.status == "active"), None)
    if first_active:
        action_html = f"""
<div class="cr-section">
    <div class="cr-section-title">🎯 Sonraki En Doğru Adım</div>
    <div class="cr-action-card">
        <div class="cr-action-label">Şu an odaklanman gereken</div>
        <div class="cr-action-title">{first_active.title}</div>
        <div class="cr-action-stats">
            <div class="cr-action-stat">
                <div class="cr-action-stat-val">{first_active.estimated_hours:.1f} saat</div>
                <div class="cr-action-stat-lbl">Tahmini Süre</div>
            </div>
            <div class="cr-action-stat">
                <div class="cr-action-stat-val">Yüksek</div>
                <div class="cr-action-stat-lbl">Etki</div>
            </div>
        </div>
        <div class="cr-action-reason">{first_active.reason}</div>
    </div>
</div>
"""
    else:
        action_html = ""

    proj_4w = "Temel teknik yapı güçlenir, ilk pratikler yapılır."
    proj_8w = f"{role.display_name} için ilk küçük proje üretilebilir."
    proj_12w = "Junior seviyede proje geliştirme güveni artar."

    projection_html = f"""
<div class="cr-section">
    <div class="cr-section-title">🔮 Kariyer Projeksiyonu</div>
    <div class="cr-projection">
        <div class="cr-proj-card">
            <div class="cr-proj-time">4 Hafta Sonra</div>
            <div class="cr-proj-text">{proj_4w}</div>
        </div>
        <div class="cr-proj-card">
            <div class="cr-proj-time">8 Hafta Sonra</div>
            <div class="cr-proj-text">{proj_8w}</div>
        </div>
        <div class="cr-proj-card">
            <div class="cr-proj-time">12 Hafta Sonra</div>
            <div class="cr-proj-text">{proj_12w}</div>
        </div>
    </div>
</div>
"""

    full_html = f"""
{css}
<div class="cr-container">
    {hero_html}
    {journey_html}
    {action_html}
    {projection_html}
</div>
"""

    st.markdown(full_html, unsafe_allow_html=True)


def render_visual_roadmap(
    weeks: List[WeekPlan],
    gap_result: GapAnalysisResult | None,
    explanation: Dict[str, str] | None,
    skills: Dict[str, Skill],
    role_id: str | None = None,
) -> None:
    render_career_roadmap(weeks, gap_result, explanation, skills, role_id)
