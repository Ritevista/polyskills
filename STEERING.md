# STEERING.md — polyskills Control Plane

<!-- AGENT PROTOCOL
     Read this file first. It tells you what this repo is, what is active,
     and how to route work. After reading: load skills/INDEX.md or agents/INDEX.md.
     Never load all SKILL.md / AGENT.md files speculatively.
-->

## What This Repo Is

**polyskills** — lean, principled, multi-agent skill library.
Write skills once, deploy across Claude Code, Codex, Kiro, Gemini, Cursor, Windsurf, Cline, and Amp.

```
STEERING.md          ← you are here (read first)
skills/INDEX.md      ← route user tasks to skills
agents/INDEX.md      ← route to spawnable worker agents
sub-agents/INDEX.md  ← atomic workers spawned by agents
common-skills/       ← shared reasoning patterns
docs/guides/         ← reference knowledge loaded by agents and skills
  skill-writing-guide.md  ← phoenix loads before drafting any definition
  steering-guide.md       ← load when producing new project structure
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

---

## Doctrine

### 1. Phoenix is narrow

Phoenix maintains the polyskills ecosystem. It owns skill lifecycle, agent lifecycle, steering, ADRs, and repository consistency. That is its entire job.

Phoenix is **not** a universal assistant. It does not write documents for other projects, does not review code outside this repo, does not perform operational work on external systems, and does not become a catch-all when no other agent exists.

If a task is not about the polyskills library itself, it does not belong to phoenix.

### 2. Agents are rare

An agent requires a distinct justification from this list:

- **Authority boundary** — the agent is permitted to do things the main session agent is not (e.g., touch external systems)
- **Risk profile** — the agent's blast radius is different enough to warrant explicit isolation and gating
- **Operating context** — the agent needs a clean context free of the main conversation to do its job
- **Delegation role** — the agent coordinates sub-agents or parallelizes work that benefits from isolation

A workflow existing is not sufficient justification. Most capabilities should begin as skills and stay there unless one of the above is clearly true. Do not create `docsmith-agent`, `review-agent`, `tester-agent`, or `requirements-agent` merely because those workflows exist.

### 3. Operator is the candidate second agent

Operator is justified because it has a distinct authority boundary and risk profile from phoenix: it interacts with real environments (shell, Kubernetes, testbeds, services) where mistakes are not reversible by editing a Markdown file.

Operator owns: diagnostics, environment inspection, shell/Kubernetes/testbed interaction, and evidence collection.

Operator must not own polyskills governance. It does not modify `skills/`, `agents/`, `STEERING.md`, ADRs, or any other polyskills artifact.

Operator is read-first. Every mutating operation requires explicit per-operation approval before execution.

See ADR-009 for the full authority boundary definition.

### 4. Skills are the default unit of reuse

The following capability families belong in skills unless they require a new authority boundary:

- Authoring and document writing
- Code and document review
- Requirements and specification
- Test planning and validation
- Research and evidence gathering
- Root cause analysis
- Communication and summarisation
- Diagrams and architecture sketches

A skill that needs a tool capability declares it via `metadata.mcp-required` and degrades gracefully without it. It does not embed tool access or API calls in its procedure steps.

### 5. MCP and tool integrations are not skills

MCP servers provide executable capabilities (fetching PRs, running queries, sending mail). Skills describe how to reason and act. Agents decide when capabilities are appropriate.

Never embed API calls, tool-specific shell commands, or credential-dependent logic inside a SKILL.md. If a skill requires a capability, declare it in frontmatter and let the MCP or host agent provide it.

### 6. Sub-agents are rare and bounded

A sub-agent is justified only when a parent agent needs to:
- parallelize identical operations across multiple inputs simultaneously, **and**
- each operation has a clean, atomic input/output contract

Sub-agents should not become hidden agents. They are never user-spawnable. They do not grow their own context or state. If a sub-agent is growing beyond a single atomic job, promote it to an agent or collapse it back into the parent's procedure.

### 7. Steering hierarchy

Steering is scoped. Load only what applies to the current context:

| Scope | File | What it governs |
|-------|------|----------------|
| Repository | `STEERING.md` (this file) | Library-wide doctrine, routing, current state |
| Agent | `agents/<name>/AGENT.md` | That agent's process, authority, and constraints |
| Skill | `skills/<name>/SKILL.md` | That skill's routing, contract, reasoning, procedure |
| Working directory | Local `CLAUDE.local.md` or equivalent | Session-specific, gitignored, ephemeral |

Load STEERING.md first, then the relevant INDEX file, then the matched definition. Never load all definitions speculatively.

### 8. Anti-patterns

| Anti-pattern | Why it's wrong |
|--------------|----------------|
| `docsmith-agent`, `review-agent`, `tester-agent` | These are skills. A workflow existing is not an agent justification. |
| Phoenix as catch-all | Phoenix owns this repo. Tasks outside it go to appropriate skills or a different agent. |
| API access rules inside SKILL.md | Skills are reasoning. Tool access belongs in MCPs and agent authority definitions. |
| Sub-agents that grow state | A sub-agent that needs context across steps is an agent. Promote or collapse it. |
| Adding an agent to INDEX.md before its AGENT.md exists | INDEX must reflect disk reality. Validate before updating INDEX. |
| Raising ceilings without an ADR update | ADR-005 is the ceiling contract. Update it or don't raise the ceiling. |

---

## Current State (2026-05-31)

| Layer | Count | Ceiling | Status |
|-------|-------|---------|--------|
| skills/ | 2 | 10 | ✅ synthesis, handoff |
| agents/ | 1 | 6 | ✅ phoenix (operator: candidate, see ADR-009) |
| sub-agents/ | 0 | none | ⏳ Added when a parent agent needs them |
| common-skills/ | 3 | none | ✅ Complete |
| templates/ | 3 | — | ✅ Complete |
| docs/adrs/ | 9 | — | ✅ Complete (ADR-009 proposed) |
| docs/specs/ | 2 | — | ✅ Complete |
| scripts/validate.py | — | — | ✅ Complete |
| .github/workflows/ | — | — | ✅ Complete |

## Agents (1 of 6)

| Agent | Role | Key capability |
|-------|------|---------------|
| phoenix | library steward | skill/agent/steering lifecycle within this repo only |
| operator | *(candidate — ADR-009)* | environment inspection, diagnostics, shell/k8s/testbed |

## Sub-Agents (0)

None yet. Added as parent agents need them — not speculatively.

## Skills (2 of 10)

| Skill | Purpose |
|-------|---------|
| `synthesis` | Distil messy multi-source input into a clear finding with confidence rating |
| `handoff` | Capture session state for resumption by next session or agent |

## Active Work

| Item | Status | Next action |
|------|--------|-------------|
| Operator agent | 🔄 ADR-009 proposed | Review ADR-009, create agents/operator/AGENT.md via phoenix |
| Skills build-out | 🔄 On demand | Add next skill when a real gap signal emerges |
| GitHub publish | ✅ Done | Live at github.com/Ritevista/polyskills |
| Kiro DAG adapter | ⏳ Pending | Wire parent→child in adapters/kiro/ |
| MCP wiring | ⏳ Pending | See mcp-servers/README.md |

## Blocked / Decision Needed

_None currently._

## MCP Wiring Status

| MCP | Wired | Unlocks |
|-----|-------|---------|
| GitHub | ❌ | github skill (PRs, reviews, repo ops) |
| GitLab | ❌ | gitlab skill (MRs, pipelines, reviews) |
| Gmail | ❌ | mail operations |
| Google Calendar | ❌ | scheduling |
| Web Search | ❌ | research agents and skills |
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
| 008 | Naming conventions (action-noun skills, role-noun agents) |
| 009 | Operator as candidate second agent (proposed) |

## Constraints

- Max 10 skills, max 6 agents — see ADR-005; raise ceiling only with ADR update
- No skill logic in adapters
- No tool/system access inside SKILL.md — use MCP and declare via `metadata.mcp-required`
- Descriptions under 200 chars (portability)
- Run `python3 scripts/validate.py` before every commit
- Phoenix gates before committing — always show diff and wait for approval
