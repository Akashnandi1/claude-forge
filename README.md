# Claude Code + Codex Independent Review Kit

Use **Claude Code as the primary author** and **OpenAI Codex as an independent adversarial reviewer** without giving up your existing Claude-only review path.

This repository installs a global, phase-gated development workflow for Claude Code and adds a parallel Codex review path that can be invoked either from Claude Code or directly from Codex.

> **Opinionated by design:** this project assumes the artifact structure and feature workflow included in this repository (`claude-features/<feature>/...`). It is intended for people who want a deliberate brainstorm → requirements → design → plan → phased implementation process with explicit review gates.

## Why this exists

Using the same model to both write and review a change can create correlated blind spots. This project keeps the roles separate:

- **Claude Code** authors and remediates.
- **Codex** reviews in a fresh, read-only, ephemeral process.
- **You** decide which findings are valid before Claude changes anything.
- **Manual checkpoints** remain separate from model review.

A Codex-backed gate therefore looks like this:

```text
Claude authors an artifact or phase
        ↓
Codex reviews it independently
        ↓
Claude verifies each Codex finding
        ↓
ACCEPT / REJECT / NEEDS USER DECISION
        ↓
You approve remediation
        ↓
Claude applies accepted fixes
        ↓
Run the Codex gate again
        ↓
PASS → continue
```

Codex does **not** fix its own findings in this workflow.

## What you get

Three independent ways to review the same work:

| Gate | Claude-only | Codex from Claude Code | Codex directly |
|---|---|---|---|
| Brainstorm | `/review-brainstorm <feature>` | `/codex-review-brainstorm <feature>` | `$codex-review-brainstorm <feature>` |
| Requirements | `/review-requirement <feature>` | `/codex-review-requirement <feature>` | `$codex-review-requirement <feature>` |
| Design | `/review-design <feature>` | `/codex-review-design <feature>` | `$codex-review-design <feature>` |
| Plan | `/review-plan <feature>` | `/codex-review-plan <feature>` | `$codex-review-plan <feature>` |
| Phase execution | `/review-execution <N> <feature>` | `/codex-review-execution <N> <feature>` | `$codex-review-execution <N> <feature>` |
| Final review | `/final-review <feature>` | `/codex-final-review <feature>` | `$codex-final-review <feature>` |

The Claude-only commands remain separate. Running `/review-design` never invokes Codex, and running `/codex-review-design` does not replace the Claude-only command.

## Core design principles

### 1. Same review contract, different reviewer mechanics

Each Codex skill mirrors the substantive checks in its corresponding Claude review command, then adds Codex-specific adversarial checks where useful.

The behavior intentionally differs:

| Claude review | Codex review |
|---|---|
| Interactive | Non-interactive |
| Can ask clarifying questions | Reports ambiguity as a finding |
| Can modify files after approval | Read-only |
| Manages remediation | Reports findings only |
| Participates in the workflow | Exits after the review |

See [`docs/REVIEW-PARITY.md`](docs/REVIEW-PARITY.md) for the stage-by-stage mapping.

### 2. Codex is isolated for every review

Codex-backed reviews are launched with the equivalent of:

```text
codex exec --ephemeral --sandbox read-only --cd <repo-root> ...
```

The review process cannot remediate the code it is judging. The launcher only persists the final Markdown review report.

### 3. No global Codex reviewer persona

The installer does **not** create a global `AGENTS.md` that forces Codex to behave like a reviewer all the time. Reviewer behavior is scoped to the installed `$codex-review-*` skills, so normal Codex usage remains normal.

### 4. Existing `CLAUDE.md` files work with Codex

The installer adds `CLAUDE.md` to Codex's global `project_doc_fallback_filenames` setting. Existing Claude-first repositories therefore do not need a duplicate `AGENTS.md` just to use these reviews.

Codex-native project instructions still take precedence when present:

```text
AGENTS.override.md
        ↓
AGENTS.md
        ↓
configured fallbacks such as CLAUDE.md
```

## Workflow assumed by this repository

The included Claude commands use this feature layout:

```text
claude-features/
└── auth-system/
    ├── brainstorm.md
    ├── requirement.md
    ├── design.md
    ├── plan.md
    ├── phases/
    │   ├── phase_1.md
    │   ├── phase_2.md
    │   └── ...
    └── reviews/
        └── codex/
```

A typical large feature moves through:

```text
/new-feature auth-system
/brainstorm auth-system
/compact
/codex-review-brainstorm auth-system
/compact
/requirement auth-system
/compact
/codex-review-requirement auth-system
/compact
/design auth-system
/compact
/codex-review-design auth-system
/compact
/plan auth-system
/compact
/codex-review-plan auth-system
/compact
/execute-plan 1 auth-system
/compact
/codex-review-execution 1 auth-system
/compact
... repeat per phase ...
/checkpoint <N> auth-system
/codex-final-review auth-system
```

