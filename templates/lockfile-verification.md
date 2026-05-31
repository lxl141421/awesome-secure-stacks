# Lockfile Verification Guide

Lockfiles are critical for supply chain security. They pin exact dependency
versions and (in some ecosystems) include integrity checksums. This guide
covers how to verify lockfile integrity across all supported ecosystems.

## Why Lockfiles Matter

Without a lockfile, a `npm install` or `pip install` could pull different
versions on different machines — or worse, a compromised version could be
published and silently picked up. Lockfiles ensure:

- **Reproducibility** — Same versions everywhere
- **Integrity** — Checksums detect tampering
- **Auditability** — Exact dependency tree is recorded

---

## npm / pnpm / yarn

### Lockfile Types

| Package Manager | Lockfile | Checksums Included |
|----------------|----------|-------------------|
| npm | `package-lock.json` | integrity (SHA-512) |
| pnpm | `pnpm-lock.yaml` | integrity (SHA-512) |
| yarn (v1) | `yarn.lock` | No (but can use `--check-files`) |
| yarn (v2+) | `yarn.lock` + `.pnp.cjs` | Yes |

### Verify Integrity

```bash
# npm — clean install verifies checksums automatically
npm ci

# npm — audit for vulnerabilities
npm audit --production

# pnpm — clean install with strict verification
pnpm install --frozen-lockfile

# yarn v1
yarn install --frozen-lockfile --check-files

# yarn v2+
yarn install --immutable
```

### Generate Checksum of Lockfile

```bash
# Record the SHA-256 hash of your lockfile
sha256sum package-lock.json > lockfile.sha256

# Verify later
sha256sum -c lockfile.sha256
```

### Best Practices

- Always commit `package-lock.json` (or equivalent)
- Use `npm ci` in CI/CD, never `npm install`
- Run `npm audit` as part of your CI pipeline
- Use `npm ci --ignore-scripts` and review post-install scripts separately
- Set `ignore-scripts=true` in `.npmrc` for untrusted packages

---

## Python (pip / Poetry / uv)

### Lockfile Types

| Tool | Lockfile | Checksums Included |
|------|----------|-------------------|
| pip | `requirements.txt` (must pin manually) | No (use hashes separately) |
| pip-compile | `requirements.txt` | Yes (with `--generate-hashes`) |
| Poetry | `poetry.lock` | Yes (SHA-256) |
| uv | `uv.lock` | Yes (SHA-256) |
| Pipenv | `Pipfile.lock` | Yes (SHA-256) |

### Verify Integrity

```bash
# pip — install with hash verification
pip install --require-hashes -r requirements.txt

# pip-compile — generate lockfile with hashes
pip-compile --generate-hashes --output-file=requirements.txt requirements.in

# Poetry — verify lockfile is up to date
poetry check --lock

# uv — verify lockfile
uv lock --check
```

### Generate Checksum of Lockfile

```bash
sha256sum requirements.txt > lockfile.sha256
# or
sha256sum poetry.lock >> lockfile.sha256
```

### Best Practices

- Use `pip-compile` (from pip-tools) or Poetry for deterministic builds
- Always generate requirements with `--generate-hashes`
- Run `pip-audit` or `safety check` in CI
- Pin all direct and transitive dependencies
- Never use `pip install -r requirements.txt` without `--require-hashes` in
  production

### Example: requirements.txt with Hashes

```
flask==3.0.0 \
    --hash=sha256:41521e9d754b5e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e \
    --hash=sha256:52632e0d6452e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3
werkzeug==3.0.1 \
    --hash=sha256:...
```

---

## Go

### Lockfile

Go uses `go.sum` which contains cryptographic hashes of all module versions.

### Verify Integrity

```bash
# Verify all dependencies match go.sum
go mod verify

# Download and verify modules
go mod download

# Check for known vulnerabilities
govulncheck ./...

# Tidy up (removes unused dependencies)
go mod tidy
```

### Generate Checksum of go.sum

```bash
sha256sum go.sum > lockfile.sha256
```

### Best Practices

- Always commit `go.sum`
- Run `go mod verify` in CI
- Use `govulncheck` for vulnerability scanning
- Run `go mod tidy` to remove unused dependencies
- Use `-mod=readonly` in CI to prevent accidental modifications

---

## Rust (Cargo)

### Lockfile

Cargo uses `Cargo.lock` which includes exact versions and checksums.

### Verify Integrity

```bash
# Build with locked dependencies (fails if Cargo.lock is outdated)
cargo build --locked

# Verify dependencies
cargo verify-lockfile

# Audit for vulnerabilities
cargo audit

# Update and verify
cargo update
cargo build --locked
```

### Generate Checksum of Cargo.lock

```bash
sha256sum Cargo.lock > lockfile.sha256
```

### Best Practices

- Commit `Cargo.lock` for applications (not libraries)
- Use `cargo build --locked` in CI
- Run `cargo audit` as part of CI pipeline
- Use `cargo deny` for license and advisory checking

---

## Recording Lockfile Checksums

Every Secure Stacks template includes a `lockfile.sha256` file that records
the SHA-256 hash of each lockfile. This is verified during CI.

### Format

```
# lockfile.sha256
# Generated: 2025-01-15T10:30:00Z
# Format: sha256  filename
a1b2c3d4e5f6...  package-lock.json
f6e5d4c3b2a1...  poetry.lock
```

### Verification in CI

```bash
#!/bin/bash
set -euo pipefail

echo "Verifying lockfile integrity..."

while IFS='  ' read -r expected_hash filename; do
    # Skip comments and empty lines
    [[ "$filename" =~ ^#.*$ || -z "$filename" ]] && continue

    if [ ! -f "$filename" ]; then
        echo "ERROR: Lockfile missing: $filename"
        exit 1
    fi

    actual_hash=$(sha256sum "$filename" | awk '{print $1}')

    if [ "$expected_hash" != "$actual_hash" ]; then
        echo "ERROR: Lockfile hash mismatch for $filename"
        echo "  Expected: $expected_hash"
        echo "  Actual:   $actual_hash"
        exit 1
    fi

    echo "OK: $filename"
done < lockfile.sha256

echo "All lockfiles verified."
```

---

## CI Integration

### GitHub Actions Example

```yaml
- name: Verify lockfiles
  run: |
    sha256sum -c lockfile.sha256

- name: npm audit
  run: npm audit --production --audit-level=high

- name: Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
    severity: 'CRITICAL,HIGH'
```

---

## Summary

| Ecosystem | Lockfile | Checksums | Verify Command |
|-----------|----------|-----------|----------------|
| npm | `package-lock.json` | SHA-512 | `npm ci` |
| pnpm | `pnpm-lock.yaml` | SHA-512 | `pnpm install --frozen-lockfile` |
| pip-tools | `requirements.txt` | SHA-256 (opt-in) | `pip install --require-hashes` |
| Poetry | `poetry.lock` | SHA-256 | `poetry check --lock` |
| Go | `go.sum` | SHA-256 | `go mod verify` |
| Cargo | `Cargo.lock` | SHA-256 | `cargo build --locked` |
