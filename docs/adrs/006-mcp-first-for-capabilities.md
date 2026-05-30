# ADR-006: MCP-First for Tool Capabilities

**Status**: Accepted
**Date**: 2026-05-30

## Context

Skills in polyagent-skills attempted to provide both reasoning instructions AND tool capabilities (e.g., mail-summarizer tried to describe how to think about email AND access email). This conflated two distinct concerns and produced skills that were useless without the underlying capability.

## Decision

**Skills are reasoning patterns. MCPs are capabilities.**

- A skill tells the agent HOW to think and what process to follow
- An MCP gives the agent ACCESS to a system (Gmail, GitHub, Calendar, filesystem)
- A skill that requires a tool capability MUST declare it in `metadata.mcp-required` and degrade gracefully when unavailable
- No skill embeds tool-specific API logic — that belongs in a script or MCP server

Skills note their MCP requirements in frontmatter:
```yaml
metadata:
  mcp-required: [web-search]
  mcp-recommended: [github]
```

## Rationale

- Skills without their required MCP are still readable and partially useful (they teach the reasoning)
- MCP wiring is environment-specific; skills are portable
- Coupling capability to skill creates skills that silently fail in environments without the MCP
- `mcp-servers/README.md` documents which MCPs to wire and what they unlock

## Consequences

- **Easier**: skills work across environments with different MCP availability
- **Harder**: some skills are limited without their MCP; user must wire MCPs separately
- **Watch for**: skills embedding API calls or tool-specific shell commands in procedure steps

## Alternatives Considered

- **Skills embed capability** — faster to use but breaks portability and creates dead skills when MCP unavailable
- **One skill per MCP** — too fine-grained; skills should map to user tasks, not tool surfaces
