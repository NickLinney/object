# Abstract Object Specification

## Purpose

Define the file-object structure required for a provenance-bearing NickLinney package to represent an Object, its construction context, its contract, its dependencies, its validation, and its lifecycle.

## Canonical tree

```text
<object-slug>/
├── packet.manifest.json
├── SKILL.md or applicable-entrypoint
├── abstract-specification.md
├── implementation-abstract.md
├── contract.md
├── agents/
│   └── openai.yaml
├── catalog/
│   └── source-register.json
├── objects/
├── instantiations/
├── references/
├── schemas/
├── scripts/
└── validation/
```

## Required semantic roles

- `packet.manifest.json`: identity, version, Object kind, entrypoint, lifecycle, required roles, dependencies, and integrity inventory.
- Entrypoint: executable or declarative surface appropriate to the Object kind. `SKILL.md` is required only for Skill Objects.
- `abstract-specification.md`: purpose, transformation, inputs, outputs, consumers, boundaries, and representational semantics.
- `implementation-abstract.md`: NickLinney-specific implementation mapping, construction route, ownership, decomposition, composition, and nonclaims.
- `contract.md`: inputs, outputs, invariants, authority, failure, abstention, termination, and side-effect boundaries.
- `agents/`: runtime-facing metadata where applicable.
- `catalog/`: source, authority, dependency, and comparison-baseline registers.
- `objects/`: embedded or referenced Object definitions, compositions, specializations, and extensions.
- `instantiations/`: concrete construction or execution records; existence of a record is not proof that its event occurred.
- `references/`: source evidence, rationale, mappings, and supporting specifications.
- `schemas/`: machine-readable input, result, manifest, and Object schemas.
- `scripts/`: deterministic validators or package utilities; scripts must not silently authorize lifecycle transitions.
- `validation/`: fixtures, validation plans, results, falsification conditions, and unresolved validation gaps.

## Lifecycle and epistemic rule

Candidate, recommendation, authorization, construction, validation, installation, activation, deployment, canonical approval, and production execution are separate states. The package must state which states are evidenced and which are not.
