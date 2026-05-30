# Agent Format Specification

**Version**: 1.0.0
**Status**: Active

Covers both agents (`agents/`) and sub-agents (`sub-agents/`).

## Directory structure

```
agents/<agent-name>/
└── AGENT.md               (required)

sub-agents/<sub-agent-name>/
└── AGENT.md               (required)
```

Agents do not have `scripts/`, `references/`, or `assets/` — those belong in skills.
Scripts or tool calls are invoked directly by the agent at runtime.

## AGENT.md frontmatter

```yaml
---
name: <lowercase-hyphenated>       # required; matches directory name
description: "<under 200 chars>"   # required; routing / spawn trigger
role: worker | sub-agent           # required
version: "1.0.0"                   # required
context-budget: tiny|small|medium|large  # required
spawned-by: [parent-agent-name]    # required for sub-agents only
mcp-required: []                   # optional
mcp-recommended: []                # optional
---
```

### Role values

| Role | Meaning |
|------|---------|
| `worker` | User-spawnable agent; goes in `agents/` |
| `sub-agent` | Spawned BY another agent only; goes in `sub-agents/` |

### Context budget guide

| Budget | Meaning | Typical use |
|--------|---------|-------------|
| `tiny` | < 5K tokens | Single lookup, single check |
| `small` | < 20K tokens | Focused validation or short research |
| `medium` | < 60K tokens | Multi-source research, document processing |
| `large` | > 60K tokens | Full codebase analysis, long synthesis |

## Required sections in AGENT.md body

```
## Purpose
## When to Spawn
## Input Contract
## Process
## Output Contract
## Constraints
```

### Input Contract section

```markdown
## Input Contract

Spawning agent must provide:
- **Field**: description (required)
- **Field**: description (optional — default: value)
```

### Output Contract section

Must include a literal output template with markdown headers matching what the agent will produce. This is what downstream agents and users can parse.

### Constraints section

Must include:
- At least one hard rule about scope boundaries
- "Do not load other SKILL.md files during execution" (sub-agents)
- "Do not spawn further sub-agents" (sub-agents only)

## Tool-specific adapter files

When an agent is deployed, the install script creates adapter files in:
- `.claude/agents/<name>.md` — adds `tools:` field with Claude Code tool names
- `.cursor/agents/<name>.md` — same frontmatter, no tools field (platform default)
- `.gemini/agents/<name>.md` — same as cursor

These are generated from the canonical `AGENT.md` — do not edit them manually.
Run the install script to regenerate after canonical changes.

## Sub-agent additional rules

- `spawned-by` must reference at least one valid agent name in `agents/INDEX.md`
- `context-budget` should be `tiny` or `small` — if a sub-agent needs `medium`, consider making it an agent
- Sub-agents must not spawn further sub-agents
- Sub-agents must not load SKILL.md files
