# ADR-001: Two-Tier Agent Architecture (agents + sub-agents)

**Status**: Accepted
**Date**: 2026-05-30

## Context

The original polyagent-skills repo had 34 skills, many of which were role definitions (entrepreneur, business-strategist, visionary-futurist) blended with process skills. This made routing unreliable and context expensive. As we redesigned, we needed a clear distinction between role-oriented workers (agents) and process patterns (skills).

A further need emerged: some agent tasks are naturally atomic and parallelizable (a single web search, reading one document, checking one assumption). Bundling these into the parent agent's context defeats the purpose of isolation.

## Decision

Two-tier agent architecture:

- **`agents/`** — user-spawnable workers. Multi-step, role-oriented, isolated context. Can themselves spawn sub-agents. Ceiling: 6.
- **`sub-agents/`** — atomic workers spawned BY agents. Single-task, tiny context budget. No further spawning. No ceiling.

## Rationale

- Separation matches how Kiro (DAG), Cursor (worktrees), and Cline (use_subagents) model the distinction natively
- Sub-agents enable parallelism within an agent's execution (e.g., researcher fires 5 web-searchers simultaneously)
- Agents remain at a human-manageable ceiling; sub-agents grow freely as needed
- Flat deployment to Claude Code / Cursor / Gemini (no nesting in those platforms) is handled by the install script copying both tiers into the tool's flat `agents/` directory

## Consequences

- **Easier**: parallelizing agent work, reasoning about what a single agent does
- **Harder**: sub-agent stubs in tool dirs can accumulate; install script must keep them in sync
- **Watch for**: sub-agents that grow complex enough to warrant becoming agents

## Alternatives Considered

- **Single `agents/` directory with a `type` field** — simpler but loses the structural clarity that sub-agents are never user-invoked
- **No sub-agents, everything in agent context** — loses parallelism on platforms that support it
