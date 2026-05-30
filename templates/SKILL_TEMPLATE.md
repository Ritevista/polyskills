---
name: [skill-name]
description: "[What it does. Use when: X. Not for: Y. Output: Z.]"
license: MIT
metadata:
  version: "1.0.0"
  owner: polyskills
allowed-tools: Read Write
---

# [Skill Name]

## Routing

**Use when**:
- [Specific trigger phrase or condition]
- [Another trigger]

**Not this skill**:
- [Near-miss] → use `[other-skill]` instead
- [Near-miss] → use `[other-skill]` instead

## Contract

**Inputs** (required):
- `[input-name]`: [description]

**Inputs** (optional):
- `[input-name]`: [description, default]

**Output**: `[filename-pattern]` — [what it contains]

**Success criteria**:
- [ ] [Verifiable condition 1]
- [ ] [Verifiable condition 2]

## Reasoning

[How the agent should think about this class of problem. What matters most, what trade-offs to make, what to prioritize when things conflict.]

## Procedure

1. **[Step name]** — [what to do and why]
2. **[Step name]** — [what to do]
3. **[Step name]** — [what to do]

   > Use `references/[checklist].md` if available.
   > Run `scripts/[script].py` for deterministic checks.

4. **[Step name]** — [what to do]

## Edge Cases

- **[Named gotcha]**: [what goes wrong and what to do instead]
- **[Named gotcha]**: [what goes wrong and what to do instead]

## Quality Gates

Apply `common-skills/quality-checklist.md` plus:

- [ ] [Skill-specific check 1]
- [ ] [Skill-specific check 2]
- [ ] Output matches the template in `assets/[template].md`

## Resources

- Checklist: `references/[checklist].md`
- Output template: `assets/[output-template].md`

## Scripts

```bash
python scripts/[validate].py --help
python scripts/[validate].py [input-file]
```
