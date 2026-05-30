# STEERING.md — polyskills Control Plane

<!-- AGENT PROTOCOL
     Read this file first. It tells you what this repo is, what is active,
     and how to route work. After reading: load skills/INDEX.md or agents/INDEX.md.
     Never load all SKILL.md / AGENT.md files speculatively.
-->

## What This Repo Is

**polyskills** — lean, principled, multi-agent skill library.
Write skills once, deploy across Claude Code, Codex, Kiro, Gemini, OpenClaw, Cursor, Windsurf, Cline, and Amp.

```
STEERING.md          ← you are here (read first)
skills/INDEX.md      ← route user tasks to skills
agents/INDEX.md      ← route to spawnable worker agents
sub-agents/INDEX.md  ← atomic workers spawned by agents
common-skills/       ← shared reasoning patterns (confidence-rating, output-formatting, quality-checklist)
docs/guides/         ← reference knowledge loaded by agents and skills
  skill-writing-guide.md  ← phoenix loads before drafting any definition
  steering-guide.md       ← scaffold skill loads when producing new project structure
```

## Routing Protocol

```
Request arrives
    │
    ▼
Load skills/INDEX.md → match? → load SKILL.md → execute
    │
    └─ no match → load agents/INDEX.md → spawn worker agent
                      │
                      └─ worker may spawn sub-agents from sub-agents/INDEX.md
```

## Current State (2026-05-30)

| Layer | Count | Ceiling | Status |
|-------|-------|---------|--------|
| skills/ | 2 | 10 | ✅ synthesis, handoff |
| agents/ | 1 | 6 | ⏳ Built on demand via phoenix |
| sub-agents/ | 0 | none | ⏳ Built on demand as agents need them |
| common-skills/ | 3 | none | ✅ Complete |
| templates/ | 3 | — | ✅ Complete |
| docs/adrs/ | 7 | — | ✅ Complete |
| docs/specs/ | 2 | — | ✅ Complete |
| scripts/validate.py | — | — | ✅ Complete |
| .github/workflows/ | — | — | ✅ Complete |

## Agents (1 of 6)

| Agent | Role | Key capability |
|-------|------|---------------|
| phoenix | worker | library maintenance and extension |

## Sub-Agents (0)

None yet. Added as parent agents need them.

## Active Work

| Item | Status | Next action |
|------|--------|-------------|
| Skills build-out | 🔄 On demand | synthesis + handoff live; add next skill when real gap emerges |
| GitHub publish | 🔄 Ready | Create repo and push (skills pass, zero errors) |
| Kiro DAG adapter | ⏳ Pending | Wire parent→child in adapters/kiro/ |
| MCP wiring guide | ⏳ Pending | See mcp-servers/README.md |

## Skills (2 of 10)

| Skill | Purpose |
|-------|---------|
| `synthesis` | Distil messy multi-source gap signals into a single clear finding |
| `handoff` | Capture session state for resumption by next session or agent |

## Blocked / Decision Needed

_None currently._

## MCP Wiring Status

| MCP | Wired | Unlocks |
|-----|-------|---------|
| Gmail | ❌ | mail operations |
| GitHub | ❌ | github skill (PRs, reviews, repo ops) |
| GitLab | ❌ | gitlab skill (MRs, pipelines, reviews) |
| Google Calendar | ❌ | scheduling |
| Web Search | ❌ | research agents |
| Filesystem | ❌ | local doc ingestion |

## Key Design Decisions (ADRs)

| ADR | Decision |
|-----|---------|
| 001 | Two-tier agent architecture (agents + sub-agents) |
| 002 | Six-layer skill structure |
| 003 | Progressive disclosure via INDEX.md-first loading |
| 004 | Cross-platform frontmatter (name + description portable core) |
| 005 | Library ceilings (10 skills, 6 agents) |
| 006 | MCP-first for tool capabilities |
| 007 | Phoenix as library self-extension mechanism |

## Constraints

- Max 10 skills, max 6 agents — see ADR-005
- No skill logic in adapters
- No tool/system access inside SKILL.md — use MCP
- Descriptions under 200 chars (portability)
- Run `python scripts/validate.py` before every commit
