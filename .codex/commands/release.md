# Release

Run the repository release automation for the supplied version argument.

Command:

- `/prompts:release`

Version argument examples:

- `/prompts:release 1.6.0`
- `/prompts:release v1.6.0`

Execution rules:

- Run `python scripts/release_orchestrator.py "$ARGUMENTS"` from the repository
  root.
- Treat loose non-release specs/plans marked `Release tag: unreleased` as the
  pending release set and stamp the shipped `vX.Y.Z` during consolidation.
- Keep the interaction focused on the script output.
- If the script reports missing prerequisites or pauses at the staging approval
  gate, surface that result directly instead of improvising extra release
  actions.
