# Secure Stacks — Templates

This directory contains reference Docker Compose configurations and guides for
building security-hardened application stacks.

## Available Templates

### Docker Compose Templates

| Template | Stack | Description |
|----------|-------|-------------|
| [docker-compose-t3-stack.yml](docker-compose-t3-stack.yml) | Next.js + tRPC + Prisma + PostgreSQL | Full T3 stack with comprehensive security hardening |
| [docker-compose-django.yml](docker-compose-django.yml) | Django + PostgreSQL + Redis + Nginx | Python web stack with Gunicorn and security best practices |
| [docker-compose-fastapi.yml](docker-compose-fastapi.yml) | FastAPI + PostgreSQL + Redis + Nginx | Async Python API stack with uvicorn and production hardening |

### Guides

| Guide | Description |
|-------|-------------|
| [lockfile-verification.md](lockfile-verification.md) | How to verify lockfile integrity for npm, pip, Go, and Cargo |

## Security Best Practices Applied

Every Docker Compose template in this directory follows these security defaults:

### Container Hardening

- **Non-root user** — Every container runs as a dedicated non-root user with
  specific UID/GID
- **Read-only filesystem** — `read_only: true` with `tmpfs` for writable paths
  (`/tmp`, `/var/run`, `/var/cache`)
- **No new privileges** — `security_opt: [no-new-privileges:true]`
- **Dropped capabilities** — `cap_drop: [ALL]`
- **Resource limits** — CPU and memory limits on every service
- **Health checks** — Liveness checks with appropriate intervals and retries

### Network Security

- **Internal networks** — Backend services communicate on an internal Docker
  network
- **Minimal port exposure** — Only the reverse proxy (nginx) is exposed to the
  host
- **Explicit network definitions** — No reliance on default bridge network

### Configuration Security

- **No hardcoded secrets** — All secrets via environment variables
- **Pinned image versions** — All images use specific version tags
- **Minimal base images** — Alpine-based images where available

## How to Use These Templates

1. Copy the template to your stack directory
2. Customize for your specific application
3. Add your application code
4. Create a `.env.example` with all required variables
5. Run `docker compose config` to validate
6. Submit a PR following the [contribution guide](../CONTRIBUTING.md)

## Generating Your Own Templates

Use these as starting points. Key things to remember:

- Always define a non-root `USER` in your Dockerfiles
- Add health checks for every service
- Use internal networks for backend communication
- Set resource limits appropriate for your workload
- Pin all image versions
- Document every environment variable

## Validation

After modifying a template, validate it:

```bash
# Check Docker Compose syntax
docker compose -f your-template.yml config

# Lint Dockerfiles
hadolint Dockerfile

# Scan for vulnerabilities
trivy image your-image:tag
```
