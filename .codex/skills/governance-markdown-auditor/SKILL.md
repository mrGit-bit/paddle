---
name: governance-markdown-auditor
description: Audit governance markdown for duplication, unclear ownership, coordination gaps, prose-only rules, and low-value spec/plan overhead; produce prioritized findings plus a consolidation-first rewrite plan.
---

# Governance Markdown Auditor

Use this skill when the user wants to review repository governance markdown as
one coordinated system instead of as isolated files.

Default review scope:

- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `CHANGELOG.md`
- `BACKLOG.md`
- `RELEASE.md`
- `specs/`
- `plans/`
- `plans/TEMPLATE.md`
- `.codex/commands/`

If the user gives a narrower scope, stay inside it.

## Review Goal

Find and explain:

- duplicated or overlapping instructions
- unclear ownership or authority boundaries between files
- verbosity that reduces agent readability
- coordination gaps between related markdown artifacts
- rules that exist only in prose and are not operationalized anywhere
- spec/plan detail that does not create clear execution value
- release-consolidation or workflow rules that appear inconsistently enforced

Bias toward simplifying the current governance set. Prefer clarifying or
shrinking existing files before proposing new governance files.

## Review Workflow

1. Read the governance files most likely to define authority first:
   - `docs/PROJECT_INSTRUCTIONS.md`
   - `AGENTS.md`
   - `README.md`
2. Read only the additional markdown files needed for the requested scope.
3. Build a file-ownership map before judging wording. State what each file
   currently appears to own.
4. Compare files for repeated rules, conflicting instructions, or responsibility
   leakage.
5. Check whether important coordination rules have an operational hook:
   - slash commands
   - templates
   - automation scripts
   - release workflow docs
   - repository conventions actually visible in the tree
6. For `specs/` and `plans/`, assess both:
   - governance intent
   - practical value in the observed workflow
7. Recommend consolidation-first fixes that make each file easier for agents to
   consult quickly.

Read `references/review-rubric.md` when you need the compact severity and
category rubric.

## Default Review Heuristics

Treat these as strong signals of governance debt:

- `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` restating the same workflow
  instead of splitting long-form vs compact authority cleanly
- `README.md` carrying release-history or changelog-style summaries instead of
  current-state repository orientation
- `CHANGELOG.md` and `BACKLOG.md` depending on manual coordination with no clear
  trigger, checklist, or automation support
- specs or plans required by governance but not reliably retrieved, referenced,
  or enforced during execution
- consolidation rules that exist in governance but are only partially reflected
  in commands or current repository state
- templates or commands that preserve obsolete process detail after governance
  changed

Do not preserve detail by default just because it already exists. If a document
or section is high-friction and low-value, say so explicitly.

## Required Output Format

Use exactly these top-level sections:

### `Summary`

State the requested scope, the files reviewed, and the overall governance
quality in 2-4 sentences.

### `Findings`

List findings in priority order. For each finding include:

- `Severity:` critical, major, or minor
- `Category:` duplication, boundary, coordination, operationalization,
  verbosity, or artifact-value
- `Evidence:` concrete file references and the specific overlap or gap
- `Why it matters:`
- `Recommended minimal fix:`

### `Ownership Map`

State the current or recommended responsibility of each reviewed file in one
short line per file. Call out files whose current scope is ambiguous.

### `Coordination Gaps`

List the workflows that rely on manual memory, hidden assumptions, or
unimplemented automation. If none exist, state `None.`

### `Rewrite Plan`

Provide a concrete consolidation-first rewrite plan. Group by behavior or file
role, not by sentence-level edits. Prefer deleting duplicated guidance over
rewriting it in multiple places.

### `Open Questions`

Only include this section if a key recommendation depends on a product or team
preference that cannot be inferred from repository context. Otherwise write
`None.`

## Review Rules

- Distinguish repository facts from recommendations.
- Do not invent automation that does not exist; call it a recommendation.
- Mark prose-only rules as defects when the workflow depends on them.
- Prefer fewer governance files with clearer roles over more coordination docs.
- Recommend new files only when no existing file has a clean ownership fit.
- Keep recommendations agent-readable and concise.
- Avoid generic markdown style advice unless it affects governance usability.
