# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the app**
```
python app.py
```
Runs the Flask dev server at `http://127.0.0.1:5001` (debug mode, port 5001).

**Install dependencies**
```
pip install -r requirements.txt
```
Requirements: flask==3.1.3, werkzeug==3.1.6, pytest==8.3.5, pytest-flask==1.3.0.

**Run tests**
```
pytest
```
There is no dedicated test directory; place test files at repo root with `test_*.py` naming to be discovered by pytest. Flask test client is available via `app.test_client()`.

**Initialize/reset database**
```
python -c "from database.db import init_db, seed_db; init_db(); seed_db()"
```
Or run `python database/db.py` directly. The database file `database/spendly.db` is gitignored and created on first app startup.

## Architecture

**Entry point**: `app.py` — creates the Flask app, calls `init_db()` and `seed_db()` on startup, defines all routes, and runs on port 5001.

**Routes** (defined in `app.py`):
- `/` → `landing.html`
- `/register` → `register.html`
- `/login` → `login.html`
- `/terms` → `terms.html`
- `/privacy` → `privacy.html`
- Placeholder routes (return stub strings): `/logout`, `/profile`, `/expenses/add`, `/expenses/<int:id>/edit`, `/expenses/<int:id>/delete`

**Database** (`database/db.py`): SQLite at `database/spendly.db`. Tables: `users`, `categories`, `expenses`. `init_db()` creates tables; `seed_db()` inserts example data (idempotent via `INSERT OR IGNORE`). `get_db()` returns a connection with `row_factory = sqlite3.Row` and foreign keys enabled.

**Templates** (`templates/`): Jinja2 templates extending `base.html`. `base.html` provides the navbar (brand + sign in/register links), main content block, and footer (Spendly brand, copy line, Terms and Conditions / Privacy Policy links). Child templates fill `{% block content %}`.

**Static assets**: `static/css/style.css` (design tokens, navbar, hero, features, footer, modal, terms/legal pages), `static/js/main.js` (empty placeholder — student JS goes here).

**Inline JS**: The "See how it works" modal logic lives inline in `landing.html` (not in `main.js`). It opens a YouTube embed iframe, sets `src=""` on close to stop playback.

**Database lifecycle**: `init_db()` and `seed_db()` run at import time in `app.py`, so the DB is created/seeded whenever the app starts.

## Files gitignored

`venv/`, `spendly.db`, `expense_tracker.db`, `__pycache__/`, `*.pyc`, `*.pyo`, `.env`, `.DS_Store`, `.claude/plans/`.
