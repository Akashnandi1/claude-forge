# Claude / Codex Review Parity

The original Claude review commands are preserved unchanged. The Codex skills deliberately use different operational instructions because Codex is a read-only, non-interactive reviewer, but each skill mirrors the substantive review contract of its corresponding Claude command.

| Claude review | Codex review | Substantive parity |
|---|---|---|
| `/review-brainstorm` | `$codex-review-brainstorm` | gaps, contradictions, vagueness, edge cases, assumptions, developer-guessing risk, foundation/re-run decision |
| `/review-requirement` | `$codex-review-requirement` | all 15 sections, bidirectional brainstorm traceability, vagueness, contradictions, edge/error behavior, assumptions, measurable goals, testable acceptance criteria, WHAT-not-HOW, cascading impact |
| `/review-design` | `$codex-review-design` | all 16 sections, requirement coverage/traceability, vagueness, contradictions, boundaries, failure handling, scalability, extensibility, risks, trade-offs, integrations, data model, alignment, cascading impact |
| `/review-plan` | `$codex-review-plan` | union coverage, phase quality, full testing rubric, self-containedness, manual verification, ordering, phase split/merge, cascading impact |
| `/review-execution N` | `$codex-review-execution N` | completeness, code quality, testing, prior-phase cohesion, design adherence, future-phase containment, completion markers, cascading impact, re-run decision |
| `/final-review` | `$codex-final-review` | requirements/acceptance/edge/performance coverage, integration/cohesion, code quality/maintainability, tests, design adherence, tech debt, final gate |

## Why wording is not identical

The Claude commands are interactive author/reviewer workflows: they can ask questions, discuss resolutions, wait for approval, and edit files. The Codex skills are intentionally isolated reviewer workflows: they ask no live questions, modify nothing, and return evidence-backed findings for Claude and the user to triage.

The Codex skills may also add adversarial checks derived from the global engineering invariants in the supplied `CLAUDE.md` (dependency direction, separation of concerns, bounded data access, explicit failures, security, observability, testing discipline). These additions strengthen the second-opinion review without changing the feature scope.

## Invariant

Substantive correctness criteria should remain aligned; reviewer mechanics should remain different.
