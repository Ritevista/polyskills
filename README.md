# polyskills

**A lean, principled multi-agent skill library. Write skills once, deploy across Claude Code, Codex, Gemini, Cursor, Kiro, Cline, and Amp. Six-layer skill format with progressive disclosure — agents load only what they need. Ships with a self-extending library agent (phoenix) that validates, indexes, and commits on approval.**

---

## How It Works

```
Request arrives
    │
    ▼
Load skills/INDEX.md → match? → load SKILL.md → execute
    │
    └─ no match → load agents/INDEX.md → spawn worker agent
```

Agents load `skills/INDEX.md` first (one line per skill). The full `SKILL.md` is loaded only when a skill matches. Context cost is O(1) per invocation, not O(n).

---

## Skills (2 of 10)

| Skill | Trigger | SKILL.md |
|-------|---------|----------|
| synthesis | Messy multi-source input (notes, docs, feedback) needs consolidating into a clear finding | [skills/synthesis/SKILL.md](skills/synthesis/SKILL.md) |
| handoff | Session ending with unfinished work; passing state to next session or agent | [skills/handoff/SKILL.md](skills/handoff/SKILL.md) |

Skills are added via phoenix as real use cases emerge — not speculatively. Ceiling: 10.

---

## Agents (1 of 6)

| Agent | When to spawn | AGENT.md |
|-------|--------------|----------|
| phoenix | Add/fix/sync anything in the polyskills library | [agents/phoenix/AGENT.md](agents/phoenix/AGENT.md) |

Phoenix owns the full maintenance loop: reads STEERING.md → produces definitions → writes files → runs validate.py → shows diff → commits on approval. It also updates its own definition when its job changes.

---

## Supported Platforms

| Platform | Adapter location |
|----------|-----------------|
| Claude Code | `.claude/agents/` |
| OpenAI Codex | `AGENTS.md` |
| Gemini CLI | `.gemini/agents/` |
| Cursor | `.cursor/agents/` |
| Kiro | `adapters/kiro/` |
| Cline | `.clinerules` |
| Amp | `adapters/amp/USAGE.md` |

---

## Quick Start

```bash
git clone https://github.com/Ritevista/polyskills.git
cd polyskills
python3 scripts/validate.py   # verify everything is clean
```

Copy or symlink the adapter for your platform into its config directory. Ask your agent: **"What skills do you have?"**

---

## Repo Structure

```
polyskills/
├── STEERING.md                  # read first — current state and routing
├── skills/
│   ├── INDEX.md                 # agents load this first
│   ├── synthesis/SKILL.md
│   └── handoff/SKILL.md
├── agents/
│   ├── INDEX.md
│   └── phoenix/AGENT.md
├── sub-agents/INDEX.md          # none yet
├── common-skills/               # confidence-rating, output-formatting, quality-checklist
├── templates/                   # SKILL_TEMPLATE, AGENT_TEMPLATE, SUB_AGENT_TEMPLATE
├── docs/
│   ├── adrs/                    # 8 ADRs covering architecture decisions
│   ├── guides/                  # skill-writing-guide, steering-guide
│   └── specs/                   # skill and agent format specs
├── scripts/validate.py          # CI validator
└── adapters/                    # platform-specific adapter sources
```

---

## Design Principles

1. **Skills are knowledge, not code** — Markdown, readable by any LLM, no runtime deps
2. **Adapters are thin** — pointers only, zero skill logic
3. **MCPs are capabilities** — never put tool access inside a skill
4. **Load lazily** — INDEX.md first, full SKILL.md only on match
5. **10 skills is a ceiling, not a floor** — earn your place or get pruned

---

## Validation

```bash
python3 scripts/validate.py
# Result: all definitions valid — N warning(s) — PASS
```

Run before every commit. Zero errors required; warnings are acceptable.

---

MIT License
