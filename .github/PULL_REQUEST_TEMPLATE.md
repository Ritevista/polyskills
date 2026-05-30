## What this changes

<!-- Skill added / Agent added / Sub-agent added / Config changed / Bug fix -->

## Checklist

- [ ] `python scripts/validate.py` passes locally
- [ ] Description is under 200 chars and written as routing logic
- [ ] Directory name matches `name` field in frontmatter
- [ ] All six layers present in SKILL.md (Routing / Contract / Reasoning / Procedure / Edge Cases / Quality Gates)
- [ ] `evals/trigger_queries.json` has ≥ 5 should-trigger and ≥ 5 should-not-trigger queries
- [ ] INDEX.md updated with the new entry
- [ ] If adding a skill: ceiling not exceeded (≤ 10) or ADR-005 updated
- [ ] If adding an agent: ceiling not exceeded (≤ 6) or ADR-005 updated
- [ ] If changing a contract (inputs/outputs): `metadata.version` bumped (major)
- [ ] ADR added if this is a significant architectural decision
