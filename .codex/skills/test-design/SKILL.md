---
name: test-design
description: Use for rankingdepadel.club test creation, TDD loops, test refactors, brittle assertion reviews, and choosing behavior-focused validation that avoids coupling tests to incidental copy, markup, CSS text, or implementation details.
---

# Test Design

Use this skill when adding, changing, or reviewing tests.

## Goal

Tests should protect user-visible behavior, business rules, accessibility,
layout contracts, and regression risk without blocking harmless implementation
or wording changes.

## Testing Principles

- Test the contract, not the current code shape.
- Prefer public behavior, rendered structure, semantic state, and persisted data
  over private helpers, exact HTML snippets, or full CSS declarations.
- Assert exact copy only when the wording is the contract, such as legal text,
  accessibility labels, error messages, navigation labels, or user-confirmed
  product language.
- For helper text and descriptive microcopy, prefer structural or semantic
  assertions unless the task explicitly changes the wording contract.
- Keep tests narrow enough to identify the broken behavior, not every incidental
  detail on the page.
- Do not remove meaningful assertions only to make a change pass; replace
  brittle assertions with stronger contract-level checks.

## TDD Loop

For non-trivial behavior changes, prefer a vertical red-green-refactor loop:

1. Add one test for one observable behavior.
2. Run it and confirm it fails for the expected reason.
3. Implement the smallest change that makes it pass.
4. Run the focused test again.
5. Repeat for the next behavior.
6. Refactor only while tests are green.

Avoid writing all tests before implementation. Keep each test tied to public
behavior, rendered structure, persisted data, permissions, ordering, or another
stable contract.

## Preferred Assertions

- Business logic: computed records, queryset scope, permissions, ordering,
  thresholds, empty states, and database effects.
- Template behavior: expected section exists, relevant cards render in the
  right area, required classes or attributes are present, links and buttons
  have the intended state.
- Accessibility: stable `aria-label`, `aria-pressed`, `aria-disabled`, roles,
  form labels, and focusable controls when they define usability.
- Style coherence: shared component classes, state-class combinations, absence
  of obsolete one-off classes, and cascade-sensitive class pairings.
- Responsive/presentation risk: use `$template-presentation-audit` when the
  concern is computed style, same-page visual consistency, or CSS cascade.

## Avoid By Default

- Full visible-copy assertions for labels that product can safely rename.
- Exact rendered HTML strings when a parser, selector, class check, or response
  context assertion would express the behavior better.
- Exact CSS declaration blocks unless the declaration itself is the contract.
- Assertions against private helper names, temporary variable names, or internal
  grouping unless no public behavior exposes the risk.
- Snapshot-style tests that fail on harmless formatting, ordering, or copy
  changes.

## Refactoring Brittle Tests

When a test fails after a small wording or markup change:

1. Identify the behavior the old assertion was trying to protect.
2. Decide whether the exact wording is part of that behavior.
3. If not, replace the assertion with a contract-level check.
4. Preserve coverage for regressions the old assertion caught, such as removed
   sections, wrong card counts, broken links, missing empty states, or lost
   accessibility state.
5. Run the smallest relevant test scope and report the command plus result.

## Examples

- Instead of asserting a full helper label like
  `Víctimas: efic&gt;60% y más victorias`, assert the `Contendientes` section
  contains the victim card group, the expected empty/data cards, and the
  accessibility labels that describe the actual records.
- Instead of asserting a full CSS block, assert the shared component selector
  exists and the state class that must override it is covered by a colocated
  combined selector.
