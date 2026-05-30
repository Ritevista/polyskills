---
name: [sub-agent-name]
description: "[Single atomic task. Spawned by: X. Input: Y. Output: Z.]"
role: sub-agent
version: "1.0.0"
context-budget: tiny
spawned-by: [parent-agent-1, parent-agent-2]
mcp-required: []
---

# [Sub-Agent Name]

## Purpose

[One sentence. Single atomic task. Why firing multiple instances in parallel is useful.]

Parent agent fires `N` instances in parallel — one per [item]. Results collected and merged by parent.

## When to Spawn

Spawned BY `[parent-agent]` — not by the user directly.

Trigger: [when the parent agent should fire this]

## Input Contract

- **[Field]**: [description] (required)
- **[Field]**: [description] (optional)

## Process

1. [Single-task step]
2. [Single-task step]
3. Return result — do not synthesize beyond the single task

## Output Contract

```markdown
## [Sub-Agent]: [identifier]

| Field | Value |
|-------|-------|
| [col] | [val] |
```

## Constraints

- Single task only — do not expand scope
- If input is invalid or inaccessible, return immediately with a clear error
- Do not load other SKILL.md files
- Do not spawn further sub-agents
