"""
Module-based progress: state scores, category percentage, and derived skill levels.
Replaces slider-based self-assessment with explicit module completion states.
"""
from __future__ import annotations

from typing import Dict, List, Any

# Module state to numeric score (0.0 - 1.0)
STATE_SCORES: Dict[str, float] = {
    "not_started": 0.0,
    "in_progress": 0.4,
    "completed": 0.75,
    "applied": 1.0,
}

MODULE_STATES = list(STATE_SCORES.keys())


def get_module_state(module_id: str, session_state: Any) -> str:
    """Return current state for a module; default not_started."""
    key = f"module_{module_id}"
    return session_state.get(key, "not_started")


def get_state_score(state: str) -> float:
    """Map state name to numeric score."""
    return STATE_SCORES.get(state, 0.0)


def get_category_progress(
    category: str,
    modules: List[Any],
    skills: Dict[str, Any],
    session_state: Any,
) -> float:
    """
    Category progress percentage = (sum of module scores / total module count) * 100.
    Only modules whose skill belongs to this category are counted.
    """
    skill_ids_in_category = {sid for sid, s in skills.items() if getattr(s, "category", "") == category}
    category_modules = [m for m in modules if m.skill_id in skill_ids_in_category]
    if not category_modules:
        return 0.0
    total = 0.0
    for m in category_modules:
        state = get_module_state(m.id, session_state)
        total += get_state_score(state)
    return (total / len(category_modules)) * 100.0


def module_progress_to_skill_levels(
    modules: List[Any],
    skill_ids: List[str],
    session_state: Any,
) -> Dict[str, int]:
    """
    Derive per-skill level (0-5) from module states.
    For each skill: average of module state scores (0-1) * 5, rounded, clamped to 0-5.
    """
    skill_levels: Dict[str, int] = {}
    for skill_id in skill_ids:
        skill_modules = [m for m in modules if m.skill_id == skill_id]
        if not skill_modules:
            skill_levels[skill_id] = 0
            continue
        total_score = 0.0
        for m in skill_modules:
            state = get_module_state(m.id, session_state)
            total_score += get_state_score(state)
        avg = total_score / len(skill_modules)
        level = round(avg * 5)
        skill_levels[skill_id] = max(0, min(5, level))
    return skill_levels


def get_overall_readiness_percentage(
    modules: List[Any],
    skill_ids: List[str],
    session_state: Any,
) -> float:
    """Overall readiness = average of all relevant module scores * 100."""
    relevant = [m for m in modules if m.skill_id in set(skill_ids)]
    if not relevant:
        return 0.0
    total = sum(get_state_score(get_module_state(m.id, session_state)) for m in relevant)
    return (total / len(relevant)) * 100.0
