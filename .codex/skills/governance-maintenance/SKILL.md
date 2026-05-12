---
name: governance-maintenance
description: Use for rankingdepadel.club governance edits, instruction version/date alignment, markdown rules, governance validation, changelog wording, and maintaining progressive disclosure between router docs and skills.
---

# Governance Maintenance

Use this skill for governance markdown edits, instruction routing, validation,
and ownership boundaries.

## File Ownership

- `docs/PROJECT_INSTRUCTIONS.md`: ChatGPT conversational design and copy-paste
  pre-spec output only.
- `AGENTS.md`: minimal Codex router, authority, branch/spec safety, skill
  routing, and validation pointers.
- `.codex/skills/`: detailed Codex workflows and progressive disclosure.
- `README.md`: repository orientation and owner-doc pointers.
- `CHANGELOG.md`: shipped and unreleased outcomes.
- `RELEASE.md`: release flow and fallback tools.
- `docs/pre-specs/`: ignored scratch planning input only.

## Progressive Disclosure Rules

- Keep always-loaded governance short.
- Move detailed workflow behavior into task-triggered skills.
- Do not duplicate long rules between `AGENTS.md`,
  `docs/PROJECT_INSTRUCTIONS.md`, and skills.
- Keep each skill body concise and move optional detail into references only
  when needed.
- New governance rules need a clear owner file or skill; avoid scattering the
  same rule across multiple surfaces.
- When governance or skills depend on external docs, MCP tools, scripts, or
  bundled references, name the source of truth and the fallback order.
- Keep always-loaded router docs policy-level. Put detailed source lookup,
  fallback disclosure, and scope-limiting workflow inside task-triggered
  skills.
- Preserve user-authored text/style intent in governance and skill edits. Ask
  before changing wording or style rules when the user's intention is unclear.

## Versioning and Validation

- Keep `Instruction Set Version` and `Last Updated` aligned in
  `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on changed Markdown files when available.
- Enforce `MD022` and `MD032`; omit `MD013` reports and do not reflow long
  lines only to satisfy line-length linting.
- Do not add `markdownlint-disable` directives unless explicitly requested.
- Preserve authoritative generated text unless a structural correction is
  required.

## Markdown Style

- Keep new or rewritten Markdown light and schematic.
- Write concise, specific Markdown, including skills. Avoid long grammar
  constructions, verbose setup, and repeated restatement.
- Prefer short sections, direct bullets, compact summaries, and no duplicate
  restatement.
- Preserve explicit user targets when documenting upgrades, migrations, or
  rewritten guidance. Do not silently substitute a "latest" target or widen
  the task beyond the stated request.
- If authoritative external guidance and repository behavior or governance
  disagree, state the conflict and stop before making broad rewrites.
- Active-work specs should capture only the scope, constraints, and checks
  needed for execution.
- Consolidated release files should be compact provenance summaries, not
  embedded copies of prior source files.
- Release changelog entries should be grouped by stable product or workflow
  domains, merge related specs and outcomes within each release, and avoid
  verbose process detail.
