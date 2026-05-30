# Mastering Agent Skills: From Basics to Expert

> Reference guide for the `phoenix` agent. Load before drafting any skill or agent definition.

## Executive Summary

Agent-readable skills are rapidly becoming a practical standard for packaging reusable procedural knowledge for AI systems. The open Agent Skills specification defines the core shape: a directory anchored by `SKILL.md`, with YAML frontmatter and optional `scripts/`, `references/`, and `assets/` folders. OpenAI's API, Codex, and ChatGPT documentation, Anthropic's Claude docs and help center, and VS Code Copilot documentation all now describe skills as reusable bundles of instructions, examples, code, and supporting resources that can be discovered and loaded when relevant rather than stuffed into every prompt up front.

The strongest cross-vendor pattern is **progressive disclosure**. At session start, an agent sees only lightweight routing metadata such as a skill's `name` and `description`; when the task matches, it loads the full `SKILL.md`; then it selectively reads referenced files or runs scripts. That design keeps base context small while allowing effectively unbounded procedural depth through filesystem access and on-demand resource loading. Official guidance across the spec, Codex, Claude, and VS Code converges on the same authoring implication: write descriptions as routing logic, keep instruction bodies concise, package examples and templates inside the skill, and push deterministic mechanics into scripts.

For a serious reference implementation, the right mental model is not "prompt engineering with folders," but a **layered engineering discipline**. A robust skill has at least six layers: routing, contract, reasoning, procedure, edge cases, and quality gates.

---

## Standards Landscape

### Cross-platform format comparison

| Surface | Core format | Required fields | Notable extensions | Loading model |
|---------|-------------|-----------------|-------------------|---------------|
| Agent Skills spec | Directory with `SKILL.md`, optional `scripts/`, `references/`, `assets/` | `name`, `description` | `license`, `compatibility`, `metadata`, `allowed-tools`; keep `SKILL.md` under 500 lines | Catalog → `SKILL.md` → resources on demand |
| OpenAI Codex | Skill directory plus optional `agents/openai.yaml` | `name`, `description` | `agents/openai.yaml` for appearance, invocation policy, tool dependencies | Initial skill list ~2% of context or 8,000 chars; full SKILL.md on selection |
| Anthropic Claude | Skill folders in Claude VM / skill upload zip | `name`, `description` | Constrained lowercase names, 1024-char descriptions (200-char for UI portability) | Metadata always loaded; SKILL.md on trigger; referenced files/scripts on demand |
| VS Code Copilot | Open-standard skill directories in repo or user profile | `name`, `description` | `argument-hint`, `user-invocable`, `disable-model-invocation`, `context: fork` | Auto-load by relevance and/or slash-command |

**Key editorial note**: Official docs do not perfectly agree. The open spec allows descriptions up to 1024 characters, and Anthropic's API docs say the same, but Anthropic's Help Center gives a 200-character maximum. **Conservative cross-platform recommendation**: lowercase-hyphen `name`, directory-name match, description under 200 characters written as routing logic.

---

## Designing High-Quality Skills

### The six-layer architecture

The layered model is the most important design pattern in this guide. Every layer exists for a reason — missing one creates a predictable failure mode.

```
Routing layer      → decides activation
Contract layer     → defines what goes in and what comes out
Reasoning layer    → frames how the agent should think
Procedure layer    → stepwise execution
Edge-case layer    → encodes domain gotchas
Quality-gate layer → forces verification before completion
```

| Layer | Core question | What to author | Common failure mode |
|-------|---------------|----------------|---------------------|
| Routing | When should this skill activate? | `name`, `description`, use/don't-use cues | False positives or skill never triggering |
| Contract | What must go in and what must come out? | Required inputs, output template, success criteria | Outputs vague, inconsistent, or unusable |
| Reasoning | How should the agent make decisions? | Priorities, trade-offs, "prefer X over Y" heuristics | Agent thrashes or picks the wrong approach |
| Procedure | What steps should be executed? | Ordered checklist, script calls, stop conditions | Skipped steps or unstructured execution |
| Edge cases | What breaks reasonable assumptions? | Gotchas, exclusions, fallback strategy | Works for easy cases only |
| Quality gates | How does the agent know it's done? | Validators, self-checks, approval points | Premature completion and silent regressions |

---

### Routing layer: description as decision boundary

The description is the decision boundary. This is the single most important authoring principle.

Official guidance from multiple platforms converges: the `description` field is the primary mechanism agents use to decide whether to load a skill. Write it as routing logic, not marketing copy.

**A good description answers three questions in under 200 characters:**
1. When to use this skill
2. When NOT to use this skill (near-miss negatives)
3. What the output is

**Bad** (describes the artifact): `"Comprehensive requirements analysis tool for software projects"`

**Good** (routing logic): `"Formalize requirements from any input. Use when: PRD, spec, stakeholder notes. Not for: implementation. Output: requirements-[feature].md."`

**Near-miss negatives are the most important part of routing.** They're what prevent false triggers. Don't use obviously irrelevant negatives ("not for baking bread") — use the skills this one is most likely to be confused with.

---

### Contract layer: output templates are mandatory

Concrete output templates are more reliable than prose format descriptions. Models follow explicit structure more consistently than vague instructions like "write a report."

Every skill contract must specify:
- **Required inputs** — what the caller must provide
- **Optional inputs** — what can be omitted and what the default is
- **Output** — exact filename pattern and what the file contains
- **Success criteria** — verifiable conditions, not vague goals

Output filename convention: `[content-type]-[topic].md` — based on what's in the file, not what skill produced it. A brief skill produces `requirements-[feature].md`, not `brief-[feature].md`.

