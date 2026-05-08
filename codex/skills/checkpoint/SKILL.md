---
name: checkpoint
description: Use when manually verifying all completed phases of a feature so far, collecting the verification checklist, diagnosing failures, and fixing only issues found during verification.
---

## CRITICAL — READ THIS FIRST
Your job is to verify all work done up to Phase {phase_number} of feature {feature_name}. You are fixing bugs found during verification, NOT implementing new phases or features.

---

Parse the user request after the skill name. The canonical format is: `$checkpoint {phase_number} {feature_name}`. For example, `$checkpoint 3 auth-system` means verify all work up to and including phase 3 of feature auth-system.

You are conducting a cumulative verification checkpoint for feature: {feature_name}, covering Phases 1 through {phase_number}.

You are acting as a staff software engineer at Google verifying that the implemented work actually functions correctly in the real application — not just that the code exists.

Read the following files:
- feat-dev/{feature_name}/plan.md
- All phase files from phase_1.md through phase_{phase_number}.md

Also read the current codebase to understand what has been built.

## Your job

This is a hands-on verification checkpoint. The goal is to confirm that everything built so far actually works when you use the real application — not just that tests pass.

## Step 1: Gather all manual verification steps

Go through each completed phase file (phase_1.md through phase_{phase_number}.md) and collect every manual verification step into a single consolidated checklist. Group them by phase but present them as one list.

Present this list to me clearly, for example:

```
## Manual Verification Checklist (Phases 1-3)

### From Phase 1:
- [ ] Visit http://localhost:3000 — should see the new dark background
- [ ] Click on a node — should show glass-effect tooltip

### From Phase 2:
- [ ] Hit GET /api/graph/AAPL — should return JSON with nodes and edges
- [ ] curl -X POST /api/search -d '{"q":"apple"}' — should return matching companies

### From Phase 3:
- [ ] Search bar should auto-complete after 3 characters
- [ ] Clicking a search result should navigate to the graph view
```

If any prerequisites are needed (server restart, build, migration, seed data), list those first with exact commands.

## Step 2: Ask me to verify

After presenting the checklist, ask me to go through each item and tell you which ones passed and which ones failed.

Wait for my response. Do NOT assume anything passes.

## Step 3: Handle failures

For each verification that fails:

1. Ask me to describe what I actually see vs. what was expected
2. Diagnose the root cause by reading the relevant code
3. Categorize the issue:
   - **Bug** — the code doesn't do what the phase file says it should
   - **Missing implementation** — something from the phase file wasn't implemented
   - **Integration issue** — individual phases work but they don't work together
   - **Environment issue** — code is correct but something needs to be rebuilt/restarted/migrated
4. For environment issues: give me the exact commands to run and ask me to re-verify
5. For bugs, missing implementation, and integration issues:
   - Explain the fix
   - Wait for my approval
   - Implement the fix
   - Tell me how to re-verify the specific item
   - Ask me to confirm it now passes

## Step 4: Update documents

After all issues are resolved:

1. Update the relevant phase files with any fixes or clarifications discovered
2. If the fix revealed that a phase file's manual verification steps were wrong or incomplete, fix them
3. Update plan.md if any phase scope changed
4. Summarize all bugs found and fixes applied

## Rules
- Do NOT implement work from future phases, even if you notice it's needed
- Do NOT skip verification items — every item in the checklist must be verified by the user
- Do NOT assume something works just because the code looks correct — the whole point is to catch things that look right but don't work
- Do NOT modify future phase files — if a bug affects future phases, flag it and tell me "We should update phase_{N}.md before executing it"
- Treat every failed verification seriously — the user saw something wrong in the real app
- Do NOT read or parse conversation log files, JSONL files, or any internal Codex data files

After all verifications pass, remind me to run /compact, then continue with `$execute-phase {next_phase_number} {feature_name}` if there are more phases, or `$final-review {feature_name}` if all phases are complete.

## REMINDER: Your job is DONE after all verifications pass and documents are updated. Do NOT start the next phase. STOP here.
