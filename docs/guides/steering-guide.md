# Steering for Agentic Systems

> Reference guide for skills that create or scaffold new projects and repositories.
> Load this when producing steering files (AGENTS.md, CLAUDE.md, etc.) as part of a new project.

## What steering is

**Steering** is the persistent, scoped instruction layer that shapes how an agent explores a codebase, chooses tools, runs commands, validates work, and presents results. It lives in versioned repository artefacts: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, and tool-specific settings, hooks, and rules.

The strongest common pattern is **hierarchical scoping**: broad defaults at global/user scope, shared norms at repository scope, narrower instructions at module/directory scope, and ephemeral guidance at session scope.

**Critical distinction**: steering files are advisory, not enforcement. Executable guardrails (hooks, permission rules, CI checks) materially improve compliance. Plain-text steering is context, not constraint.

---

## Steering scope taxonomy

| Scope | Owner | What belongs here | Examples |
|-------|-------|-------------------|---------|
| **Global** | Org/machine policy | Non-negotiable institutional defaults | Claude managed settings, Codex system config |
| **User** | Individual | Personal editor/review/response preferences | `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` |
| **Repository** | Team | Shared stable norms: layout, build, test, invariants | Root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` |
| **Module/directory** | Subsystem owner | Package-specific commands, framework conventions | Nested `AGENTS.md`, path-scoped rules |
| **Worktree-local** | Individual | Private, temporary, branch-specific notes | `CLAUDE.local.md` (gitignored) |
| **Testbed** | Platform/infra | Environment setup, secrets injection, evidence collection | Setup scripts, sandbox policy, runner config |
| **Session** | Task | Current task brief, acceptance criteria, risk focus | User prompt, attached artefacts |

---

## What belongs in steering (and what does not)

### Include

- What the system is and where code lives
- How to build, test, lint (exact commands)
- Mandatory quality gates before completion
- Architecture constraints and invariants
- Coding conventions and patterns specific to the repo
- Cross-cutting review standards

### Exclude

- **Secrets, tokens, credentials** — use secret stores or environment variables, never steering files
- Long narrative prose or duplicated documentation
- Stale operational facts that change frequently
- Things better served by tools, MCP integrations, or environment setup scripts
- Everything a competent engineer would already know

**Writing style**: short, imperative, well-structured directives. Specific and concise instructions are followed more consistently than long paragraphs. One domain per file. Explicit examples beat abstract descriptions.

---

## Tool-agnostic steering stack

For any new project, produce these layers:

### Layer 1: Shared canonical contract (`AGENTS.md`)

The single source of truth. Every tool either reads this directly or via a thin adapter.

```markdown
# AGENTS.md

## What this is
[One sentence on the system.]

## Layout
- [Key directories and what they contain]

## Build and test
- Setup: `[command]`
- Tests: `[command]`
- Before completing any task: run lint + tests relevant to changed files

