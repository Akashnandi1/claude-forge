# Claude Code Feature Workflow

A structured, gated workflow for building features with Claude Code. Forces a deliberate progression through brainstorming, requirements, design, planning, and phased execution — with review gates at every step.

## Installation

Copy the commands into your global Claude config:

```bash
cp -r .claude/commands/ ~/.claude/commands/
```

Available in every project. For project-specific commands, copy to `<project-root>/.claude/commands/` instead.

### CLAUDE.md (Optional Companion)

The included `CLAUDE.md` provides always-on rules for code quality, architecture, and error recovery. The commands handle the workflow; `CLAUDE.md` handles coding standards. They don't conflict.

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

## Directory Structure

All planning documents are saved relative to your project root:

```
your-project/
└── claude-features/
    └── auth-system/
        ├── brainstorm.md
        ├── requirement.md
        ├── design.md
        ├── plan.md
        └── phases/
            ├── phase_1.md
            ├── phase_2.md
            └── ...
```

## Commands

### `/new-feature xyz`

Creates `claude-features/xyz/`. Does nothing if it already exists.

### `/brainstorm xyz`

Deep, interactive conversation to explore the feature. Asks focused questions, challenges vague ideas, proposes options when you're stuck, and searches the internet for similar features and prior art. No code is written.

**Enforces:** No file is written until you explicitly approve. Conversation continues until all gray areas are eliminated.

**Output:** `brainstorm.md` — Problem statement, agreed approach, alternatives considered, key decisions, edge cases, constraints.

### `/review-brainstorm xyz`

Critically reviews `brainstorm.md` for logical gaps, vague areas, missing edge cases, and unstated assumptions. Walks through issues one at a time and updates the document after each resolution.

**Enforces:** No changes without your approval. Recommends re-running `/brainstorm` if the foundation is fundamentally flawed rather than patching it.

### `/requirement xyz`

Converts the brainstorm into a formal, implementation-ready specification with 15 sections: feature overview, problem statement, goals, non-goals, user stories, functional requirements, user flow, API/backend requirements, frontend requirements, edge cases, performance requirements, security/privacy, analytics/logging, acceptance criteria, and open questions.

**Enforces:** Every item must be specific enough for an engineer to implement without asking questions. No design decisions — captures WHAT, not HOW.

**Output:** `requirement.md`

### `/review-requirement xyz`

Validates `requirement.md` against `brainstorm.md`. Checks all 15 sections for completeness, flags vague language, untestable acceptance criteria, and missing coverage.

**Enforces:** Cross-references every brainstorm decision against the requirements. Recommends re-running `/requirement` if fundamentally broken.

### `/design xyz`

Creates the technical design — translates requirements into concrete architecture, component design, data models, API design, error handling, scalability, extensibility, trade-offs, risks, and testing strategy. Searches the internet for architectural patterns and known pitfalls.

**Enforces:** Every design choice must trace back to a requirement. No "TBD" decisions — everything is resolved or explicitly listed as an open question.

**Output:** `design.md`

### `/review-design xyz`

Validates `design.md` against `requirement.md`. Checks for missing requirement coverage, vague design decisions, scalability bottlenecks, weak trade-off reasoning, and data model issues.

**Enforces:** Alignment between design and requirements. Flags overbuilding beyond non-goals.

### `/plan xyz`

Breaks the design into ordered, independently testable implementation phases. Produces a high-level overview (`plan.md`) and one self-contained file per phase (`phases/phase_N.md`).

Each phase file includes all relevant design and requirement context pulled in, so during execution only the phase file and the codebase are needed.

**Enforces:** Every phase must be independently testable. Every part of the design must be covered by at least one phase. Testing criteria must include happy path, error path, edge cases, and integration tests — specific enough to write test cases from.

**Output:** `plan.md` + `phases/phase_1.md`, `phase_2.md`, ...

### `/review-plan xyz`

The most comprehensive review. Validates that the union of all phases fully covers both `design.md` and `requirement.md`. Checks each phase for self-containedness, testability, sizing, ordering, and testing criteria quality.

**Enforces:** No gaps between phases. No phantom work that doesn't trace back to design or requirements. No phase that can't be independently verified.

### `/execute-plan N xyz`

Implements phase N and only phase N. Reads the phase file and the codebase — no other planning documents. Writes code and tests, then marks the phase complete in `plan.md`.

Searches the internet for library docs, API references, and implementation patterns as needed.

**Enforces:** Will not start if dependencies (prior phases) aren't complete. Will not touch work belonging to other phases. Everything specified in the phase file gets built.

**Usage:** `/execute-plan 1 auth-system` — phase number first, then feature name.

### `/review-execution N xyz`

Reviews code changes from phase N. Reads the current phase file and all prior phase files to check cohesion across phases. Evaluates completeness, code quality, testing, integration, and design adherence.

Issues are categorized as **must fix** (blocks next phase), **should fix** (quality concern), or **nit** (minor).

**Enforces:** Every testing criterion from the phase file must be satisfied. Code must integrate cleanly with prior phases — no regressions, consistent patterns. Recommends re-running `/execute-plan` if implementation is fundamentally broken.

**Usage:** `/review-execution 1 auth-system` — phase number first, then feature name.

### `/final-review xyz`

Run after all phases are complete. Reviews the entire feature as a unified whole — not phase by phase. Checks requirement coverage, cross-phase integration, overall code quality, test coverage, and design adherence.

**Enforces:** Every functional requirement and acceptance criterion from `requirement.md` must be implemented and verified. This is the last gate.

## Full Workflow

```
/new-feature auth-system
/brainstorm auth-system                → /compact
/review-brainstorm auth-system         → /compact
/requirement auth-system               → /compact
/review-requirement auth-system        → /compact
/design auth-system                    → /compact
/review-design auth-system             → /compact
/plan auth-system                      → /compact
/review-plan auth-system               → /compact
/execute-plan 1 auth-system            → /compact
/review-execution 1 auth-system        → /compact
/execute-plan 2 auth-system            → /compact
/review-execution 2 auth-system        → /compact
... repeat for each phase ...
/final-review auth-system
```

Run `/compact` between every step. All state lives on disk — the conversation is disposable.

## How It Manages Context

Each step only reads what it needs. By the execution phase, Claude reads a single phase file and the codebase — not the brainstorm, requirements, or full design. Phase files are self-contained with all relevant context pulled in during planning.

This keeps the context window lean. `/compact` between steps keeps it leaner.

## Cascading Updates

Every command can update prior documents if findings warrant it:

- **Small clarifications:** Discussed with you, then applied directly
- **Significant changes:** Flagged with a recommendation to re-run the relevant review step
- **Fundamental issues:** Recommendation to re-run the creation step entirely

No patching broken foundations.

## Customization

Each command is a markdown file. Edit directly — no build step. Changes take effect immediately.

```bash
vim ~/.claude/commands/brainstorm.md
```

To add a new command, create a new `.md` file. The filename becomes the command name. Use `$ARGUMENTS` to capture user input.
