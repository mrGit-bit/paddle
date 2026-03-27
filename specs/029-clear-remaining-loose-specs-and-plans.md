# Clear Remaining Loose Specs and Plans

## Tracking

- Task ID: `clear-remaining-loose-specs-and-plans`
- Plan: `plans/2026-03-27_clear-remaining-loose-specs-and-plans.md`
- Release tag: `v1.6.2`

## Goal

- Consolidate remaining released loose spec/plan files into shipped release
  archives.
- Roll non-shipped `1.6.0` history into `1.6.1`.

## Scope

- In:
  - regroup remaining loose historical files by shipped production release
  - update consolidated release files
  - remove superseded loose historical files
  - remove `1.6.0` as a shipped changelog section
  - document non-shipped release rollover in governance/release docs
- Out:
  - product code changes
  - workflow changes
  - rewriting shipped facts

## Files

- Allowed:
  - `specs/*.md`
  - `plans/*.md`
  - `README.md`
  - `AGENTS.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `RELEASE.md`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/**`
  - `.github/workflows/**`
  - `.codex/private/**`

## Acceptance

- [ ] No loose released spec/plan files remain for the cleaned releases.
- [ ] `1.6.0` is removed as a shipped changelog release.
- [ ] Governance states that non-shipped planned releases roll into the next
      production release that ships the work.

## Checks

- Confirm `release-1.6.1` absorbs the former `v1.6.0` loose files.
- Confirm `CHANGELOG.md` no longer has a `1.6.0` release header.
- Confirm only active future work remains loose in `specs/` and `plans/`.
- Confirm governance docs describe the rollover rule consistently.
