---
name: output-formatting
type: common-skill
version: "1.0.0"
used-by: [all agents, all skills]
---

# Output Formatting

Standard formatting rules for all polyskills agents and skills.

## Structure rules

1. **Lead with verdict or summary** — put the most important thing first, never bury it
2. **Use tables for comparisons** — three or more items with multiple attributes get a table
3. **Use numbered lists for sequences** — steps, phases, priorities
4. **Use bullet lists for sets** — unordered items, findings, constraints
5. **Use code blocks for all file content, commands, and structured data**

## Heading levels

- `#` — document title only
- `##` — major sections (used in all SKILL.md and AGENT.md files)
- `###` — subsections within a major section
- `####` — avoid; split into a new section instead

## Filename conventions

| Output type | Pattern |
|-------------|---------|
| Skill output | `[skill-name]-[topic].md` |
| Agent report | `[agent-name]-report-[topic].md` |
| ADR | `docs/adrs/[NNN]-[slug].md` |
| Research | `research-[topic].md` |

## Length rules

- Agent output: under 1 page unless the contract specifies otherwise
- Skill output: as long as the contract requires, no longer
- Descriptions (frontmatter): under 200 chars for portability
- Confidence reasons: one parenthetical clause, not a paragraph

## What to avoid

- No "As an AI language model..." preambles
- No trailing summaries that repeat what was just said
- No padded introductions — start with substance
- No marketing language in descriptions or outputs
