# Agents Index

<!-- AGENT ROUTING
     Agents are user-spawnable workers with isolated context, explicit authority boundaries,
     and clean input/output contracts.
     Spawn only when: the task has a distinct authority boundary, risk profile,
     operating context, or delegation role.
     Stay inline (use a skill) when: the task is a reusable workflow, reasoning pattern,
     authoring/review activity, or short collaborative task.
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
