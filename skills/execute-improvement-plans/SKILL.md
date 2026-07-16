---
name: execute-improvement-plans
description: Execute implementation plans produced by the Improve skill through an explain, approve, implement, review, and commit workflow. Use when a repository contains self-contained Improve-generated plan files and the user wants to implement them sequentially, including when they explicitly batch-authorize remaining plans while preserving one coherent commit per accepted plan. Do not use to generate plans or when no Improve-generated plans exist.
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

Treat plan files as mutable execution records, not implementation files. Update the plan index, status, checklists, or execution notes when useful for accurately tracking progress, and follow any plan-specific instructions for maintaining those artifacts. Do not delete or broadly reformat plan artifacts unless the user explicitly requests it or repository instructions require it.

Keep the entire plans directory out of implementation commits. Plan artifacts may be modified or newly created during execution, but do not stage or commit them; leave them in the working tree for the user to review separately. If the user has told you to leave plan artifacts untouched, that instruction wins and completion must be reported outside the plans directory.

Record the active execution policy before starting: branch, plan order, approval mode, review mode, commit policy, protected paths, and validation commands. Carry explicit standing instructions (for example, “one commit per plan” or “leave `plans/` untracked”) across later plans until the user changes them.

## Select one plan

Choose the next incomplete plan from the index, respecting dependencies and documented order. By default, approval applies to one plan only.

If the plan is stale relative to the current code:

- explain which assumptions no longer hold;
- propose the smallest adjustment that preserves the plan's intent;
- request renewed approval when the adjustment materially changes scope or architecture.

If user feedback reveals that the plan itself does not represent the intended product behavior, distinguish the plan defect from an implementation defect. Stop implementation, report the exact intent-to-plan delta, and let the user revise the plan rather than improvising a different architecture. After plan artifacts are updated, reread the complete index and affected plans, reassess dependencies and validation, and require renewed approval for materially changed scope unless it is already covered by explicit authorization.

## Explain before editing

Inspect enough current code to verify the plan, then explain:

- **What:** the behavior, boundaries, and files expected to change;
- **Why:** the concrete problem and the architectural or product benefit;
- **How:** the implementation sequence, important design choices, migration concerns, and validation.

Call out risks, likely review points, and anything intentionally out of scope. Do not modify implementation files yet.

End this phase by waiting for explicit approval. Approval for one plan does not approve later plans unless the user unmistakably batch-authorizes a defined set of plans as described below.

## Honor explicit batch authorization

The user may explicitly replace the per-plan pauses, for example: “you have approval for every remaining plan; implement and verify all of them without stopping.” Do not infer this from “continue,” urgency, silence, or a general request to finish.

When the authorized set is unambiguous:

1. State the resulting execution policy once, briefly. Do not repeat every plan explanation if the user waived that step.
2. Still execute plans in dependency order, one coherent plan at a time. A batch is authorization to continue, not permission to blend scopes.
3. Verify each plan against current code before implementing it. Treat plan details as a design hypothesis; preserve the intent while following current repository architecture and instructions.
4. Run focused validation after each plan and inspect its isolated diff before moving on.
5. Preserve one commit per plan only when commits are explicitly authorized by the current request or a standing commit instruction. Batch approval alone does not authorize commits.
6. Do not pause between authorized plans unless a stop condition below applies.
7. After the last plan, run the combined repository gates. Later plans can invalidate earlier tests or assumptions even when every focused check passed.

If the user requests one review at the end, provide a combined review handoff with the per-plan commits, deviations, and validation results.

## Implement after approval

After explicit approval:

1. Implement only the approved plan and necessary supporting changes.
2. Follow repository conventions and use the narrowest coherent design.
3. Verify assumptions against current code instead of copying plan details mechanically. Existing architecture, vendored source-of-truth repositories, and explicit user feedback outrank a stale implementation prescription in a plan.
4. Update relevant documentation and JSDoc when behavior or boundaries changed.
5. Run focused checks during implementation, then the repository's appropriate formatting, lint, typecheck, test, build, and coverage gates. In a batch, defer only genuinely global gates until the end; do not defer focused checks that isolate plan regressions.
6. Do not commit.

Report the completed implementation, validation results, and any justified deviation from the plan. Wait for user review unless an explicit batch authorization waived the per-plan review pause.

