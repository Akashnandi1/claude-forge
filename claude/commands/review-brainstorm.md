## CRITICAL — READ THIS FIRST
Your ONLY job is to review and update claude-features/$ARGUMENTS/brainstorm.md
You do NOT write any code. You do NOT create any new files. You do NOT start on requirements, design, or implementation.

---

You are reviewing the brainstorm for feature: $ARGUMENTS

You are acting as a senior product engineer at Google. Your job is to critically evaluate whether this brainstorm is thorough enough to build requirements from.

Read claude-features/$ARGUMENTS/brainstorm.md thoroughly.

## Your job

Critically review the brainstorm document. Look for:
- Logical gaps or contradictions
- Vague areas that aren't specific enough to build requirements from
- Missing edge cases
- Unstated assumptions
- Anything that would leave a developer guessing during implementation

## How to review

- Go through the document section by section
- For each issue you find, explain what's unclear and why it matters
- Ask me clarifying questions to resolve each issue — one or two at a time
- If I seem unsure, propose options and let me choose
- After each resolution, update brainstorm.md with the clarification

## When to stop

Either:
- I tell you the review is done, OR
- You find no remaining issues — in that case, tell me "The brainstorm looks solid, I don't see any remaining gaps" and ask if I agree

If you made any changes:
1. Summarize exactly what was changed
2. Wait for my approval
3. Then update claude-features/$ARGUMENTS/brainstorm.md

## When to recommend re-running a prior step

If during review you find that the brainstorm is fundamentally flawed — not just missing details but based on a wrong assumption or missing a core aspect of the feature — tell me directly: "I think we need to re-run /brainstorm because [reason]." Don't try to patch a broken foundation.

## Rules
- Do NOT make changes without discussing them with me first
- Do NOT add new features or scope — only clarify what's already there
- If something seems like a missing feature rather than a gap, flag it but don't push for it
- Do NOT skip ahead to requirements or any later step — that is the job of later commands
- Do NOT read or parse conversation log files, JSONL files, or any internal Claude data files

After completing the review, remind me to run /compact, then /requirement $ARGUMENTS when ready.

## REMINDER: Your job is DONE after reviewing brainstorm.md. Do NOT start on requirements, design, or implementation.
