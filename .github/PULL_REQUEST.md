## Description

<!-- Provide a brief description of your changes. -->

## Type of Change

<!-- Check the relevant option(s). -->

- [ ] **New stack** — Adding a new security-hardened stack template
- [ ] **Stack update** — Updating dependencies or configuration for existing stack
- [ ] **Security fix** — Patching a vulnerability in a stack
- [ ] **Documentation** — Improving or correcting documentation
- [ ] **Tooling** — Improving validation, CI, or automation scripts
- [ ] **Bug fix** — Fixing a non-security bug in tooling or configuration

## Related Issues

<!-- Link related issues. Use "Closes #123" to auto-close on merge. -->

- Related to #
- Closes #

## New Stack Checklist

<!-- Complete ALL items if adding a new stack. Remove this section otherwise. -->

### Structure & Metadata

- [ ] `stack.yml` exists and passes schema validation
- [ ] `README.md` includes prerequisites, quick start, configuration, and
      security features
- [ ] `.env.example` lists all required environment variables with comments
- [ ] All dependencies have pinned versions (no ranges)
- [ ] Lockfile is present and checksum recorded in `lockfile.sha256`

### Container Security

- [ ] All containers run as non-root users (specific UID/GID)
- [ ] All containers have `read_only: true` with `tmpfs` for writable paths
- [ ] All containers have `security_opt: [no-new-privileges:true]`
- [ ] All containers have `cap_drop: [ALL]`
- [ ] All containers have CPU and memory resource limits
- [ ] All containers have health checks defined
- [ ] No container uses `privileged: true`
- [ ] No container uses `network_mode: host`
- [ ] All images use specific version tags (no `latest`)
- [ ] Base images are Alpine, distroless, or similarly minimal

### Network & Application Security

- [ ] Internal services are on an internal Docker network
- [ ] Only necessary ports are exposed to the host
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options, etc.)
- [ ] No hardcoded secrets, passwords, or API keys in any file
- [ ] CORS is configured with explicit origins (no wildcards)
- [ ] Debug mode is disabled by default

### Testing

- [ ] `docker compose up` starts successfully
- [ ] Smoke tests pass
- [ ] Security tests pass
- [ ] No critical or high vulnerabilities in `trivy image` scan

### Documentation

- [ ] All environment variables documented
- [ ] Architecture diagram included (for complex stacks)
- [ ] Customization guide included
- [ ] Troubleshooting section included

## Stack Update Checklist

<!-- Complete ALL items if updating a stack. Remove this section otherwise. -->

- [ ] Dependencies updated to latest secure versions
- [ ] Lockfile regenerated and checksum updated
- [ ] `trivy image` scan shows no new critical/high vulnerabilities
- [ ] Stack starts and passes smoke tests
- [ ] Changelog entry added
- [ ] Version bumped appropriately (semver)

## Security Fix Checklist

<!-- Complete ALL items if fixing a security issue. Remove this section otherwise. -->

- [ ] Vulnerability described and linked to CVE/advisory if applicable
- [ ] Fix verified to resolve the vulnerability
- [ ] No new vulnerabilities introduced
- [ ] Audit report updated if one exists
- [ ] Affected versions documented

## Testing Performed

<!-- Describe the testing you've done. -->

- [ ] Ran `python scripts/validate-stack.py` — passes
- [ ] Ran `docker compose up -d` — all services healthy
- [ ] Ran smoke tests — all pass
- [ ] Ran security tests — all pass
- [ ] Ran `trivy image` — no critical/high findings
- [ ] Manually tested key functionality:

## Screenshots / Logs

<!-- If applicable, add screenshots or log output showing the stack working. -->

## Additional Notes

<!-- Any additional context, concerns, or notes for reviewers. -->

## Reviewer Notes

<!-- For maintainers: items to focus on during review. -->

- [ ] Security audit checklist items verified
- [ ] Architecture is sound
- [ ] Documentation is complete and accurate
- [ ] No licensing issues with dependencies
