# Agents Index

<!-- AGENT ROUTING
     Agents are user-spawnable workers with isolated context and clean I/O.
     Spawn when: task is parallelizable, benefits from fresh context,
     or has a fixed input/output contract.
     Stay inline (use a skill) when: task is iterative, collaborative, or short.
-->

| Agent | Trigger | Sub-agents it uses | MCP | AGENT.md |
|-------|---------|-------------------|-----|----------|
| phoenix | add/fix/sync anything in the polyskills library | none | — | agents/phoenix/AGENT.md |

## Agent Count Rule

Ceiling: **6**. Current: 1.
Agents are added via phoenix as real use cases emerge — not speculatively.

## Tool-Specific Directories

| Tool | Location | Notes |
|------|----------|-------|
| Claude Code | `.claude/agents/` | flat layout |
| Cursor | `.cursor/agents/` | flat layout |
| Gemini CLI | `.gemini/agents/` | flat layout |
| Kiro | `adapters/kiro/` | DAG adapter wires parent→child |
| Cline / Amp | inline spawn | use AGENT.md as brief template |

## Sub-Agents

See `sub-agents/INDEX.md`. Added as parent agents need them — not speculatively.
