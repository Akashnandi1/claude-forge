---
description: Run an independent Codex phase-execution review, then triage and remediate accepted findings in Claude Code.
argument-hint: <phase-number> <feature-name>
disable-model-invocation: true
---

## CRITICAL - ROLE SEPARATION

This command uses Codex as the independent reviewer. You are the author/remediator, not the primary reviewer.

Do NOT replace Codex's review with your own fresh review. Verify each reported finding against the repository before accepting it, because Codex can be wrong.

## Independent Codex report

<codex-review-report>
!`__CODEX_FEATURE_REVIEW__ execution "$0" "$1"`
</codex-review-report>

## Your job: triage the report

1. If the report is `BLOCKED`, explain the blocker and what must be fixed before review can run. Do not pretend the review passed.
2. If the report is `PASS`, do not invent additional review findings. State that the independent Codex gate passed and tell me the next workflow command: `/execute-plan <next-phase> $1` (or `/codex-final-review $1` when this is the last phase and you are staying on the Codex review path).
3. For every finding in a `FAIL` report, verify it against the actual documents/code and classify it as:
   - **ACCEPT** - Codex is correct and the finding should be remediated.
   - **REJECT** - Codex is incorrect; explain specifically why with repository evidence.
   - **NEEDS USER DECISION** - the finding exposes a real ambiguity that cannot be resolved from the artifacts.
4. Do not silently accept Codex's proposed correction. The defect may be real while the suggested fix is wrong.
5. Present the triage clearly. Ask at most one or two focused questions at a time for NEEDS USER DECISION items.
6. For accepted findings, explain the proposed remediation and wait for my approval before modifying anything.
7. After approval, make only changes allowed at this gate: the current phase implementation and its directly affected tests/docs only. Do not implement future-phase work. Preserve the phase boundary.
8. Run the relevant tests/checks after code changes when this gate permits code changes.
9. After remediation, tell me to run this same `/codex-review-execution` command again. The gate closes only when a fresh Codex run returns PASS.

After accepted fixes, ensure `plan.md` and `phases/phase_$0.md` accurately reflect completion before asking for the fresh Codex re-review. If the phase approach is fundamentally wrong, recommend re-running `/execute-plan $0 $1`.

Do not proceed into the next workflow stage until the Codex gate has returned PASS.
