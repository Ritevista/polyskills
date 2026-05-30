---
name: quality-checklist
type: common-skill
version: "1.0.0"
used-by: [all skills, phoenix]
---

# Quality Checklist

Run this before delivering any skill output. Skills add their own skill-specific gates on top.

## Universal gates

- [ ] Output matches the contract defined in the skill's `## Contract` section
- [ ] Every claim has a confidence rating where applicable (`common-skills/confidence-rating.md`)
- [ ] Output uses the format in `common-skills/output-formatting.md`
- [ ] No vague language without measurable criteria ("fast", "easy", "soon", "better")
- [ ] Contradictions are surfaced, not silently resolved
- [ ] "What we don't know" or "Open questions" is explicit — not omitted
- [ ] File follows the naming convention in `common-skills/output-formatting.md`

## For research and evidence outputs

- [ ] Every key claim cites a source
- [ ] LOW confidence items are flagged, not buried

## For design and architecture outputs

- [ ] Every significant decision has a rationale
- [ ] Alternatives considered are noted, even if briefly
- [ ] Non-functional requirements (latency, scale, security) are addressed

## For plans and task breakdowns

- [ ] Every task is actionable (starts with a verb, has a clear done condition)
- [ ] Dependencies between tasks are explicit
- [ ] External dependencies (third-party APIs, infra) are flagged

## Stop conditions

Do not deliver output if:
- A Critical issue is unresolved and not explicitly risk-accepted
- The output contract is not met (missing required sections)
- Confidence is uniformly LOW and no higher-confidence source is available
