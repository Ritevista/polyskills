---
name: handoff
description: "Captures session state for resumption. Use when: pausing mid-task, switching agents, or context is about to be lost. Not for: completed work or permanent project docs."
metadata:
  version: "1.0.0"
  mcp-required: []
user-invocable: true
---

# handoff

## Routing

Use this skill when a session will end or transfer before work is complete and the next session (or agent) needs enough context to continue without losing ground.

**Use when:**
- Ending a session with unfinished tasks
- Passing work to another agent or a future instance of the same agent
- Context window is approaching its limit and continuation is needed
- A long-running task is being paused and must be resumable

**Do not use when:**
- Work is complete — write a summary or close the task instead
- The output is meant as permanent project documentation — use a different format
- The task is short enough to restart from scratch — don't over-engineer continuity

## Contract

**Required:**
- `task` — what was being worked on (one sentence)
- `status` — what has been done and what has not

**Optional:**
- `blockers` — anything that stopped progress or requires a decision before continuing
- `files` — key files that are in a modified or intermediate state
- `next-step` — the exact first action the next session should take

**Output:** `handoff-[topic]-[YYYY-MM-DD].md` placed in the current working directory or as inline output.

**Success criteria:**
- A cold-start agent or future session can pick up without re-reading the full prior context
- No ambiguity about what is done vs not done
- The single next action is identified explicitly

## Reasoning

A handoff is a resumption contract, not a summary. Its job is to eliminate re-work and decision ambiguity for whoever picks up next.

- **The next-step is the most important field.** A handoff without a clear next action forces the receiver to re-derive where to start. That is the failure this skill exists to prevent.
- **Done vs not-done must be unambiguous.** "In progress" is not a state — specify what exists on disk and what does not.
- **Blockers are not excuses.** List a blocker only if it must be resolved before proceeding. If the work can continue around it, note the blocker separately but keep the next-step clear.
- **Scope to resumption, not documentation.** A handoff document is ephemeral — it is not a design doc or a log. Once work resumes and completes, the handoff is superseded.
- **The most common mistake** is writing a handoff that summarizes what happened rather than specifying how to continue. If the document looks like meeting notes, rewrite it as a task state.

## Procedure

1. **State the task** — one sentence: what is being worked on and what the end goal is.
2. **List what is done** — enumerate completed steps or artifacts that exist on disk. Be specific (file names, not vague descriptions).
3. **List what is not done** — enumerate remaining steps in order. Use the same level of specificity as the original task.
4. **Identify the single next action** — the first thing the next session must do. One imperative sentence. If there is a decision to make first, state the decision and the options.
5. **List blockers** (if any) — items that must be resolved before or during continuation. For each: what is blocked, and what would unblock it.
6. **List key files in intermediate state** (if any) — files that are partially written, modified but not committed, or otherwise mid-flight.
7. **Note any context that would be lost** — non-obvious decisions made during the session, rejected alternatives, or constraints discovered mid-work.
8. **Write output** to `handoff-[topic]-[YYYY-MM-DD].md`.

## Edge Cases

**Work is 95% complete:** Finish it instead of writing a handoff. A handoff for one remaining step wastes more time than completing the step.

**Multiple blockers with no clear next step:** The handoff is blocked. State this explicitly and list what decisions need to be made before work can resume. Do not manufacture a false next-step.

**Files are in a broken intermediate state:** Note the exact state — what was partially written, what is missing, and whether the partial state is safe to build on or should be discarded.

**Context window is the reason for handoff:** Include the most critical reasoning and decisions made in the session — these are exactly what gets lost in a new context and cannot be re-derived from files alone.

**Handoff to a different agent type:** Note what tools, permissions, or context the receiving agent will need that the current agent had.

## Quality Gates

Before delivering output:

- [ ] Task is stated in one sentence with a clear end goal
- [ ] Done items reference specific files or artifacts, not vague descriptions
- [ ] Not-done items are ordered by dependency (what must happen before what)
- [ ] A single next action is present — imperative, unambiguous
- [ ] Any blocker has a corresponding "what would unblock it" entry
- [ ] Files in intermediate state are listed with their current condition
- [ ] A cold-start reader can act on the handoff without asking follow-up questions
