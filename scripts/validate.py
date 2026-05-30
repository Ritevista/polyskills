#!/usr/bin/env python3
"""
polyskills library validator
Validates all SKILL.md and AGENT.md definitions for format compliance.
Exit 0 = all pass (warnings allowed). Exit 1 = errors found.
"""

import sys
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)


ROOT = Path(__file__).parent.parent
DESCRIPTION_WARN_LIMIT = 200
DESCRIPTION_MAX = 1024

SKILL_REQUIRED_SECTIONS = [
    "## Routing",
    "## Contract",
    "## Reasoning",
    "## Procedure",
    "## Edge Cases",
    "## Quality Gates",
]

AGENT_REQUIRED_SECTIONS = [
    "## Input Contract",
    "## Output Contract",
    "## Constraints",
]


def parse_frontmatter(filepath: Path):
    """Return (frontmatter_dict, body_str) or (None, full_content)."""
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None, content
    try:
        end = content.index("---", 3)
        fm = yaml.safe_load(content[3:end]) or {}
        return fm, content[end + 3:]
    except (ValueError, yaml.YAMLError) as e:
        return None, content


def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9-]*$", name))


def validate_skill(skill_dir: Path):
    errors, warnings = [], []
    label = f"skills/{skill_dir.name}"
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"{label}: missing SKILL.md"], []

    fm, body = parse_frontmatter(skill_md)

    if fm is None:
        return [f"{label}: missing or invalid YAML frontmatter"], []

    # name
    name = fm.get("name", "")
    if not name:
        errors.append(f"{label}: missing 'name' field")
    elif name != skill_dir.name:
        errors.append(f"{label}: name '{name}' does not match directory '{skill_dir.name}'")
    elif not is_valid_name(name):
        errors.append(f"{label}: name must be lowercase-hyphenated (got '{name}')")

    # description
    desc = str(fm.get("description", "")).strip()
    if not desc:
        errors.append(f"{label}: missing 'description' field")
    elif len(desc) > DESCRIPTION_MAX:
        errors.append(f"{label}: description exceeds {DESCRIPTION_MAX} chars ({len(desc)})")
    elif len(desc) > DESCRIPTION_WARN_LIMIT:
        warnings.append(f"{label}: description over {DESCRIPTION_WARN_LIMIT} chars ({len(desc)}) — may not work in all products")

    # metadata
    meta = fm.get("metadata", {}) or {}
    if not meta.get("version"):
        warnings.append(f"{label}: missing metadata.version")

    # required sections
    for section in SKILL_REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{label}: missing section '{section}'")

    # evals
    evals_dir = skill_dir / "evals"
    tq = evals_dir / "trigger_queries.json"
    if not evals_dir.exists():
        warnings.append(f"{label}: missing evals/ directory")
    elif not tq.exists():
        warnings.append(f"{label}: missing evals/trigger_queries.json")
    else:
        try:
            tq_data = json.loads(tq.read_text())
            should = tq_data.get("should_trigger", [])
            should_not = tq_data.get("should_not_trigger", [])
            if len(should) < 3:
                warnings.append(f"{label}: fewer than 3 should_trigger queries in evals/")
            if len(should_not) < 3:
                warnings.append(f"{label}: fewer than 3 should_not_trigger queries in evals/")
        except (json.JSONDecodeError, KeyError):
            errors.append(f"{label}: evals/trigger_queries.json is invalid JSON or missing keys")

    return errors, warnings


