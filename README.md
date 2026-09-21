# Pikestia Learning Hub

Modern, secure, scalable, responsive Django platform for university learning.

## Philosophy
Simple now, scalable later.

## Quick start
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Architecture
- `pikestia/` project config + security middleware
- `apps/accounts/` custom user, auth, Google OAuth, theme persistence
- `apps/core/` public pages, search, cookie consent, theming
- `apps/subjects/` Subject/Category/Topic hierarchy
- `apps/learning/` LearningResource
- `apps/practice/` PracticeQuestion
- `apps/opportunities/` Opportunity
- `apps/bookmarks/` Bookmarks
- Modular, no god files

## Security built-in
ORM only, CSRF, CSP, HSTS, rate limiting, bleach sanitization, HttpOnly cookies, server-side authz

## Theming
Light / Dark / System stored server-side in User.display_mode
