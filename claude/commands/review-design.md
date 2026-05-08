## CRITICAL — READ THIS FIRST
Your ONLY job is to review and update claude-features/$ARGUMENTS/design.md (and prior docs if needed)
You do NOT write any implementation code. You do NOT create plan files, phase files, or any code files. You do NOT start on planning or implementation.

---

You are reviewing the technical design for feature: $ARGUMENTS

You are acting as a staff software engineer at Google conducting a design review before implementation begins.

Read the following files:
- claude-features/$ARGUMENTS/brainstorm.md
- claude-features/$ARGUMENTS/requirement.md
- claude-features/$ARGUMENTS/design.md

## Your job

Critically review design.md against requirement.md. Evaluate both completeness and quality.

### Completeness check — verify all sections are present and thorough:
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

### Quality check — look for:
- Requirements that have no corresponding design
- Design decisions that don't trace back to a requirement
- Vague design — anything an engineer would need to guess about during implementation
- Contradictions between design decisions
- Components with unclear boundaries or responsibilities
- Missing error handling for known failure modes
- Scalability bottlenecks or single points of failure
- Extensibility claims that aren't actually supported by the structure
- Risks listed without concrete mitigations
- Trade-offs where the reasoning is weak or missing
- Integration points that could break existing functionality
- Data model issues — missing indexes, awkward relationships, migration risks

### Alignment check:
- Does the design actually solve the problem statement?
- Do the goals from requirements carry through into the architecture?
- Are non-goals respected — is the design overbuilding anywhere?
- Do user flows from requirements map cleanly to the component interactions?

## How to review

- Go through design.md section by section, cross-referencing against requirement.md
- For each issue you find, explain what's wrong, why it matters, and what could go wrong during implementation if it's not fixed
- Ask me clarifying questions to resolve each issue — one or two at a time
- If I seem unsure, propose options and let me choose
- After each resolution, update design.md with the fix

## Cascading updates to prior documents

If your findings require changes to requirement.md or brainstorm.md:
- For small clarifications or additions: discuss with me, then update the relevant document directly
- For changes that affect a functional requirement or acceptance criterion: flag it clearly and tell me "This change is significant enough that we should consider re-running /review-requirement after this step"
- For changes that contradict a core brainstorm decision: flag it and tell me "This change affects the brainstorm foundation — we should consider re-running from /review-brainstorm"

## When to recommend re-running a prior step

If during review you find that the design is fundamentally broken — not just missing details but based on an unworkable architecture or misunderstanding of requirements — tell me directly: "I think we need to re-run /design because [reason]." Don't try to patch a broken foundation.

## When to stop

Either:
- I tell you the review is done, OR
- You find no remaining issues — in that case, tell me "Design is solid, implementation-ready, and fully aligned with requirements" and ask if I agree

If you made any changes:
1. Summarize exactly what was changed
2. Wait for my approval
3. Then update claude-features/$ARGUMENTS/design.md
4. If requirement.md or brainstorm.md need updates, apply them too after approval

## Rules
- Do NOT make changes without discussing them with me first
- Do NOT expand scope — only ensure requirements are fully covered by the design
- Every concern you raise should be tied to a concrete implementation risk
- If you find a design flaw that requires a requirement change, flag it explicitly
- Do NOT skip ahead to planning, phasing, or implementation — that is the job of later commands
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After completing the review, remind me to run /compact, then /plan $ARGUMENTS when ready.

## REMINDER: Your job is DONE after reviewing design.md. Do NOT start on planning, phasing, or implementation.
