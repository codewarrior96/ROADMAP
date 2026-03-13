from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

from .algorithm import GapAnalysisResult, SkillGap
from .data_loader import Skill


@dataclass
class WeeklySkillPlan:
    skill_id: str
    display_name: str
    estimated_hours: float
    difficulty: int
    mini_tasks: List[str]
    rationale: str


@dataclass
class WeekPlan:
    week_index: int  # 1-based
    total_hours: float
    skills: List[WeeklySkillPlan]


def _estimate_skill_hours(gap: SkillGap) -> float:
    """
    Simple workload estimation:
    - higher gaps and higher difficulty take more time
    - result is approximate weekly hours needed
    """
    base = gap.gap * gap.difficulty * 1.5
    # Quick wins biraz daha kısa sürede tamamlanabilir
    if gap.quick_win:
        base *= 0.8
    return max(2.0, round(base, 1))


def build_weekly_plan(
    gap_result: GapAnalysisResult,
    skills: Dict[str, Skill],
    weekly_hours: float,
    num_weeks: int = 4,
) -> List[WeekPlan]:
    """
    Build a simple 4-week roadmap.

    Kurallar:
    - Haftada en fazla 2 odak beceri
    - Önce önkoşullar, sonra daha ileri konular
    - Zor beceriler aynı haftada birikmesin
    - Haftalık saat sınırı mümkün olduğunca aşılmasın
    """
    if num_weeks <= 0:
        num_weeks = 4

    # Başlangıç boş hafta yapısı (tam olarak seçilen süre kadar)
    weeks: List[WeekPlan] = [
        WeekPlan(week_index=i + 1, total_hours=0.0, skills=[]) for i in range(num_weeks)
    ]

    for gap in gap_result.skill_gaps:
        skill_meta = skills[gap.skill_id]
        est_hours = _estimate_skill_hours(gap)

        # Beceri için en uygun haftayı seç: yeterli boş saat ve zorlayıcılık dengesi
        chosen_week = _choose_week_for_skill(weeks, gap, weekly_hours, est_hours)
        # Eğer hiçbir haftaya sığmıyorsa, süre ve saat sınırı nedeniyle bu plana alınmaz
        if chosen_week is None:
            continue

        rationale_parts = []
        if gap.missing_prerequisites:
            rationale_parts.append("Bu becerinin eksik önkoşulları önceki haftalarda ele alınacak.")
        if gap.quick_win:
            rationale_parts.append("Hızlı motivasyon kazandıran, nispeten çabuk öğrenilebilen bir beceri.")
        if gap.difficulty >= 4:
            rationale_parts.append("Zorluk seviyesi yüksek olduğundan haftaya tek büyük odak olarak yerleştirildi.")

        if not rationale_parts:
            rationale_parts.append("Rol için önemli ve mevcut seviyenle arasında anlamlı bir boşluk bulunan bir beceri.")

        weekly_skill = WeeklySkillPlan(
            skill_id=gap.skill_id,
            display_name=gap.display_name,
            estimated_hours=est_hours,
            difficulty=gap.difficulty,
            mini_tasks=skill_meta.mini_tasks[:4],
            rationale=" ".join(rationale_parts),
        )

        chosen_week.skills.append(weekly_skill)
        chosen_week.total_hours += est_hours

    return weeks


def _choose_week_for_skill(
    weeks: List[WeekPlan],
    gap: SkillGap,
    weekly_hours: float,
    est_hours: float,
) -> WeekPlan | None:
    """
    Select a week for the given skill.

    Heuristics:
    - Maximum 2 skills per week.
    - Stay within weekly_hours.
    - Avoid grouping multiple high-difficulty skills.
    - Prefer earlier weeks overall.
    """
    # Önce kısıtlara en çok uyan haftaları bul
    candidate_weeks: List[WeekPlan] = []
    for week in weeks:
        if len(week.skills) >= 2:
            continue

        projected_hours = week.total_hours + est_hours
        # Haftalık saatin üzerine ÇIKMA (sert kısıt)
        if projected_hours > weekly_hours:
            continue

        # Zor becerileri aynı haftaya yığmaktan kaçın
        difficulty_sum = sum(s.difficulty for s in week.skills) + gap.difficulty
        if difficulty_sum > 8:
            continue

        candidate_weeks.append(week)

    if candidate_weeks:
        # En erken hafta öncelikli
        candidate_weeks.sort(key=lambda w: w.week_index)
        return candidate_weeks[0]

    # Hiçbir hafta kısıtları sağlamıyorsa, bu beceri bu plana dahil edilmez
    return None


def weekly_plan_to_table(weeks: List[WeekPlan]) -> List[dict]:
    """
    Helper: UI'da tablo/özet için kolay kullanılabilir bir sözlük listesi.
    """
    rows: List[dict] = []
    for week in weeks:
        for skill in week.skills:
            rows.append(
                {
                    "Hafta": week.week_index,
                    "Beceri": skill.display_name,
                    "Tahmini Saat": round(skill.estimated_hours, 1),
                    "Zorluk (1-5)": skill.difficulty,
                }
            )
    return rows

