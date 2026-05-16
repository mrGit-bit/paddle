# Harness

This repository is a Django product plus a development harness. The harness is
the set of instructions, specs, checks, scripts, and release gates that make
changes repeatable.

## Source Of Truth

- `AGENTS.md`: Codex router, authority order, branch gate, spec gate, and
  validation pointers.
- `docs/PROJECT_INSTRUCTIONS.md`: ChatGPT-only conversational and pre-spec
  guidance.
- `.codex/skills/`: detailed Codex workflows loaded by task type.
- `specs/`: active SDD specs and consolidated release records.
- `scripts/`: executable repository checks and release automation.
- `.github/workflows/`: pull request, release, security, and mobile CI gates.

## Local Checks

Run the full harness check before process, governance, or release-script
changes:

```bash
bash scripts/check_harness.sh
```

The wrapper runs:

- `python scripts/validate_governance.py`
- `python scripts/validate_specs.py`
- `python scripts/release_orchestrator.py --check`
- Markdown linting with `MD013` disabled by `.markdownlint.json`

For product code changes, also run the smallest relevant pytest scope.

## CI Gates

Pull requests to `develop`, `staging`, and `main` run:

- Harness validation: governance, active specs, release dry run, Markdown lint.
- Product tests: frontend and Americano pytest suites with coverage gates.

## Release Check

Use this non-destructive release preflight when editing release automation:

```bash
python scripts/release_orchestrator.py --check
```

It validates local release inputs without GitHub authentication, SSH, commits,
tags, branch changes, or deploys.

## Spec Check

Use this when creating or editing active SDD specs:

```bash
python scripts/validate_specs.py
```

The check verifies active non-release specs have required tracking metadata,
required sections, valid status values, and expected filename shape.
