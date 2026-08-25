# Design notes

## Deliberate choices

1. **Separate command namespaces.** Existing Claude review names are preserved. Codex-backed reviews receive the `codex-` prefix, so the user chooses the reviewer explicitly at every gate.
2. **Global-only installation.** No `.claude/`, `.agents/`, `AGENTS.md`, or tool configuration is written into any repository.
3. **Reuse project `CLAUDE.md` globally.** The installer adds `CLAUDE.md` to Codex's `project_doc_fallback_filenames` in the user's global Codex config. Existing fallback entries are preserved, so Claude-first repositories need no duplicate `AGENTS.md`. Native `AGENTS.override.md`/`AGENTS.md` still take precedence when present.
4. **No global Codex reviewer persona.** A global `~/.codex/AGENTS.md` would affect unrelated Codex work. Reviewer constraints live inside the six explicit Codex skills instead.
5. **Read-only Codex process.** `codex exec --sandbox read-only` enforces author/reviewer separation instead of relying only on prompt wording.
6. **Ephemeral Codex process.** `--ephemeral` prevents review conversations from contaminating later reviews.
7. **Disk artifacts are the handoff.** Codex reads the `claude-features/<feature>/` artifacts and codebase. It does not need Claude's conversational context.
8. **Review reports are immutable evidence for the turn.** The launcher writes a timestamped report. Claude can remediate source/docs, but should not rewrite the report that triggered the remediation.
9. **Fresh re-review closes the gate.** Claude never self-certifies that it fixed Codex's findings. The same Codex gate is rerun until it returns PASS.
10. **Human checkpoint remains separate.** Manual application verification is not replaced by model review.
11. **No hard-coded Codex model.** The runner inherits the user's current Codex configuration, with an optional `CODEX_REVIEW_MODEL` override.
12. **One cross-platform implementation.** Shared Python cores implement install, verification, uninstall, Codex config editing, and review launching. Bash and PowerShell are thin entry points, preventing Windows and Unix behavior from drifting.
13. **Shell-neutral Windows Claude invocation.** The installer renders a detected Python 3.11+ launcher and absolute runner path into the six Codex-backed Claude commands. The invocation is valid whether native Claude Code executes `!` commands through Git Bash or PowerShell.
14. **WSL is independent.** WSL uses the Unix installer and its own home/configuration; native Windows uses the PowerShell installer. Install in both only if both environments are used.

## Review-contract parity

The Claude and Codex files are not intended to be word-for-word identical. Claude review commands are interactive and may discuss/modify work after approval; Codex review skills are read-only and return a report. However, each Codex skill mirrors every substantive checklist in the corresponding supplied Claude review command. Codex may add adversarial checks derived from the supplied global engineering invariants, but it may not remove or weaken the original review contract or expand feature scope.

See `REVIEW-PARITY.md`.

