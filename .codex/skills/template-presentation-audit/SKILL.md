---
name: template-presentation-audit
description: Audit a specific Django template's presentation for same-page UI coherence, CSS reuse, cascade conflicts, computed-style mismatches, and responsive layout risks. Use when the user asks to review or audit the presentation of one template, compare cards/controls/sections inside the same page, diagnose CSS cascade or inherited computed-style issues, or prevent visual inconsistencies before implementation.
---

# Template Presentation Audit

Use this skill only with a concrete target template path. If the user does not
provide one, ask for the template path before auditing.

## Required Input

- Target Django template path, for example
  `paddle/frontend/templates/frontend/player_detail.html`.
- Optional focus area, such as card groups, buttons, wheels, headings, mobile
  layout, or a reported visual mismatch.

## Workflow

1. Read `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` for project constraints.
2. Read the target template and identify its rendered UI groups:
   - section headings
   - repeated cards or rows
   - buttons rendered as cards
   - includes/partials
   - JavaScript hooks that toggle state classes
3. Trace every class used by the target UI through CSS files, included
   partials, and shared base templates.
4. Compare equivalent elements inside the same page before judging style:
   - same role, same visual component, same interaction state
   - active/inactive/empty variants
   - link, button, and plain-card variants
5. Audit cascade and computed-style risks:
   - inherited fonts from broad selectors such as `button`, `a`, `body`, or
     heading rules
   - user-agent defaults on native controls, especially `button` padding,
     border, font, display, alignment, and appearance
   - Bootstrap utility classes overriding or competing with component classes
   - selector specificity/order where state classes must override base classes
   - shared partials rendered under different ancestors with different
     inherited styles
6. When possible, verify computed styles with a browser or rendered HTML. If a
   browser is unavailable, state that limitation and base findings on cascade
   tracing from source.
7. Recommend fixes that reuse existing component classes or reset the divergent
   ancestor. Prefer narrow, colocated selectors over broad global changes.
8. Suggest focused regression tests for class presence, absence of obsolete
   overrides, state class combinations, or rendered heading/card structure.

## Finding Criteria

Surface only medium or high severity findings.

- **High:** likely broken layout, inaccessible interaction, hidden content,
  inconsistent rendered state that users will notice, or a cascade issue that
  affects multiple repeated elements.
- **Medium:** visible same-page inconsistency, inherited computed-style
  mismatch, duplicate component styling, or fragile selector order that is
  likely to regress.
- **Low:** purely cosmetic preference with no clear inconsistency. Mention only
  in a short note if useful; do not list as an active finding.

## Report Shape

Lead with findings, ordered by severity. For each finding include:

- Severity
- Location: template line and CSS selector/file when known
- Evidence: why the computed or inherited style differs
- Root cause: cascade, markup variant, utility class, state class, or partial
  context
- Recommended fix: narrow change reusing existing page/component styles
- Suggested test or manual check

If there are no medium/high findings, say so clearly and list residual risk,
such as lack of browser-computed-style verification.

## Guardrails

- Do not implement fixes unless the user explicitly asks for implementation.
- Do not introduce new component systems for one-off mismatches.
- Do not rely only on screenshot appearance when source cascade explains the
  issue; connect visual symptoms to selectors or markup.
- Do not ignore native element defaults when a visual component is rendered as
  a `button`, `a`, `input`, or `select`.
- Keep Spanish UI text unchanged unless the audit scope explicitly includes
  copy review.
