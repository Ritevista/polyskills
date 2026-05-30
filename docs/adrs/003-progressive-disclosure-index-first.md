# ADR-003: Progressive Disclosure via INDEX.md-First Loading

**Status**: Accepted
**Date**: 2026-05-30

## Context

With 10 skills, 6 agents, and 4+ sub-agents, loading all definitions at session start would consume significant context. The open Agent Skills specification, Anthropic, and Codex documentation all recommend progressive disclosure: agents see only lightweight routing metadata at session start, then load the full definition only on match.

## Decision

Three-level loading model:

1. **Session start** — agent loads `STEERING.md` (repo state) + `skills/INDEX.md` + `agents/INDEX.md`
2. **On match** — agent loads `skills/<name>/SKILL.md` or `agents/<name>/AGENT.md`
3. **During execution** — agent loads `references/`, runs `scripts/`, reads `assets/` only as needed

`STEERING.md` is always loaded first (it tells the agent what the repo is and what's active).
No agent or skill loads all definitions speculatively — this is a hard rule.

## Rationale

- Keeps base context O(1) regardless of library size
- Matches the loading model described in the open Agent Skills spec and confirmed across major vendor implementations
- INDEX.md entries are one line each — the routing cost is minimal
- STEERING.md gives the agent enough context to route correctly without reading everything

## Consequences

- **Easier**: adding new skills/agents without increasing session-start context cost
- **Harder**: INDEX.md must be kept in sync with actual definitions (validator checks this)
- **Watch for**: agents loading full SKILL.md for multiple candidates before deciding — this defeats progressive disclosure

## Alternatives Considered

- **Load all definitions at session start** — simpler but context-expensive and doesn't scale
- **No INDEX.md, route by filename** — loses the trigger/routing metadata that makes matching reliable
