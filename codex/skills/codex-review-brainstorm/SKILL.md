---
name: codex-review-brainstorm
description: Independently and adversarially review the feature brainstorm document before requirements are written. Use when explicitly asked to review a feature brainstorm for gaps, contradictions, assumptions, edge cases, or implementation ambiguity. Never edit files or expand scope.
---

# Independent Brainstorm Review

## Reviewer posture

Act as an independent adversarial reviewer, not a co-author.

- Do not modify, create, delete, format, or patch repository files.
- Do not implement fixes.
- Do not expand product scope.
- Try to falsify the brainstorm rather than confirm it.
- Distinguish a defect from a preference. Only report the former as MUST FIX or SHOULD FIX.
- Tie every substantive finding to a concrete downstream risk: ambiguous requirements, incorrect implementation, integration failure, security/performance risk, or avoidable rework.
- Treat files on disk as authoritative. Do not infer decisions from prior conversations.
- Do not read conversation logs, JSONL files, Claude internal data, or Codex session transcripts.
- Do not ask the user questions during this run. Put genuine questions or intent choices under `Unresolved decisions`.
- Prefer evidence from exact sections and relevant codebase constraints over generic advice.

## Input

The invocation supplies a feature name. Read:

- `claude-features/<feature>/brainstorm.md`
- The current codebase structure and relevant existing code where needed to understand project context, integration constraints, or feasibility.

If `brainstorm.md` is missing, return `BLOCKED`.

## Review contract

Mirror the substantive review performed by the Claude `/review-brainstorm` command, but remain read-only and non-interactive.

Review the brainstorm section by section and look for:

- Logical gaps or contradictions.
- Vague areas that are not specific enough to build requirements from.
- Missing edge cases or failure scenarios implied by the stated feature.
- Unstated assumptions.
- Anything that would leave a developer or requirements author guessing later.
- Existing-code or integration constraints that make a stated assumption questionable.
- Scope, behavior, error handling, user experience, integration, constraints, and performance implications that are already part of the stated feature but insufficiently resolved.

Do not add new features or scope merely because they might be useful. If something looks like a missing feature rather than a gap in the stated feature, identify it only as a scope observation and do not promote it to MUST FIX unless existing decisions logically require it.

For every finding:

- Explain exactly what is unclear, contradictory, missing, or unsupported.
- Explain why it matters to the next requirements stage.
- State the concrete failure or rework risk if it remains unresolved.
- Recommend the narrowest clarification needed; do not redesign the feature.

## Foundation check

If the brainstorm is fundamentally flawed rather than merely incomplete — for example, it rests on a wrong core assumption or omits a core aspect necessary for the stated feature to make sense — make that a MUST FIX finding and recommend re-running `/brainstorm <feature>` rather than patching the document piecemeal.

## Required report format

Return one Markdown report and nothing else.

```markdown
# Codex Review - Brainstorm - <feature>

## Verdict
PASS | FAIL | BLOCKED

## Summary
<2-6 sentences>

## Findings

### <ID> - MUST FIX | SHOULD FIX | NIT - <short title>
- **Location:** <file/section; include line numbers when practical>
- **Basis:** <brainstorm decision/codebase constraint/reviewer invariant>
- **Problem:** <what is wrong or insufficient>
- **Why it matters:** <why requirements or later implementation would be at risk>
- **Failure mode:** <concrete consequence if left unresolved>
- **Recommended clarification:** <specific direction, not a rewrite or implementation patch>
- **Verification:** <what must be true in brainstorm.md for this finding to be closed>

## Unresolved decisions
- <questions or product-intent choices Claude should discuss with the user; otherwise `None`>

## Workflow recommendation
- <`Proceed to requirements`, `Resolve findings then re-review`, or `Re-run /brainstorm <feature>`>
```

Verdict rules:
- `FAIL` if at least one MUST FIX or SHOULD FIX finding remains.
- `PASS` when there are no MUST FIX or SHOULD FIX findings. NIT findings may remain.
- `BLOCKED` only when missing inputs prevent a responsible review.

Do not manufacture findings merely to avoid returning PASS.
