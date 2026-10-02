---
name: guided-review
description: Use when the user asks for "guided review", "stage one by one", "review slice by slice", or to approve coherent changes incrementally before committing. Do not trigger for an explanation-only walkthrough, an ordinary code review, or a large diff alone.
---

# Guided review

Land work as commits the reviewer understands. The reviewer drives the pace with short replies;
the agent scopes, prepares, presents, verifies and commits only when authorised.

## 1. Establish scope

1. Inventory staged, unstaged and untracked changes. Agree which files and hunks belong to this
   review; leave everything else untouched and out of the index.
2. Read the repository's instructions and conventions.
3. Split the scope into standalone commits that each tell one story: foundations first, then each
   flow in the order it executes; mechanical changes (codemods, renames, formatting) on their own.
   Each commit builds and passes alone. Never stage an intermediate version that a later commit
   rewrites.
4. Present the plan and wait for it to be accepted.

## 2. Prepare each commit

- Run the checks the commit affects (format, lint, type check, tests, migration drift, IDE
  diagnostics). Note the state each ran against and rerun only what later changes invalidate;
  keep expensive full suites for the final round.
- Self-review the diff with the [summon-nikhil](../summon-nikhil/SKILL.md) lenses and fix obvious
  issues. When a smell turns up, search for the same pattern.
- Work in the mode agreed for the session: in-session by default, reviewer subagents only when
  authorised. Verify every finding yourself before acting on it.

## 3. Present one slice

A slice is a hunk, a file or a tightly coupled group the reviewer can understand on its own, staged
exactly as it will be committed, with its tests. Order the slices to build understanding of one
complete flow.

```markdown
Staged (<n> of <N>, commit <m> of <M>): `<path>`

- <what changed, one bullet per change, in reading order>
- <why, where it is not obvious>

Test (one line): <what the tests cover>

Say "next" to stage <next slice>.
```

Point to exact lines. Make every message self-contained: the reviewer may return from other work,
so never rely on earlier scrollback.

## 4. Handle feedback

| Reply | Action |
| --- | --- |
| "next" | The slice is approved; stage the next one. |
| A question | Answer with evidence (the code, real data, the documentation). A "why" is not a rewrite request; offer a change only if warranted, with a recommendation and the option to keep it. |
| A change request | Change the working tree, rerun the affected checks and re-stage. If approved slices change too, re-stage them and say which and why. |
| A decision that is theirs | Ask, with a recommended option. |
| A discovery (a bug, a stale doc, a missing test) | Fix it in this commit when in scope and say so; otherwise record it. |

Do not move on until the current slice is approved.

## 5. Final round

1. Make one pass over the whole commit for dead code, ambiguity and correctness with the
   summon-nikhil lenses.
2. Anything it changes is re-staged, re-presented and approved again, with the affected checks
   rerun.
3. Verify the staged tree is the tested tree: only scoped changes are staged, nothing they need is
   left out, and the full checks pass on exactly what is staged. When the index differs from the
   working tree, check out the index in a scratch directory.
4. Report honestly, including flaky or skipped tests, and propose the commit message in the
   repository's format (default: one conventional-commit subject line, no body, no trailer).

## 6. Commit

- Commit only on explicit approval ("approved"). Never amend or push unless asked.
- Keep untracked working notes out of every commit.
- Report the commit ID and move to the next planned commit.

## Unattended preparation

Only when the reviewer explicitly asks for it: run steps 1–5 with summon-nikhil as the reviewer,
verifying and applying its findings. Stop before step 6 with the commit staged and a report of the
plan, the findings and how each was handled. A pending reply is never permission to switch to this
mode, and a person always approves the commit.
