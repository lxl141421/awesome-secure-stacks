#!/usr/bin/env python3
"""
validate-stack.py — Validates Secure Stacks YAML stack definitions.

Checks for:
- Required fields and structure
- Valid YAML syntax
- Security configuration completeness
- Dependency pinning
- Docker Compose reference validation

Usage:
    python scripts/validate-stack.py stacks/your-stack/stack.yml
    python scripts/validate-stack.py stacks/          # validate all stacks
    python scripts/validate-stack.py --strict stacks/  # treat warnings as errors
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

# ─── Constants ───────────────────────────────────────────────────────────────

REQUIRED_TOP_LEVEL_FIELDS = [
    "name",
    "version",
    "description",
    "category",
    "framework",
    "components",
    "security",
    "maintainers",
]

VALID_CATEGORIES = [
    "fullstack",
    "backend",
    "frontend",
    "infra",
    "mobile",
    "devtools",
]

VALID_COMPONENT_ROLES = [
    "application",
    "database",
    "cache",
    "proxy",
    "queue",
    "search",
    "storage",
    "monitoring",
    "other",
]

REQUIRED_SECURITY_HARDENING = [
    "non-root-user",
    "read-only-filesystem",
    "resource-limits",
    "no-new-privileges",
]

SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


# ─── Validation Helpers ─────────────────────────────────────────────────────


class ValidationResult:
    """Collects errors and warnings during validation."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def print_report(self) -> None:
        status = "PASS" if self.passed else "FAIL"
        print(f"\n{'='*60}")
        print(f"  {status}: {self.filepath}")
        print(f"{'='*60}")

        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for i, err in enumerate(self.errors, 1):
                print(f"    {i}. {err}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for i, warn in enumerate(self.warnings, 1):
                print(f"    {i}. {warn}")

        if not self.errors and not self.warnings:
            print("  All checks passed! ✓")

        print()


def validate_yaml_syntax(filepath: str, result: ValidationResult) -> dict | None:
    """Parse YAML and return the data, or None on failure."""
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.error(f"Invalid YAML syntax: {e}")
        return None
    except FileNotFoundError:
        result.error(f"File not found: {filepath}")
        return None
    except PermissionError:
        result.error(f"Permission denied: {filepath}")
        return None

    if not isinstance(data, dict):
        result.error("Root element must be a mapping (dict)")
        return None

    return data


def validate_required_fields(data: dict, result: ValidationResult) -> None:
    """Check that all required top-level fields are present."""
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            result.error(f"Missing required field: '{field}'")


def validate_name(data: dict, result: ValidationResult) -> None:
    """Validate the stack name."""
    name = data.get("name", "")
    if not isinstance(name, str) or not name.strip():
        result.error("'name' must be a non-empty string")
        return

    # Check naming convention: lowercase, alphanumeric with hyphens
    if not re.match(r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$|^[a-z0-9]$", name):
        result.warn(
            f"'name' should be lowercase alphanumeric with hyphens: '{name}'"
        )


def validate_version(data: dict, result: ValidationResult) -> None:
    """Validate the version field follows semver."""
    version = data.get("version", "")
    if not isinstance(version, str):
        result.error("'version' must be a string")
        return

    if not SEMVER_PATTERN.match(version):
        result.error(
            f"'version' must follow semantic versioning (e.g., 1.0.0): '{version}'"
        )


def validate_category(data: dict, result: ValidationResult) -> None:
    """Validate the category field."""
    category = data.get("category", "")
    if category not in VALID_CATEGORIES:
        result.error(
            f"'category' must be one of {VALID_CATEGORIES}, got: '{category}'"
        )


def validate_framework(data: dict, result: ValidationResult) -> None:
    """Validate the framework section."""
    framework = data.get("framework")
    if not isinstance(framework, dict):
        result.error("'framework' must be a mapping")
        return

    for field in ["name", "version"]:
        if field not in framework:
            result.error(f"'framework.{field}' is required")

    if "url" in framework and not framework["url"].startswith("http"):
        result.error(f"'framework.url' must be a valid URL: '{framework['url']}'")


def validate_components(data: dict, result: ValidationResult) -> None:
    """Validate the components list."""
    components = data.get("components")
    if not isinstance(components, list) or len(components) == 0:
        result.error("'components' must be a non-empty list")
        return

    for i, comp in enumerate(components):
        prefix = f"components[{i}]"

        if not isinstance(comp, dict):
            result.error(f"'{prefix}' must be a mapping")
            continue

        if "name" not in comp:
            result.error(f"'{prefix}.name' is required")

        if "image" not in comp:
            result.error(f"'{prefix}.image' is required")
        else:
            image = comp["image"]
            if isinstance(image, str):
                # Check for :latest or missing tag
                if image.endswith(":latest"):
                    result.warn(
                        f"'{prefix}.image' uses ':latest' tag — pin to a specific version: '{image}'"
                    )
                elif ":" not in image and "@" not in image:
                    result.warn(
                        f"'{prefix}.image' has no version tag — pin to a specific version: '{image}'"
                    )

        role = comp.get("role", "")
        if role and role not in VALID_COMPONENT_ROLES:
            result.warn(
                f"'{prefix}.role' should be one of {VALID_COMPONENT_ROLES}, got: '{role}'"
            )


def validate_security(data: dict, result: ValidationResult) -> None:
    """Validate the security section."""
    security = data.get("security")
    if not isinstance(security, dict):
        result.error("'security' must be a mapping")
        return

    # Check hardening list
    hardening = security.get("hardening", [])
    if not isinstance(hardening, list):
        result.error("'security.hardening' must be a list")
        return

    for item in REQUIRED_SECURITY_HARDENING:
        if item not in hardening:
            result.warn(f"Recommended hardening option missing: '{item}'")

    # Validate audit fields
    last_audit = security.get("last_audit")
    if last_audit is not None:
        if isinstance(last_audit, str):
            # Should be a date
            if not re.match(r"^\d{4}-\d{2}-\d{2}", last_audit):
                result.warn(
                    f"'security.last_audit' should be a date (YYYY-MM-DD): '{last_audit}'"
                )

    audit_score = security.get("audit_score")
    if audit_score is not None:
        if not isinstance(audit_score, (int, float)):
            result.error("'security.audit_score' must be a number")
        elif not (0 <= audit_score <= 100):
            result.error(
                f"'security.audit_score' must be between 0 and 100: {audit_score}"
            )


def validate_dependencies(data: dict, result: ValidationResult) -> None:
    """Validate the dependencies list."""
    dependencies = data.get("dependencies", [])
    if not isinstance(dependencies, list):
        if dependencies is not None:
            result.error("'dependencies' must be a list")
        return

    for i, dep in enumerate(dependencies):
        prefix = f"dependencies[{i}]"

        if not isinstance(dep, dict):
            result.error(f"'{prefix}' must be a mapping")
            continue

        for field in ["name", "version"]:
            if field not in dep:
                result.error(f"'{prefix}.{field}' is required")

        version = dep.get("version", "")
        if isinstance(version, str) and version.startswith((">=", "<=", ">", "<", "~", "^")):
            result.warn(
                f"'{prefix}.version' uses a range — pin to exact version: '{version}'"
            )

        checksum = dep.get("checksum")
        if not checksum:
            result.warn(f"'{prefix}.checksum' is recommended for supply chain security")


def validate_maintainers(data: dict, result: ValidationResult) -> None:
    """Validate the maintainers list."""
    maintainers = data.get("maintainers")
    if not isinstance(maintainers, list) or len(maintainers) == 0:
        result.error("'maintainers' must be a non-empty list")
        return

    for i, maint in enumerate(maintainers):
        prefix = f"maintainers[{i}]"

        if not isinstance(maint, dict):
            result.error(f"'{prefix}' must be a mapping")
            continue

        if "github" not in maint:
            result.error(f"'{prefix}.github' is required")


def check_docker_compose(stack_dir: str, result: ValidationResult) -> None:
    """Check if docker-compose.yml exists and is valid YAML."""
    compose_path = os.path.join(stack_dir, "docker-compose.yml")

    if not os.path.isfile(compose_path):
        result.warn("No docker-compose.yml found in stack directory")
        return

    try:
        with open(compose_path, "r") as f:
            compose_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.error(f"Invalid YAML in docker-compose.yml: {e}")
        return

    if not isinstance(compose_data, dict):
        result.error("docker-compose.yml root must be a mapping")
        return

    services = compose_data.get("services", {})
    if not services:
        result.error("docker-compose.yml must define at least one service")
        return

    for svc_name, svc_config in services.items():
        if not isinstance(svc_config, dict):
            continue

        # Check security_opt
        sec_opts = svc_config.get("security_opt", [])
        has_no_new_priv = any(
            "no-new-privileges" in str(opt) for opt in sec_opts
        )
        if not has_no_new_priv:
            result.warn(
                f"Service '{svc_name}': missing security_opt: no-new-privileges:true"
            )

        # Check cap_drop
        cap_drop = svc_config.get("cap_drop", [])
        if "ALL" not in cap_drop:
            result.warn(
                f"Service '{svc_name}': should have cap_drop: [ALL]"
            )

        # Check read_only
        if not svc_config.get("read_only"):
            result.warn(
                f"Service '{svc_name}': read_only should be true"
            )

        # Check resource limits
        deploy = svc_config.get("deploy", {})
        resources = deploy.get("resources", {})
        limits = resources.get("limits", {})
        if not limits:
            result.warn(
                f"Service '{svc_name}': missing deploy.resources.limits"
            )

        # Check healthcheck
        if "healthcheck" not in svc_config:
            result.warn(
                f"Service '{svc_name}': missing healthcheck"
            )

        # Check image version
        image = svc_config.get("image", "")
        if isinstance(image, str) and image.endswith(":latest"):
            result.warn(
                f"Service '{svc_name}': image uses ':latest' tag"
            )

    # Check for internal networks
    networks = compose_data.get("networks", {})
    has_internal = any(
        isinstance(v, dict) and v.get("internal") for v in networks.values()
    )
    if not has_internal:
        result.warn(
            "No internal network defined — backend services should use internal networks"
        )


def check_readme(stack_dir: str, result: ValidationResult) -> None:
    """Check if README.md exists and is not empty."""
    readme_path = os.path.join(stack_dir, "README.md")

    if not os.path.isfile(readme_path):
        result.error("No README.md found in stack directory")
        return

    content = readme_path
    try:
        with open(readme_path, "r") as f:
            content = f.read()
    except Exception as e:
        result.error(f"Cannot read README.md: {e}")
        return

    if len(content.strip()) < 100:
        result.warn("README.md appears to be very short — ensure it covers prerequisites, setup, and security features")


def check_env_example(stack_dir: str, result: ValidationResult) -> None:
    """Check if .env.example exists."""
    env_path = os.path.join(stack_dir, ".env.example")

    if not os.path.isfile(env_path):
        result.warn("No .env.example found — document all required environment variables")


def check_lockfile(stack_dir: str, result: ValidationResult) -> None:
    """Check for lockfiles and lockfile checksums."""
    lockfiles = [
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "requirements.txt",
        "poetry.lock",
        "uv.lock",
        "Pipfile.lock",
        "go.sum",
        "Cargo.lock",
    ]

    found_lockfile = any(
        os.path.isfile(os.path.join(stack_dir, lf)) for lf in lockfiles
    )

    if not found_lockfile:
        result.warn("No lockfile found — include one for reproducible builds")

    checksum_path = os.path.join(stack_dir, "lockfile.sha256")
    if not os.path.isfile(checksum_path):
        result.warn(
            "No lockfile.sha256 found — record lockfile checksums for integrity verification"
        )


# ─── Main Validation ────────────────────────────────────────────────────────


def validate_stack(filepath: str, strict: bool = False) -> bool:
    """Validate a single stack.yml file. Returns True if valid."""
    result = ValidationResult(filepath)

    # Parse YAML
    data = validate_yaml_syntax(filepath, result)
    if data is None:
        result.print_report()
        return result.passed

    # Field validation
    validate_required_fields(data, result)
    validate_name(data, result)
    validate_version(data, result)
    validate_category(data, result)
    validate_framework(data, result)
    validate_components(data, result)
    validate_security(data, result)
    validate_dependencies(data, result)
    validate_maintainers(data, result)

    # Check companion files
    stack_dir = os.path.dirname(os.path.abspath(filepath))
    check_docker_compose(stack_dir, result)
    check_readme(stack_dir, result)
    check_env_example(stack_dir, result)
    check_lockfile(stack_dir, result)

    # In strict mode, warnings become errors
    if strict:
        result.errors.extend(result.warnings)
        result.warnings = []

    result.print_report()
    return result.passed


def find_stack_files(directory: str) -> list[str]:
    """Find all stack.yml files in a directory tree."""
    stack_files = []
    for root, dirs, files in os.walk(directory):
        if "stack.yml" in files:
            stack_files.append(os.path.join(root, "stack.yml"))
    return sorted(stack_files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Secure Stacks YAML stack definitions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s stacks/t3-stack/stack.yml          Validate a single stack
  %(prog)s stacks/                             Validate all stacks
  %(prog)s --strict stacks/                    Strict mode (warnings = errors)
        """,
    )
    parser.add_argument(
        "path",
        help="Path to a stack.yml file or a directory containing stack directories",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (stricter validation)",
    )

    args = parser.parse_args()
    path = os.path.abspath(args.path)

    if os.path.isfile(path):
        # Validate a single file
        passed = validate_stack(path, strict=args.strict)
        return 0 if passed else 1

    elif os.path.isdir(path):
        # Find and validate all stacks in directory
        stack_files = find_stack_files(path)

        if not stack_files:
            print(f"No stack.yml files found in: {path}")
            return 1

        print(f"Found {len(stack_files)} stack(s) to validate.\n")

        results = []
        for filepath in stack_files:
            passed = validate_stack(filepath, strict=args.strict)
            results.append((filepath, passed))

        # Summary
        total = len(results)
        passed_count = sum(1 for _, p in results if p)
        failed_count = total - passed_count

        print(f"{'='*60}")
        print(f"  SUMMARY: {passed_count}/{total} passed, {failed_count} failed")
        print(f"{'='*60}")

        return 0 if failed_count == 0 else 1

    else:
        print(f"ERROR: Path does not exist: {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
