---
name: confidence-rating
type: common-skill
version: "1.0.0"
used-by: [all agents, synthesis skill]
---

# Confidence Rating

Consistent confidence scale used across all agents that return findings, validations, or extractions.

## Scale

| Level | Meaning | Use when |
|-------|---------|----------|
| HIGH | Multiple independent primary sources, or direct domain knowledge with no known exceptions | You would stake the decision on this |
| MEDIUM | Single source, secondary source, or primary source with known caveats | You'd act on this but want a second check |
| LOW | Inferred, unverified, or based on analogy | Flag it and don't act without verification |

## Rules

1. **Every claim gets a rating** — no unrated assertions in agent output
2. **Explain LOW and MEDIUM** — add a reason in parentheses: `LOW (only found in one blog post, no primary source)`
3. **Do not average** — if a section has mixed confidence, rate each item separately
4. **Contradict, don't blend** — if two sources disagree, report both at their individual confidence levels, not a blend

## Format

```
- [Claim] — Confidence: HIGH
- [Claim] — Confidence: MEDIUM (single source: [ref])
- [Claim] — Confidence: LOW (inferred from analogy with [X], not directly verified)
```
