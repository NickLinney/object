# NickLinney Abstract Object Package Structure

This repository contains the governed, portable package representation for a NickLinney Enterprise Object.

The package separates identity, semantics, implementation, contract, provenance, composition, instantiation, schemas, deterministic tooling, validation evidence, and lifecycle state. Packageability does not imply executability, and executability does not imply authorization.

## Status

Current release: `0.0.0-pre-alpha.2`

This repository is experimental. Pre-alpha releases are immutable snapshots and provide no API stability guarantee.

## Repository layout

- `src/object/` — the packaged Object implementation
- `VERSION.md` — release-specific version record
- `CHANGELOG.md` — release history
- `ARCHITECTURE.md` — architectural intent and boundaries
- `ABSTRACT.md` — package abstraction summary
- `CONTRIBUTING.md` — contribution and branch discipline
- `VERSIONING.md` — versioning policy
- `RELEASING.md` — release-event checklist

## Validation

The packaged Object provides its own deterministic validation tooling. Validation claims remain bounded to the checks actually executed; structural presence and JSON parsing are not equivalent to schema conformance.
