# Governance Review Rubric

Use this file only when you need a compact rubric while reviewing governance
markdown.

## Categories

- `duplication`: the same rule or instruction is repeated across files without a
  clear reason
- `boundary`: a file owns guidance that should belong to another file, or file
  roles are unclear
- `coordination`: related docs or workflows drift because the connection between
  them is manual or underspecified
- `operationalization`: governance says a rule exists, but no command, template,
  workflow hook, or observable practice makes it reliable
- `verbosity`: wording is harder to execute than necessary for an agent
- `artifact-value`: required artifacts are over-detailed, stale, unused, or not
  pulling their weight in the workflow

## Severity

- `critical`: contradictory authority, unworkable workflow expectations, or
  rules that must be followed but have no reliable operational path
- `major`: duplicated guidance, unclear ownership, drift-prone coordination, or
  process artifacts that create recurring friction
- `minor`: readability, structure, or brevity issues that do not materially
  break the workflow

## Default Recommendations

- Consolidate before adding files.
- Keep one source of truth per rule.
- Keep README focused on current-state orientation, not release history.
- Treat manual-only cross-file coordination as a defect, not a preference.
- Challenge spec/plan detail when it is not reused in execution.
