"""Validate the Abstract Object package and emit bounded machine-readable evidence."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "1.0.0-alpha.1"
root = Path(__file__).parents[1]
manifest_path = root / "packet.manifest.json"
evidence_path = root / "validation" / "package-validation.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_type_ok(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def validate_schema(value: Any, schema: dict[str, Any], location: str = "$", errors: list[str] | None = None) -> list[str]:
    """Validate the JSON Schema subset used by this package without external dependencies."""
    errors = [] if errors is None else errors
    expected = schema.get("type")
    if expected and not schema_type_ok(value, expected):
        errors.append(f"{location}: expected {expected}")
        return errors
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{location}: missing required property {name}")
        for name, child_schema in schema.get("properties", {}).items():
            if name in value and isinstance(child_schema, dict):
                validate_schema(value[name], child_schema, f"{location}.{name}", errors)
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            validate_schema(item, schema["items"], f"{location}[{index}]", errors)
    return errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def result(check: str, status: str, **details: Any) -> dict[str, Any]:
    return {"check": check, "status": status, **details}


def main() -> int:
    evidence: dict[str, Any] = {
        "validator_version": VALIDATOR_VERSION,
        "package": "OBJ-ABSTRACT-OBJECT-PACKAGE-STRUCTURE",
        "scope": "exact working-tree package at validation time",
        "checks": [],
        "claims_proved": [],
        "nonclaims": [
            "behavioral execution is not validated",
            "authorization, activation, deployment, and production execution are not inferred",
            "manifest integrity is delegated to an external release envelope or signature",
        ],
    }
    failures = False

    try:
        manifest = load_json(manifest_path)
        evidence["checks"].append(result("JSON_PARSE_PASS", "PASS", artifact="packet.manifest.json"))
    except Exception as exc:
        evidence["checks"].append(result("JSON_PARSE_PASS", "FAIL", artifact="packet.manifest.json", error=str(exc)))
        evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        return 1

    required_roles = [
        "packet.manifest.json",
        "abstract-specification.md",
        "implementation-abstract.md",
        "contract.md",
        "catalog/source-register.json",
        "schemas/package.manifest.schema.json",
        "validation/README.md",
    ]
    missing = [path for path in required_roles if not (root / path).exists()]
    if missing:
        failures = True
        evidence["checks"].append(result("STRUCTURAL_PASS", "FAIL", missing=missing))
    else:
        evidence["checks"].append(result("STRUCTURAL_PASS", "PASS", required_roles=required_roles))

    parse_failures = []
    for path in sorted(root.rglob("*.json")):
        if path == evidence_path:
            continue
        try:
            load_json(path)
        except Exception as exc:
            parse_failures.append({"artifact": str(path.relative_to(root)), "error": str(exc)})
    if parse_failures:
        failures = True
        evidence["checks"].append(result("JSON_PARSE_PASS", "FAIL", failures=parse_failures))
    else:
        evidence["checks"].append(result("JSON_PARSE_PASS", "PASS", scope="all package JSON except generated evidence"))

    schema_failures = []
    engine = "builtin-json-schema-subset"
    for binding in manifest.get("schema_bindings", []):
        artifact = root / binding["artifact"]
        schema_path = root / binding["schema"]
        try:
            errors = validate_schema(load_json(artifact), load_json(schema_path))
        except Exception as exc:
            errors = [str(exc)]
        if errors:
            schema_failures.append({"artifact": binding["artifact"], "schema": binding["schema"], "errors": errors})
    if schema_failures:
        failures = True
        evidence["checks"].append(result("SCHEMA_CONFORMANCE_PASS", "FAIL", engine=engine, failures=schema_failures))
    else:
        evidence["checks"].append(result("SCHEMA_CONFORMANCE_PASS", "PASS", engine=engine, bindings=manifest.get("schema_bindings", [])))

    integrity_failures = []
    inventory = {entry["path"]: entry for entry in manifest.get("files", [])}
    excluded = set(manifest.get("integrity", {}).get("content_inventory_excludes", []))
    for path, entry in inventory.items():
        actual = root / path
        if not actual.exists():
            integrity_failures.append({"path": path, "error": "missing"})
            continue
        actual_hash = sha256(actual)
        actual_bytes = actual.stat().st_size
        if actual_hash != entry.get("sha256") or actual_bytes != entry.get("bytes"):
            integrity_failures.append({"path": path, "expected_sha256": entry.get("sha256"), "actual_sha256": actual_hash, "expected_bytes": entry.get("bytes"), "actual_bytes": actual_bytes})
    if "packet.manifest.json" in inventory or "packet.manifest.json" not in excluded:
        integrity_failures.append({"path": "packet.manifest.json", "error": "manifest self-integrity must be externalized"})
    if integrity_failures:
        failures = True
        evidence["checks"].append(result("INTEGRITY_PASS", "FAIL", failures=integrity_failures))
    else:
        evidence["checks"].append(result("INTEGRITY_PASS", "PASS", inventory_entries=len(inventory), excluded=sorted(excluded)))

    evidence["state"] = "VALIDATED_WITH_EXPLICIT_EVIDENCE" if not failures else "VALIDATION_FAILED"
    if not failures:
        evidence["claims_proved"] = [
            "required package roles are present",
            "package JSON records parse",
            "declared artifact-to-schema bindings conform",
            "ordinary content inventory hashes and byte counts match",
        ]
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: abstract Object package validation" if not failures else "FAIL: abstract Object package validation")
    for check in evidence["checks"]:
        print(f"{check['status']}: {check['check']}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
