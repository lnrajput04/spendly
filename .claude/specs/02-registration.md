# Spec: Registration

## Overview
This feature implements account creation for Spendly. The `/register` route already
renders a form (`register.html`) but only handles `GET` requests. This step adds `POST`
handling so a visitor can submit the form, have their password hashed and stored via
`database/db.py`'s `get_db()`, and be logged in immediately via a Flask session. This
session is the mechanism that the not-yet-implemented `/logout` (Step 3) and `/profile`
(Step 4) routes will depend on.

## Depends on
- Step 1 — Database Setup (`get_db()`, `init_db()`, `users` table) must be complete.

## Routes
- `GET /register` — renders the registration form — public (already implemented, unchanged)
- `POST /register` — validates input, creates the user, logs them in, redirects — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`,
`created_at`) already has every column needed; no new tables, columns, or constraints
are required.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — no structural changes expected; it already
  posts to `/register` and renders `{{ error }}` when present. Only touch it if a
  validation message needs a matching field to render against.

## Files to change
- `app.py` — add a `SECRET_KEY` config (required for sessions), import `request`,
  `redirect`, `url_for`, and `session` from Flask, and implement `POST` handling on
  `/register`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash` / `check_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though the form has HTML5 `required`/`type="email"`
  attributes (never trust client-side-only validation)
- Re-render `register.html` with `error` set (HTTP 200) on validation failure —
  don't redirect on error, so the user's input context isn't lost
- Enforce a minimum password length of 8 characters, matching the form's placeholder
- Check for a duplicate email (case-insensitive) before inserting and show a clear
  error instead of letting the `UNIQUE` constraint raise an unhandled exception
- On success, store the new user's id in `session` (e.g. `session["user_id"]`) so the
  user is logged in immediately, then redirect (never render directly after a POST)

## Definition of done
- [ ] Visiting `/register` still renders the form on `GET`
- [ ] Submitting the form with a name, valid email, and an 8+ character password
      creates a row in the `users` table with a hashed (not plaintext) password
- [ ] After a successful submission, the browser is redirected (not just rendered)
      and `session["user_id"]` is set to the new user's id
- [ ] Submitting with an email that already exists in `users` re-renders
      `register.html` with an error message and does not create a duplicate row
- [ ] Submitting with a password shorter than 8 characters re-renders
      `register.html` with an error message and does not create a user
- [ ] Submitting with a missing name, email, or password re-renders `register.html`
      with an error message and does not create a user
- [ ] No plaintext passwords ever appear in the database or in server logs
