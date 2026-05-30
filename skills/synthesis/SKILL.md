---
name: synthesis
description: "Distils any messy multi-source input into a clear finding. Use when: notes, docs, feedback, or mixed sources need consolidating. Not for: single clear input, live research, or permanent docs."
metadata:
  version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Bash
---

# synthesis

## Routing

Use this skill when you have noisy, overlapping, or contradictory inputs from multiple sources and need to produce a single clear answer to a specific question.

**Use when:**
- Session notes, prompts, or chat history need consolidating before acting
- Design docs, ADRs, or specs partially overlap or contradict each other
- User feedback, bug reports, or error logs share a common theme that needs extracting
- Any mix of text sources — regardless of format — needs a clear finding

**Do not use when:**
- Input is already a single clear question or task — respond directly
- Sources need live research or web lookups — use a research agent
- Output is meant to be a permanent reference document — use a different output type
- Sources are from GitHub or GitLab — use the github or gitlab skill instead

## Contract

**Required:**
- `sources` — one or more raw inputs: session notes, prompts, error messages, chat excerpts, design docs, user feedback, or any other text
- `question` — the specific question this synthesis must answer (e.g., "What skill is missing?", "What is the real blocker?")

**Optional:**
- `context` — background on the project or domain that helps interpret the sources

**Output:** `synthesis-[topic].md` placed in the current working directory or as inline output if no file path is given.

**Success criteria:**
- The central question is answered in the first paragraph
- Every claim cites at least one source
- Conflicts between sources are surfaced, not silently resolved
- A confidence rating (High / Medium / Low) is given with justification

## Reasoning

Synthesis answers a question using sources as evidence. It is not summary.

- **Prefer conflicts over consensus.** When sources disagree, that disagreement is usually the most valuable signal — it marks the boundary of what is known.
- **Distinguish between independent and correlated sources.** Three people all citing the same session have one data point, not three.
- **Confidence must be calibrated.** High = multiple independent sources converge. Medium = one strong source or partial corroboration. Low = single source or significant uncertainty.
- **Scope the output to the question.** Stop when the question is answered. Do not produce a general summary of all sources.
- **The most common mistake** is summarizing all inputs instead of answering the question. If you find yourself writing "source A says X, source B says Y," stop and reframe around the question.

## Procedure

1. **Restate the question** in one sentence. If you cannot state it clearly, stop and ask for clarification.
2. **Inventory the sources** — list each source and its type (session note, prompt, error, etc.).
3. **Extract claims** relevant to the question from each source. Ignore off-topic content.
4. **Map agreements and conflicts** — group claims that say the same thing; flag claims that contradict each other.
5. **Check source independence** — if multiple sources trace back to the same origin, treat them as one.
6. **Reconcile conflicts** — for each conflict, determine if one source is more authoritative, more recent, or more specific. If not resolvable, present both positions.
7. **Draft the finding** — answer the question in one paragraph. Support with the strongest claims.
8. **Rate confidence** — High / Medium / Low with a one-sentence justification.
9. **List open gaps** — questions the sources cannot answer, and what would resolve them.
10. **Write output** to `synthesis-[topic].md` or return inline if no file context.

## Edge Cases

**All sources agree:** Check whether they are truly independent. If all sources are from the same session or one person's writing, confidence is Medium at most — not High.

**Single source:** This is an observation, not a synthesis. State the finding as "Based on one source" and rate confidence Low unless the source is authoritative.

**Irreconcilable conflict:** Do not pick a side. Present both positions clearly, note the conflict, and list what evidence would resolve it.

**Sources are out of date:** Flag the date gap. If the sources predate a known change (e.g., a library rewrite, a policy update), note that findings may not reflect current state.

**Question is underspecified:** Stop at step 1. Return a clarifying question. Do not synthesize toward an unclear target.

**Sources are very long:** Extract only the claims directly relevant to the question. Do not attempt to synthesize entire documents.

## Quality Gates

Before delivering output:

- [ ] The central question is answered explicitly in paragraph 1 — not implied
- [ ] Every claim in the finding has at least one named source
- [ ] If sources conflict, the conflict is named and both positions are present
- [ ] Confidence rating is present with a one-sentence justification
- [ ] Open gaps section lists at least one item, or explicitly states "none identified"
- [ ] Output is scoped to the question — no unrequested general summary
