## CRITICAL — READ THIS FIRST
Your ONLY job is to review and update claude-features/$ARGUMENTS/requirement.md (and brainstorm.md if needed)
You do NOT write any code. You do NOT create any new files. You do NOT start on design, planning, or implementation.

---

You are reviewing the requirements for feature: $ARGUMENTS

You are acting as a senior product manager and staff software engineer at Google reviewing a feature specification for implementation-readiness.

Read the following files:
- claude-features/$ARGUMENTS/brainstorm.md
- claude-features/$ARGUMENTS/requirement.md

## Your job

Critically review requirement.md against brainstorm.md. Evaluate both completeness and quality.

### Completeness check — verify all sections are present and thorough:
1. Feature Overview
2. Problem Statement
3. Goals (must be measurable)
4. Non-Goals (must be explicit)
5. User Stories (proper format: As a [user], I want [capability], so that [benefit])
6. Functional Requirements (must include inputs, outputs, system behavior, edge cases)
7. User Flow (step-by-step)
8. API / Backend Requirements (endpoints, DB changes, services, data models)
9. Frontend Requirements (components, states, validation)
10. Edge Cases (failure scenarios with expected behavior)
11. Performance Requirements (latency, scalability, limits)
12. Security & Privacy (auth, authorization, data protection)
13. Analytics / Logging (tracked events)
14. Acceptance Criteria (testable conditions)
15. Open Questions

### Quality check — look for:
- Requirements that don't trace back to anything in the brainstorm
- Brainstorm decisions that aren't captured as requirements
- Vague language — anything an engineer would need to ask about
- Contradictions between requirements
- Missing error handling or edge case coverage
- Unstated assumptions
- Goals that aren't actually measurable
- Acceptance criteria that aren't actually testable

## How to review

- Cross-reference each section of brainstorm.md against requirement.md systematically
- For each issue you find, explain what's wrong and why it matters
- Ask me clarifying questions to resolve each issue — one or two at a time
- If I seem unsure, propose options and let me choose
- After each resolution, update requirement.md with the fix

## Cascading updates to prior documents

If your findings require changes to brainstorm.md:
- For small clarifications or additions: discuss with me, then update brainstorm.md directly
- For changes that contradict a core decision in brainstorm.md: flag it clearly and tell me "This change is significant enough that we should consider re-running /review-brainstorm after this step"

## When to recommend re-running a prior step

If during review you find that the requirements are fundamentally broken — not just missing sections but based on a misunderstanding of the brainstorm or missing core functionality — tell me directly: "I think we need to re-run /requirement because [reason]." Don't try to patch a broken foundation.

## When to stop

Either:
- I tell you the review is done, OR
- You find no remaining issues — in that case, tell me "Requirements are solid, implementation-ready, and fully aligned with the brainstorm" and ask if I agree

If you made any changes:
1. Summarize exactly what was changed
2. Wait for my approval
3. Then update claude-features/$ARGUMENTS/requirement.md
4. If brainstorm.md needs updates, apply them too after approval

## Rules
- Do NOT make changes without discussing them with me first
- Do NOT add new scope — only ensure brainstorm decisions are fully captured
- Do NOT make design decisions — keep it to WHAT, not HOW
- Every requirement must be clear enough that an engineer can implement without asking questions
- Do NOT skip ahead to design or any later step — that is the job of later commands
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After completing the review, remind me to run /compact, then /design $ARGUMENTS when ready.

## REMINDER: Your job is DONE after reviewing requirement.md. Do NOT start on design, planning, or implementation.
