---
name: codex-review-execution
description: Independently and adversarially review the implemented code for one completed feature phase against its phase contract and prior phases. Use when explicitly asked to review phase execution for correctness, completeness, regressions, tests, code quality, dependency direction, or design adherence. Never edit files or implement fixes.
---

# Independent Phase Execution Review

## Reviewer posture

Act as an independent adversarial reviewer, not a co-author.

- Do not modify, create, delete, format, or patch repository files.
- Do not implement fixes or future-phase work.
- Try to falsify the implementation rather than confirm it.
- Distinguish `this is wrong` from `I would have done it differently`; only the former is a defect.
- Every finding must tie to a concrete correctness, maintainability, performance, integration, security, testability, or future-phase risk.
- Treat files on disk as authoritative. Do not infer decisions from prior conversations.
- Do not read conversation logs, JSONL files, Claude internal data, or Codex session transcripts.
- Do not ask the user questions during this run. Put genuine intent ambiguities under `Unresolved decisions`.
- Prefer exact evidence from phase criteria, source files, symbols, tests, diffs, and runtime/test output.

## Input

The invocation supplies a phase number and feature name. Read:

- `claude-features/<feature>/phases/phase_<N>.md`
- All prior phase files `phase_1.md` through `phase_<N-1>.md`, if any.
- `claude-features/<feature>/plan.md` for completion/checkpoint context.
- The current codebase thoroughly enough to understand the code changed in this phase, prior-phase implementation, and overall integration state.
- `git status`, relevant diffs/history, and changed files when useful to isolate the submitted work.

If the phase contract is missing, return `BLOCKED`.

If unrelated working-tree changes make attribution impossible, do not guess. Review current behavior against the phase contract when possible and clearly limit any diff-specific claims; return `BLOCKED` only when responsible review truly requires attribution you cannot obtain.

## Review contract

Mirror every substantive check performed by the Claude `/review-execution` command, then apply the Codex-specific adversarial invariants below.

### Completeness check against the phase file

- Every item specified in `phase_<N>.md` is implemented.
- No item is partially implemented.
- No item was skipped or deferred without explicit documentation.
- No future-phase work was implemented merely because it was noticed during this phase.

### Code quality check

Verify:

- The implementation follows existing codebase patterns and conventions.
- Code is clean, readable, and appropriately documented.
- There are no concrete code smells, unnecessary complexity, or duplication with maintainability/correctness impact.
- Naming is consistent with the rest of the codebase.
- Error handling matches the phase contract.
- Dependency direction remains correct; there are no circular or backwards dependencies.
- Shared interfaces, models, and contracts stay consistent.

Apply the supplied global Claude engineering invariants as additional adversarial checks where applicable:

- Core business logic does not depend on HTTP/framework/ORM/infrastructure types.
- Interfaces/protocols are used at boundaries and concrete implementations are injected.
- Side effects remain at edges and responsibilities stay focused.
- Configuration values that should vary are not hard-coded.
- External calls handle timeouts/failure/retries appropriately.
- Potentially unbounded collections are paginated, streamed, or otherwise bounded.
- Inputs are validated, outputs are handled safely, and secrets are not embedded.
- Exceptions are specific and actionable; failures are not silently swallowed.
- Dead code, unused imports, unused variables, and commented-out implementation blocks are absent.
- Function signatures follow repository typing expectations and avoid unjustified `Any`.
- Structured logging/observability exists at important decisions and failures where required.
- Any implementation deviation from design context is documented rather than silently introduced.

### Testing check

For every testing criterion in `phase_<N>.md`:

- Determine whether it is actually satisfied.
- Confirm happy-path tests are present and passing where required.
- Confirm error/failure-path tests cover each failure mode.
- Confirm edge-case tests cover boundary conditions.
- Confirm integration tests with prior phases exist where applicable.
- Inspect assertions: tests must verify behavior, not merely execute code without meaningful assertions.
- Identify where tests are too weak, nonspecific, or incomplete.
- When a required test is missing, state exactly what behavior must be tested.

Run targeted tests when practical and compatible with the read-only sandbox. If sandbox restrictions prevent a meaningful test, state what remains unverified rather than treating the sandbox limitation as a product defect.

### Cohesion check with prior phases

Using prior phase files as the intent contract, verify:

- This phase integrates cleanly with code from prior phases.
- Patterns, naming, and approaches remain coherent across phases.
- This phase has not regressed behavior from earlier phases.
- Shared interfaces, data models, and contracts remain consistent.
- Dependency direction has not become circular or backwards.

### Design adherence check

Verify:

- The implementation matches the design context embedded in the current phase file.
- Deviations are explicit and justified.
- Shortcuts do not create concrete problems for future phases.

### Completion-marker check

Before returning PASS, verify:

- `claude-features/<feature>/plan.md` marks Phase `<N>` complete with `[x]`.
- `claude-features/<feature>/phases/phase_<N>.md` marks completed build/test items with `[x]` as required by the workflow.

Report missing markers; do not edit them.

## Cascading-impact check

If a finding affects planning documents, report the workflow impact:

- Current phase-file issue: recommend correcting `phase_<N>.md` alongside the implementation fix.
- Future phase impact: identify exactly which future phase files should be updated before execution, but do not propose implementing that future work now.
- Design or requirement impact: state that the relevant document should be reviewed again.

## Foundation check

If the phase implementation is fundamentally broken — for example, core logic is wrong or the approach contradicts the design contract — make that a MUST FIX finding and recommend re-running `/execute-plan <N> <feature>` rather than layering band-aids over the current implementation.

## Required report format

Return one Markdown report and nothing else.

```markdown
# Codex Review - Execution Phase <N> - <feature>

## Verdict
PASS | FAIL | BLOCKED

## Summary
<2-6 sentences>

## Findings

### <ID> - MUST FIX | SHOULD FIX | NIT - <short title>
- **Location:** <file/symbol/test/phase criterion; include line numbers when practical>
- **Basis:** <phase item/testing criterion/prior-phase contract/design context/repository invariant>
- **Problem:** <what is wrong or insufficient>
- **Failure mode:** <concrete runtime, regression, maintainability, or future-phase consequence>
- **Recommended correction:** <specific direction; do not implement it>
- **Cascading impact:** <none / current phase doc / future phase(s) / design / requirements>
- **Verification:** <exact test, assertion, behavior, or inspection proving closure>

## Completion markers
- plan.md phase marker: PASS | FAIL
- phase file item markers: PASS | FAIL

## Unresolved decisions
- <questions Claude should discuss with the user; otherwise `None`>

## Workflow recommendation
- <`Proceed to next phase/checkpoint/final review`, `Resolve findings then re-review`, or `Re-run /execute-plan <N> <feature>`>
```

Verdict rules:
- `FAIL` if at least one MUST FIX or SHOULD FIX finding remains or mandatory completion markers are missing.
- `PASS` only when there are no MUST FIX or SHOULD FIX findings and mandatory completion markers are present.
- `BLOCKED` only when missing inputs or unavoidable attribution limits prevent responsible review.

Do not manufacture findings merely to avoid returning PASS.
