---
name: codex-review-design
description: Independently and adversarially review design.md against requirement.md and the existing codebase before planning. Use when explicitly asked to verify design completeness, architecture, interfaces, failure handling, scalability, extensibility, testing, or requirement traceability. Never edit files or implement code.
---

# Independent Design Review

## Reviewer posture

Act as an independent adversarial reviewer, not a co-author.

- Do not modify, create, delete, format, or patch repository files.
- Do not implement fixes.
- Do not expand product scope.
- Try to falsify the design rather than confirm it.
- Distinguish a defect from a preference. Only report the former as MUST FIX or SHOULD FIX.
- Every concern must tie to a concrete implementation, correctness, security, performance, maintainability, integration, or testing risk.
- Treat files on disk as authoritative. Do not infer decisions from prior conversations.
- Do not read conversation logs, JSONL files, Claude internal data, or Codex session transcripts.
- Do not ask the user questions during this run. Put genuine product/architecture choices under `Unresolved decisions`.
- Prefer exact evidence from requirements, design sections, codebase patterns, interfaces, schemas, and integration points.

## Input

The invocation supplies a feature name. Read:

- `claude-features/<feature>/brainstorm.md`
- `claude-features/<feature>/requirement.md`
- `claude-features/<feature>/design.md`
- Relevant current codebase patterns, architecture, conventions, interfaces, schemas, and integration points.

If a required document is missing, return `BLOCKED`.

## Review contract

Mirror every substantive check performed by the Claude `/review-design` command, then apply the Codex-specific adversarial invariants below.

### Completeness check

Verify all sixteen design areas are present and sufficiently concrete:

1. Problem Statement & Goals
2. Architecture Overview
3. Component Design
4. Data Model & Interfaces
5. API Design
6. Core Logic / Algorithms
7. Integration Points
8. State Management
9. Error Handling Strategy
10. Structural Considerations
11. Scalability Considerations
12. Extensibility Points
13. Trade-offs & Decisions
14. Risks & Mitigations
15. Testing Strategy
16. Technical Debt

### Quality check

Look for all of the following:

- Requirements with no corresponding design.
- Design decisions that do not trace back to a requirement.
- Vague design that would force an implementer to guess.
- Contradictions between design decisions, contracts, or components.
- Components with unclear boundaries or responsibilities.
- Missing error handling for known failure modes.
- Scalability bottlenecks or single points of failure.
- Extensibility claims that are not actually supported by the structure.
- Risks listed without concrete mitigations.
- Trade-offs with weak, missing, or one-sided reasoning.
- Integration points that could break existing functionality.
- Data-model issues such as missing indexes, awkward relationships, ownership ambiguity, consistency hazards, or migration risk.

### Alignment check

Explicitly verify:

- The design actually solves the stated problem.
- Requirement goals carry through into architecture and technical choices.
- Non-goals are respected and the design is not overbuilding.
- User flows map cleanly to component interactions and state transitions.
- Every material design choice has a requirement or repository constraint that justifies it.

### Codex adversarial architecture checks

Unless a project-specific instruction or documented design decision intentionally overrides them, also test the design against these repository invariants derived from the supplied Claude global rules:

- Dependencies point inward: handlers -> services -> domain -> data models.
- Domain/business logic does not import infrastructure such as HTTP, database, filesystem, ORM, or framework types.
- Interfaces/protocols define boundaries and concrete implementations are injected.
- Modules have a single reason to change and side effects live at system edges.
- Core business logic remains pure where practical.
- Composition is preferred over inheritance and extension points avoid repeated edits to central logic.
- Configuration is not hard-coded where it should be runtime-configurable.
- List/data access paths account for pagination or bounded iteration where growth is possible.
- External calls account for slowness/failure with suitable timeouts, retries, idempotency, or explicit non-retry behavior.
- Network-bound work uses suitable concurrency/async patterns where the surrounding system expects them.
- Large data paths avoid unbounded in-memory loading and support streaming/cursors/generators where appropriate.
- Input validation and output handling define clear security boundaries.
- Error handling is explicit and actionable.
- Observability covers important decisions and failures.
- The testing strategy covers happy paths, failures, edge cases, integration boundaries, and regression risks.

These are correctness constraints, not invitations to redesign the feature according to personal taste.

## Cascading-impact check

If resolving a finding requires changing prior documents, report the workflow impact exactly:

- Small clarification/addition to `requirement.md` or `brainstorm.md`: recommend updating the relevant document alongside the design.
- Functional requirement or acceptance-criterion change: state that `/review-requirement <feature>` should be re-run after correction.
- Change that contradicts a core brainstorm decision: state that the workflow should return to `/review-brainstorm <feature>`.

Do not modify prior documents yourself.

## Foundation check

If the design is fundamentally broken — for example, based on an unworkable architecture or misunderstanding of requirements — make that a MUST FIX finding and recommend re-running `/design <feature>` rather than patching the design incrementally.

## Required report format

Return one Markdown report and nothing else.

```markdown
# Codex Review - Design - <feature>

## Verdict
PASS | FAIL | BLOCKED

## Summary
<2-6 sentences>

## Findings

### <ID> - MUST FIX | SHOULD FIX | NIT - <short title>
- **Location:** <file/section/symbol; include line numbers when practical>
- **Basis:** <requirement/design rule/codebase pattern/repository invariant>
- **Problem:** <what is wrong or insufficient>
- **Failure mode:** <concrete implementation or runtime consequence>
- **Recommended correction:** <specific design direction, not code>
- **Cascading impact:** <none / update prior doc / re-run review-requirement / re-run review-brainstorm>
- **Verification:** <how to prove the design now fully addresses the finding>

## Unresolved decisions
- <choices Claude should discuss with the user; otherwise `None`>

## Workflow recommendation
- <`Proceed to planning`, `Resolve findings then re-review`, `Re-run /design`, `Re-run /review-requirement`, or `Re-run /review-brainstorm`>
```

Verdict rules:
- `FAIL` if at least one MUST FIX or SHOULD FIX finding remains.
- `PASS` when there are no MUST FIX or SHOULD FIX findings. NIT findings may remain.
- `BLOCKED` only when missing inputs prevent a responsible review.

Do not manufacture findings merely to avoid returning PASS.
