from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class DataLoadError(Exception):
    """Raised when JSON data cannot be loaded or validated."""


@dataclass
class Skill:
    id: str
    display_name: str
    category: str
    difficulty: int
    quick_win: bool
    prerequisites: List[str]
    mini_tasks: List[str]


@dataclass
class RoleSkillRequirement:
    required_level: int  # 1–5
    weight: float        # importance weight for role


@dataclass
class Role:
    id: str
    display_name: str
    description: str
    skills: Dict[str, RoleSkillRequirement]


def load_json(path: Path) -> Any:
    """Safely load JSON file and return parsed object."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise DataLoadError(f"JSON dosyası bulunamadı: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataLoadError(f"JSON format hatası: {path}") from exc


def load_skills() -> Dict[str, Skill]:
    """Load skills.json into a dict keyed by skill id."""
    raw = load_json(DATA_DIR / "skills.json")
    skills: Dict[str, Skill] = {}
    for item in raw:
        skill = Skill(
            id=item["id"],
            display_name=item["display_name"],
            category=item["category"],
            difficulty=int(item["difficulty"]),
            quick_win=bool(item["quick_win"]),
            prerequisites=list(item.get("prerequisites", [])),
            mini_tasks=list(item.get("mini_tasks", [])),
        )
        skills[skill.id] = skill
    # basic internal consistency check for prerequisites
    missing_prereq = []
    for skill in skills.values():
        for prereq in skill.prerequisites:
            if prereq not in skills:
                missing_prereq.append((skill.id, prereq))
    if missing_prereq:
        detail = ", ".join(f"{sid}->{pid}" for sid, pid in missing_prereq)
        raise DataLoadError(f"Tanımsız önkoşul beceri referansları: {detail}")
    return skills


def load_roles(skills: Dict[str, Skill]) -> Dict[str, Role]:
    """Load roles.json and validate that all referenced skills exist."""
    raw = load_json(DATA_DIR / "roles.json")
    roles: Dict[str, Role] = {}
    for item in raw:
        role_skills: Dict[str, RoleSkillRequirement] = {}
        for skill_id, cfg in item["skills"].items():
            if skill_id not in skills:
                raise DataLoadError(
                    f"Rol '{item['id']}' tanımsız beceriye referans veriyor: {skill_id}"
                )
            role_skills[skill_id] = RoleSkillRequirement(
                required_level=int(cfg["required_level"]),
                weight=float(cfg["weight"]),
            )
        role = Role(
            id=item["id"],
            display_name=item["display_name"],
            description=item.get("description", ""),
            skills=role_skills,
        )
        roles[role.id] = role
    return roles


def load_all() -> Dict[str, Any]:
    """Convenience loader used by the app."""
    skills = load_skills()
    roles = load_roles(skills)
    return {"skills": skills, "roles": roles}

