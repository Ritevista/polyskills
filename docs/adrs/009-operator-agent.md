# ADR-009: Operator as Candidate Second Agent

**Status**: Proposed
**Date**: 2026-05-31

## Context

The architecture review (2026-05-31) assessed whether a second agent is warranted. The previous design had reached ~10 agents (docsmith, review-agent, requirement-study-agent, test-analyst-agent, remote-ops-agent, and others). Most were skill-shaped work promoted to agents because a capability existed — not because a distinct authority boundary existed.

The rebuild collapsed all skill-shaped work back to skills. Phoenix was established as the single governance agent for the polyskills library. The question: is a second agent ever justified?

The test for a second agent (from STEERING.md doctrine):
1. Distinct authority boundary — what it is permitted to do is different
2. Different risk profile — blast radius differs materially
3. Different operating context — clean context serves the job
4. Delegation role — it coordinates or parallelizes work that benefits from isolation

Phoenix fails tests 1 and 2 for external system interaction: it is not permitted to touch external systems, and its blast radius is capped at this repo's files. Any agent that needs to run `kubectl`, read logs, inspect running services, or run shell commands against live infrastructure has a fundamentally different authority profile.

## Decision

**Operator is the candidate second agent.**

Operator is accepted in principle. Its AGENT.md will be authored via phoenix when the use case is confirmed active. It is listed as a candidate in STEERING.md and INDEX.md until then.

### Authority boundary

| Area | Phoenix | Operator |
|------|---------|---------|
| Mission | Keep the polyskills library correct and consistent | Discover, inspect, and report on real environments |
| Authority | May modify any polyskills repo artifact | May read from real systems; may mutate only with explicit per-operation approval |
| Allowed actions | Read/write files in this repo; run validate.py; commit on approval | kubectl get/describe/logs, shell reads, config dumps, log tails, metric queries |
| Forbidden actions | Access external systems; run shell against live infra | Modify polyskills repo files; run destructive operations autonomously |
| Operating context | Library conventions, ADRs, templates | Environment state, service topology, config, logs, metrics |

### Safety model

Operator is **read-first by default**. The three safety levels:

- `read-only` (default) — no write or mutate operations, even if requested
- `approve-mutations` — proposed mutations are shown with exact command and effect; user approves each
- `auto-remediate` — reserved for tightly scoped automated workflows; never the default

The safety level must be stated explicitly by the caller. If unspecified, Operator defaults to `read-only`.

## Rationale

- The authority/risk boundary is real: a wrong SKILL.md is corrected by editing a Markdown file; a wrong `kubectl delete` is not
- Environment investigation is multi-step and context-heavy — it benefits from isolated context and clean I/O
- Keeping Operator separate from Phoenix prevents Phoenix from accumulating external system access over time ("just add one kubectl call")
- Operator's output is always a structured evidence report — it does not remediate unless explicitly authorized

## Consequences

- **Easier**: Phoenix stays narrow; operational tasks have a defined home
- **Harder**: Two agents to maintain; boundary must be respected in practice, not just in doctrine
- **Watch for**: Operator growing document-writing or planning responsibilities — those are skills, not Operator's job

## Alternatives Considered

- **No second agent — MCP only**: MCP gives the host agent system access directly, so Operator is technically redundant. Rejected because it removes the explicit safety boundary and mixes operational context into the main conversation.
- **Operator as a skill family**: Skills are reasoning patterns. A skill cannot own tool access or enforce a safety model. Rejected.
- **Operator as a sub-agent**: Sub-agents are atomic and spawned by parents. Operator is multi-step, user-spawnable, and has its own authority model. Rejected.
