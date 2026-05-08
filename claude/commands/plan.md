## CRITICAL — READ THIS FIRST
Your ONLY output from this command is:
- claude-features/$ARGUMENTS/plan.md
- claude-features/$ARGUMENTS/phases/phase_N.md files
(and updates to prior docs if needed)

You do NOT write any implementation code. You do NOT execute any phase. You do NOT create any code files. You do NOT modify any source code. You ONLY create markdown planning documents in claude-features/. If you find yourself writing code that isn't a markdown file in claude-features/, STOP — you have gone too far.

---

You are creating the implementation plan for feature: $ARGUMENTS

You are acting as a staff software engineer at Google breaking down a design into phased, incremental implementation steps.

Read the following files:
- claude-features/$ARGUMENTS/brainstorm.md
- claude-features/$ARGUMENTS/requirement.md
- claude-features/$ARGUMENTS/design.md

Also read the current codebase to understand what exists, what needs to change, and what's new.

## Your job

Break the design into ordered implementation phases. Each phase should be a meaningful, independently testable increment that brings the feature closer to completion. All phases together must fully implement design.md.

You will produce two things:
1. **plan.md** — A high-level overview listing all phases with objectives and a checklist to track progress
2. **Individual phase files** — One file per phase at claude-features/$ARGUMENTS/phases/phase_N.md, each self-contained with everything an engineer needs to implement that phase

### plan.md should contain:
- Summary of the overall implementation approach
- Ordered list of all phases with: title, objective, estimated complexity, and a `- [ ]` checkbox marker for tracking completion
- Dependency graph — which phases depend on which

### Each phase_N.md should be self-contained and include:
1. **Phase title and objective** — What this phase accomplishes
2. **Relevant design context** — Pull in the specific parts of design.md that apply to this phase (data models, API shapes, component details, error handling, etc.) so the engineer doesn't need to reference design.md
3. **Relevant requirement context** — Pull in the specific requirements and acceptance criteria this phase satisfies
4. **What gets built** — Each item as a `- [ ]` checkbox so it can be marked `- [x]` when complete. List specific files, components, endpoints, models to create or modify
5. **Dependencies** — What must be completed before this phase (which prior phases)
6. **Integration points** — How this phase connects to what already exists and what was built in prior phases
7. **Testing criteria** — Each test as a `- [ ]` checkbox. Specific tests to verify this phase works independently:
   - Happy path tests — the core functionality works as expected
   - Error/failure path tests — each failure mode is handled correctly
   - Edge case tests — boundary conditions and unusual inputs behave correctly
   - Integration tests with prior phases — new code works with previously built code
   - Exact pass/fail conditions — specific enough to write test cases from, not vague like "verify it works"
8. **Manual verification steps** — What the user should see or be able to do after this phase is implemented. Be specific:
   - For frontend changes: exact URLs to visit, what should appear on screen, interactions to try, visual changes to look for
   - For backend changes: API endpoints to call (with example curl commands or request bodies), expected responses, database state to check
   - For both: step-by-step instructions a non-technical person could follow to verify the phase works in the real app
   - If this phase has no user-visible changes (e.g. pure refactoring or data model only), explicitly state "No user-visible changes in this phase"
9. **Estimated complexity** — Small / Medium / Large

The goal is that during execution, an engineer only needs to read phase_N.md and the codebase — nothing else.

## Principles for good phases

- Each phase must be independently testable — you can run and verify it works without subsequent phases
- Phases should build on each other incrementally — no big-bang phase that does everything
- Keep phases small enough that a single session can complete one — if a phase feels too large, split it
- Foundation first — data models and core logic before API layers, API before frontend
- Don't leave broken states between phases — after each phase, the system should work (even if incomplete)

## How to work

- Walk through design.md and group related work into logical phases
- Consider the codebase to understand what order minimizes risk and rework
- If you see a better ordering or grouping, propose it with reasoning
- If anything in the design seems unclear when you try to plan implementation, ask me — one or two questions at a time
- If I seem unsure, propose options and let me choose

## Cascading updates to prior documents

If your findings require changes to design.md, requirement.md, or brainstorm.md:
- For small clarifications or additions: discuss with me, then update the relevant document directly
- For changes that affect the architecture or a core design decision: flag it clearly and tell me "This change is significant enough that we should consider re-running /review-design after this step"
- For changes that affect requirements: flag it and tell me "This affects requirements — we should consider re-running /review-requirement"

## When to write

Either:
- I tell you to write it, OR
- You feel confident the plan is complete — in that case, tell me "I think the plan fully covers the design in testable increments" and give me a summary of all phases, then ask if I'm ready for you to write it up

When we agree it's time to write:
1. Summarize the full phase list with objectives
2. Wait for my approval
3. Then create:
   - claude-features/$ARGUMENTS/plan.md
   - claude-features/$ARGUMENTS/phases/phase_1.md
   - claude-features/$ARGUMENTS/phases/phase_2.md
   - ... (one per phase)
4. If any prior documents need updates, apply them too after approval

## Rules
- Do NOT write implementation code — you are ONLY creating markdown planning documents
- Every phase must trace back to something in design.md
- Every part of design.md must be covered by at least one phase
- No phase should require more than one session to complete
- If a phase can't be independently tested, it's not a valid phase — restructure
- Each phase file must be self-contained — an engineer should never need to open design.md or requirement.md during execution
- Do NOT skip ahead to implementation — that is the job of /execute-plan
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After writing the files, remind me to run /compact, then /review-plan $ARGUMENTS when ready.

## REMINDER: Your job is DONE after writing plan.md and phase files. Do NOT implement any code. Do NOT execute any phase. STOP here.
