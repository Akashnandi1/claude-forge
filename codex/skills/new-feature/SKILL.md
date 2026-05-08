---
name: new-feature
description: Use when initializing a new feature workspace under feat-dev for a named feature before brainstorming begins.
---

Parse the user request after the skill name. The canonical format is: `$new-feature {feature_name}`. For example, `$new-feature auth-system`.

Create the directory feat-dev/{feature_name}/ if it doesn't already exist.

If it already exists, inform me and do NOT overwrite anything.

If it doesn't exist, create it and confirm it's ready.

After creating the directory, tell me to run `$brainstorm {feature_name}` when ready.
