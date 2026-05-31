# polyskills — Amp Adapter

Amp spawns sub-agents inline via the `Spawn` tool — no predefined agent files needed.
The skill library is still useful: load `skills/INDEX.md` and match to a skill before coding.

## Skill Routing in Amp

Paste this at the start of an Amp session or add to your Amp system prompt:

```
You have access to a skill library at skills/INDEX.md.
1. Load skills/INDEX.md first.
2. Match the user's request to a skill trigger.
3. Load skills/<name>/SKILL.md and follow its Process steps.
```

## Agent Spawning in Amp

Amp spawns agents on-demand with inline prompts. Use the agent definitions in
`agents/<name>/AGENT.md` as the briefing template:

```
Spawn the phoenix agent:
  Task: [add skill / fix agent / sync INDEX / update STEERING]
  Scope: polyskills repo only
  See full spec: agents/phoenix/AGENT.md
```

Available agents: phoenix

## No Config File

Amp does not currently read a project instruction file automatically.
Use the Amp system prompt setting or paste the routing instructions manually.
