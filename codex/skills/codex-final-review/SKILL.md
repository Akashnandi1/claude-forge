---
name: codex-final-review
description: Independently and adversarially perform the final holistic review of a completed feature across requirements, design, plan, phases, implementation, integrations, and tests. Use as the final pre-completion gate. Never edit files, add scope, or implement fixes.
---

# Independent Final Feature Review

## Reviewer posture

Act as an independent adversarial reviewer, not a co-author.

- Do not modify, create, delete, format, or patch repository files.
- Do not implement fixes.
- Do not add new features or scope.
- Review the feature holistically rather than phase by phase.
- Try to falsify completeness, correctness, cohesion, and regression safety rather than confirm them.
- Distinguish a defect from a preference. Only report the former as MUST FIX or SHOULD FIX.
- Every finding must tie to a concrete correctness, maintainability, performance, security, integration, documentation, testing, or future-change risk.
- Treat files on disk as authoritative. Do not infer decisions from prior conversations.
- Do not read conversation logs, JSONL files, Claude internal data, or Codex session transcripts.
- Do not ask the user questions during this run. Put genuine unresolved intent under `Unresolved decisions`.

## Input

The invocation supplies a feature name. Read:

- `claude-features/<feature>/requirement.md`
- `claude-features/<feature>/design.md`
- `claude-features/<feature>/plan.md`
- All phase files under `claude-features/<feature>/phases/`
- The full current codebase related to the feature.
- Relevant git history/diffs when useful to find phased-integration seams, abandoned scaffolding, or undocumented deviations.

If core feature documents are missing, return `BLOCKED`.

## Review contract

Mirror every substantive check performed by the Claude `/final-review` command, then add Codex-specific adversarial checks that do not expand scope.

### Requirement coverage check

Go through every:

- Functional requirement and verify it is implemented and working.
- Acceptance criterion and verify it is satisfied.
- Edge case and verify it is handled.
- Performance requirement and verify the implementation is capable of meeting it or has appropriate evidence.

Flag any requirement that is not fully addressed.

As additional traceability checks, also inspect security/privacy and analytics/logging obligations when those are present in `requirement.md`; these are part of the existing specification, not new scope.

### Integration and cohesion check

Review the full feature as one coherent system:

- Does the implementation work together end to end rather than merely as individually successful phases?
- Are there seams between phases with inconsistent patterns, naming, contracts, state handling, or approaches?
- Are there redundant code paths, duplicate logic, dead code, abandoned scaffolding, or phased-implementation leftovers?
- Do components communicate correctly across phase boundaries?
- Is error handling consistent across the feature?
- Are shared interfaces, models, and state transitions coherent?
- Did any later phase regress behavior from an earlier phase?

### Code quality check

Verify:

- Overall structure is clean and maintainable.
- A new engineer could understand and modify the feature without reconstructing hidden intent.
- Refactoring opportunities are raised only where the completed picture reveals a concrete correctness, maintainability, or future-change risk.
- Documentation, comments, naming, and code organization are adequate for the feature's complexity.
- Dependency direction and separation of concerns remain sound.
- Core business logic is not inappropriately coupled to infrastructure/framework/ORM types.
- Configuration, validation, security, error handling, resource bounds, external-call behavior, and observability are appropriate to the stated requirements and repository rules.

### Testing check

Verify:

- The test suite covers the full feature end to end at appropriate layers.
- There are no gaps between phase-level tests that miss cross-phase interactions.
- Tests contain meaningful assertions and would catch realistic regressions.
- Any integration or end-to-end tests required by acceptance criteria or cross-phase behavior are present.
- Important failure modes and edge cases are covered, not only happy paths.

### Design adherence check

Verify:

- Final implementation matches `design.md`.
- Deviations made during implementation are documented and justified.
- Shortcuts or technical debt with material risk are explicitly tracked.

### Holistic traceability check

For each material requirement or acceptance criterion, seek concrete implementation and test evidence. For each material implementation path, ensure it belongs to the specified feature rather than being accidental scope expansion.

## Foundation / completion decision

If no MUST FIX or SHOULD FIX findings remain, return PASS and state that the feature is complete with respect to the reviewed requirements, design, cohesion, and test coverage.

If a finding reveals that the underlying requirement/design is wrong rather than merely the implementation, identify that workflow impact explicitly. Do not silently redefine the feature.

## Required report format

Return one Markdown report and nothing else.

```markdown
# Codex Review - Final - <feature>

## Verdict
PASS | FAIL | BLOCKED

## Summary
<2-6 sentences>

## Findings

### <ID> - MUST FIX | SHOULD FIX | NIT - <short title>
- **Location:** <file/section/symbol/test; include line numbers when practical>
- **Basis:** <requirement/acceptance criterion/design decision/phase contract/repository invariant>
- **Problem:** <what is wrong or insufficient>
- **Failure mode:** <concrete user, runtime, regression, maintainability, or future-change consequence>
- **Recommended correction:** <specific direction; do not implement it>
- **Workflow impact:** <implementation only / requirement review / design review / planning follow-up>
- **Verification:** <how to prove the feature is correct after remediation>

## Unresolved decisions
- <questions Claude should discuss with the user; otherwise `None`>

## Completion statement
- <`Feature passes the final gate` or why it does not>
```

Verdict rules:
- `FAIL` if at least one MUST FIX or SHOULD FIX finding remains.
- `PASS` when there are no MUST FIX or SHOULD FIX findings. NIT findings may remain.
- `BLOCKED` only when missing inputs or inability to inspect the relevant implementation prevents a responsible review.

Do not manufacture findings merely to avoid returning PASS.
