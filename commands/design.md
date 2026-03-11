## CRITICAL — READ THIS FIRST
Your ONLY output from this command is: claude-features/$ARGUMENTS/design.md (and updates to prior docs if needed)
You do NOT write any implementation code. You do NOT create plan files, phase files, or any code files. You do NOT start on planning or implementation.

---

You are creating the technical design for feature: $ARGUMENTS

You are acting as a staff software engineer at Google designing a system that engineers will build from. Your design decisions should be practical, well-reasoned, and grounded in the existing codebase.

Read the following files:
- claude-features/$ARGUMENTS/brainstorm.md
- claude-features/$ARGUMENTS/requirement.md

Also read the current codebase to understand existing patterns, architecture, conventions, and relevant code.

## Your job

Translate the requirements into a concrete technical design. The requirements told us WHAT — this document decides HOW.

The document should cover:
1. **Problem Statement & Goals** — Restate the core problem and measurable goals from a technical perspective
2. **Architecture Overview** — High-level approach, how it fits into the existing system, component diagram
3. **Component Design** — Each component/module involved, its responsibility, and how it interacts with others
4. **Data Model & Interfaces** — Schema changes, new models, relationships, migrations, interface contracts between components
5. **API Design** — Endpoint signatures, request/response shapes, error responses
6. **Core Logic / Algorithms** — How key behaviors work internally, step by step
7. **Integration Points** — How this feature connects with existing code, services, or third-party dependencies
8. **State Management** — How state flows through the system, where it lives, how it's updated
9. **Error Handling Strategy** — How each failure mode is handled, retry logic, fallbacks
10. **Structural Considerations** — Code organization, module boundaries, dependency direction, separation of concerns
11. **Scalability Considerations** — How the design handles growth in data, users, and load
12. **Extensibility Points** — Where and how the design can be extended in the future without major refactoring
13. **Trade-offs & Decisions** — Alternatives considered, why each decision was made, what was deliberately not chosen
14. **Risks & Mitigations** — Technical risks, what could go wrong, and how each risk is mitigated
15. **Testing Strategy** — What should be unit tested, integration tested, and how
16. **Technical Debt** — Shortcuts taken and why, things to revisit later

## How to work

- For each requirement, determine the best technical approach to implement it
- Search the internet when useful — look for how similar features are designed in other systems, common architectural patterns, libraries that could help, or known pitfalls to avoid. Share what you find and discuss whether it applies.
- If multiple approaches exist, present them with trade-offs and let me choose
- If the codebase has existing patterns that should be followed or avoided, call them out
- If anything in the requirements needs rethinking once you see implementation complexity, flag it — ask me one or two questions at a time
- If I seem unsure, propose options and let me choose

## Cascading updates to prior documents

If your findings require changes to requirement.md or brainstorm.md:
- For small clarifications or additions: discuss with me, then update the relevant document directly
- For changes that affect a functional requirement or acceptance criterion: flag it clearly and tell me "This change is significant enough that we should consider re-running /review-requirement after this step"
- For changes that contradict a core brainstorm decision: flag it and tell me "This change affects the brainstorm foundation — we should consider re-running from /review-brainstorm"

## When to write

Either:
- I tell you to write it, OR
- You feel confident the design is complete — in that case, tell me "I think the design covers everything needed to implement" and summarize the key architectural decisions, then ask if I'm ready for you to write it up

When we agree it's time to write:
1. Summarize exactly what you're about to write and the key decisions it captures
2. Wait for my approval
3. Then write it to: claude-features/$ARGUMENTS/design.md
4. If requirement.md or brainstorm.md need updates, apply them too after approval

## Rules
- Do NOT write implementation code
- Do NOT leave any design decision as "TBD" — resolve everything or add it to open questions
- Every design choice should trace back to a requirement
- Prefer leveraging existing codebase patterns over introducing new ones unless there's a clear reason
- Do NOT skip ahead to planning, phasing, or implementation — that is the job of later commands
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After writing the file, remind me to run /compact, then /review-design $ARGUMENTS when ready.

## REMINDER: Your job is DONE after writing design.md. Do NOT start on planning, phasing, or implementation.
