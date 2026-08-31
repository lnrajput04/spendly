# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" is a personal expense tracker built as a step-by-step Flask learning exercise. The app is
intentionally incomplete: routes and templates for auth (`/register`, `/login`) and the landing page
are implemented, but the database layer and most functional routes are stubs left for the learner to
fill in, referenced in code comments as numbered "Steps":

- `database/db.py` — currently just comments describing Step 1: implement `get_db()` (SQLite
  connection with `row_factory` and foreign keys enabled), `init_db()` (create tables with
  `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample data for dev).
- `/logout` (Step 3), `/profile` (Step 4), `/expenses/add` (Step 7), `/expenses/<id>/edit` (Step 8),
  `/expenses/<id>/delete` (Step 9) — each currently just returns a placeholder string in `app.py`.

When asked to "implement the next step" or similar, check `app.py` and `database/db.py` for the
step markers to figure out what's next, since there is no separate curriculum/instructions doc in
the repo.

## Commands

```bash
# activate the existing venv (Python 3.9)
source venv/bin/activate

# install deps
pip install -r requirements.txt

# run the dev server (http://localhost:5001)
python app.py

# run tests
pytest
```

There is no test suite yet (`pytest`/`pytest-flask` are in `requirements.txt` but no test files
exist). When adding tests, use `pytest-flask`'s `client` fixture against the Flask `app` in `app.py`.

There is no build step, linter, or frontend package manager configured — static assets in
`static/css` and `static/js` are served directly by Flask, no bundler.

## Architecture

- **`app.py`** — single-file Flask app; all routes are defined here directly (no blueprints).
  Routes render Jinja templates from `templates/` via `render_template`.
- **`database/db.py`** — intended to be the sole place for SQLite access (connection setup, schema
  creation, seeding). No ORM is used/expected — raw SQLite via `sqlite3`.
- **`templates/base.html`** — the shared layout (nav, footer, font imports) that every page extends
  via `{% extends "base.html" %}` with `title`/`content` blocks. New pages should follow this
  pattern rather than duplicating the `<head>`/nav/footer markup.
- **`static/css/style.css`** — shared/global styles (auth forms, nav, footer, etc.); **`static/css/landing.css`**
  is landing-page-specific and loaded only from `landing.html` via its own `head` block.
- Forms POST directly to routes matching their `action` (e.g. `register.html`'s form posts to
  `/register`); the corresponding `GET` handlers currently only render the form, so POST handling
  for these needs to be added to `app.py` when implementing auth.
