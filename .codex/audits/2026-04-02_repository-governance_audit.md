# Governance Audit Report

## Summary

- Scope: Repository governance markdown and release coordination after adding
  lifecycle tracking to loose specs.
- Audited target: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `README.md`,
  `RELEASE.md`, `.codex/commands/release.md`, `scripts/release_orchestrator.py`,
  and the focused release-tooling tests.
- Audit date: `2026-04-02`
- Reviewer: Codex

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: The new loose-spec lifecycle rules are authoritative in
  [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md#L78)
  and [AGENTS.md](/workspaces/paddle/AGENTS.md#L62), but the rest of the
  release-governance surface still models loose specs only through
  `Release tag`: [README.md](/workspaces/paddle/README.md#L94),
  [RELEASE.md](/workspaces/paddle/RELEASE.md#L54),
  [.codex/commands/release.md](/workspaces/paddle/.codex/commands/release.md#L20),
  [scripts/release_orchestrator.py](/workspaces/paddle/scripts/release_orchestrator.py#L20),
  and [test_release_orchestrator.py](/workspaces/paddle/paddle/frontend/tests/test_release_orchestrator.py#L196).
  The current parser and release-source selector ignore `Status` entirely.
- Why it matters: The repo now depends on a two-field spec lifecycle model, but
  the release docs and automation still enforce only half of that contract. That
  leaves contributors without one operational source of truth for when a loose
  spec should remain `approved`, move to `implemented`, or be eligible for
  shipment.
- Recommended minimal fix: Propagate the `Status` lifecycle model through
  README, release docs, release wrapper instructions, release-source parsing,
  and its focused tests so the governance rule is enforceable and discoverable
  outside the top-level docs.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact authority source for minimum SDD gates and spec
    lifecycle rules.
  - Recommended role: Keep owning the compact lifecycle contract.
- File: `AGENTS.md`
  - Current role: Long-form execution behavior and closure semantics.
  - Recommended role: Mirror the same lifecycle contract without becoming the
    only place where the rule is practically understandable.
- File: `README.md`
  - Current role: Repository orientation and quick routing.
  - Recommended role: Reflect the current loose-spec lifecycle model at a high
    level so contributors do not learn an obsolete release-tag-only story.
- File: `RELEASE.md`
  - Current role: Primary release-flow source of truth.
  - Recommended role: Describe how `Status` and `Release tag` interact before
    and during shipment.
- File: `.codex/commands/release.md`
  - Current role: Optional wrapper contract for release automation.
  - Recommended role: Mirror `RELEASE.md` without omitting lifecycle metadata
    that the higher-authority docs now require.
- File: `scripts/release_orchestrator.py`
  - Current role: Operational release enforcement.
  - Recommended role: Parse and tolerate the full loose-spec tracking block so
    release governance and automation stay aligned.

## Coordination Gaps

- Gap: The loose-spec lifecycle rule is documented but not yet operationalized
  across release docs and release automation.
  - Evidence: Top-level governance requires `Status` plus `Release tag`, while
    README, RELEASE docs, wrapper instructions, and release parsing still
    operate as if `Release tag` were the only tracking field.
  - Recommended minimal fix: Update the release-facing docs and source
    selection code together in one change set.

## Rewrite Plan

- Step: Align the release-facing docs with the new loose-spec lifecycle model.
  - Goal: Make the `approved -> implemented -> shipped` path discoverable in
    the same places contributors already use for release guidance.
  - Files primarily affected: `README.md`, `RELEASE.md`,
    `.codex/commands/release.md`
- Step: Align release automation and tests with the current tracking block.
  - Goal: Ensure loose spec parsing remains correct when specs include
    `Status` as part of the tracking section.
  - Files primarily affected: `scripts/release_orchestrator.py`,
    `paddle/frontend/tests/test_release_orchestrator.py`

## Open Questions

- None.
