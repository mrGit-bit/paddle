---
name: governance-markdown-auditor
description: Audit governance markdown and workflow skills for duplication, unclear ownership, coordination gaps, prose-only rules, and low-value SDD artifact overhead; export a reviewable governance audit report with prioritized findings and a consolidation-first rewrite plan.
---

# Governance Markdown Auditor

Use this skill when the user wants to review repository governance markdown and
workflow skills as one coordinated system instead of as isolated files.

Use this skill for governance documentation and workflow coordination only. Do
not use it to audit rendered Django template presentation; route concrete
template presentation, CSS cascade, and same-page UI-coherence reviews to
`template-presentation-audit`. Route Django view behavior, architecture, and ORM
performance reviews to `audit`.

Default review scope:

- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `CHANGELOG.md`
- `BACKLOG.md`
- `RELEASE.md`
- `specs/`
- `.codex/commands/`
- `.codex/skills/`

If the user gives a narrower scope, stay inside it.

## Review Goal

Find and explain:

- duplicated or overlapping instructions
- unclear ownership or authority boundaries between files
- verbosity that reduces agent readability
- always-loaded governance that should move into task-triggered skills
- skill detail that should stay out of always-loaded router docs
- coordination gaps between related markdown artifacts
- rules that exist only in prose and are not operationalized anywhere
- SDD artifact detail that does not create clear execution value
- release-consolidation or workflow rules that appear inconsistently enforced

Bias toward simplifying the current governance set. Prefer clarifying or
shrinking existing files and skills before proposing new governance surfaces.

## Review Workflow

1. Read the governance files most likely to define authority first:
   - `docs/PROJECT_INSTRUCTIONS.md`
   - `AGENTS.md`
   - `README.md`
2. Read task-triggered workflow skills when the scope touches Codex execution,
   SDD, closure, release, or governance maintenance.
3. Read only the additional markdown files needed for the requested scope.
4. Build a file/skill ownership map before judging wording. State what each
   surface currently appears to own.
5. Compare files and skills for repeated rules, conflicting instructions, or responsibility
   leakage.
6. Check whether important coordination rules have an operational hook:
   - slash commands
   - templates
   - automation scripts
   - skills
   - release workflow docs
   - repository conventions actually visible in the tree
7. For `specs/`, assess both:
   - governance intent
   - practical value in the observed workflow
8. Recommend consolidation-first fixes that keep always-loaded docs short and
   make each task-triggered skill easy for agents to consult quickly.

Read `references/review-rubric.md` when you need the compact severity and category rubric.
Read `references/report-template.md` when you need to export or update a
reviewable governance audit report.

## Default Review Heuristics

Treat these as strong signals of governance debt:

- `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` restating the same workflow
  instead of splitting ChatGPT guidance, Codex routing, and skill detail cleanly
- `AGENTS.md` carrying detailed handoff, release, audit, or markdown workflows
  that belong in task-triggered skills
- `docs/PROJECT_INSTRUCTIONS.md` carrying Codex execution rules instead of
  ChatGPT design and pre-spec guidance
- `README.md` carrying release-history or changelog-style summaries instead of
  current-state repository orientation
- `CHANGELOG.md` and `BACKLOG.md` depending on manual coordination with no clear
  trigger, checklist, or automation support
- specs required by governance but not reliably retrieved, referenced, or
  enforced during execution
- consolidation rules that exist in governance but are only partially reflected
  in commands or current repository state
- templates or commands that preserve obsolete process detail after governance
  changed
- skills that duplicate each other or duplicate router docs without adding
  task-specific execution value

Do not preserve detail by default just because it already exists. If a document
or section is high-friction and low-value, say so explicitly.

## Required Output Format

Export a reviewable governance audit report under `.codex/audits/` by default
unless the user explicitly asks for inline-only results or a different
repository-local location.

Use predictable file names:

- `YYYY-MM-DD_repository-governance_audit.md`
- `YYYY-MM-DD_<target>_governance_audit.md`

Convert spaces and path separators to `-` and keep names short and stable
enough for later updates.

Use the structure from `references/report-template.md`.

The exported report must include these top-level sections:

- `Summary`
- `Governance Findings`
- `Ownership Map`
- `Coordination Gaps`
- `Rewrite Plan`
- `Open Questions`

For each governance finding include:

- `Status:` pending, accepted, discarded, or solved
- `Type:` Confirmed issue, Possible risk, or Suggestion
- `Severity:` critical, major, or minor
- `Category:` duplication, boundary, coordination, operationalization,
  verbosity, or artifact-value
- `Evidence:`
- `Why it matters:`
- `Recommended minimal fix:`
- `Discard explanation:`

Use stable finding IDs with the `GF-###` pattern.

## Review Rules

- Distinguish repository facts from recommendations.
- Do not invent automation that does not exist; call it a recommendation.
- Mark prose-only rules as defects when the workflow depends on them.
- Prefer fewer governance surfaces with clearer roles over more coordination
  docs or overlapping skills.
- Recommend new files only when no existing file has a clean ownership fit.
- Keep recommendations agent-readable and concise.
- Avoid generic markdown style advice unless it affects governance usability.

## Markdown Export Rules

When exporting or updating a governance audit:

- Write the report under `.codex/audits/` by default.
- Reuse the existing audit file for the same target when the filename still
  fits the current scope.
- Preserve stable finding IDs across later revisions.
- Start new findings as `pending` unless the user explicitly says otherwise.
- Mark findings `accepted` or `discarded` only when the user explicitly chooses
  that review outcome.
- Mark a finding `solved` only after the related repository change has been
  implemented and verified.
- Keep evidence concrete and repository-specific.
- Keep ownership-map, coordination-gap, and rewrite-plan sections concise and
  update-friendly.
