---
name: execute-improvement-plans
description: Execute implementation plans produced by the Improve skill through an explain, approve, implement, review, and commit workflow. Use when a repository contains self-contained Improve-generated plans that should be implemented sequentially or as an explicitly authorized batch, with one coherent commit per accepted plan. Do not use to generate plans or when no Improve-generated plans exist.
---

# Execute Improvement Plans

Execute Improve-generated plans while preserving user control over scope, review, and commits.

## Establish the execution policy

1. Locate the plan index and selected plan. Read both completely.
2. Confirm the plans are Improve-generated and self-contained: problem, affected code, intended
   changes, and validation. If not, stop; do not invent replacement plans.
3. Read repository instructions and inspect the branch, `HEAD`, upstream, and working tree.
4. Record the branch, plan order, approval mode, review mode, commit policy, protected paths, and
   validation commands. Carry explicit standing instructions until changed.

Treat plan files as mutable execution records. Update statuses, checklists, and execution notes when
useful, but never stage or commit the plans directory. A user instruction to leave plans untouched
wins.

Re-check the execution context at each plan boundary and after a merge, push, checkout, resumed
session, or requested branch change. Do not continue on a stale or unexpected branch. An explicit
branch instruction overrides a plan's suggested branch; record the deviation.

## Execute one plan

### Select and explain

Choose the next incomplete plan in dependency order and verify it against current code. Treat its
implementation details as a design hypothesis; repository architecture, source-of-truth references,
and explicit user feedback outrank stale prescriptions.

If assumptions are stale, explain the drift and propose the smallest intent-preserving adjustment.
Request renewed approval only when scope or architecture materially changes. If the plan describes
the wrong product behavior, report the intent-to-plan mismatch and let the user revise it.

Before editing, explain:

- **What:** behavior, boundaries, and expected files;
- **Why:** the concrete problem and benefit;
- **How:** sequence, important choices, risks, validation, and exclusions.

Wait for explicit approval. Approval applies to one plan unless the user clearly authorizes a
defined batch.

### Implement

After approval:

1. Implement only the approved plan and necessary support, using the narrowest coherent design.
2. Update relevant documentation when behavior or boundaries change.
3. Run focused validation and inspect the isolated diff. Run appropriate repository-wide gates
   before review, or after the final plan in an authorized batch.
4. Report changes, validation, and justified deviations. Do not commit.

### Review

For each finding:

1. Locate it by symbol or behavior, not a possibly stale line number.
2. Classify it as genuine, false-positive, or intentional.
3. Fix genuine, valuable findings within scope; briefly explain skipped findings.
4. Request approval before changing public contracts, core architecture, or plan scope.
5. Re-run proportional validation and return for review.

Apply the same process to post-commit findings. Use a separate corrective commit when requested; do
not amend unless explicitly asked.

### Commit

Commit only after acceptance or under an explicit commit-after-validation policy:

1. Review the final diff, working tree, and affected documentation.
2. Reuse still-current validation; rerun only what the final changes invalidate.
3. Stage explicit implementation paths, excluding unrelated changes, protected paths, and plans.
4. Create one focused commit for the plan and confirm the commit ID and remaining status.

Then select and explain the next plan unless it is covered by batch authorization.

## Batch authorization

Only an unmistakable authorization for a defined set removes per-plan pauses. Under a batch:

- state the policy once;
- keep dependency order and one coherent scope at a time;
- verify each plan against current code;
- run focused validation and inspect each isolated diff;
- commit only if separately authorized;
- stop only for a stop condition below;
- run combined gates after the final plan.

A request for one review at the end permits a combined handoff; it does not permit blended commits.

## Adjacent work

If validation exposes work outside the plan and the user explicitly asks to fix it:

- classify whether the issue was caused by, exposed by, or unrelated to the plan;
- state the boundary and track it as a separate workstream;
- pause the plan if the fix is needed for a trustworthy baseline, then resume it;
- keep its diff, validation, review, and commit separate.

If “commit this” covers an accepted plan plus a previously disclosed adjacent fix, create the
separate focused commits already described.

## Validation integrity

- Validate runtime or visual behavior directly when relevant; static gates alone are insufficient.
- Never describe a scoped check as a full gate.
- Avoid formatters that rewrite protected plan artifacts; run the narrowest equivalent check.
- Track which working-tree state each result covers and reuse current expensive results.
- For long checks, record the command, expected runtime, retry policy, state, and outcome.
- Diagnose flakes from exact artifacts or retries-disabled reproduction before changing assertions,
  timeouts, or retries. Distinguish product defects, test synchronization, and runner latency.
- Treat interrupted or incomplete runs as inconclusive. Recover surviving processes or artifacts,
  then rerun the narrowest definitive check without discarding unrelated valid results.

When required evidence exists only after commit and push:

1. Leave the plan `IN PROGRESS` and record the baseline, local evidence, expected jobs, success
   criteria, and stop thresholds.
2. Do not push or dispatch external work without authorization.
3. When evidence arrives, verify it matches the relevant commit and configuration, record the
   result, and set `DONE`, `REJECTED`, or `BLOCKED` as justified.

Do not call implementation-ready work fully validated while required external evidence is pending.

## Authorization and stop rules

- “Continue” selects and explains the next plan.
- “Commit and continue” commits the accepted plan, then selects and explains the next.
- A review request authorizes review work, not unrelated cleanup.
- “Finish” does not waive approval or review gates without explicit batch authorization.

Stop when work requires material unapproved scope, conflicting plans, destructive action, new
credentials or authority, an external decision, or overlapping user changes that cannot be
preserved. Also stop when validation exposes a cross-cutting failure outside authorized scope.

Do not stop for ordinary implementation difficulty, stale line numbers, or small
intent-preserving adjustments.

## Close the plan set

After the final plan:

1. Reconcile every index status; keep externally pending plans `IN PROGRESS`.
2. Confirm combined validation is current.
3. Report commits, deviations, branch/upstream state, remaining changes, and plan artifact status.
4. When later evidence completes a plan, update only its execution records unless code changes are
   required; do not create an empty implementation commit.
