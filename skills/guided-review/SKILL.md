---
name: guided-review
description: Use when the user asks for "guided review", "stage one by one", "review slice by slice", or to approve coherent changes incrementally before committing. Do not trigger for an explanation-only walkthrough, an ordinary code review, or a large diff alone.
---

# Guided review

Prepare coherent commits the reviewer understands. Discover conventions, tooling and verification
commands from the current repository; no particular stack or runtime helper is required.

## 1. Agree scope and authority

Inspect the branch/worktree, staged, unstaged and untracked changes, and relevant instructions.
Identify the review scope; preserve unrelated working-tree and index changes. For multiple issues,
map each to its base branch and scoped changes. Infer known choices from the session and Git.

Propose standalone commits in dependency order, each independently valid. Separate mechanical
changes from behavior changes; avoid knowingly temporary implementations within a commit.
State the review mode and commit policy once, carrying existing authorization forward:

| Mode | Who reviews | Progression |
| --- | --- | --- |
| Interactive (default) | User | Accept the plan, then approve each slice |
| Delegated (explicit request only) | Designated reviewer, or summon-nikhil | Review and fix within the approved scope without per-slice user pauses |

Review delegation does not authorize commits. Commit only on explicit commit approval or under a
standing commit-after-validation policy. A simulated verdict supplies evidence, not authorization.
Use reviewer subagents only when authorized; otherwise review in-session. Silence never changes mode.

Choose granularity from the change, respecting requests for finer review:

- **Mechanical:** one coherent batch; inspect all changes, present a representative diff, paths
  and behavioral exceptions.
- **Feature:** one complete user flow.
- **Model or architecture:** one meaningful decision at a time.

## 2. Prepare and verify

Review with [summon-nikhil](../summon-nikhil/SKILL.md), verify its findings and fix issues within
scope. The review skill remains advisory; this workflow performs authorized edits. Before a
substantial correction, compare owning decisions and a named sibling implementation. Discuss
unresolved design choices before expanding the change; record out-of-scope discoveries separately.

Run checks appropriate to the change and repository policy. Track what state they cover, reuse
current results, and rerun only checks invalidated by subsequent edits. Reserve expensive combined
gates for the final round where appropriate; do not add redundant tests or require permanent tests
when the session calls for temporary validation.

For runtime checks, establish the actual target, checkout and build mode using existing tooling.
Reuse intended services; do not assume local-only, production or isolated-worktree policy.
For state/data changes, select relevant lifecycle boundaries—create, edit, clear, serialize, save,
reload, navigate away/back—and affected sibling surfaces. For bugs or broad regression reviews,
use [verification and coverage](references/review-state.md#verification-and-coverage).

## 3. Stage and present

A slice is a coherent hunk, file or group, including relevant tests. Stage it exactly as intended
for the commit, in an order that explains the flow. “Staged” means visible in the user's normal
Git index. Label scratch indexes/worktrees as validation artifacts, not visible staged work.

For interactive review:

```text
Staged: slice <n>/<N>, commit <m>/<M> — <paths and exact lines>
Changes: <what and why; representative example for a mechanical batch>
Validation: <checks and observed results, or what remains unverified>
Next: <next slice, or final verification if this is the last slice>
```

Make the presentation understandable without scrollback. Wait for slice approval before advancing.
In delegated mode, use the same coherent scopes for reviewer handoffs without asking for “next”.

| Reply | Action |
| --- | --- |
| “next” | Approve this slice and advance; after the last slice, run final verification. No commit authorization implied. |
| A question | Answer with evidence and a recommendation; do not treat it as a rewrite request. |
| A change request | Edit within scope, rerun affected checks and re-stage. Re-present changed approved slices in the agreed mode. |
| “approved” | Apply to the proposal just presented. Slice approval alone does not authorize committing. |

Stop for an unresolved decision outside the approved scope, not routine implementation difficulty.

## 4. Finish the commit

- Review the assembled commit for omissions, ambiguity and correctness. Re-review any resulting
  edits in the agreed mode and rerun invalidated checks.
- Ensure the intended commit tree matches the relevant tested state. If the index differs from
  the working tree, validate the candidate tree in scratch space. Preserve unrelated staged work;
  if it prevents a clean scoped commit, resolve that boundary rather than including or discarding it.
- Report scoped changes, findings handled, validation and gaps. For bugs, include reproduction,
  before/after evidence and user verification steps; distinguish inspection from execution.
- Propose a commit message in the repository's format. Default to a conventional-commit subject
  without a body or trailer unless context or instructions call for them.
- If committing is authorized, commit only the reviewed scope and report the ID; otherwise stop
  with it staged. Keep working notes out of the commit. Never amend or push unless asked.

Continue to the next planned commit under the same policy.

## Resume and handoff

At interruption, handoff, commit or mode-change boundaries, refresh the compact
[checkpoint](references/review-state.md#checkpoint). On resume, reconcile it against actual Git
state and artifacts before repeating work. Temporary progress belongs in the conversation or the
existing scratch convention; durable decisions belong in owning docs.

Use the reference's RCA or cross-agent brief only when requested. Do not create a permanent diary
or another tracking system for routine work.
