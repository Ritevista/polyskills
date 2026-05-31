# MCP Servers

Skills are reasoning patterns. MCP servers provide the capabilities skills reason about.
Never embed API calls or tool-specific logic inside a SKILL.md — declare the requirement
via `metadata.mcp-required` and let the MCP provide it.

## Planned integrations

| MCP | Unlocks | Status | Notes |
|-----|---------|--------|-------|
| GitHub | github skill — PRs, reviews, repo ops | ❌ Not wired | Skill pending |
| GitLab | gitlab skill — MRs, pipelines, reviews | ❌ Not wired | Skill pending |
| Gmail | Mail operations | ❌ Not wired | Skill pending |
| Google Calendar | Scheduling | ❌ Not wired | Skill pending |
| Web Search | Research agents and skills | ❌ Not wired | Agent pending |
| Filesystem | Local doc ingestion | ❌ Not wired | — |

## Wiring an MCP

Each tool has its own MCP configuration path:

- **Claude Code**: add to `.claude/settings.json` under `mcpServers`
- **Cursor**: add to `.cursor/mcp.json`
- **Gemini CLI**: add to `.gemini/settings.json`
- **Kiro**: configure in the Kiro MCP settings panel

Once wired, skills that declare `metadata.mcp-required: [mcp-name]` will have full
capability. Without the MCP, those skills operate in degraded mode (reasoning only,
no live data fetch).
