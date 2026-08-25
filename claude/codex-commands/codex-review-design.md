---
description: Run an independent Codex design review, then triage and remediate accepted findings in Claude Code.
argument-hint: <feature-name>
disable-model-invocation: true
---

## CRITICAL - ROLE SEPARATION

This command uses Codex as the independent reviewer. You are the author/remediator, not the primary reviewer.

Do NOT replace Codex's review with your own fresh review. Verify each reported finding against the repository before accepting it, because Codex can be wrong.

## Independent Codex report

<codex-review-report>
!`__CODEX_FEATURE_REVIEW__ design "$0"`
</codex-review-report>

## Your job: triage the report

1. If the report is `BLOCKED`, explain the blocker and what must be fixed before review can run. Do not pretend the review passed.
2. If the report is `PASS`, do not invent additional review findings. State that the independent Codex gate passed and tell me the next workflow command: `/plan $0`.
3. For every finding in a `FAIL` report, verify it against the actual documents/code and classify it as:
   - **ACCEPT** - Codex is correct and the finding should be remediated.
   - **REJECT** - Codex is incorrect; explain specifically why with repository evidence.
   - **NEEDS USER DECISION** - the finding exposes a real ambiguity that cannot be resolved from the artifacts.
4. Do not silently accept Codex's proposed correction. The defect may be real while the suggested fix is wrong.
5. Present the triage clearly. Ask at most one or two focused questions at a time for NEEDS USER DECISION items.
6. For accepted findings, explain the proposed remediation and wait for my approval before modifying anything.
7. After approval, make only changes allowed at this gate: `claude-features/$0/design.md`, plus prior docs only when the accepted correction genuinely requires a cascade. Do not create plan/phase files or implementation code.
8. Run the relevant tests/checks after code changes when this gate permits code changes.
9. After remediation, tell me to run this same `/codex-review-design` command again. The gate closes only when a fresh Codex run returns PASS.

If an accepted design correction changes a functional requirement or core brainstorm decision, explicitly send the workflow back to the corresponding earlier review gate.

Do not proceed into the next workflow stage until the Codex gate has returned PASS.
