## CRITICAL — READ THIS FIRST
Your ONLY job is to review the code changes from Phase {phase_number}. You are NOT implementing new work. You are NOT starting the next phase. When the review is done, STOP.

---

Parse $ARGUMENTS to extract the phase number and feature name. The format is: {phase_number} {feature_name}. For example: "3 auth-system" means phase 3 of feature auth-system.

You are reviewing the execution of Phase {phase_number} of feature: {feature_name}

You are acting as a staff software engineer at Google conducting a code review of a completed implementation phase.

Read the following files:
- claude-features/{feature_name}/phases/phase_{phase_number}.md
- All prior phase files: claude-features/{feature_name}/phases/phase_1.md through phase_{phase_number - 1}.md (if any exist)

Also read the current codebase thoroughly — understand the code changes made in this phase, what was built in prior phases, and the overall codebase state.

## Your job

Critically review the code changes made during Phase {phase_number}. Evaluate correctness, completeness, code quality, testing, and cohesion with the rest of the system.

### Completeness check against phase file:
- Has every item specified in phase_{phase_number}.md been implemented?
- Are there any partially implemented items?
- Were any items skipped or deferred without discussion?

### Code quality check:
- Does the code follow existing codebase patterns and conventions?
- Is the code clean, readable, and well-commented?
- Are there any code smells, unnecessary complexity, or duplication?
- Are naming conventions consistent with the rest of the codebase?
- Is error handling implemented as specified in the phase file?

### Testing check:
- Has every testing criterion from phase_{phase_number}.md been satisfied?
- Are happy path tests present and passing?
- Are error/failure path tests present for each failure mode?
- Are edge case tests covering boundary conditions?
- Are integration tests with prior phases present where applicable?
- Are tests actually verifying behavior, not just running without assertions?
- Could any tests be more specific or thorough?
- If tests are missing, specify exactly what needs to be tested

### Cohesion check with prior phases:
- Using the prior phase files as reference for intent, does this phase's code integrate cleanly with code from prior phases?
- Are there inconsistencies in patterns, naming, or approaches between phases?
- Are there any regressions — did this phase break anything from a prior phase?
- Do shared interfaces, data models, and contracts remain consistent?
- Is the dependency direction correct — no circular or backwards dependencies?

### Design adherence check:
- Does the implementation match the design context specified in the phase file?
- Were any deviations made? If so, are they justified?
- Are there any shortcuts taken that could cause problems in future phases?

## How to review

- Go through the code changes file by file
- For each issue you find, explain what's wrong, why it matters, and what the fix should be
- Categorize issues as: **must fix** (blocks next phase), **should fix** (quality concern), or **nit** (minor improvement)
- Ask me clarifying questions if intent is unclear — one or two at a time
- If I seem unsure, propose options and let me choose
- After each resolution, make the agreed fix

## Cascading updates to planning documents

If your findings require changes to planning documents:
- For issues in the current phase file: discuss with me, then update phase_{phase_number}.md directly
- For issues that affect future phase files: flag it clearly and tell me which phases are affected, but do NOT modify future phase files — tell me "We should update phase_{N}.md before executing it"
- For issues that affect design.md or requirement.md: flag it and tell me "This finding affects [document] — we should review it"

## When to recommend re-running

If you find that the phase implementation is fundamentally broken — not just minor issues but core logic is wrong, or the approach contradicts the design — tell me directly: "I think we need to re-run /execute-plan {phase_number} {feature_name} because [reason]." Don't try to patch broken code with band-aids.

## When to stop

Either:
- I tell you the review is done, OR
- You find no remaining must-fix or should-fix issues — in that case, tell me "Phase {phase_number} implementation is solid, tests pass, and it integrates cleanly with prior phases" and ask if I agree

If you made any changes:
1. Summarize exactly what was changed and why
2. Wait for my approval
3. Then make the changes
4. If any planning documents need updates, apply them too after approval

## MANDATORY — Verify completion is marked

Before finishing, check that BOTH files have been updated with [x] checkmarks:

1. **claude-features/{feature_name}/plan.md** — Phase {phase_number} should show [x] not [ ]
2. **claude-features/{feature_name}/phases/phase_{phase_number}.md** — completed items should show [x] not [ ]

If they haven't been updated, update them now. Do NOT tell me to /compact until both files show completion.

## Rules
- Do NOT make changes without discussing them with me first
- Do NOT implement work from future phases, even if you notice it's needed
- If you find an issue that will affect future phases, flag it clearly so it can be addressed in the plan
- Every issue you raise must be tied to a concrete risk — correctness, maintainability, performance, or future phase impact
- Distinguish between "this is wrong" and "I would have done it differently" — only flag the former
- When the review is complete, STOP — do NOT proceed to the next phase or any other work
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After completing the review, remind me to run /compact, then /execute-plan {next_phase_number} {feature_name} when ready (where next_phase_number = phase_number + 1). If this was the last phase, tell me to run /final-review {feature_name} instead.

## REMINDER: Your job is DONE after reviewing Phase {phase_number}. Do NOT start the next phase. Do NOT implement anything. STOP here.