def validate_agent(agent_dir: Path, is_sub_agent: bool = False):
    errors, warnings = [], []
    tier = "sub-agents" if is_sub_agent else "agents"
    label = f"{tier}/{agent_dir.name}"
    agent_md = agent_dir / "AGENT.md"

    if not agent_md.exists():
        return [f"{label}: missing AGENT.md"], []

    fm, body = parse_frontmatter(agent_md)

    if fm is None:
        return [f"{label}: missing or invalid YAML frontmatter"], []

    # name
    name = fm.get("name", "")
    if not name:
        errors.append(f"{label}: missing 'name' field")
    elif name != agent_dir.name:
        errors.append(f"{label}: name '{name}' does not match directory '{agent_dir.name}'")

    # description
    desc = str(fm.get("description", "")).strip()
    if not desc:
        errors.append(f"{label}: missing 'description' field")
    elif len(desc) > DESCRIPTION_MAX:
        errors.append(f"{label}: description exceeds {DESCRIPTION_MAX} chars ({len(desc)})")
    elif len(desc) > DESCRIPTION_WARN_LIMIT:
        warnings.append(f"{label}: description over {DESCRIPTION_WARN_LIMIT} chars — may not work in all products")

    # role
    role = fm.get("role", "")
    if not role:
        errors.append(f"{label}: missing 'role' field (worker | sub-agent)")
    elif is_sub_agent and role != "sub-agent":
        warnings.append(f"{label}: role should be 'sub-agent' for files in sub-agents/")
    elif not is_sub_agent and role not in ("worker", "agent", "orchestrator"):
        warnings.append(f"{label}: unexpected role '{role}' for files in agents/")

    # spawned-by (sub-agents only)
    if is_sub_agent and not fm.get("spawned-by"):
        errors.append(f"{label}: sub-agent missing 'spawned-by' field")

    # context-budget
    if not fm.get("context-budget"):
        warnings.append(f"{label}: missing 'context-budget' field (tiny|small|medium|large)")

    # required sections
    for section in AGENT_REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{label}: missing section '{section}'")

    return errors, warnings


def check_index_sync(index_path: Path, definitions_dir: Path, kind: str):
    """Warn if a definition directory is not listed in the INDEX.md."""
    warnings = []
    if not index_path.exists() or not definitions_dir.exists():
        return warnings

    index_content = index_path.read_text()
    for d in sorted(definitions_dir.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name != "INDEX.md":
            if d.name not in index_content:
                warnings.append(f"INDEX: {kind}/{d.name} not listed in {index_path.relative_to(ROOT)}")
    return warnings


def main():
    all_errors = []
    all_warnings = []
    names_seen = {}

    # --- Skills ---
    skills_dir = ROOT / "skills"
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                e, w = validate_skill(d)
                all_errors.extend(e)
                all_warnings.extend(w)
                if d.name in names_seen:
                    all_errors.append(f"DUPLICATE name '{d.name}' in skills/ and {names_seen[d.name]}")
                else:
                    names_seen[d.name] = "skills/"

    # --- Agents ---
    agents_dir = ROOT / "agents"
    if agents_dir.exists():
        for d in sorted(agents_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                e, w = validate_agent(d, is_sub_agent=False)
                all_errors.extend(e)
                all_warnings.extend(w)
                if d.name in names_seen:
                    all_errors.append(f"DUPLICATE name '{d.name}' in agents/ and {names_seen[d.name]}")
                else:
                    names_seen[d.name] = "agents/"

    # --- Sub-agents ---
    sub_agents_dir = ROOT / "sub-agents"
    if sub_agents_dir.exists():
        for d in sorted(sub_agents_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                e, w = validate_agent(d, is_sub_agent=True)
                all_errors.extend(e)
                all_warnings.extend(w)

    # --- Index sync checks ---
    all_warnings.extend(check_index_sync(ROOT / "skills" / "INDEX.md", skills_dir, "skills"))
    all_warnings.extend(check_index_sync(ROOT / "agents" / "INDEX.md", agents_dir, "agents"))
    all_warnings.extend(check_index_sync(ROOT / "sub-agents" / "INDEX.md", sub_agents_dir, "sub-agents"))

    # --- Report ---
    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(f"  ⚠  {w}")
        print()

    if all_errors:
        print("ERRORS:")
        for e in all_errors:
            print(f"  ✗  {e}")
        print(f"\nResult: {len(all_errors)} error(s), {len(all_warnings)} warning(s) — FAIL")
        sys.exit(1)
    else:
        status = f"{len(all_warnings)} warning(s)" if all_warnings else "clean"
        print(f"Result: all definitions valid — {status} — PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
