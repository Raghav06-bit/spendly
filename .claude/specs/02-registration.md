# Spec: Registration

## Overview
Implement user registration for Spendly so new users can create an account with a full name, email address, and password. This feature processes the registration form submit, validates input (checking for missing fields and existing email addresses), hashes the password securely using Werkzeug, inserts the new user into the database, logs the user in via Flask session, and redirects to the landing page with a confirmation flash message.

## Depends on
- Step 01: Database Setup (`database/db.py`, `users` table)

## Routes
- `GET /register` — Render the registration form (`templates/register.html`) — Public
- `POST /register` — Process registration form, validate input, save user, log in, and redirect — Public

## Database changes
No database schema changes needed. Uses existing `users` table:
- `name` (TEXT, NOT NULL)
- `email` (TEXT, UNIQUE, NOT NULL)
- `password_hash` (TEXT, NOT NULL)
- `created_at` (DEFAULT datetime('now'))

## Templates
- **Create:** None
- **Modify:**
  - `templates/register.html` — Ensure form method is `POST`, action is `/register`, fields have correct `name` attributes (`name`, `email`, `password`), display error messages if present, and retain entered name/email values on validation failure.
  - `templates/base.html` — Add flash message banner support if not already present.

## Files to change
- `app.py` — Add `POST` handler for `/register`, input validation, database query, session management, and error/flash messaging.
- `templates/register.html` — Wire up form fields and error display.

## Files to create
- `test_register.py` — Unit tests for registration functionality.

## New dependencies
No new pip packages needed. Uses standard Flask session, `database.db.get_db()`, and `werkzeug.security.generate_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs — use direct SQLite via `database.db.get_db()`
- Parameterised queries only — e.g. `cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, password_hash))`
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Set `session['user_id'] = user_id` and `session['user_name'] = name` upon successful registration
- Form validation:
  - Trim whitespace from name and email
  - Reject empty fields with user-friendly error message
  - Validate email format / case-insensitively check for existing email
  - Reject password if fewer than 8 characters
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] `GET /register` displays the registration form correctly
- [ ] Submitting valid data creates a new row in the `users` table with a hashed password
- [ ] Email uniqueness is enforced with a user-friendly error message ("Email address is already registered")
- [ ] Empty/missing form fields show appropriate error messages without crashing
- [ ] Password length of less than 8 characters displays a validation error
- [ ] Successful registration logs the user in by setting session variables (`user_id`, `user_name`)
- [ ] Successful registration redirects to the home/landing page with a success flash message
- [ ] `pytest test_register.py` passes all tests
---