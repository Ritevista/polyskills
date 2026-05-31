---
name: skillcraft
description: "Creates, reviews, refactors, and migrates skills, agents, sub-agents, and templates. Use when designing definitions, checking overlap, or improving trigger quality."
metadata:
  version: "1.0.0"
  mcp-required: []
user-invocable: true
---

# skillcraft

## Routing

Use this skill when the work is about the design, quality, or structure of skill-library definitions — not about executing the capability those definitions describe.

**Use when:**
- Creating a new skill, agent, sub-agent, or common-skill definition
- Reviewing an existing definition for clarity, routing quality, or format compliance
- Deciding whether a capability belongs in a skill, agent, sub-agent, common-skill, MCP, steering rule, or plain documentation
- Checking a definition for overlap with existing skills
- Refactoring, merging, splitting, renaming, or retiring definitions
- Converting an old agent, prompt, or workflow into the current six-layer skill format
- Designing or improving trigger evals (`evals/trigger_queries.json`)
- Reviewing naming conventions against ADR-008
- Checking frontmatter structure and six-layer section compliance
- Migrating skill definitions between platforms or formats
- Reviewing a Phoenix proposal before accepting it

**Do not use when:**
- The request is to execute the domain the skill describes (e.g., preparing interview questions is `interviewing`, not `skillcraft`)
- The task is pure repo maintenance with no definition design (file moves, git operations) — respond directly
- The task requires live external system access
- The user asks for normal writing, coding, research, or evaluation output unrelated to skill-library design

**Modes** — caller specifies or inferred from context:

| Mode | When to use |
|------|-------------|
| `classify` | Decide what layer a capability belongs to |
| `create` | Design a new definition from scratch |
| `review` | Evaluate an existing definition against quality standards |
| `refactor` | Merge, split, rename, or retire definitions |
| `migrate` | Convert old agents/skills/prompts to current Polyskills format |
| `evals` | Create or improve trigger evaluation queries |

## Contract

**Required inputs:**
- `mode` — one of: classify, create, review, refactor, migrate, evals
- At least one of: capability description, existing definition text, old prompt or agent, skill name and intended purpose

**Per-mode required inputs:**

| Mode | Minimum required |
|------|-----------------|
| `classify` | Description of the capability or workflow |
| `create` | Capability description + intended trigger context |
| `review` | The SKILL.md or AGENT.md text to review |
| `refactor` | One or more definitions + the reason for change |
| `migrate` | Old definition, prompt, or agent description |
| `evals` | Skill name + routing description or existing SKILL.md |

**Optional inputs:**
- `existing-skills` — list of current skills to check for overlap
- `platform` — target platform if migrating for a specific tool
- `adrs` — relevant ADR numbers to apply during review or create

**Outputs by mode:**

| Mode | Output |
|------|--------|
| `classify` | Classification decision with rationale (inline) |
| `create` | Complete SKILL.md or AGENT.md in six-layer format (inline or file) |
| `review` | Structured findings: layer-by-layer assessment, issue list, recommended fixes |
| `refactor` | Revised definition(s) with change rationale |
| `migrate` | Six-layer SKILL.md converted from old format, with migration notes |
| `evals` | `trigger_queries.json` with ≥8 should-trigger and ≥8 should-not-trigger entries |

**Success criteria:**
- Every output definition passes `validate.py` with zero errors
- Descriptions are under 200 characters and written as routing logic
- No definition embeds tool access or API calls
- Overlap with existing skills is explicitly checked and addressed
- Naming follows ADR-008 conventions

## Reasoning

Skillcraft is the meta-skill: it designs the tools that run the library. The judgment calls here are harder than they look because the failure modes are architectural, not just stylistic.

**A capability existing does not justify a new agent.** The classification test is not "can this be an agent?" — almost anything can be an agent. The test is "does this NEED a distinct authority boundary, risk profile, operating context, or delegation role?" If none of those are true, it is a skill.

