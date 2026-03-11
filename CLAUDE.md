# Claude Code — Global Rules

These rules are always active regardless of what task or command is running.

---

## TRIVIAL VS NON-TRIVIAL

**Trivial** (ALL must be true): single file, <5 lines changed, no new functions/classes, no test behavior change.
→ State why it's trivial, make the change, write and run a test.

**Non-trivial** (everything else): use the workflow slash commands (`/brainstorm`, `/requirement`, `/design`, `/plan`, `/execute-plan`, etc.) before writing code. When in doubt, non-trivial.

---

## CONTEXT MANAGEMENT

All persistent state lives on disk (`claude-features/<feature_name>/` — brainstorm.md, requirement.md, design.md, plan.md, phases/). The conversation is disposable — these files are not.

### When to `/compact`
Use `/compact` at phase boundaries — after output is saved to disk and review is done.
Always include a focus instruction:
- After brainstorm: `/compact preserve brainstorm decisions and key constraints`
- After requirements: `/compact preserve requirement summary and acceptance criteria`
- After design: `/compact preserve design decisions and architecture overview`
- After planning: `/compact preserve phase plan overview and current phase number`
- After phase execution review: `/compact preserve phase N results, test output, and follow-ups`

**Never** `/compact` mid-implementation. If auto-compact triggers during a phase, immediately re-read the current phase file (`claude-features/<feature_name>/phases/phase_N.md`) before continuing.

### When to `/clear`
Use `/clear` (full reset) when:
- Switching to a completely different task
- Context is badly polluted (many failed attempts, wrong directions)
- Starting a new day on the same task — read the relevant phase file to resume

### Proactive context hygiene
- Run `/context` periodically to check usage
- If above 60%, compact at the next phase boundary — don't wait for auto-compact
- Disable unused MCP servers before they eat context

---

## ARCHITECTURE PRINCIPLES

These are non-negotiable. Every design and every line of code must respect these:

### Dependency Direction
- Dependencies point inward: handlers → services → domain → data models.
- Domain/business logic NEVER imports from infrastructure (HTTP, database, file I/O).
- Use interfaces/protocols at boundaries. Concrete implementations are injected, not imported directly.

### Separation of Concerns
- Each module/file has ONE reason to change.
- Business logic is pure: no HTTP objects, no ORM objects, no framework types in core logic.
- Side effects (I/O, database, network) live at the edges, never in core logic.

### Extensibility by Default
- Design for the Open-Closed Principle: open for extension, closed for modification.
- New features should require ADDING files, not MODIFYING existing ones.
- Use composition over inheritance. Prefer protocols/interfaces over base classes.
- Configuration-driven behavior where reasonable (feature flags, strategy selection via config).

### Scalability Awareness
- Assume every list endpoint will need pagination. Add it from day one.
- Assume every external call can fail and can be slow. Add timeouts and retries.
- Prefer async I/O for network-bound work. Use streaming for large data.
- Never load unbounded data into memory. Use cursors, generators, or streaming.

---

## CODE QUALITY

- Functions: ~40 lines max, single responsibility
- Error handling: explicit, no silent swallowing, specific exceptions, actionable messages
- No magic numbers — named constants only
- Zero dead code — no unused imports, variables, or commented-out blocks
- Naming: consistent, no abbreviations, intention-revealing
- Comments: explain why, not what
- Type annotations: on every function signature, no `Any` unless justified
- Tests: must be run and passing, not just written
- Security: validate all inputs at boundaries, sanitize outputs, no secrets in code
- Observability: structured logging at key decision points, error context for debugging
- Design adherence: code matches design documents; update docs first if deviating

---

## ERROR RECOVERY

1. Stop. Do not retry blindly.
2. Read the full error. State what it means.
3. Diagnose root cause. Run targeted diagnostics if needed.
4. Propose a fix and explain why it should work.
5. After 2 failed attempts, stop and tell the user what you know and recommend.

Never retry the same command hoping for a different result.

---

## DESIGN FLAW RECOVERY

If implementation reveals the design was wrong:
1. Stop implementation.
2. Explain what broke and why.
3. Update the relevant document in `claude-features/<feature_name>/` with a revision note.
4. Reassess remaining phases.
5. Get user confirmation before resuming.

---

## NEVER DO

- Write production code before design documents exist (non-trivial work)
- Start a new phase before the previous is declared complete
- Deviate from design documents without updating them first
- Skip tests because something seems simple
- Leave dead code, unused imports, or commented-out blocks
- Proceed past any review gate without explicit user confirmation
- Retry a failing command more than twice without stopping to diagnose
- Import concrete implementations in business logic — use interfaces
- Hard-code configuration values (URLs, ports, timeouts, limits, credentials)
- Write business logic that depends on HTTP framework types or ORM types

---

## COMMUNICATION

- Be direct and concise.
- One sentence for design decision reasoning.
- Say if there's a better approach before doing it.
- Flag risks proactively.
- At every review gate, state what's done and what you're waiting for.
