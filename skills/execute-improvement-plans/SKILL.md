---
name: execute-improvement-plans
description: Execute implementation plans produced by the Improve skill through a strict explain, approve, implement, review, and commit loop. Use when a repository already contains self-contained Improve-generated plan files and the user wants to implement them sequentially with explicit approval before each plan, iterative review before each commit, and one accepted plan per commit. Do not use to generate plans or when no Improve-generated plans exist.
---

# Execute Improvement Plans

Implement one Improve-generated plan at a time while keeping the user in control of scope and commits.

## Verify the prerequisite

Require implementation plans produced by the [Improve skill](https://www.skills.sh/shadcn/improve/improve). This skill executes those plans; it does not replace Improve's read-only audit and planning work.

1. Locate the plan index and referenced plan files. Prefer paths named by the user; otherwise inspect likely locations such as `plans/`.
2. Read the index and the selected plan completely.
3. Confirm the artifacts are self-contained implementation plans produced by Improve. They should identify the problem, affected code, intended changes, and validation.
4. If the plans are absent, incomplete, or not Improve-generated, stop and state that this skill requires Improve-generated plans. Do not generate replacement plans unless the user separately asks to use Improve.
5. Read repository instructions and inspect the working tree before changing code. Preserve unrelated and user-owned changes.

Treat plan files as control inputs. Do not edit, delete, stage, or commit them unless the user explicitly requests it or the repository instructions require it.

## Select one plan

Choose the next incomplete plan from the index, respecting dependencies and documented order. Never implement multiple plans under one approval.

If the plan is stale relative to the current code:

- explain which assumptions no longer hold;
- propose the smallest adjustment that preserves the plan's intent;
- request renewed approval when the adjustment materially changes scope or architecture.

## Explain before editing

Inspect enough current code to verify the plan, then explain:

- **What:** the behavior, boundaries, and files expected to change;
- **Why:** the concrete problem and the architectural or product benefit;
- **How:** the implementation sequence, important design choices, migration concerns, and validation.

Call out risks, likely review points, and anything intentionally out of scope. Do not modify implementation files yet.

End this phase by waiting for explicit approval. Approval for one plan does not approve later plans.

## Implement after approval

After explicit approval:

1. Implement only the approved plan and necessary supporting changes.
2. Follow repository conventions and use the narrowest coherent design.
3. Verify assumptions against current code instead of copying plan details mechanically.
4. Update relevant documentation and JSDoc when behavior or boundaries changed.
5. Run focused checks during implementation, then the repository's appropriate formatting, lint, typecheck, test, build, and coverage gates.
6. Do not commit.

Report the completed implementation, validation results, and any justified deviation from the plan. Wait for user review.

## Iterate on review

For every review round:

1. Verify each finding against the current code.
2. Fix findings that remain valid and add real value.
3. Skip stale, incorrect, duplicate, or low-value findings with a brief concrete reason.
4. Keep changes within the approved plan.
5. If feedback changes core architecture, public contracts, or plan scope, explain the impact and wait for explicit approval before implementing it.
6. Re-run validation proportional to the changes.
7. Return the implementation for another review without committing.

Repeat until the user explicitly says the implementation is accepted or asks to commit. Do not infer acceptance from silence or from a successful test run.

## Commit the accepted plan

When the user asks to commit:

1. Review the final diff and working tree.
2. Refresh affected documentation if it is stale.
3. Run the final relevant validation gates.
4. Stage only files belonging to the accepted plan. Exclude unrelated changes and plan artifacts unless explicitly authorized.
5. Create one focused commit for the plan using the repository's commit style.
6. Confirm the commit identifier and remaining working-tree state.

After the commit, select the next plan and return to **Explain before editing**. Never begin its implementation until the user approves it.

## Preserve the gates

- A request to “continue” after acceptance authorizes selecting and explaining the next plan, not implementing it.
- A request to “commit and continue” authorizes committing the accepted plan and explaining the next one.
- A review request authorizes inspection and feedback handling, not unrelated cleanup.
- A terminal request such as “finish all plans” does not remove the per-plan approval and review gates unless the user explicitly changes this workflow.
- When blocked by missing authority, external state, or a material design choice, report the blocker and wait rather than broadening scope.