## Iterate on review

For every review round:

1. Verify each finding against the current code. Locate it by the symbol or code it describes, not the line number it cites — review findings routinely reference a pre-edit revision, so the cited line is often shifted or wrong.
2. Fix findings that remain valid and add real value.
3. Skip stale, incorrect, duplicate, or low-value findings with a brief concrete reason. When a finding comes from a static analyzer or review bot, verify it against the repository's frameworks and conventions before accepting it — analyzers routinely raise false positives they cannot model (compiler-based memoization, framework base classes, idiomatic library APIs). Classify each explicitly as genuine, false-positive, or intentional, and leave analyzer suppression or issue-tracker triage to the user unless asked.
4. Keep changes within the approved plan.
5. If feedback changes core architecture, public contracts, or plan scope, explain the impact and wait for explicit approval before implementing it.
6. Re-run validation proportional to the changes.
7. Return the implementation for another review without committing, unless the user has explicitly authorized commit-after-validation for this plan or batch.

Repeat until the user explicitly says the implementation is accepted or asks to commit. Do not infer acceptance from silence or from a successful test run.

Review findings may arrive after the plan has been committed. Treat actionable post-commit feedback as a follow-up correction to that plan: use the same verify, fix, and validate loop, and create a separate focused commit only when the user asks or a standing commit policy applies. Do not amend the accepted commit unless the user explicitly requests it.

## Commit the accepted plan

When the user asks to commit, or has established a standing commit-after-validation policy:

1. Review the final diff and working tree.
2. Refresh affected documentation if it is stale.
3. Run the final relevant validation gates.
4. Stage explicit implementation paths belonging only to the accepted plan. Exclude unrelated changes, protected paths, and the entire plans directory.
5. Create one focused commit for the plan using the repository's commit style.
6. Confirm the commit identifier and remaining working-tree state. Verify that every plan artifact remains unstaged, whether modified or untracked.

After the commit, select the next plan and return to **Explain before editing**, unless it is already covered by explicit batch authorization.

## Handle validation without violating scope

- Lint, type, and test gates confirm a change is well-formed, not that it behaves correctly. For changes with a runtime or visual surface, confirm the actual behavior of the affected flow (or explicitly offer to) before reporting the fix as done — a passing build regularly coexists with a broken screen, and one finding's fix can regress a neighboring behavior.
- Prefer the repository's full gates when they can run without mutating protected or unrelated files.
- If a global formatter or checker would rewrite plan artifacts unintentionally, exclude the plans directory and run the narrowest equivalent check over changed implementation files. Never stage plan artifacts merely to make a gate pass, and report exactly which global gate could not be claimed.
- Never describe a scoped check as the full repository gate.
- Track which working-tree state each validation result covers. Reuse a still-current passing result instead of rerunning an expensive gate solely because the user asks to commit; rerun when relevant code or configuration changed afterward, or when the earlier check did not cover the final scope.
- At the end of a batch, run integration and end-to-end checks that cross plan boundaries. If a later accepted change intentionally invalidates an earlier test assumption, update that test within the later plan's scope and record the reason.
- After every commit, re-check status so user-owned changes cannot silently leak into the next plan.

## Stop conditions

Even under batch authorization, stop and ask when:

- a required change materially expands product behavior, public contracts, or architecture beyond the plans;
- plans conflict and there is no safe dependency-preserving interpretation;
- completion needs new authority, destructive action, credentials, or an external decision;
- unrelated user changes overlap the same code and cannot be preserved safely;
- validation exposes a pre-existing or cross-cutting failure whose fix is not reasonably attributable to an authorized plan.

Ordinary implementation difficulty, a stale line number, or a small intent-preserving deviation is not a reason to stop. Make progress, document the deviation, and continue.

## Preserve the gates

- A request to “continue” after acceptance authorizes selecting and explaining the next plan, not implementing it.
- A request to “commit and continue” authorizes committing the accepted plan and explaining the next one.
- A review request authorizes inspection and feedback handling, not unrelated cleanup.
- A terminal request such as “finish all plans” does not remove the per-plan approval and review gates unless the user explicitly changes this workflow. When they do, follow **Honor explicit batch authorization**.
- When blocked by missing authority, external state, or a material design choice, report the blocker and wait rather than broadening scope.
