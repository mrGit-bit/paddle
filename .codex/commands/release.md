# Release

Run the repository release automation for the supplied version argument.
This slash command is an optional wrapper around the primary entrypoint
`python scripts/release_orchestrator.py <version>`.

Command:

- `/prompts:release`

Version argument examples:

- `/prompts:release 1.6.0`
- `/prompts:release v1.6.0`
- `/prompts:release --next-patch`

Execution rules:

- Run `python scripts/release_orchestrator.py "$ARGUMENTS"` from the repository
  root.
- Expect only closure-complete loose specs to be prepared for shipment:
  `Status: implemented` (or `shipped` if already reconciled) plus the
  requested `Release tag: vX.Y.Z`.
- Leave unrelated in-progress loose specs on `Status: approved` with
  `Release tag: unreleased` so consolidation skips them.
- Treat closure-complete loose specs left at `Release tag: unreleased` as a
  release-blocking metadata error, not as unrelated work.
- Keep the interaction focused on the script output.
- Keep release sessions context-light: summarize long-running command progress
  instead of pasting repeated poll output, avoid full diffs unless diagnosing a
  failure, and report only the decision-relevant lines from GitHub, SSH deploy,
  and validation commands.
- If the script reports missing prerequisites or pauses at the staging approval
  gate, surface that result directly instead of improvising extra release
  actions.
- Treat the initial release request as permission to reach staging only. Never
  promote staging to production unless the user explicitly approves production
  promotion after the staging manual checks, or supplies the documented
  `--staging-approved` resume command.
