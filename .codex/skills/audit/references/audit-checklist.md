# Audit Checklist

## Access Control

- Does the view enforce ownership where needed?
- Is `login_required` or equivalent protection present where appropriate?
- Can direct URL access bypass intended restrictions?

## View Responsibility

- Is the view doing too much orchestration, validation, and formatting?
- Should form validation or helper logic be reused instead of embedded in the view?
- Is the template carrying business decisions that belong in Python?

## Query Efficiency / Duplication

- Is queryset construction repeated across multiple views?
- Are filtering or ordering patterns duplicated without a shared helper?
- Is the same related-data loading logic repeated?

## Performance / ORM Efficiency

- Are there likely N+1 query patterns?
- Is `select_related` or `prefetch_related` obviously missing?
- Is a large queryset evaluated too early?
- Are indexes likely missing for repeated filter or ordering paths?

## Reuse of Forms/Helpers

- Does the code bypass an existing form, helper, or shared utility?
- Is validation duplicated across view and template layers?
- Can a smaller reuse-based fix solve the issue?

## Template Boundary Enforcement

- Is there business logic in the template?
- Is JavaScript duplicating backend or template responsibilities?
- Does the template violate the Spanish UI text rule?

## Tests

- Do tests cover permissions, happy path, and likely edge cases?
- Are new findings already protected by existing tests?
- Is the smallest realistic test scope clear?

## Governance Compliance

- Does the implementation drift from the approved spec?
- Does it introduce deprecated DRF or API usage?
- Are recommendations minimal and free of unrelated cleanup?
