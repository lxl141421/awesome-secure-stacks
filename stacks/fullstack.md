# Full-Stack Combos — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly
> Each combo includes a complete version matrix and lockfile template

---

## 1. T3 Stack ⭐ TypeScript Full-Stack Recommendation

**Security Grade: A**

### Version Matrix

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Next.js | 14.2.15 | MIT | 0 (patched) |
|| tRPC | 11.1.3 | MIT | 0 |
|| Prisma | 6.8.2 | Apache-2.0 | 0 |
|| Auth.js | 5.0.0-beta.25 | ISC | 0 |
| Tailwind CSS | 3.4.14 | MIT | 0 |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |
| Zod | 3.23.8 | MIT | 0 |

### Lockfile Template

```json
{
  "name": "t3-app",
  "packageManager": "pnpm@9.12.3",
  "dependencies": {
    "next": "14.2.15",
    "@trpc/server": "11.1.3",
    "@trpc/client": "11.1.3",
    "@trpc/next": "11.1.3",
    "@trpc/react-query": "11.1.3",
    "@prisma/client": "6.8.2",
    "next-auth": "5.0.0-beta.25",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "zod": "3.23.8",
    "superjson": "2.2.1"
  },
  "devDependencies": {
    "prisma": "6.8.2",
    "typescript": "5.4.5",
    "tailwindcss": "3.4.14",
    "postcss": "8.4.47",
    "autoprefixer": "10.4.20",
    "@types/react": "18.3.12"
  }
}
```

### Security Features
- **tRPC:** End-to-end type safety eliminates runtime type mismatches
- **Prisma:** Parameterized queries prevent SQL injection by design
- **Zod:** Runtime input validation on all API boundaries
- **NextAuth:** CSRF protection, secure session management built-in
- **Pnpm:** `pnpm-lock.yaml` with integrity checksums

### Security Checklist
- [ ] Enable `sameSite: "lax"` and `secure: true` in NextAuth config
- [ ] Use `Prisma.$transaction` for multi-step operations
- [ ] Validate all tRPC inputs with Zod schemas
- [ ] Enable CSP headers in `next.config.js`
- [ ] Use `pnpm ci` (not `pnpm install`) in CI

---

## 2. Django Full-Stack

**Security Grade: A+**

### Version Matrix

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
|| Django | 5.2 LTS | BSD-3 | 0 critical |
|| Python | 3.13.3 | PSF | 0 critical |
| HTMX | 2.0.3 | BSD-0 | 0 |
| Alpine.js | 3.14.3 | MIT | 0 |
| django-allauth | 65.1.0 | MIT | 0 |
| django-htmx | 1.19.0 | MIT | 0 |
| gunicorn | 22.0.0 | MIT | 0 |
| WhiteNoise | 6.7.1 | MIT | 0 |
| psycopg | 3.2.3 | LGPL-3.0 | 0 |

### Lockfile Template

```toml
# pyproject.toml (uv or poetry)
[project]
name = "django-app"
requires-python = ">=3.12"
dependencies = [
    "django==5.2",
    "django-allauth==65.1.0",
    "django-htmx==1.19.0",
    "gunicorn==22.0.0",
    "whitenoise==6.7.1",
    "psycopg[binary]==3.2.3",
    "dj-database-url==2.2.0",
]

[tool.uv]
dev-dependencies = [
    "pytest-django==4.9.0",
    "ruff==0.7.4",
    "mypy==1.12.1",
    "django-stubs==5.1.0",
]
```

```bash
# Generate lockfile with hashes
uv pip compile pyproject.toml --hash --universal -o requirements-lock.txt
```

### Security Features
- Django's built-in CSRF, XSS, SQL injection, clickjacking protection
- ORM parameterized queries by default
- HTMX: Server-rendered HTML eliminates XSS from client-side templates
- `SECURE_*` settings enforce HTTPS, HSTS, secure cookies

### Critical Django Settings
```python
# settings/production.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

---

## 3. Ruby on Rails

**Security Grade: A**

### Version Matrix

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
|| Ruby | 3.4.2 | Ruby | 0 critical |
|| Rails | 8.0.2 | MIT | 0 |
|| PostgreSQL | 16.4 | PostgreSQL | 0 |
|| Puma | 6.6.0 | BSD-3 | 0 |
| Devise | 4.9.4 | MIT | 0 |
| Turbo | 2.0.11 | MIT | 0 |
| Stimulus | 3.2.2 | MIT | 0 |

### Lockfile Template

```ruby
# Gemfile
source "https://rubygems.org"

