# Skill Format Specification

**Version**: 1.0.0
**Status**: Active

## Directory structure

```
skills/<skill-name>/
├── SKILL.md               (required)
├── scripts/               (optional — deterministic mechanics)
│   └── <script>.py
├── references/            (optional — checklists, taxonomies, domain rules)
│   └── <checklist>.md
├── assets/                (optional — output templates)
│   └── <template>.md
└── evals/                 (required for production skills)
    ├── trigger_queries.json
    └── files/             (optional — input fixtures)
```

## SKILL.md frontmatter

```yaml
---
name: <lowercase-hyphenated>       # required; must match directory name
description: "<under 200 chars>"   # required; routing logic only
license: MIT                        # required
metadata:
  version: "1.0.0"                  # required
  owner: <team or person>           # required
  mcp-required: []                  # optional
  mcp-recommended: []               # optional
allowed-tools: Read Write           # optional; restrict agent tools
---
```

### Name rules
- Lowercase, hyphen-separated
- Matches the directory name exactly
- Describes a TASK, not a role (`security-review` not `security-guardian`)

### Description rules
- Under 200 characters
- Must answer: **When to use** · **When NOT to use** · **What output**
- Written as routing logic, not marketing copy
- Example: `"Analyze and write software requirements from notes or docs. Use when formalizing a feature request. Not for implementation planning. Output: structured REQ-* document."`

## Required sections in SKILL.md body

All six layers are required. Section headers must be exact:

```
## Routing
## Contract
## Reasoning
## Procedure
## Edge Cases
## Quality Gates
```

### Routing section

```markdown
## Routing

**Use when**:
- [Specific trigger phrase or condition]

**Not this skill**:
- [Near-miss] → use `[other-skill]` instead
```

At least 2 "Use when" entries and 2 "Not this skill" near-misses required.

### Contract section

```markdown
## Contract

**Inputs** (required):
- `name`: description

**Output**: `filename-pattern.md` — [what it contains]

**Success criteria**:
- [ ] Verifiable condition
```

### evals/trigger_queries.json format

```json
{
  "skill": "skill-name",
  "should_trigger": [
    "write requirements for the new auth feature",
    "analyze this PRD"
  ],
  "should_not_trigger": [
    "create a task breakdown",
    "design the database schema"
  ]
}
```

At least 5 should-trigger and 5 should-not-trigger queries. Near-misses (skills that are close but wrong) are more valuable than obviously irrelevant queries.

## Scripts ergonomics

Scripts in `scripts/` must be:
- Non-interactive (no user prompts)
- Accept input via arguments or stdin
- Output structured data to stdout (JSON or Markdown)
- Errors to stderr
- Support `--help` flag
- Idempotent and deterministic
- Support `--dry-run` where applicable

## Versioning

`metadata.version` follows semver. Bump:
- **patch** (1.0.x): typo fixes, clarifications
- **minor** (1.x.0): new edge cases, procedure improvements, new scripts
- **major** (x.0.0): contract changes (inputs/outputs change), routing changes
