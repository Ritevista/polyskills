---
name: [agent-name]
description: "[What it does. Spawn when: X. Returns: Y. Context: isolated.]"
role: worker
version: "1.0.0"
context-budget: small | medium | large
mcp-required: []
mcp-recommended: []
---

# [Agent Name]

## Purpose

[One paragraph. What this agent does, why it benefits from isolated context, and how it differs from the closest existing agent.]

## When to Spawn

- [Specific trigger: when would a user or orchestrator actually spawn this?]
- [Another concrete scenario]

**Not this agent**:
- [Near-miss scenario] → use `[other-agent]` or `[skill]` instead

## Input Contract

Spawning agent must provide:

- **[Field]**: [description] (required)
- **[Field]**: [description] (optional — default: [value])

## Process

1. [Step — what to do and why]
2. [Step]
3. [Step]
4. [Step — produce output]

## Output Contract

```markdown
## [Agent Name]: [Topic]

**[Key field]**: [value]

### [Section]
- [Item] — [qualifier]

### [Section]
- [Item]
```

## Constraints

- [Hard rule the agent must follow]
- [Hard rule]
- Do not load other SKILL.md files during execution