**Workflow-shaped things are skills; authority-shaped things are agents.** A workflow is a repeatable sequence of reasoning steps — that is what skills encode. An agent needs separate isolation because its blast radius, context requirements, or permissions are meaningfully different from the parent conversation. When in doubt, start as a skill and promote only when a concrete need emerges.

**MCP and tool access belong to capabilities, not skill instructions.** A SKILL.md describes how to reason and act. It does not make API calls, run shell commands, or embed credential logic. Declare tool requirements in `metadata.mcp-required` and let the host agent or MCP provide access.

**Steering governs behavior; skills teach procedure.** If the output of a definition is a constraint on how an agent should behave in a context (what to avoid, what authority it has, what scope it operates in), it belongs in steering — not in a skill. If the output is a procedure for accomplishing a task, it belongs in a skill.

**Trigger quality matters more than clever naming.** A perfectly named skill that never triggers, or triggers on the wrong input, has zero value. The description and `should_trigger` / `should_not_trigger` evals are the most important quality signals. Write descriptions as routing logic, not marketing copy. Near-miss negatives are more valuable than obviously irrelevant examples.

**Prefer merging overlapping skills over adding another skill.** Before creating a new skill, check whether the trigger surface overlaps with an existing one. Overlap is the primary failure mode of skill libraries. If two skills would activate on the same input, merge them or sharpen their boundaries.

**The most common mistake** in `create` mode is writing a skill that is really just a procedure list without routing discipline. A skill without clear "do not use when" cases will be activated indiscriminately. The routing layer is not a formality — it is the most important layer.

## Procedure

### classify mode
1. Describe the capability in one sentence: what it does, what it takes as input, what it produces as output.
2. Apply the classification tests in order:
   - Does it require a distinct authority boundary (e.g., external system access, different blast radius)? → **agent**
   - Is it atomic and intended to be parallelized by a parent agent? → **sub-agent**
   - Is it a shared reasoning pattern used across multiple skills? → **common-skill**
   - Is it a constraint on agent behavior in a scope? → **steering rule**
   - Is it an executable system capability (API, shell, data source)? → **MCP/tool**
   - Is it a reusable procedure-shaped reasoning pattern? → **skill**
   - Is it one-off documentation? → **plain doc**
3. State the classification and the reasoning. If multiple layers apply, recommend the primary layer and note the secondary use.
4. Flag if the classification is ambiguous and describe what additional information would resolve it.

### create mode
1. Confirm the capability description and intended trigger context.
2. Run `classify` mode first if the layer is not already established.
3. Check existing skills for overlap — list any that have similar trigger surfaces.
4. Apply ADR-008 naming: single action-noun for skills, role-noun (-er form) for agents, [domain]-[role]er for sub-agents.
5. Draft the frontmatter: name, description (≤200 chars as routing logic), metadata.
6. Write all six layers in order: Routing, Contract, Reasoning, Procedure, Edge Cases, Quality Gates.
7. Write `evals/trigger_queries.json` with ≥8 should-trigger and ≥8 should-not-trigger entries. Near-miss negatives first.
8. Verify the description answers: when to use, when NOT to use, what the output is.
9. Return the complete definition and flag any sections that need domain-specific input from the caller.

### review mode
1. Load the definition. Identify which skill/agent it is and its intended purpose.
2. Evaluate layer by layer:
   - **Routing**: Is the description routing logic or marketing copy? Are near-miss negatives present? Are "do not use when" cases specific?
   - **Contract**: Are required inputs explicit? Is the output format specified? Are success criteria verifiable?
   - **Reasoning**: Does it encode judgment, or does it restate the procedure? Are trade-off heuristics present?
   - **Procedure**: Are steps numbered and imperative? Are stop conditions explicit? Are scripts or assets referenced correctly?
   - **Edge Cases**: Are they named? Do they have specific actions, not generic warnings?
   - **Quality Gates**: Are they independently verifiable, not restatements of the procedure?