gem "rails", "~> 8.0.2"
gem "pg", "~> 1.5.8"
gem "puma", "~> 6.6.0"
gem "devise", "~> 4.9.4"
gem "turbo-rails", "~> 2.0.11"
gem "stimulus-rails", "~> 3.2.2"
gem "jbuilder", "~> 2.13.0"
gem "rack-cors", "~> 2.0.2"
gem "bundler-audit", "~> 0.9.2", require: false
```

```bash
# Security auditing
bundle audit check --update
bundle exec brakeman --no-pager
```

### Security Features
- Rails built-in CSRF, XSS, SQL injection protection
- Strong Parameters for mass assignment prevention
- Devise: secure authentication with bcrypt
- Brakeman: static analysis security scanner
- `bundler-audit`: dependency vulnerability scanner

### Known CVEs (patched)
- None in current version

---

## 4. Laravel

**Security Grade: A**

### Version Matrix

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
|| PHP | 8.4.6 | PHP-3.01 | 0 critical |
|| Laravel | 12.7.2 | MIT | 0 |
| Livewire | 3.5.12 | MIT | 0 |
| Pest | 3.5.1 | MIT | 0 |
| Laravel Sanctum | 4.0.2 | MIT | 0 |
| Tailwind CSS | 3.4.14 | MIT | 0 |

### Lockfile Template

```json
{
  "require": {
    "php": ">=8.3",
    "laravel/framework": "12.7.2",
    "livewire/livewire": "3.5.12",
    "laravel/sanctum": "4.0.2",
    "laravel/pint": "1.18.1"
  },
  "require-dev": {
    "pestphp/pest": "3.5.1",
    "pestphp/pest-plugin-laravel": "3.1.0",
    "laravel/pail": "1.1.1"
  }
}
```

```bash
# Security auditing
composer audit
./vendor/bin/pint --test  # Code style
php artisan tinker         # Verify app boots
```

### Security Features
- Eloquent ORM: parameterized queries by default
- Blade templating: auto HTML escaping (XSS prevention)
- Sanctum: API token authentication + SPA cookie auth
- Livewire: server-side rendering with morphing (limited XSS surface)
- CSRF protection on all forms (Blade `@csrf`)
- Rate limiting via `ThrottleRequests` middleware

### Security Configuration
```php
// config/session.php
'secure' => true,
'http_only' => true,
'same_site' => 'lax',
'encrypt' => true,

// config/cors.php — restrict origins
'allowed_origins' => ['https://app.example.com'],
'supports_credentials' => true,
```

---

## Full-Stack Security Comparison

| Feature | T3 Stack | Django | Rails | Laravel |
|---------|----------|--------|-------|---------|
| Language | TypeScript | Python | Ruby | PHP |
| Auth Built-in | NextAuth | django-allauth | Devise | Sanctum |
| ORM/DB | Prisma | Django ORM | ActiveRecord | Eloquent |
| SQL Injection Protection | ✅ | ✅ | ✅ | ✅ |
| CSRF Protection | ✅ | ✅ | ✅ | ✅ |
| XSS Protection | Manual | Auto-escape | Auto-escape | Auto-escape |
| Type Safety | Full (E2E) | Optional | ❌ | Partial |
| Static Analysis | ESLint + tsc | mypy + ruff | Brakeman | PHPStan + Pint |
| Dependency Audit | pnpm audit | pip-audit | bundler-audit | composer audit |
| **Security Grade** | **A** | **A+** | **A** | **A** |

---

## Recommended Deployment Stack (Per Combo)

| Combo | App Server | Database | Cache | Reverse Proxy |
|-------|-----------|----------|-------|---------------|
| T3 Stack | Next.js standalone | PostgreSQL 16.4 | Redis 7.4.1 | Cloudflare / Nginx |
| Django | Gunicorn + Uvicorn | PostgreSQL 16.4 | Redis 7.4.1 | Nginx + WhiteNoise |
| Rails | Puma 6.4.3 | PostgreSQL 16.4 | Redis 7.4.1 | Nginx |
| Laravel | Octane (Swoole) | PostgreSQL 16.4 | Redis 7.4.1 | Nginx |
