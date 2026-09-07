# Spec: Login and Logout

## Overview
This feature lets an existing Spendly user sign back into their account, and lets a
signed-in user sign back out. `/login` already renders a form (`login.html`) but only
handles `GET`; this step adds `POST` handling that verifies credentials against the
`users` table and, on success, logs the user in the same way Step 2 (Registration)
does — via `session["user_id"]`. `/logout` is currently a placeholder string; this step
makes it clear the session and redirect to a public page. Because there was previously
no way to reach `/logout` from the UI (the nav always shows "Sign in" / "Get started"),
this step also updates the shared nav in `base.html` to reflect logged-in vs.
logged-out state.

## Depends on
- Step 1 — Database Setup (`get_db()`, `init_db()`, `users` table).
- Step 2 — Registration (`get_user_by_email()` in `database/db.py`, the
  `session["user_id"]` login pattern and `SECRET_KEY` config already added to `app.py`).

## Routes
- `GET /login` — renders the sign-in form — public (already implemented, unchanged)
- `POST /login` — verifies credentials, logs the user in, redirects — public
- `GET /logout` — clears the session, redirects — logged-in (safe to hit while logged
  out too; it just becomes a no-op redirect)

## Database changes
No database changes. `get_user_by_email()` (added in Step 2) is reused as-is to look up
the account; no new tables, columns, or constraints are required.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — add `value="{{ email or '' }}"` to the email input so a
    failed login doesn't force retyping the email (matching the pattern already used in
    `register.html`). Password is never repopulated.
  - `templates/base.html` — the nav (`.nav-links`) currently always shows "Sign in" /
    "Get started". Change it to check for a logged-in session: when logged in, show a
    link to `/profile` and a "Sign out" link to `/logout`; when logged out, show the
    existing "Sign in" / "Get started" links unchanged. This is the only way a user can
    discover `/logout` in the UI.

## Files to change
- `app.py` — implement `POST` handling on `/login` (credential verification with
  `werkzeug.security.check_password_hash`, session login, redirect) and implement
  `/logout` (clear the session, redirect).
- `database/db.py` — no changes expected; reuses the existing `get_user_by_email()`.
- `templates/login.html` — email value repopulation on error.
- `templates/base.html` — conditional nav based on `session`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — use `check_password_hash(user["password_hash"], password)`
  to verify, never compare hashes or plaintext directly
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though the form has HTML5 `required`/`type="email"` attributes
- Use one generic error message for both "no account with that email" and "wrong
  password" (e.g. "Invalid email or password.") — never reveal which part was wrong,
  so a login attempt can't be used to enumerate registered emails
- Re-render `login.html` with `error` set (HTTP 200) on any failure — don't redirect on
  error, so the user's email input isn't lost
- On success, store the user's id in `session["user_id"]` (matching Step 2's pattern
  exactly) then redirect — never render directly after a successful POST
- `/logout` must clear the session (`session.clear()` or `session.pop("user_id", None)`)
  and redirect — never just render a page while leaving the session intact
- Keep the nav change minimal: check `"user_id" in session`, don't introduce a new
  template context processor or helper unless directly reusing something that already
  exists

## Definition of done
- [ ] Visiting `/login` still renders the form on `GET`, with the nav showing
      "Sign in" / "Get started" (since no one is logged in yet)
- [ ] Submitting `/login` with a registered email and its correct password redirects
      (not renders) and sets `session["user_id"]` to that user's id
- [ ] Submitting `/login` with a registered email and the wrong password re-renders
      `login.html` with "Invalid email or password." and does not set the session
- [ ] Submitting `/login` with an email that has no account re-renders `login.html`
      with the same "Invalid email or password." message (not a different one)
- [ ] Submitting `/login` with a missing email or password re-renders `login.html`
      with an error and does not attempt a DB lookup
- [ ] After a successful login, the nav shows a link to `/profile` and a "Sign out"
      link instead of "Sign in" / "Get started"
- [ ] Visiting `/logout` while logged in clears `session["user_id"]`, redirects, and
      the nav reverts to showing "Sign in" / "Get started" on the next page load
- [ ] Visiting `/logout` while already logged out doesn't error — it just redirects
- [ ] No plaintext passwords ever appear in server logs during a login attempt
