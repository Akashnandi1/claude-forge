# Installed command map

| Purpose | Claude-only | Codex via Claude | Codex direct |
|---|---|---|---|
| Brainstorm review | `/review-brainstorm <feature>` | `/codex-review-brainstorm <feature>` | `$codex-review-brainstorm <feature>` |
| Requirement review | `/review-requirement <feature>` | `/codex-review-requirement <feature>` | `$codex-review-requirement <feature>` |
| Design review | `/review-design <feature>` | `/codex-review-design <feature>` | `$codex-review-design <feature>` |
| Plan review | `/review-plan <feature>` | `/codex-review-plan <feature>` | `$codex-review-plan <feature>` |
| Phase execution review | `/review-execution <N> <feature>` | `/codex-review-execution <N> <feature>` | `$codex-review-execution <N> <feature>` |
| Final holistic review | `/final-review <feature>` | `/codex-final-review <feature>` | `$codex-final-review <feature>` |

The original Claude path remains independent and unchanged. Running a Claude-only review never invokes Codex. Running a Codex-backed Claude review invokes Codex once at command preprocessing time and then gives Claude only the review report for triage/remediation.
