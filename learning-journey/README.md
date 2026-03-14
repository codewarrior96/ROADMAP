# Öğrenme Yolculuğu — Flask (Python only)

Dynamic learning roadmap UI: **Flask** backend, **Jinja2** templates, **plain CSS**. No JavaScript, no Node, no npm.

## Structure

- `app.py` — Flask app, single route `/`
- `templates/` — `base.html`, `journey.html`
- `static/css/journey.css` — all styles (dark theme `#0f1117`)
- `data/modules_config.py` — data-driven modules; edit here to change content

## Run

```bash
cd learning-journey
pip install -r requirements.txt
flask --app app run
# or: python app.py
````

Open http://127.0.0.1:5001/

## Features

- Overall progress bar (X/Y tamamlandı — %Z) and XP
- Status badges: TAMAMLANDI, AKTİF (pulse), SIRADAKİ, KİLİTLİ
- Expandable module cards (click header)
- Per-module topics list, sub-progress, resources, tips, CTA (Başla / Mini Quiz)
- Gamification row: level, streak, next target
- Responsive, accessible (ARIA, semantic HTML)