## Invariants
- [Hard rules that cannot be violated]
- [Prefer X over Y when Z]
```

### Layer 2: Tool adapters (thin, reference AGENTS.md)

Only add these when the tool requires a different filename:

| File | Tool | Notes |
|------|------|-------|
| `CLAUDE.md` | Claude Code | Can import/reference AGENTS.md |
| `GEMINI.md` | Gemini CLI | Or configure `context.fileName` to point to AGENTS.md |
| `.github/copilot-instructions.md` | GitHub Copilot | Repo-wide Copilot steering |
| `.github/instructions/*.instructions.md` | Copilot path-specific | Use `applyTo` globs for monorepo subsystems |
| `.kiro/steering/product.md` etc. | Kiro | `always` / `fileMatch` / `manual` / `auto` inclusion modes |

Keep adapters thin — their job is to point to AGENTS.md, not duplicate it.

### Layer 3: Module-level steering (close to the code)

Add nested `AGENTS.md` files only when a subsystem has genuinely different conventions:

```markdown
# packages/api/AGENTS.md

## Package rules
- Run commands from `packages/api/`
- Use `make test-api`, not the repo-wide test command
- Route handlers stay thin; business logic in `domain/`
- Never access secrets directly from handlers
```

### Layer 4: Worktree-local (gitignored, temporary)

For personal or branch-specific notes. **Always gitignore this file.**

```markdown
# .agent-local.md  (gitignored)

## Personal local notes
- Use local test dataset `sample-small`
- Current branch is exploratory; avoid schema migrations
- Delete or rewrite before sharing this worktree
```

### Layer 5: Testbed/environment (executable, not prose)

Environment steering should be mostly executable configuration, not narration.

```markdown
# testbeds/staging/steering.md

## Environment purpose
- Integration validation only

## Setup
- `docker compose -f testbeds/staging/compose.yml up -d`
- `scripts/seed_staging.sh`

## Evidence required after each run
- Failing test names
- Service logs for touched components
- Exact commit, config profile, and dataset used
```

### Layer 6: Enforcement (hooks, permissions, CI)

Advisory steering + executable enforcement > advisory steering alone.

| Mechanism | What it enforces |
|-----------|-----------------|
| Hooks (`PreToolUse`) | Block specific tool patterns before execution |
| Permission rules | Scope what the agent may read/write/run |
| CI pipeline | Gate merges on lint, test, security checks |
| Sandbox policy | Network and filesystem boundaries |

---

## Recommended file layout for a new project

```text
repo-root/
├── AGENTS.md                          # Canonical shared steering
├── CLAUDE.md                          # Adapter: imports AGENTS.md
├── GEMINI.md                          # Adapter: imports AGENTS.md
├── .github/
│   ├── copilot-instructions.md        # Copilot repo-wide steering
│   ├── instructions/
│   │   └── [subsystem].instructions.md  # Path-specific (monorepo)
│   └── workflows/
│       └── copilot-setup-steps.yml    # Copilot cloud-agent testbed setup
├── .claude/
│   ├── rules/                         # Path-scoped rules
│   └── settings.json                  # Permissions and settings
├── .codex/
│   ├── config.toml
│   └── hooks.json
├── .gemini/
│   └── settings.json
├── .kiro/
│   └── steering/
│       ├── product.md
│       ├── tech.md
│       └── structure.md
├── packages/
│   ├── api/
│   │   └── AGENTS.md                  # Module-local steering
│   └── web/
│       └── AGENTS.md
└── .agent-local.md                    # Gitignored personal/worktree-local note
```

---

## Loading and precedence rules

Precedence differs across tools — do not rely on intuition.

| Tool | Precedence model |
|------|-----------------|
| Codex | Root-to-CWD hierarchy; closer file wins; `AGENTS.override.md` takes precedence over `AGENTS.md` |
| Claude | Ancestor files concatenate root-to-CWD; `CLAUDE.local.md` appends after shared at each level; subdirectory files load on demand |
| Gemini | Hierarchical concatenation + JIT discovery when tools access directories |
| Copilot | Personal > org > repo; path-specific files combine with repo-wide where both apply |
| Kiro | Workspace overrides global; `always` > `fileMatch` > `auto` > `manual` |

**Generic rule**: enforced controls outrank advisory text; more specific scope outranks broader scope; most explicit/recent task instruction wins within the same scope.

---

## Verification checklist

When producing steering for a new project, verify:

- [ ] `AGENTS.md` exists at repo root with build/test commands and invariants
- [ ] Tool adapter files are present for each target platform
- [ ] No secrets or credentials in any steering file
- [ ] Module-level `AGENTS.md` files exist for subsystems with different conventions
- [ ] `.agent-local.md` is listed in `.gitignore`
- [ ] At least one enforcement mechanism (hook, permission rule, or CI gate) is configured
- [ ] Testbed setup is executable (scripts, not just prose)
- [ ] All steering files use short, imperative directives (not narrative prose)

---

## Session brief template

For ephemeral task-level steering (not committed):

```markdown
Task: [one sentence]

Constraints:
- Touch only [scope] unless necessary
- Prefer [X] over [Y]
- Stop and ask before [risky action]

Done when:
- [Verifiable condition 1]
- [Verifiable condition 2]
- Root cause or decision is summarised in the final note
```

---

## Key design principle

> Keep repo and module steering **versioned and shareable**, worktree-local steering **gitignored and temporary**, and testbed steering **executable and auditable**.

One Markdown file cannot carry repository knowledge, local quirks, and environment provisioning all at once. The layered model exists precisely to avoid that mistake.
