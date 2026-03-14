"""
Öğrenme Yolculuğu — Flask app (Python only).
Run: flask --app app run
"""
from flask import Flask, render_template
import os

from data.modules_config import MODULES

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)


def _progress(modules):
    completed = sum(1 for m in modules if m.get("status") == "TAMAMLANDI")
    total = len(modules)
    percent = (completed / total * 100) if total else 0
    return {"completed": completed, "total": total, "percent": round(percent)}


def _total_xp(modules):
    return sum(
        m.get("xp_points", 0)
        for m in modules
        if m.get("status") == "TAMAMLANDI"
    )


def _enrich_modules(modules):
    out = []
    for m in modules:
        topics = m.get("topics") or []
        completed = sum(1 for t in topics if t.get("completed"))
        m_copy = dict(m)
        m_copy["completed_topics"] = completed
        m_copy["total_topics"] = len(topics)
        out.append(m_copy)
    return out


@app.route("/")
def index():
    modules = _enrich_modules(MODULES)
    progress = _progress(modules)
    total_xp = _total_xp(modules)
    next_target = next(
        (m for m in modules if m.get("status") in ("SIRADAKİ", "AKTİF")),
        None,
    )
    return render_template(
        "journey.html",
        modules=modules,
        progress=progress,
        total_xp=total_xp,
        next_target=next_target,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
