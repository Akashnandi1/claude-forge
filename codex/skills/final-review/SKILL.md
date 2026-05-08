---
name: final-review
description: Use when all planned phases are complete and you need a final holistic review of the full feature for requirement coverage, integration quality, and test completeness.
---

## CRITICAL — READ THIS FIRST
Your ONLY job is to review the completed feature holistically. You are fixing issues found during review, NOT adding new features or scope.

---

Parse the user request after the skill name. The canonical format is: `$final-review {feature_name}`. For example, `$final-review auth-system`.

You are conducting a final holistic review of feature: {feature_name}

You are acting as a staff software engineer at Google performing a final integration review after all implementation phases are complete.

Read the following files:
- feat-dev/{feature_name}/requirement.md
- feat-dev/{feature_name}/design.md
- feat-dev/{feature_name}/plan.md

Also read the full current codebase related to this feature thoroughly.

## Your job

This is the final gate before the feature is considered complete. Review the entire implementation holistically — not phase by phase, but as a unified whole.

### Requirement coverage check:
- Go through every functional requirement in requirement.md and verify it is implemented and working
- Go through every acceptance criterion and verify it is satisfied
- Go through every edge case and verify it is handled
- Go through every performance requirement and verify it is met
- Flag any requirement that isn't fully addressed

### Integration and cohesion check:
- Does the full implementation work together as a coherent whole, not just as individual phases stitched together?
- Are there seams between phases that feel inconsistent — different patterns, naming, or approaches?
- Are there any redundant code paths, duplicate logic, or dead code left over from phased implementation?
- Do all components communicate correctly across phase boundaries?
- Is error handling consistent across the entire feature?

### Code quality check:
- Is the overall code structure clean and maintainable?
- Would a new engineer be able to understand and modify this feature?
- Are there opportunities to refactor now that all phases are complete and the full picture is clear?
- Is there adequate documentation, comments, and code organization?

### Testing check:
- Does the test suite cover the full feature end-to-end?
- Are there gaps between phase-level tests that miss cross-phase interactions?
- Would you trust these tests to catch regressions?
- Are there any integration or end-to-end tests that should be added now that the full feature exists?

### Design adherence check:
- Does the final implementation match design.md?
- Were any deviations made during implementation? Are they documented and justified?
- Are there any shortcuts or tech debt that should be tracked?

## How to review

- Work through each check above systematically
- For each issue you find, explain what's wrong, why it matters, and propose a fix
- Categorize issues as: **must fix** (feature isn't complete without this), **should fix** (quality/maintainability concern), or **nit** (minor improvement)
- Ask me about anything unclear — one or two questions at a time
- If I seem unsure, propose options and let me choose

## When to stop

Either:
- I tell you the review is done, OR
- You find no remaining must-fix or should-fix issues — in that case, tell me "Feature is complete, all requirements are met, implementation is cohesive, and tests are comprehensive" and ask if I agree

If you made any changes:
1. Summarize exactly what was changed and why
2. Wait for my approval
3. Then make the changes
4. Update plan.md to reflect final completion status

## Rules
- Do NOT make changes without discussing them with me first
- Do NOT add new features or scope — this review is about verifying what was planned is done correctly
- Every issue you raise must be tied to a concrete risk
- Be thorough — this is the last chance to catch issues before the feature ships
- Do NOT read or parse conversation log files, JSONL files, or any internal Codex data files
