---
name: debug
description: Disciplined debugging loop for broken behavior, failing tests, exceptions, flaky failures, and performance regressions. Use when the user says "debug this", "diagnose this", "this is broken", "this is failing", or reports a reproducible or intermittent bug.
---

# Debug

Use this skill for bugs where the cause is not already confirmed. Skip a phase
only when the reason is explicit.

## Goal

Convert a reported symptom into a fast, repeatable pass/fail signal, use that
signal to test falsifiable hypotheses, then preserve the fix with the narrowest
meaningful regression coverage.

## Phase 1: Build The Loop

Before hypothesizing, create the smallest agent-runnable feedback loop that
shows the bug or raises its reproduction rate enough to debug.

Prefer loops in this order:

1. Focused failing test at the seam that reaches the real bug.
2. Django test client or HTTP request against the affected view.
3. CLI, management command, or script with fixture input and expected output.
4. Browser or DOM harness when the bug is UI-only.
5. Replay of captured logs, payloads, database rows, or request artifacts.
6. Throwaway harness around the smallest callable path.
7. Repeated stress loop for flaky, timing, ordering, or data-dependent bugs.
8. Bisect or differential loop when old and new behavior can be compared.

Improve the loop before moving on:

- Make it faster by narrowing setup and scope.
- Make it sharper by asserting the exact symptom.
- Make it deterministic by pinning time, randomness, data, and external IO.

If no useful loop is possible, stop and state what was tried. Ask for the
missing artifact or access needed to reproduce the bug.

## Phase 2: Reproduce

Run the loop and confirm it matches the user's reported failure.

- Capture the exact symptom: exception, wrong output, missing record, visual
  state, query count, timing, or log line.
- Confirm repeated failures, or for flakes, confirm the reproduction rate is
  high enough to guide changes.
- Avoid fixing a nearby failure unless it is proven to be the same bug.

## Phase 3: Hypothesize

Write 3 to 5 ranked hypotheses before changing code.

Each hypothesis must be falsifiable:

- Name the suspected cause.
- State what evidence would support it.
- State what evidence would rule it out.
- Choose the first probe that separates it from the other hypotheses.

Share the ranked list when the user is available, but keep moving with the best
current ranking if they are not.

## Phase 4: Instrument

Probe one hypothesis at a time.

- Prefer debugger, REPL, targeted assertions, or focused test output over broad
  logging.
- If logs are needed, tag temporary lines with a unique `[DEBUG-...]` prefix.
- For performance regressions, establish a baseline measurement before changing
  code.
- Change one variable per probe so the result actually teaches something.

## Phase 5: Fix And Lock Down

Turn the minimized reproduction into a regression test before the fix when
there is a correct seam.

A correct seam exercises the real bug pattern at or near the call site. Do not
add a shallow test that passes while the real path remains broken.

Fix workflow:

1. Add or adapt the focused failing check.
2. Confirm it fails for the expected reason.
3. Apply the smallest fix that addresses the confirmed cause.
4. Confirm the focused check passes.
5. Re-run the original loop from Phase 1.

If no correct seam exists, document that limitation and why the architecture
prevents reliable regression coverage.

## Phase 6: Clean Up

Before declaring the bug fixed:

- Re-run the original reproduction loop.
- Run the focused regression test or document why none was added.
- Remove all `[DEBUG-...]` instrumentation.
- Delete throwaway harnesses unless they are intentionally kept as tests or
  clearly named debug artifacts.
- State the confirmed root cause and the validation command in the final
  response.

## Repository Notes

- Respect the active SDD workflow for non-trivial implementation work.
- Use `$test-design` when deciding where regression coverage belongs.
- Use `$template-presentation-audit` for template CSS, cascade, and responsive
  presentation bugs that require visual coherence review.
- Keep temporary debug files out of release artifacts unless they become
  maintained tests or scripts.
