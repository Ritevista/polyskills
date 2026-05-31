---
name: steering
description: "Designs and reviews scoped steering instructions for repos, working directories, agents, and testbeds. Use when defining doctrine, precedence, or local rules."
metadata:
  version: "1.0.0"
  mcp-required: []
user-invocable: true
---

# steering

## Routing

Use this skill when the work is about designing, reviewing, or applying the behavioral instruction layer that governs how agents operate in a scope — not about performing the work those instructions describe.

**Use when:**
- Creating or reviewing STEERING.md, AGENTS.md, AGENT.md, CLAUDE.md, GEMINI.md, or equivalent instruction files
- Defining repository doctrine (what the system is, how agents should behave, what is forbidden)
- Defining local working-directory or testbed-specific instruction rules
- Deciding steering precedence when multiple instruction files apply to the same context
- Resolving conflicts between global, repo, agent, skill, local, or testbed instructions
- Writing rules for safe command execution, tool usage boundaries, or authority constraints
- Documenting anti-patterns and operating constraints for an agent system
- Converting ad-hoc session instructions into versioned, scoped steering files
- Reviewing existing steering for gaps, contradictions, scope leakage, or enforceability

**Do not use when:**
- The user wants to perform the work that steering governs (e.g., run a deployment, write code, plan a sprint)
- The request is generic documentation with no behavioral constraint purpose
- The task is editing prose that is not an instruction file
- The request requires direct external system access
- The task is creating a reusable procedural skill — use `skillcraft` instead

**Modes** — caller specifies or inferred from context:

| Mode | When to use |
|------|-------------|
| `design` | Create new steering doctrine for a repo, agent, or scope |
| `review` | Evaluate existing steering for gaps, contradictions, and enforceability |
| `precedence` | Resolve conflicts between instruction layers |
| `localize` | Adapt general steering to a specific repo, directory, or testbed |
| `anti-patterns` | Identify and document bad steering practices |
| `migration` | Convert ad-hoc instructions into scoped steering files |

## Contract

**Required inputs:**
- `mode` — one of: design, review, precedence, localize, anti-patterns, migration
- At least one of: existing instruction file(s), scope description, repository context, ad-hoc instructions to convert

**Per-mode required inputs:**

| Mode | Minimum required |
|------|-----------------|
| `design` | Scope description (what the system is, what agents operate in it) |
| `review` | One or more existing instruction files |
| `precedence` | Two or more instruction files that apply to the same context |
| `localize` | Base steering + target scope description (repo, directory, testbed) |
| `anti-patterns` | Existing instruction file(s) or context description |
| `migration` | Ad-hoc instructions, session notes, or informal rules to convert |

**Optional inputs:**
- `tools` — the agent tools in use (Claude Code, Gemini CLI, Cursor, Kiro, etc.) for platform-specific format guidance
- `safety-level` — how strict the output should be (default: balanced)
- `existing-files` — other instruction files in scope so conflicts can be detected

**Outputs by mode:**

| Mode | Output |
|------|--------|
| `design` | Structured instruction file (STEERING.md, AGENTS.md, or equivalent) |
| `review` | Findings report: gaps, contradictions, enforceability issues, scope leakage |
| `precedence` | Precedence resolution with rationale; merged or layered instruction set |
| `localize` | Scoped instruction file for the target environment |
| `anti-patterns` | Named anti-pattern list with impact and fix for each |
| `migration` | Converted scoped instruction file with migration notes |

**Success criteria:**
- Scope is explicit: every instruction file states what context it governs
- Authority boundaries are clear: what agents may and may not do in this scope
- Precedence is defined when multiple files apply
- Rules are enforceable: observable conditions, not vague intentions
- No credentials, secrets, or sensitive data in any output
- No broad catch-all instructions that would match everything

## Reasoning

Steering is doctrine, not task procedure. This distinction is the most important judgment call in this skill.

**Skills teach how; steering constrains when, where, and under what authority.** A skill says "here is the process for doing X." Steering says "in this scope, you may only do X under these conditions, with these limits, and never doing Y." If the output is a procedure, it belongs in a skill. If it is a constraint or an operating boundary, it belongs in steering.

**Repo steering should not contain every workflow detail.** Repository-level steering documents what the system is, what agents should know about the layout and build process, and what invariants must not be violated. It is not a tutorial, a style guide, or a prompt collection. Keep it minimal, imperative, and stable.

**Local steering should be narrow, temporary, and explicit.** Working-directory and session-level instructions exist to handle context that is ephemeral — a specific task, a testbed session, a branch-scoped constraint. They should be gitignored (or at least clearly marked as temporary) and should not leak into global repo doctrine.

**Testbed steering should be safety-heavy and environment-specific.** Testbeds have real infrastructure. Steering for testbeds must be explicit about what the agent is allowed to touch, what requires confirmation, and what is forbidden. "Read-first" and "gate before mutate" principles apply here most strongly.

**Precedence must be explicit when multiple steering files apply.** The standard loading order is: global → user → repo → module/directory → worktree-local → testbed → session. When files conflict, the narrower scope wins unless the broader scope explicitly overrides. If this is ambiguous, surface the conflict rather than silently resolving it.

**Good steering is enforceable, scoped, minimal, and conflict-aware.** Every rule in a steering file should be checkable: either the agent did it or it didn't. Vague instructions ("be careful," "use good judgment") are not steering — they are noise. If a rule cannot be violated in an observable way, it is not a rule.

