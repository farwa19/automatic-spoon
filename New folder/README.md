# Smart Health — with a real database

This turns the site from a static HTML file into a small full-stack app:

- **Backend:** `app.py` — a Flask server that serves the site and exposes
  a JSON API for auth and analyses.
- **Database:** `smarthealth.db` — a real SQLite database file, created
  automatically the first time you run the app. Two tables:
  - `users` — id, name, email, **hashed** password, bio, created_at
  - `analyses` — id, user_id (linked to `users`), severity, care pathway,
    symptoms, precautions, conflicts, created_at
- **Frontend:** `templates/index.html` — your site, now talking to the
  backend via `fetch()` instead of the browser's localStorage.

## How it works

- Signing up creates a row in `users`. Passwords are hashed with
  Werkzeug's salted PBKDF2 (`generate_password_hash`) — the plain-text
  password is never stored, and isn't recoverable from the hash.
- Logging in checks the submitted password against that hash and starts
  a signed, HTTP-only session cookie — the browser only ever holds a
  cookie, not user data.
- Every time a logged-in user completes the symptom checker, the result
  (severity, care pathway, symptoms, precautions, any conflicts) is
  saved to the `analyses` table, tied to their `user_id`.
- Their profile page shows their past checks by querying `/api/analyses`.
- If someone uses the symptom checker while logged out, that run isn't
  saved — there's no user to attach it to.

## Run it locally

```bash
cd smarthealth-app
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser. The database file
(`smarthealth.db`) will be created next to `app.py` automatically.

## Inspecting the database

```bash
python3 -c "
import sqlite3
db = sqlite3.connect('smarthealth.db')
for row in db.execute('SELECT id, name, email, created_at FROM users'):
    print(row)
"
```

(Or open it with any SQLite browser, e.g. DB Browser for SQLite.)

## Notes on going further

- This uses Flask's built-in dev server (`app.run(debug=True)`) — fine
  for local use, but for a real deployment put it behind a proper WSGI
  server (gunicorn/uwsgi) and disable debug mode.
- `app.secret_key` is a placeholder — set a real secret via the
  `SMARTHEALTH_SECRET_KEY` environment variable before deploying anywhere
  public.
- SQLite is great for a single-server prototype like this. If you expect
  concurrent traffic at scale, migrating to Postgres is a straightforward
  next step (the queries here are simple enough to port directly).
- Nothing here should be treated as a substitute for professional medical
  advice — that's already noted on the site itself.