---

### Reasoning layer: model the decision, don't restate the procedure

The reasoning layer is the most commonly miswritten section. It should capture **how the agent should think**, not what it should do (that's procedure).

Good reasoning sections contain:
- Trade-off heuristics: "Prefer X over Y when Z"
- Priority rules: "If constraints conflict, defer to A"
- Scope guards: "The goal is X, not Y — stop when X is achieved"
- Failure modes to avoid: "The most common mistake is..."

Bad reasoning sections restate the procedure in paragraph form. If your reasoning section says "First do A, then do B, then do C" — move that to procedure.

---

### Procedure layer: stepwise, imperative, stop-condition explicit

Steps should be:
- **Numbered** — order matters
- **Imperative** — "Read the spec completely" not "The spec should be read"
- **Specific** — name the inputs, name the outputs, reference the templates
- **Bounded** — include stop conditions and "do not proceed until X" gates

Reference scripts and assets explicitly: `> Run scripts/validate.py before proceeding.`

---

### Edge-case layer: named, actionable, not generic

Every edge case should have a **name** (so it can be referenced) and an **action** (what to do, not just what happens).

**Bad**: `"Handle large inputs carefully"`

**Good**: `"**Spec is too vague to task**: Stop. Return to brief. Do not invent tasks for ambiguous requirements."`

Edge cases are the hardest layer to write well because they require domain knowledge. They should capture the gotchas that practitioners typically miss — not the obvious failure modes.

---

### Quality-gate layer: verifiable, not checkbox

Quality gates fail when they're restatements of the procedure ("make sure you did all the steps"). They should be **independently verifiable conditions** — things that can be checked without re-reading the procedure.

**Bad**: `- [ ] Followed all steps in the procedure`

**Good**: `- [ ] Every spec requirement maps to at least one task (or is explicitly listed as descoped)`

Apply `common-skills/quality-checklist.md` first, then add skill-specific gates.

---

## Trigger Engineering

### Trigger evals: the official evaluation loop

The standard eval format is `evals/trigger_queries.json` with `should_trigger` and `should_not_trigger` arrays.

Rules for good evals:
- **Near-miss negatives are more valuable than obviously irrelevant ones.** Use the skills most likely to be confused with this one as your should-not-trigger examples.
- **Model behavior is nondeterministic** — repeat runs are needed to estimate trigger rates, not just single-pass checks.
- **Minimum 5 queries per list** (polyskills convention); aim for 7+ for richer coverage.
- **Don't overfit** descriptions to your eval queries — the eval should test the description, not be written to pass it.

### With-skill vs without-skill evaluation

The most useful execution eval is a comparison: does this skill improve output quality versus the agent reasoning without it? This is the gold standard for whether a skill earns its place in the library.

---

## Script Ergonomics

Scripts bundled in a skill should be **agentic**: designed to run without human interaction.

Required properties:
- `--help` flag with usage and examples
- Non-interactive (no prompts, no stdin reads)
- Structured stdout (JSON or parseable lines)
- Diagnostics to stderr (not mixed with output)
- Meaningful exit codes (0 = success, 1 = error, 2 = usage error)
- Idempotent where possible
- `--dry-run` support for mutating operations

---

## Testing and Evals

### Test suite types

| Suite | What it checks | Pass criteria |
|-------|---------------|---------------|
| Trigger suite | Whether the right skill activates | High true-positive rate, low false-positive rate |
| Contract suite | Whether required outputs exist and are parseable | Output shape matches contract |
| Procedure suite | Whether steps are followed in order | No skipped mandatory steps |
| Edge-case suite | Whether known gotchas are handled | Edge cases handled without regressions |
| Script suite | Whether scripts behave agentically | Deterministic, idempotent, structured output |
| Regression suite | Whether new versions improve or preserve value | Positive or justified deltas vs baseline |

### Metrics

| Metric family | What to track |
|---------------|---------------|
| Routing | Trigger precision, recall, false-positive rate |
| Outcome quality | Assertion pass rate, human review score |
| Efficiency | Mean latency, token cost |
| Stability | Standard deviation across reruns |
| Adoption | Invocation count, explicit vs implicit use |

---

## Authoring Checklist

Before adding any skill to the library:

- [ ] `name` and directory match; lowercase-hyphen style
- [ ] Description written as routing logic, not description of artifact
- [ ] "When not to use" cases and near-miss negatives are present
- [ ] Context includes only what the agent wouldn't already know
- [ ] Output template or contract is explicit (not prose format description)
- [ ] Scripts (if any) are non-interactive and structured
- [ ] Quality gates are independently verifiable (not restatements of procedure)
- [ ] Trigger evals have ≥5 should-trigger and ≥5 should-not-trigger queries
- [ ] All six layers are present and non-empty
- [ ] `validate.py` passes with no errors

---

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Description as marketing copy | Skill never triggers correctly | Rewrite as routing logic with use/don't-use/output |
| Reasoning restates procedure | Reasoning layer adds no value | Replace with trade-off heuristics and priority rules |
| Generic edge cases | "Handle large inputs carefully" | Name each case; add a specific action |
| Checkbox quality gates | "Make sure all steps were followed" | Replace with independently verifiable conditions |
| Overly broad skill | Triggers on everything, does too much | Split into focused single-job skills |
| Overly narrow skill | Only works for one specific case | Generalize the contract; parameterize |
| Output format in prose | Model ignores format inconsistently | Use explicit template in assets/ |
| Skill does what an agent should do | Skill has its own search/research logic | Push tool use to MCP; keep skill as reasoning pattern |
