Run the repository release automation for the supplied version argument.

Usage:

- `/release 1.6.0`
- `/release v1.6.0`

Execution rules:

- Run `python scripts/release_orchestrator.py "$ARGUMENTS"` from the repository
  root.
- Keep the interaction focused on the script output.
- If the script reports missing prerequisites or pauses at the staging approval
  gate, surface that result directly instead of improvising extra release
  actions.
