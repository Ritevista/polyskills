# ADR-002: Six-Layer Skill Structure

**Status**: Accepted
**Date**: 2026-05-30

## Context

Previous skills (from polyagent-skills) were monolithic Markdown files — a mix of purpose, process steps, and quality checks with no consistent structure. This made them hard to route, hard to test, and prone to bloat. The open Agent Skills specification and research across OpenAI, Anthropic, and VS Code guidance converge on a layered approach.

## Decision

Every `SKILL.md` must contain six layers in order:

1. **Routing** — when to use, when NOT to use (near-miss redirects)
2. **Contract** — exact inputs, exact outputs, success criteria
3. **Reasoning** — how to think about this class of problem
4. **Procedure** — ordered steps
5. **Edge Cases** — named gotchas and exceptions
6. **Quality Gates** — verifiable pre-delivery checks

Deterministic mechanics go in `scripts/`. Reference material goes in `references/`. Output templates go in `assets/`. Trigger evaluation test cases go in `evals/trigger_queries.json`.

## Rationale

- Routing layer enables lightweight INDEX.md-first dispatch without loading full SKILL.md
- Contract layer makes skills composable — downstream agents know what to expect
- Reasoning layer encodes domain judgment that procedural steps cannot capture
- Edge case layer prevents silent failures on common boundary conditions
- Quality gates provide a machine-checkable stop condition
- Separating scripts/references/assets matches the open Agent Skills spec's progressive disclosure model

## Consequences

- **Easier**: testing (each layer is independently checkable), routing (description is the single boundary), composability
- **Harder**: authoring new skills takes more upfront thought; phoenix must follow the template strictly
- **Watch for**: reasoning layer becoming a second procedure layer (it should encode heuristics, not steps)

## Alternatives Considered

- **Flat SKILL.md with no required sections** — authoring is faster but skills become inconsistent and hard to test
- **Four layers (no reasoning, no edge cases)** — lighter but misses the class of failures that come from wrong mental model and boundary conditions
