# polyskills

**Lean, principled, multi-agent skill library. Write skills once — use across Claude Code, Codex, Kiro, Gemini, OpenClaw, Cursor, Windsurf, and more.**

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Layer 3: Adapters       (thin, per-agent, no logic)      │
│  CLAUDE.md / AGENTS.md / .kiro/ / .gemini/ / .cursor/     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: Skill Library  (portable Markdown, ~10 skills)  │
│  skills/INDEX.md  →  skills/<name>/SKILL.md               │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Foundation     (shared patterns + MCP wiring)   │
│  common-skills/   mcp-servers/   templates/               │
└──────────────────────────────────────────────────────────┘
```

Skills are **reasoning patterns** — they tell the agent how to think.
MCPs are **capabilities** — they give the agent access to systems.
Never conflate the two.

---

## Supported Agents

| Agent | Adapter | Status |
|-------|---------|--------|
| Claude Code | `CLAUDE.md` → `~/.claude/CLAUDE.md` | ✅ |
| OpenAI Codex | `AGENTS.md` → `~/.codex/AGENTS.md` | ✅ |
| AWS Kiro | `.kiro/specs/polyskills.md` | ✅ |
| Gemini CLI / Code Assist | `.gemini/instructions.md` | ✅ |
| Cursor | `.cursor/rules.md` | ✅ |
| Windsurf | `.windsurfrules` | ✅ |
| OpenClaw | `adapters/openclaw/` | ✅ |
| Cline | `.clinerules` | ✅ |
| Amp | `adapters/amp/USAGE.md` | ✅ (manual) |

---

## Agents (6, ceiling)

| Agent | When to Spawn | MCP |
|-------|--------------|-----|
| [researcher](agents/researcher/AGENT.md) | deep investigation in parallel, evidence gathering | web-search |
| [critic](agents/critic/AGENT.md) | adversarial review, stress-test a plan/doc | — |
| [sme](agents/sme/AGENT.md) | "SME [domain]" — validate domain assumption | — |
| [scout](agents/scout/AGENT.md) | idea triage before committing to a repo | optional |
| [distiller](agents/distiller/AGENT.md) | extract structure from transcripts, notes, raw drafts | — |
| [phoenix](agents/phoenix/AGENT.md) | identify library gaps, propose new skill/agent/sub-agent | — |

## Sub-Agents (4, no ceiling)

Atomic workers spawned BY agents — not by the user directly.

| Sub-Agent | Spawned By | Task |
|-----------|-----------|------|
| [web-searcher](sub-agents/web-searcher/AGENT.md) | researcher, scout | single query → results |
| [doc-reader](sub-agents/doc-reader/AGENT.md) | researcher, distiller | single source → extract |
| [assumption-checker](sub-agents/assumption-checker/AGENT.md) | critic | single assumption → counter-argument |
| [section-extractor](sub-agents/section-extractor/AGENT.md) | distiller | single section → structured list |

Agent + sub-agent files deployed to `.claude/agents/`, `.cursor/agents/`, `.gemini/agents/` (flat — Claude Code/Cursor/Gemini don't distinguish tiers). Kiro uses a DAG adapter. Cline and Amp spawn inline.

---

## Skills (10)

| Skill | Trigger | MCP Needed |
|-------|---------|-----------|
| [requirement-study](skills/requirement-study/SKILL.md) | analyze/write/validate requirements, PRD, feature spec | — |
| [implementation-sketch](skills/implementation-sketch/SKILL.md) | implementation plan, task breakdown from spec | — |
| [systems-architect](skills/systems-architect/SKILL.md) | system design, architecture decision, trade-off analysis | — |
| [research-analyst](skills/research-analyst/SKILL.md) | deep research, evidence synthesis, competitive analysis | Web Search |
| [qa-validator](skills/qa-validator/SKILL.md) | test strategy, acceptance criteria, pre-delivery validation | — |
| [security-guardian](skills/security-guardian/SKILL.md) | threat model, security review, vulnerability analysis | — |
| [domain-expert](skills/domain-expert/SKILL.md) | "SME [domain]" — parameterized deep domain expertise | — |
| [repo-bootstrap](skills/repo-bootstrap/SKILL.md) | scaffold new repo, CI/CD setup, project structure | GitHub |
| [poc-spike](skills/poc-spike/SKILL.md) | proof-of-concept, de-risk technical unknown | — |
| [context-handoff](skills/context-handoff/SKILL.md) | session handoff, context pack, cross-agent state transfer | — |

---

## Quick Start

```bash
# Clone
git clone https://github.com/<you>/polyskills.git
cd polyskills

# Global install (copies adapters + skill library to agent config dirs)
python3 scripts/polyskillsctl.py install-global

# Or: symlink for live development
python3 scripts/polyskillsctl.py install-global --link
```

After install, ask any supported agent: **"What skills do you have?"**

---

## Context Efficiency Protocol

Agents load `skills/INDEX.md` first (one file, one line per skill).
Full `SKILL.md` is loaded only for the matched skill.
This keeps context usage O(1) per invocation instead of O(n).

---

## MCP Wiring

Skills are reasoning only. Capabilities come from MCPs.
See [`mcp-servers/README.md`](mcp-servers/README.md) for which MCPs to wire and how.

Recommended: Gmail, GitHub, Google Calendar, filesystem, web search.

---

## Design Principles

1. **Skills are knowledge, not code** — Markdown, readable by any LLM, no runtime deps
2. **Adapters are thin** — pointers only, zero skill logic
3. **MCPs are capabilities** — never put tool access inside a skill
4. **Load lazily** — INDEX.md first, full SKILL.md only on match
5. **10 skills is a ceiling, not a floor** — prune before you add

---

## Repo Structure

```
polyskills/
├── CLAUDE.md                  # Claude Code root adapter
├── AGENTS.md                  # Codex root adapter
├── .windsurfrules              # Windsurf adapter
├── .kiro/specs/polyskills.md  # Kiro adapter
├── .gemini/instructions.md    # Gemini adapter
├── .cursor/rules.md           # Cursor adapter
│
├── skills/
│   ├── INDEX.md               # ← agents load this first
│   ├── requirement-study/
│   ├── implementation-sketch/
│   ├── systems-architect/
│   ├── research-analyst/
│   ├── qa-validator/
│   ├── security-guardian/
│   ├── domain-expert/
│   ├── repo-bootstrap/
│   ├── poc-spike/
│   └── context-handoff/
│
├── common-skills/             # shared reasoning patterns
├── mcp-servers/               # MCP wiring guides
├── adapters/                  # canonical adapter sources
├── templates/                 # SKILL_TEMPLATE + doc templates
└── docs/                      # principles, ADRs
```

---

MIT License
