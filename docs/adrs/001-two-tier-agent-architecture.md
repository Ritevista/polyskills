# ADR-001: Two-Tier Agent Architecture (agents + sub-agents)

**Status**: Accepted
**Date**: 2026-05-30

## Context

The original polyagent-skills repo had 34 skills, many of which were role definitions (entrepreneur, business-strategist, visionary-futurist) blended with process skills. This made routing unreliable and context expensive. As we redesigned, we needed a clear distinction between reusable process patterns (skills), user-spawnable workers (agents), and atomic delegated workers (sub-agents).

A further need emerged: some agent tasks are naturally atomic and parallelizable (checking one input, reading one document, verifying one assumption). Bundling these into the parent agent's context defeats the purpose of isolation.

## Decision

Two-tier agent architecture:

- **`agents/`** — user-spawnable workers. Multi-step, role-oriented, isolated context. Each agent must justify itself through a distinct authority boundary, risk profile, operating context, or delegation role. Agents may themselves spawn sub-agents.
- **`sub-agents/`** — atomic workers spawned BY agents. Single-task, tiny context budget, clean input/output contract. No further spawning. No ceiling.

Workflows that do not require an agent boundary remain skills.

## Rationale

- Separates role/authority boundaries from reusable task procedures
- Sub-agents enable parallelism within an agent's execution when the work is atomic and contract-shaped
- Agents remain at a human-manageable ceiling; sub-agents grow only as parent agents prove they need them
- Flat deployment to Claude Code / Cursor / Gemini (no nesting in those platforms) is handled by the install script copying both tiers into the tool's flat `agents/` directory

## Consequences

- **Easier**: reasoning about why an agent exists, parallelizing bounded work, avoiding skill/agent confusion
- **Harder**: sub-agent stubs in tool dirs can accumulate; install script must keep them in sync
- **Watch for**: workflows being promoted into agents merely because they are common; sub-agents that grow complex enough to warrant becoming agents

## Alternatives Considered

- **Single `agents/` directory with a `type` field** — simpler but loses the structural clarity that sub-agents are never user-invoked
- **No sub-agents, everything in agent context** — loses parallelism on platforms that support it
