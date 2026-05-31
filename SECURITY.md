# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in any of
our stack templates, tooling, or documentation, please report it responsibly.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, use one of the following channels:

- **Email:** [security@secure-stacks.dev](mailto:security@secure-stacks.dev)
- **GitHub Security Advisories:**
  [Submit via GitHub](https://github.com/lxl141421/awesome-secure-stacks/security/advisories/new)

Please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Affected stack/template(s)
- Potential impact assessment
- Suggested fix (if available)

### Response Timeline

| Stage | Timeline |
|-------|----------|
| **Acknowledgment** | Within 48 hours of report submission |
| **Triage & Assessment** | Within 7 days — severity classified, affected components identified |
| **Fix & Release** | Within 30 days for critical/high severity; 90 days for medium/low |

We will keep you informed of our progress throughout the process.

## Scope

### In Scope

- All Docker Compose templates in `templates/`
- All stack configurations in `stacks/`
- Validation and scoring scripts in `scripts/`
- CI/CD pipeline configurations in `.github/`
- Documentation that could lead to insecure deployments
- Default configurations that introduce security weaknesses

### Out of Scope

- Vulnerabilities in upstream dependencies (report to the respective project)
- Social engineering attacks against maintainers
- Denial of service attacks against the repository or infrastructure
- Issues requiring physical access to a user's environment
- Third-party services referenced in templates (report to their maintainers)

## Bug Bounty

We do not currently offer a monetary bug bounty program. However, we recognize
and appreciate security researchers who help improve the project:

- **Public acknowledgment** in our SECURITY.md and release notes (with your
  permission)
- **Hall of Fame** listing for verified vulnerability reports
- **Contributor badge** on the project for repeat contributors

We believe in building a security-conscious community and value every report
that helps make these templates safer for all developers.

## Security Best Practices

When using our templates, we recommend:

1. Always use the latest version of a template
2. Review and customize security settings for your specific deployment
3. Never commit `.env` files or secrets to version control
4. Regularly update dependencies and re-scan for vulnerabilities
5. Run the provided security tests before deploying to production

---

*This security policy is inspired by industry best practices and the
[GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)
framework.*
