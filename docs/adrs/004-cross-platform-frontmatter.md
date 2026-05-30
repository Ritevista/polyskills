# ADR-004: Cross-Platform Frontmatter Format

**Status**: Accepted
**Date**: 2026-05-30

## Context

Claude Code, Cursor, and Gemini CLI all use YAML frontmatter in markdown agent definition files, and all three converge on `name` and `description` as the minimum required fields. Tool names in the `tools` field differ across platforms.

Anthropic's API docs allow descriptions up to 1024 chars; Anthropic's Help Center recommends under 200 chars for consumer UI portability; the open spec allows 1024. This inconsistency needs a practical resolution.

## Decision

Canonical frontmatter for all `AGENT.md` and `SKILL.md` files:

```yaml
---
name: [lowercase-hyphenated, matches directory name]
description: "[Under 200 chars. Routing logic: when to use, when not, what output.]"
# --- polyskills metadata (tools ignore unknown fields) ---
role: worker | agent | sub-agent
version: "1.0.0"
---
```

- `name` + `description` are the portable core — used by all three platforms
- polyskills-specific fields (`role`, `version`, `context-budget`, `spawned-by`) are ignored by tools but used by the validator and phoenix
- `tools` field is added only in the tool-specific adapter files (`.claude/agents/`, `.cursor/agents/`, `.gemini/agents/`) — not in the canonical definition
- Description target: under 200 chars (conservative, works everywhere)

## Rationale

- Write once: canonical `agents/<name>/AGENT.md` is the source of truth
- Tool-specific directories receive copies/symlinks with tool-appropriate `tools` fields added by the install script
- Unknown YAML fields are silently ignored by all three platforms

## Consequences

- **Easier**: one canonical definition, no translation needed
- **Harder**: tool-specific `tools` field must be maintained separately in adapter files
- **Watch for**: descriptions creeping over 200 chars (validator warns, does not error)

## Alternatives Considered

- **Tool-specific canonical files** — more control but duplication and divergence risk
- **No `tools` field anywhere** — portable but loses tool restriction capability for Claude Code
