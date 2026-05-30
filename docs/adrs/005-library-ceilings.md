# ADR-005: Library Ceilings (Skills and Agents)

**Status**: Accepted
**Date**: 2026-05-30

## Context

The original polyagent-skills repo had 34 skills with significant overlap. Many were role definitions rather than process skills. The primary symptom: routing became unreliable because too many skills had similar trigger conditions, and maintaining 34 definitions was unsustainable.

## Decision

- **Skills ceiling: 10** — if a new skill would be added, an existing one must be proven non-overlapping or replaced
- **Agents ceiling: 6** — same rule; raise explicitly with documented rationale
- **Sub-agents: no ceiling** — they are atomic and naturally bounded by their parent's needs
- **Common-skills: no ceiling** — shared patterns that earn their own file are always welcome

Ceilings are enforced by the validator (warning) and by the INDEX.md rule:
> "Add only by replacing an existing one or raising the ceiling explicitly."

## Rationale

- Overlap is the primary failure mode for skill libraries — ceilings force the question "does this really need to be separate?"
- Sub-agents don't need a ceiling because they're single-task and don't contribute to routing ambiguity
- Common-skills don't need a ceiling because they're referenced, not routed to

## Consequences

- **Easier**: routing stays reliable, library stays maintainable
- **Harder**: adding a genuinely new skill requires justifying it against the ceiling
- **Watch for**: ceiling being raised without documenting why — update this ADR when raised

## Current counts (2026-05-30)

| Layer | Count | Ceiling |
|-------|-------|---------|
| skills/ | 0 (in progress) | 10 |
| agents/ | 6 | 6 |
| sub-agents/ | 4 | none |
| common-skills/ | 3 | none |

## Alternatives Considered

- **No ceiling** — led to the 34-skill problem in the predecessor repo
- **Ceiling of 5 skills** — too restrictive for a reference implementation
