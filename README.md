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


## Local configuration

Copy \`.env.example\` to \`.env\` and replace \`SECRET_KEY\` with a long random value before running the application. Keep \`DEBUG=True\` only for local development. Production must set \`DEBUG=False\`, provide a private \`SECRET_KEY\`, configure \`ALLOWED_HOSTS\`, and serve the site over HTTPS. \`SECURE_SSL_REDIRECT\` is configurable because reverse-proxy deployments must forward HTTPS information correctly.

The default timezone is \`Africa/Kampala\`; set \`TIME_ZONE\` in \`.env\` when deploying for a different region.

## Publishing and verification

Publisher-created learning resources and news articles are assigned to the submitting publisher and enter **In Review**. Publishers can see and edit their own submissions but cannot publish, feature, or delete them. An administrator approves and publishes the content.

New opportunities begin as drafts. Only opportunities marked both **Active** and **Verified** are displayed in public lists, homepage discovery, and global search.