You can substitute any `/codex-review-*` gate with its existing `/review-*` Claude-only equivalent, or intentionally run both.

## Platform support

The repository contains platform-specific entry points backed by the same shared Python implementation.

| Platform | Installer | Verifier |
|---|---|---|
| macOS | `./install.sh` | `./verify-install.sh` |
| Linux | `./install.sh` | `./verify-install.sh` |
| WSL | `./install.sh` | `./verify-install.sh` |
| Windows PowerShell | `.\install.ps1` | `.\verify-install.ps1` |

WSL and native Windows are separate user environments. If you use both, install the kit in both environments.

See [`docs/PLATFORM-NOTES.md`](docs/PLATFORM-NOTES.md) for platform details and caveats.

## Prerequisites

Install and authenticate the tools you plan to use before installing this kit:

- Python 3.11+
- Git
- Claude Code CLI available on `PATH`
- Codex CLI available on `PATH`
- Codex authenticated so `codex exec` can run non-interactively

Check the CLIs with:

```text
claude --version
codex --version
```

On macOS/Linux/WSL, `python3` should be available on `PATH`.

On native Windows, the installer detects a compatible Python 3.11+ launcher from `py -3`, `python`, or `python3`.

## Installation

> **Important:** installation writes to your user-level Claude and Codex configuration. Read [What installation changes](#what-installation-changes) before running it, especially if you already maintain global commands with the same names.

### macOS / Linux / WSL

Clone or download the repository, then run from its root:

```bash
chmod +x install.sh verify-install.sh uninstall-codex-integration.sh
./install.sh
./verify-install.sh
```

### Windows PowerShell

From the repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
.\verify-install.ps1
```

`Set-ExecutionPolicy -Scope Process Bypass` applies only to the current PowerShell process. Omit it if your environment already permits local scripts.

After installation, start a **new Claude Code and/or Codex session** so global commands, skills, and instructions are rediscovered.

## What installation changes

The installer operates at user scope. It does not copy integration files into every project.

It installs or configures:

```text
Claude Code
  <CLAUDE_CONFIG_DIR or ~/.claude>/CLAUDE.md
  <CLAUDE_CONFIG_DIR or ~/.claude>/commands/*.md
  <CLAUDE_CONFIG_DIR or ~/.claude>/review-system/bin/

Codex
  ~/.agents/skills/<skill-name>/
  <CODEX_HOME or ~/.codex>/config.toml
```

On Windows, `~` corresponds to the current user's home directory, normally `%USERPROFILE%`.

The installer:

1. Installs the included Claude workflow commands globally.
2. Installs the separate `/codex-review-*` Claude commands.
3. Installs the shared review/configuration helpers.
4. Installs six Codex review skills under the user's global `.agents/skills` directory.
5. Adds `CLAUDE.md` to Codex `project_doc_fallback_filenames` without removing existing fallback names.
6. Creates timestamped backups before replacing different installed files or modifying an existing Codex configuration.
7. Avoids overwriting a different existing global `CLAUDE.md`; the bundled version is written separately for manual comparison/merge.

### What it does not do

Installation does **not**:

- create `AGENTS.md` in your repositories;
- modify project source files;
- modify project `.gitignore` files;
- force Codex into reviewer mode globally;
- replace the Claude-only review commands with Codex-backed commands.

Running a Codex review later **does** create a review report under the feature directory.

## Using it in existing projects

After one global installation, a Claude-first repository can remain as simple as:

```text
my-project/
├── CLAUDE.md
├── claude-features/
├── src/
└── tests/
```

No project-level installation is required.

If a project already has `AGENTS.md`, Codex uses it according to its normal instruction precedence. Otherwise the configured `CLAUDE.md` fallback allows Codex to reuse the repository guidance you already maintain for Claude Code.

## What happens during a Codex-backed Claude review

For example:

```text
/codex-review-design auth-system
```

The global Claude command launches the shared review runner. The runner:

1. Finds the repository root.
2. Launches a fresh Codex process in read-only, ephemeral mode.
3. Explicitly invokes the matching global Codex review skill.
4. Captures the final report.
5. Writes it to:

   ```text
   claude-features/auth-system/reviews/codex/design-YYYYMMDD-HHMMSS.md
   ```

6. Returns the report to Claude Code.
7. Claude independently verifies each finding and classifies it as:
   - `ACCEPT`
   - `REJECT`
   - `NEEDS USER DECISION`
8. Claude presents the triage to the user **before making changes**.
9. After approval, Claude remediates accepted findings.
10. The same Codex gate should be rerun until it returns `PASS`.

This distinction is intentional: Codex makes the accusation; Claude verifies it; the user arbitrates; Claude remediates.

## Direct Codex use

The same review skills are available directly inside Codex:

```text
$codex-review-brainstorm auth-system
$codex-review-requirement auth-system
$codex-review-design auth-system
$codex-review-plan auth-system
$codex-review-execution 1 auth-system
$codex-final-review auth-system
```

Use `/skills` in Codex to confirm that the global skills have been discovered.

## Review reports and source control

Codex reports are stored under:

```text
claude-features/<feature>/reviews/codex/
```

Commit them if you want an audit trail. If you prefer local-only reports, add this to your project's `.gitignore`:

```gitignore
claude-features/*/reviews/codex/
```

The installer deliberately does not make that decision for you.

## Model selection

The review runner uses your normal Codex configuration by default. To force a specific model only for these review invocations, set `CODEX_REVIEW_MODEL`.

macOS/Linux/WSL:

```bash
export CODEX_REVIEW_MODEL='<model-id>'
```

PowerShell:

```powershell
$env:CODEX_REVIEW_MODEL = '<model-id>'
```

No model or reasoning level is hard-coded into the repository, which avoids silently pinning the workflow to a stale model configuration.

## Safety and trust model

The workflow uses several independent safeguards:

- Codex review sessions are ephemeral.
- Codex is launched with a read-only sandbox.
- Review skills explicitly prohibit remediation.
- The only artifact written by the review launcher is the Markdown review report.
- Claude is instructed to verify Codex findings instead of blindly accepting them.
- Claude-backed remediation remains approval-gated by the workflow instructions.
- Human `/checkpoint` verification remains a separate gate.

As with any agentic development tooling, review the installer and generated changes before using it on sensitive repositories. A model review is an additional quality signal, not a substitute for tests, security review, or human judgment.

## Uninstalling the Codex integration

The uninstall command intentionally leaves the original Claude workflow commands and global `CLAUDE.md` in place.

### macOS / Linux / WSL

```bash
./uninstall-codex-integration.sh
```

### Windows PowerShell

```powershell
.\uninstall-codex-integration.ps1
```

If this kit added `CLAUDE.md` to Codex's fallback list, uninstall removes only that entry and preserves other Codex configuration. If it was already configured before installation, uninstall leaves it untouched.

## Repository layout

```text
.
├── README.md
├── install.py
├── install.sh
├── install.ps1
├── verify_install.py
├── verify-install.sh
├── verify-install.ps1
├── uninstall_codex_integration.py
├── uninstall-codex-integration.sh
├── uninstall-codex-integration.ps1
├── claude/
│   ├── CLAUDE.md
│   ├── commands/              # Claude-only workflow and reviews
│   ├── codex-commands/        # Claude commands that call Codex
│   └── review-system/bin/     # Shared cross-platform runners
├── codex/
│   └── skills/                # Codex-native adversarial review skills
└── docs/
    ├── COMMAND-MAP.md
    ├── DESIGN-NOTES.md
    ├── PLATFORM-NOTES.md
    └── REVIEW-PARITY.md
```

## Troubleshooting

### Commands or skills are not visible after installation

Start a new Claude Code/Codex session. Command and skill discovery is normally performed at session startup.

Then run the verifier again:

```bash
./verify-install.sh
```

or on Windows:

```powershell
.\verify-install.ps1
```

### Codex does not appear to use my project `CLAUDE.md`

Run the verifier and inspect your Codex `config.toml`. The installer should have added `CLAUDE.md` to `project_doc_fallback_filenames` while preserving existing values.

If the project contains `AGENTS.md` or `AGENTS.override.md`, those have higher precedence than a fallback `CLAUDE.md`.

### Codex review cannot run

Confirm that:

```text
codex --version
```

works in the same environment and that Codex is already authenticated for non-interactive execution.

### A global Claude command already exists

The installer creates timestamped backups before replacing different installed files. Review the installer output and backup before relying on the installed version.

## Documentation

- [`docs/COMMAND-MAP.md`](docs/COMMAND-MAP.md) — command names across Claude and Codex
- [`docs/REVIEW-PARITY.md`](docs/REVIEW-PARITY.md) — substantive parity between the two review paths
- [`docs/DESIGN-NOTES.md`](docs/DESIGN-NOTES.md) — architecture and design rationale
- [`docs/PLATFORM-NOTES.md`](docs/PLATFORM-NOTES.md) — platform-specific details

## Contributing

Issues and pull requests are welcome. When changing review behavior, preserve the central invariant:

> **Keep the substantive correctness contract aligned between Claude and Codex, while keeping the reviewer mechanics independent.**

Changes to a Claude review rubric should normally be reflected in the corresponding Codex review skill, without turning Codex into an author/remediator.

## Disclaimer

This is an independent community workflow and is not affiliated with, endorsed by, or maintained by Anthropic or OpenAI. Claude, Claude Code, Codex, and OpenAI are trademarks or product names of their respective owners.
