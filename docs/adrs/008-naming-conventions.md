# ADR-008: Naming Conventions for Skills, Agents, and Sub-agents

**Status**: Accepted  
**Date**: 2026-05-30

## Context

Early skill names (`implementation-sketch`, `requirement-study`, `architecture-design`) described the artifact or process, not the capability. They were long, hyphenated, and read like documentation headings rather than things you reach for. Agent and sub-agent names were inconsistent — some were role-nouns, some were descriptive compounds.

Names matter because they appear in INDEX.md routing tables, trigger queries, cross-references in SKILL.md files, and in conversation when humans invoke skills. A name that requires thinking to recall is a name that will be bypassed.

## Decision

Apply a single naming principle across all library definitions:

> **Name the action or role, not the artifact or process. Prefer one word. Omit everything redundant.**

### Skills

Skills are capabilities you invoke. Name them as **short action-nouns or verbs**.

| Pattern | Examples | Notes |
|---------|----------|-------|
| Single action-noun | `spike`, `brief`, `plan`, `scaffold`, `design`, `handoff`, `synthesis`, `consult` | Preferred |
| Hyphenated pair | `threat-model`, `test-plan` | Only when each word is load-bearing and the compound is an established term |

Rules:
- Prefer one word; add a second only when the concept is a compound noun in the domain
- Do not use the skill name as a prefix in the output filename (output names describe content, not the invoking skill)
- No `-study`, `-review`, `-analysis` suffixes — these describe the artifact, not the action

### Agents

Agents are workers you spawn. Name them as **single role-nouns**, preferring the `-er` form.

| Pattern | Examples |
|---------|----------|
| Role noun | `researcher`, `critic`, `distiller`, `phoenix`, `scout` |
| Short acronym | `sme` (when widely recognized) |

Rules:
- Single word only
- The name describes what the agent IS (its role), not what it produces

### Sub-agents

Sub-agents are atomic workers spawned by agents. Name them as **`[domain]-[role]`** compounds.

| Pattern | Examples |
|---------|----------|
| `[domain]-[role]er` | `web-searcher`, `doc-reader`, `assumption-checker`, `section-extractor` |

Rules:
- Two-part hyphenated compound: domain + role
- `[role]` should be the `-er` form (a worker noun)
- Keep both parts short; avoid three-word names

### Poly-maintainer guidance

When the `phoenix` agent proposes a new name, apply these tests in order:
1. Can it be one word? If yes, use one word.
2. Is the second word genuinely load-bearing (removes ambiguity)? If yes, add it.
3. Is the name a description of the artifact rather than the action? If yes, rename.
4. Does the name conflict with an existing skill, agent, or sub-agent name? If yes, rename.

## Consequences

- Existing skill names renamed (see ADR-007 for full list of old→new)
- INDEX.md routing entries updated
- All SKILL.md cross-references updated
- Curator AGENT.md updated with naming guidance
- Future phoenix proposals must pass the naming tests above before acceptance

## Rejected Alternatives

- **Verb-first names** (`specify`, `architect`, `synthesize`): Verbs as skill names are harder to use as nouns in cross-references ("use `specify` instead" reads awkwardly vs "use `brief` instead")
- **Domain-noun compounds for skills** (`requirements`, `architecture`, `security`): Too generic; these are the domains, not the capabilities
- **Consistent `-er` suffix for skills**: Skills are capabilities, not roles; the `-er` form implies a doer, which is right for agents but wrong for skills
