from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple

import networkx as nx

from .data_loader import Skill, Role


@dataclass
class SkillGap:
    skill_id: str
    display_name: str
    category: str
    difficulty: int
    quick_win: bool
    current_level: int
    required_level: int
    gap: int
    role_weight: float
    priority_score: float
    missing_prerequisites: List[str]


@dataclass
class GapAnalysisResult:
    role: Role
    skill_gaps: List[SkillGap]
    dependency_graph: nx.DiGraph


def _compute_unlock_scores(skills: Dict[str, Skill]) -> Dict[str, int]:
    """Return a simple count of how many skills depend on each skill."""
    counts: Dict[str, int] = {sid: 0 for sid in skills.keys()}
    for skill in skills.values():
        for prereq in skill.prerequisites:
            if prereq in counts:
                counts[prereq] += 1
    return counts


def analyze_gaps(
    role: Role,
    skills: Dict[str, Skill],
    current_levels: Dict[str, int],
) -> GapAnalysisResult:
    """
    Core rule-based gap analysis.

    Steps:
    1. Compare user levels vs role requirements.
    2. Build a dependency graph between skills.
    3. Compute transparent priority scores.
    4. Respect prerequisite ordering.
    """
    unlock_counts = _compute_unlock_scores(skills)

    # 1) Compute raw gaps for skills that are part of the role
    gaps: Dict[str, SkillGap] = {}
    for skill_id, req in role.skills.items():
        skill = skills[skill_id]
        current = int(current_levels.get(skill_id, 0))
        required = int(req.required_level)
        raw_gap = max(0, required - current)
        if raw_gap <= 0:
            continue  # yeterince iyi durumda

        # Role weight: önem katsayısı
        role_weight = float(req.weight)

        # Quick win bonusu: daha kolay ve motivasyon arttırıcı başlıklar
        quick_win_bonus = 1.0 if skill.quick_win else 0.0

        # Unlock bonusu: pek çok becerinin önkoşulu olan başlıklara ek puan
        unlock_bonus = 0.4 * unlock_counts.get(skill_id, 0)

        # Bu seviyede overload_penalty sabit tutuluyor;
        # asıl yük dengelemesi haftalık planlayıcıda yapılacak.
        overload_penalty = 0.0

        priority = (raw_gap * role_weight) + unlock_bonus + quick_win_bonus - overload_penalty

        # Eksik önkoşul listesi (sadece seviyesinin düşük olduğu prerequisite'ler)
        missing_prereqs: List[str] = []
        for prereq_id in skill.prerequisites:
            prereq_current = int(current_levels.get(prereq_id, 0))
            if prereq_current < 1:
                missing_prereqs.append(prereq_id)

        gaps[skill_id] = SkillGap(
            skill_id=skill_id,
            display_name=skill.display_name,
            category=skill.category,
            difficulty=skill.difficulty,
            quick_win=skill.quick_win,
            current_level=current,
            required_level=required,
            gap=raw_gap,
            role_weight=role_weight,
            priority_score=priority,
            missing_prerequisites=missing_prereqs,
        )

    # 2) Build dependency graph only for missing skills
    g = nx.DiGraph()
    for sid in gaps.keys():
        g.add_node(sid)

    for sid, gap in gaps.items():
        skill = skills[sid]
        for prereq in skill.prerequisites:
            if prereq in gaps:
                # Önkoşul -> beceri
                g.add_edge(prereq, sid)

    # 3) Topological-like ordering with priority awareness
    ordered_ids = _topological_with_priority(g, gaps)

    # 4) Final list in order
    ordered_gaps: List[SkillGap] = [gaps[sid] for sid in ordered_ids]

    return GapAnalysisResult(role=role, skill_gaps=ordered_gaps, dependency_graph=g)


def _topological_with_priority(graph: nx.DiGraph, gaps: Dict[str, SkillGap]) -> List[str]:
    """
    Custom topological sort:
    - respects dependency directions
    - among available nodes, picks higher priority first
    - falls back gracefully if graph is not a DAG
    """
    if len(graph.nodes) == 0:
        return []

    try:
        # Basit durum: saf DAG ise, öncelik skoruna göre hafifçe yeniden sıralayalım.
        topo = list(nx.topological_sort(graph))
        # Stable sort by priority descending
        topo.sort(key=lambda sid: gaps[sid].priority_score, reverse=True)
        return topo
    except nx.NetworkXUnfeasible:
        # Çevrim varsa, sadece öncelik skoruna göre sıralayalım.
        return sorted(graph.nodes, key=lambda sid: gaps[sid].priority_score, reverse=True)


def gaps_to_table(gap_result: GapAnalysisResult, skills: Dict[str, Skill]) -> List[Dict[str, Any]]:
    """
    Convenience helper for UI: convert gap result to a list of dicts
    that can be turned into a pandas DataFrame.
    """
    rows: List[Dict[str, Any]] = []
    for gap in gap_result.skill_gaps:
        if gap.missing_prerequisites:
            missing_display_names: List[str] = []
            for sid in gap.missing_prerequisites:
                skill = skills.get(sid)
                missing_display_names.append(skill.display_name if skill else sid)
            missing_prereq_text = ", ".join(missing_display_names)
        else:
            missing_prereq_text = "-"

        rows.append(
            {
                "beceri_id": gap.skill_id,
                "Beceri": gap.display_name,
                "Kategori": gap.category,
                "Zorluk (1-5)": gap.difficulty,
                "Hızlı Kazanım": "Evet" if gap.quick_win else "Hayır",
                "Mevcut Seviye": gap.current_level,
                "Hedef Seviye": gap.required_level,
                "Boşluk": gap.gap,
                "Rol Ağırlığı": round(gap.role_weight, 2),
                "Öncelik Skoru": round(gap.priority_score, 2),
                "Eksik Önkoşullar": missing_prereq_text,
            }
        )
    return rows

