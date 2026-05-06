---
name: write-a-skill
description: Create or update rankingdepadel.club Codex skills with concise instructions, triggerable metadata, progressive disclosure, and repository validation. Use when the user asks to create, write, build, adapt, or revise a skill under .codex/skills.
---

# Write a Skill

Use this skill for repository-local Codex skills.

## Scope

- Target path: `.codex/skills/<skill-name>/`.
- Required file: `SKILL.md`.
- Recommended file: `agents/openai.yaml` for UI metadata.
- Optional folders: `references/`, `scripts/`, and `assets/` only when they
  directly support the skill.
- Do not add auxiliary docs such as `README.md`, quick references, or
  changelogs inside a skill.

## Workflow

1. Verify the branch before editing. If not on `develop`, warn and wait.
2. Gather enough requirements from the user and repository context:
   - task or domain the skill covers
   - trigger phrases and situations
   - expected workflow or decision points
   - whether deterministic scripts, references, or assets are needed
3. Inspect nearby skills for tone, section shape, and metadata style.
4. Draft or update `SKILL.md` with concise frontmatter and only core workflow
   instructions.
5. Add one-level-deep references only when optional detail would otherwise
   bloat `SKILL.md`.
6. Add scripts only for repeatable, deterministic work that Codex would
   otherwise regenerate.
7. Add or refresh `agents/openai.yaml` when the skill should appear in the UI.
8. If router instructions change, update `AGENTS.md` and keep its
   version/date header aligned with `docs/PROJECT_INSTRUCTIONS.md`.
9. Validate changed Markdown and governance metadata.

## SKILL.md Rules

- Frontmatter must include `name` and `description`.
- Use kebab-case for `name` and the directory.
- The description is the trigger surface; make it specific.
- Prefer two description sentences:
  - what the skill does
  - `Use when ...` with concrete triggers
- Keep the body compact and procedural.
- Trust Codex's general knowledge; include only repo-specific workflow,
  constraints, edge cases, or validation steps.
- Keep detailed examples out unless they prevent likely mistakes.

## Progressive Disclosure

- Keep `SKILL.md` under 100 lines when practical.
- Split details into `references/<topic>.md` when a section is long, rarely
  needed, or domain-specific.
- Link every reference directly from `SKILL.md` and state when to read it.
- Avoid nested reference chains.

## Local UI Metadata

Use this shape unless the repository has changed its convention:

```yaml
display_name: Skill Name
short_description: Short human-facing purpose.
default_prompt: Use $skill-name to ...
```

Keep `default_prompt` short and include the `$skill-name` invocation.

## Validation

- Run `python scripts/validate_governance.py` after governance or router edits.
- Run markdownlint on changed Markdown files when available; `MD013` is
  non-blocking.
- For scripts added to a skill, run their smallest meaningful check.
