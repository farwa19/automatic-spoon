"""
Smart Health — backend
Serves the site and stores users + their symptom-checker analyses in a
real SQLite database (smarthealth.db, created automatically on first run).

Run locally:
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000

Passwords are hashed server-side with werkzeug's PBKDF2-SHA256 (salted) —
plain-text passwords are never stored. Auth uses a signed, HTTP-only
session cookie; no user data is kept in the browser beyond that cookie.
"""
import os
import re
import sqlite3
from datetime import datetime, timezone

from flask import Flask, g, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smarthealth.db")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)
# In production, set this via an environment variable instead of hardcoding it.
app.secret_key = os.environ.get("SMARTHEALTH_SECRET_KEY", "dev-secret-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


# ── Database ────────────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            bio TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            severity TEXT NOT NULL,
            care_pathway TEXT NOT NULL,
            symptoms TEXT NOT NULL,      -- JSON array
            precautions TEXT NOT NULL,   -- JSON array
            conflicts TEXT NOT NULL,     -- JSON array
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """
    )
    db.commit()
    db.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def user_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "bio": row["bio"],
        "created_at": row["created_at"],
    }


def current_user_row():
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def require_login():
    row = current_user_row()
    if row is None:
        return None
    return row


# ── Page ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Auth API ────────────────────────────────────────────────────────────────
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"error": "Please enter a valid email address."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        return jsonify({"error": "That email is already registered. Try logging in instead."}), 409

    password_hash = generate_password_hash(password)
    created_at = now_iso()
    cur = db.execute(
        "INSERT INTO users (name, email, password_hash, bio, created_at) VALUES (?, ?, ?, '', ?)",
        (name, email, password_hash, created_at),
    )
    db.commit()
    user_row = db.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()

    session.clear()
    session["user_id"] = user_row["id"]
    return jsonify({"user": user_to_dict(user_row)}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    db = get_db()
    user_row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user_row is None or not check_password_hash(user_row["password_hash"], password):
        return jsonify({"error": "Incorrect email or password."}), 401

    session.clear()
    session["user_id"] = user_row["id"]
    return jsonify({"user": user_to_dict(user_row)})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me", methods=["GET"])
def me():
    row = require_login()
    if row is None:
        return jsonify({"error": "Not logged in."}), 401
    return jsonify({"user": user_to_dict(row)})


@app.route("/api/profile", methods=["PUT"])
def update_profile():
    row = require_login()
    if row is None:
        return jsonify({"error": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    bio = (data.get("bio") or "").strip()

    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    db = get_db()
    conflict = db.execute(
        "SELECT id FROM users WHERE email = ? AND id != ?", (email, row["id"])
    ).fetchone()
    if conflict:
        return jsonify({"error": "That email is already in use by another account."}), 409

    db.execute(
        "UPDATE users SET name = ?, email = ?, bio = ? WHERE id = ?",
        (name, email, bio, row["id"]),
    )
    db.commit()
    updated = db.execute("SELECT * FROM users WHERE id = ?", (row["id"],)).fetchone()
    return jsonify({"user": user_to_dict(updated)})


# ── Analyses API ────────────────────────────────────────────────────────────
@app.route("/api/analyses", methods=["POST"])
def save_analysis():
    row = require_login()
    if row is None:
        return jsonify({"error": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    severity = data.get("severity") or "mild"
    care_pathway = data.get("carePathway") or "home_care"
    symptoms = data.get("symptoms") or []
    precautions = data.get("precautions") or []
    conflicts = data.get("conflicts") or []

    import json

    db = get_db()
    db.execute(
        """INSERT INTO analyses (user_id, severity, care_pathway, symptoms, precautions, conflicts, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            row["id"],
            severity,
            care_pathway,
            json.dumps(symptoms),
            json.dumps(precautions),
            json.dumps(conflicts),
            now_iso(),
        ),
    )
    db.commit()
    return jsonify({"ok": True}), 201


@app.route("/api/analyses", methods=["GET"])
def list_analyses():
    row = require_login()
    if row is None:
        return jsonify({"error": "Not logged in."}), 401

    import json

    db = get_db()
    rows = db.execute(
        "SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC LIMIT 50",
        (row["id"],),
    ).fetchall()
    analyses = [
        {
            "id": r["id"],
            "severity": r["severity"],
            "care_pathway": r["care_pathway"],
            "symptoms": json.loads(r["symptoms"]),
            "precautions": json.loads(r["precautions"]),
            "conflicts": json.loads(r["conflicts"]),
            "created_at": r["created_at"],
        }
        for r in rows
    ]
    return jsonify({"analyses": analyses})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
else:
    # Also make sure the DB exists when run under a WSGI server.
    init_db()
