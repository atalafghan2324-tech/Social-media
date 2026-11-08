# Social Network FastAPI Backend (MVP)

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Set `JWT_SECRET` to a long random secret before deploying. Then run:

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to test register, login, profiles, posts, likes, comments, and follows. Use the Authorize button with the access token returned by `/auth/login`.

## Scope

This is a learning MVP, not production ready. Photo uploads, refresh tokens, email verification, password reset, rate limiting, moderation, and migrations are not implemented yet. The database is stored in `social.db` in the working directory. Keep it private and do not commit it to Git.

All source files are in one directory. Run commands from this directory.