3. Check for: description length (>200 chars is a warning), embedded tool access (error), overlap with existing skills (flag).
4. Check naming against ADR-008.
5. Produce a structured findings report: per-layer assessment, issue severity (error / warning / suggestion), and recommended fix for each issue.

### refactor mode
1. State the reason for refactoring: overlap, scope creep, naming violation, format drift, or retirement.
2. If merging: identify the primary skill, migrate unique content from the secondary, update routing to cover both former trigger surfaces, update INDEX.md entries.
3. If splitting: define the boundary between the two new skills, ensure no trigger surface overlap, create separate definitions.
4. If renaming: apply ADR-008, update all cross-references in INDEX.md, STEERING.md, and any skill that references the old name.
5. If retiring: confirm no active INDEX.md entries point to it, then remove the directory and update counts.
6. Run `review` mode on the result before marking complete.

### migrate mode
1. Parse the old definition: extract purpose, trigger conditions, steps, and any quality constraints.
2. Map to the six-layer format: identify which old content maps to which layer.
3. Identify what is missing from the old format: usually Reasoning and Edge Cases.
4. Rewrite in six-layer format. Do not preserve formatting artifacts from the old format.
5. Check for embedded tool access or API calls — move to `metadata.mcp-required`.
6. Apply ADR-008 naming if the old name does not conform.
7. Add `evals/trigger_queries.json` if not present.
8. Produce a migration note: what was changed, what was added, what was intentionally dropped.

### evals mode
1. Read the skill's Routing layer: extract the "use when" and "do not use when" conditions.
2. Write `should_trigger` entries: cover the primary use case, edge-case uses, and varied phrasings. ≥8 entries.
3. Write `should_not_trigger` entries: near-miss negatives first (skills most likely confused with this one), then obviously out-of-scope examples. ≥8 entries.
4. Verify no `should_trigger` example could plausibly activate a different existing skill.
5. Verify no `should_not_trigger` example is obviously irrelevant (those add no value).
6. Return the complete `trigger_queries.json`.

## Edge Cases

**The capability is genuinely ambiguous between skill and agent:** Apply the classification tests strictly. If still ambiguous, default to skill — it is easier to promote a skill to an agent later than to demote an agent.

**Two existing skills have overlapping trigger surfaces:** Flag both, do not silently pick one. Present the overlap clearly and propose either a boundary sharpening (update both routing sections) or a merge.

**The old format being migrated has embedded tool calls:** Extract them, document what MCP or capability would be needed, add to `metadata.mcp-required`, and note in the migration output that the skill will degrade gracefully without the MCP.

**The skill ceiling is at or near 10:** Before creating, check the count in INDEX.md. If at ceiling, the caller must either retire an existing skill or raise the ceiling via an ADR-005 update. Do not silently exceed the ceiling.

**Review reveals the definition is fundamentally wrong (wrong layer, wrong name, wrong scope):** Do not patch it incrementally. Recommend a rewrite and flag the severity. A cosmetic fix on a structurally wrong definition produces a polished wrong definition.

**Evals are being written for a skill that doesn't exist yet:** Write the evals against the intended routing description, not an assumed SKILL.md. Flag that the evals should be validated once the full skill is written.

## Quality Gates

Before delivering any output:

- [ ] Description is ≤200 characters and reads as routing logic (when to use / when not / what output)
- [ ] "Do not use when" cases are specific near-miss negatives — not obvious irrelevancies
- [ ] No API calls, tool-specific commands, or credential logic embedded in any procedure step
- [ ] Overlap with existing skills has been checked and addressed
- [ ] Naming follows ADR-008 (single action-noun for skills; role-noun for agents)
- [ ] All six layers are present and non-empty
- [ ] Evals contain ≥8 should-trigger and ≥8 should-not-trigger with near-miss negatives present
- [ ] If new definition: `validate.py` would pass with zero errors
- [ ] If affecting counts: INDEX.md and STEERING.md are updated
- [ ] No new agent or sub-agent created speculatively
