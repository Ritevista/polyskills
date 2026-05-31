# ADR-007: Phoenix as Library Self-Extension Mechanism

**Status**: Accepted
**Date**: 2026-05-30

## Context

A skill library that can only be extended by its authors scales poorly. Users and teams discover gaps through usage — a transcript shows a recurring task without a skill, a new agent workflow reveals a missing sub-agent. We needed a mechanism to extend the library that itself follows the library's conventions.

## Decision

`phoenix` is a spawnable agent whose sole job is to extend the library:
- Reads existing INDEX files to understand current state
- Analyzes gap signals (distiller output, session notes, or plain descriptions)
- Determines the correct type: skill | agent | sub-agent | common-skill
- Checks for overlap with existing definitions
- Produces a properly formatted new definition using `templates/` as the source
- **Returns a proposal for review — never writes files directly**

The phoenix agent is the only path for adding new definitions. This creates a consistent, auditable extension mechanism.

## Rationale

- Library conventions (six layers, frontmatter format, ceiling rules) are encoded in phoenix's process — every new definition inherits them
- "Never write directly" rule ensures human review before library changes
- Using phoenix to build skills (rather than writing them by hand) bootstraps the library with consistent quality
- Phoenix itself uses the library's templates, so it demonstrates the format it enforces

## Consequences

- **Easier**: new contributors can spawn phoenix rather than learning all conventions manually
- **Harder**: phoenix must be kept up to date when conventions change; it's a dependency
- **Watch for**: phoenix proposing definitions that technically pass format checks but have overlapping trigger conditions — overlap-check is a required step, not optional

## Alternatives Considered

- **Manual authoring with a style guide** — lower barrier but inconsistent; conventions drift
- **Script-based generator** — deterministic but can't reason about overlap or type classification
