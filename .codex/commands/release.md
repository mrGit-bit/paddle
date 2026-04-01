# Release

Run the repository release automation for the supplied version argument.
This slash command is an optional wrapper around the primary entrypoint
`python scripts/release_orchestrator.py <version>`.

Command:

- `/prompts:release`

Version argument examples:

- `/prompts:release 1.6.0`
- `/prompts:release v1.6.0`

Execution rules:

- Run `python scripts/release_orchestrator.py "$ARGUMENTS"` from the repository
  root.
- Expect only the actually shipped loose specs to already be marked with the
  requested `Release tag: vX.Y.Z` before the release command runs.
- Leave unrelated in-progress loose specs on `Release tag: unreleased` so
  consolidation skips them.
- Keep the interaction focused on the script output.
- If the script reports missing prerequisites or pauses at the staging approval
  gate, surface that result directly instead of improvising extra release
  actions.
