# Spec: Profile Page Design

## Overview
This feature implements `/profile`, currently a placeholder string in `app.py`
("Profile page — coming in Step 4"). Since the roadmap has no separate "dashboard"
route and Steps 7–9 (add/edit/delete expense) already have stub routes with nothing to
view them against, `/profile` becomes the logged-in user's home page: it shows their
account details (name, email, member since) and a read-only list of their own expenses
with a running total. Editing/deleting expenses stays out of scope (Steps 8/9); this
step is about giving a logged-in user somewhere to land and see their data.

## Depends on
- Step 1 — Database Setup (`get_db()`, `init_db()`, `users`/`expenses` tables).
- Step 2 — Registration (`session["user_id"]` login pattern).
- Step 3 — Login and Logout (`.claude/specs/03-login-and-logout.md`) — `/profile`
  requires a working sign-in flow to be reachable normally, and the shared nav's
  logged-in state (a "Profile" link) depends on that step's change to `base.html`.
  **Note: Step 3 is implemented on `feature/login-logout` but not yet merged into
  `main` as of this spec** — this branch was created from `main` per the standard
  workflow, so it does not yet include Step 3's `app.py`/`base.html` changes. Merge or
  rebase onto Step 3 before/while implementing this step, otherwise there's no UI path
  to reach `/profile` and the nav won't reflect login state (registering still sets a
  session directly, so `/profile` remains reachable and testable in the meantime).

## Routes
- `GET /profile` — shows the current user's account info and their expenses — logged-in
  only. If no `session["user_id"]`, redirect to `/login` (no error message needed —
  simply not being logged in isn't a validation failure).

## Database changes
No schema changes — the `users` and `expenses` tables already have every column
needed. Add two read-only helper functions to `database/db.py`, following the existing
`get_user_by_email()` pattern (connect via `get_db()`, query, close, return):
- `get_user_by_id(user_id)` — `SELECT * FROM users WHERE id = ?`, `.fetchone()`. Needed
  because the session only stores `user_id`; nothing currently fetches a user by id.
- `get_expenses_by_user(user_id)` — `SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC`,
  `.fetchall()`. Returns only that user's own expenses, never another user's.

## Templates
- **Create:** `templates/profile.html` — extends `base.html`. Shows:
  - An account card: name, email, and member-since date (formatted from `created_at`).
  - The user's expenses as a list (description, category, amount, date), or an empty
    state message ("No expenses yet.") if they have none.
  - A total spent figure (sum of the listed amounts).
- **Modify:** none required beyond what Step 3 already adds to `base.html` (the
  logged-in nav showing a link to `/profile`).

## Files to change
- `app.py` — implement `/profile`: check `session["user_id"]`, redirect to `/login` if
  absent; otherwise fetch the user via `get_user_by_id`, fetch their expenses via
  `get_expenses_by_user`, compute the total, and render `profile.html`.
- `database/db.py` — add `get_user_by_id()` and `get_expenses_by_user()`.
- `static/css/style.css` — add styling for the new profile card / expense list, using
  the existing CSS variables (no new hex values).

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (not relevant to new code here, but no change to
  existing hashing)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `/profile` must check `"user_id" in session` before doing anything else and redirect
  unauthenticated visitors to `/login` — never leak another user's data by trusting a
  client-supplied id; the user is always identified from `session`, never from a query
  parameter
- `get_expenses_by_user()` must filter by `user_id` in SQL (`WHERE user_id = ?`), not by
  fetching all expenses and filtering in Python
- Format currency/amounts and dates for display without introducing a new templating
  dependency (plain Jinja filters/Python formatting is sufficient)

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Registering or logging in as "Nitish Kumar" (`nitish@example.com`) and visiting
      `/profile` shows his name, email, member-since date, and exactly his 4 seeded
      expenses (Groceries, Electricity bill, Movie tickets, Bus pass) with a total of
      161.50
- [ ] Logging in as "Asha Patel" (`asha@example.com`, no seeded expenses) and visiting
      `/profile` shows her account info and the empty-state message, not Nitish's data
- [ ] The page extends `base.html` and renders correctly in the shared layout (nav,
      footer)
- [ ] No new hardcoded hex colors were introduced in `style.css`
- [ ] No plaintext passwords or other sensitive data appear anywhere on the rendered
      page
