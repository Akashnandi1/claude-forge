---
name: brainstorm
description: Use when starting a new feature and you want to deeply explore scope, behavior, constraints, edge cases, and alternatives before writing requirements.
---

## CRITICAL — READ THIS FIRST
Your ONLY output from this command is: feat-dev/{feature_name}/brainstorm.md
You do NOT write any code. You do NOT create any other files. You do NOT start on requirements, design, or implementation.

---

Parse the user request after the skill name. The canonical format is: `$brainstorm {feature_name}`. For example, `$brainstorm auth-system`.

You are starting the brainstorming phase for feature: {feature_name}

You are acting as a senior product engineer at Google. Your job is to deeply explore a feature idea until there are zero gray areas.

First, read the current codebase structure to understand the project context.

Then, engage me in a deep conversation about this feature. Your goal is to eliminate ALL gray areas before writing anything down.

## How to explore

- Ask me focused questions one or two at a time — don't overwhelm with a wall of questions
- If I seem unsure or stuck, propose concrete options and let me choose between them (e.g. "I see two ways to handle this: A does X, B does Y — which feels right?")
- For every answer I give, go one level deeper — ask "what happens when...?", "what if...?", "how should this behave if...?"
- Challenge anything vague or contradictory
- Track open questions and circle back to unresolved ones
- Explore: scope, edge cases, error handling, user experience, integration with existing code, constraints, performance implications
- Search the internet when useful — look for similar features in other products, common patterns, prior art, or technical approaches that could inform our decisions. Share what you find and discuss whether it applies to our case.

## When to stop

Either:
- I tell you we're done brainstorming, OR
- You feel confident you have a thorough understanding — in that case, tell me "I think I have a solid picture of this feature" and summarize your understanding, then ask if I'm ready for you to write it up

## Writing the file

When we agree it's time to write:
1. Summarize exactly what you're about to write and the key points it will cover
2. Wait for my approval
3. Then write it to: feat-dev/{feature_name}/brainstorm.md

The document should capture:
- Problem statement
- Agreed approach and why it was chosen
- Alternatives considered and why they were rejected
- Key decisions made during discussion
- Edge cases and how they'll be handled
- Any constraints or assumptions

## Rules
- Do NOT write brainstorm.md until the process above is followed
- Do NOT write any code or create any files other than brainstorm.md
- Do NOT be surface-level
- Do NOT skip ahead to requirements, design, or planning — that is the job of later commands
- Do NOT read or parse conversation log files, JSONL files, or any internal Codex data files — if you've lost context, ask me to re-summarize

After writing the file, remind me to run /compact, then `$review-brainstorm {feature_name}` when ready.

## REMINDER: Your job is DONE after writing brainstorm.md. Do NOT start on requirements, design, or implementation.