**Avoid making steering a hidden prompt dump.** The most common failure is turning a steering file into an accumulated pile of instructions that grew session by session. This produces unpredictable behavior, routing confusion, and contradictions. Steering files should be intentionally designed and periodically reviewed, not passively accumulated.

## Procedure

### design mode
1. Establish scope: what system or environment is this steering for, and which agents will load it?
2. Identify the appropriate file type and location based on scope:
   - Repository-wide: `STEERING.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
   - Agent-specific: `agents/<name>/AGENT.md`
   - Working-directory: `CLAUDE.local.md` or equivalent (gitignored)
   - Testbed: co-located with testbed setup, environment-specific
3. Define the core sections for repo-level steering: what the system is, layout, build/test commands, invariants, and agent routing.
4. Write rules as imperative directives. Avoid prose paragraphs. One rule per line where possible.
5. Flag anything that should be in an ADR or a skill rather than in steering.
6. Check that no credentials, secrets, or sensitive paths are included.
7. Return the complete instruction file.

### review mode
1. Load all supplied instruction files and note their scope and intended audience.
2. Check for gaps: are there agent behaviors that are unaddressed? Are there implicit assumptions that should be explicit?
3. Check for contradictions: do any rules in the same file conflict? Do rules across files conflict?
4. Check enforceability: for each rule, ask "can an agent observably violate this?" If not, flag it as a non-rule.
5. Check scope leakage: does a local or testbed file contain rules that belong in repo steering, or vice versa?
6. Check for anti-patterns (see `anti-patterns` mode for the full list).
7. Produce a findings report: gap / contradiction / enforceability / scope-leakage issues, each with a specific recommendation.

### precedence mode
1. List all instruction files in scope and their scope level (global / repo / module / local / testbed / session).
2. For each conflict: identify which rule wins under the standard loading order (narrower scope wins).
3. Flag cases where a broader scope explicitly overrides a narrower one — these are intentional overrides and should be documented.
4. Flag cases where the conflict is genuinely ambiguous — do not resolve silently.
5. Propose a merged or layered result that makes the precedence explicit, with comments in the output files noting the resolution.

### localize mode
1. Load the base steering file.
2. Identify which rules are universal (keep as-is) and which need adaptation for the target scope.
3. Write a scoped overlay: rules that apply only in the target directory, testbed, or environment.
4. Ensure the overlay does not contradict the base without explicit rationale.
5. Mark the output as scoped: include a header noting what context it governs and that it supplements (does not replace) the base steering.

### anti-patterns mode
1. Review the supplied files for the following named anti-patterns:
   - **Prompt dump**: instruction file is a bag of accumulated session instructions with no structure or expiry
   - **Scope bleed**: local or testbed rules are in repo-level files, or vice versa
   - **Vague constraint**: rules that cannot be verified ("be careful," "use judgment," "act professionally")
   - **Hidden credentials**: secrets, tokens, or paths to sensitive resources embedded in instruction text
   - **Catch-all override**: a rule so broad it applies to everything and effectively overrides all specific rules
   - **Contradictory authority**: two rules granting or denying the same permission in the same scope
   - **Missing precedence**: multiple files apply to the same context with no defined loading order
   - **Workflow buried in steering**: a procedure that should be a skill is written as a steering rule
2. For each pattern found: name it, quote the offending text, explain the impact, and recommend a fix.

### migration mode
1. Parse the ad-hoc instructions: identify which are constraints (→ steering), which are procedures (→ skill), and which are documentation (→ plain doc).
2. For the constraint subset: group by scope (global, repo, agent, local, testbed).
3. Write a properly scoped instruction file for each scope with content from step 2.
4. Flag any instruction that is too ambiguous to place — return it to the caller for clarification.
5. Produce a migration note: what was converted, what was redirected to a skill, and what was dropped as noise.

## Edge Cases

**Multiple instruction files exist and no one knows what loads when:** Run `precedence` mode. Do not guess the loading order — establish it explicitly and document it in each file's header.

**Instructions contain embedded credentials or tokens:** Flag immediately. Do not include them in any output. The fix is always to move credentials to environment variables or a secrets manager.

**Steering file has grown to hundreds of lines:** Apply the prompt-dump anti-pattern check. Long steering files are almost always a sign that procedures, documentation, and constraints have been mixed together. Separate them.

**Testbed steering conflicts with repo steering on a safety constraint:** The testbed file wins for testbed-specific behavior, but it must state the override explicitly. A silent override is an anti-pattern regardless of intent.

**Caller asks for steering that would grant an agent unrestricted system access:** Flag this as a safety concern. Propose a gated alternative: the agent may request an operation, but a human confirms before execution.

**The task is ambiguous between designing steering and creating a skill:** Apply the "constraint vs. procedure" test. If the output is a rule that limits behavior, it is steering. If the output is a sequence of steps for accomplishing a task, it is a skill. If both, produce both outputs and label them clearly.

## Quality Gates

Before delivering any output:

- [ ] Every instruction file has an explicit scope header: what it governs and who loads it
- [ ] Authority boundaries are stated: what agents may do and what is forbidden in this scope
- [ ] Precedence is defined when more than one file applies to the same context
- [ ] Every rule is enforceable: observable, not vague
- [ ] No credentials, secrets, or sensitive paths appear in any output
- [ ] No broad catch-all instruction that applies to everything without scoping
- [ ] Local or testbed rules are clearly marked as scoped and do not appear in global/repo files
- [ ] Contradictions are surfaced and resolved — not silently dropped
- [ ] Anti-patterns section is present in review outputs when any pattern is found
- [ ] If a procedure was found in the input and redirected to a skill, this is noted explicitly in the output
