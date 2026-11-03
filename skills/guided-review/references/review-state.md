# Review state and delivery

Read only the section needed. Link existing artifacts instead of duplicating them. Keep credentials
and private payloads out. Adapt output to repository conventions; omit irrelevant fields.

## Checkpoint

Refresh at interruption, handoff, commit or mode-change boundaries:

| Field | Record |
| --- | --- |
| Goal | Behavior change and reason |
| Checkout | Branch, base revision, worktree and issue where applicable |
| Review | Current unit, approved scope and remaining units |
| Decisions | Open questions and links to accepted decisions with rationale |
| Validation | Command/scenario, outcome, revision and relevant uncommitted state |
| Authority | Review mode, commit policy and next authorized action |

On resume, compare this with actual Git state and surviving validation artifacts; another agent may
have completed work. A revision alone does not identify tested uncommitted changes. Reuse checks
only when relevant inputs are unchanged. Briefly state the goal, current unit and next step.
Reconcile completed progress rather than retaining a historical diary.

## Verification and coverage

For a bug fix, establish the reported symptom and affected variant before assigning a cause.
Use the repository's diagnosis workflow or an available diagnosis skill when useful.

```text
Symptom and affected variant:
Environment and revision:
Reproduction:
Before → after:
Provenance: introduced here / pre-existing / unknown
User verification steps:
Remaining uncertainty:
```

A regression claim needs baseline evidence. Mark unexecuted scenarios as unverified; unrelated
passing checks do not prove a fix. Preserve reproductions according to the session's test policy.

For broad audits or changes spanning surfaces, show coverage:

| Surface / behavior | Evidence or scenario | Result | Remaining gap |
| --- | --- | --- | --- |
| Reported failure | Reproduction and baseline | Before/after outcome | Uncertainty |
| Related surface | Source trace or runtime check | Inspected / exercised / unchecked | Next useful check |

Choose relevant lifecycle boundaries and sibling surfaces, not every possible combination. Further
passes target gaps, changed code or new evidence. Broad inspection is not end-to-end verification;
neither proves universal regression freedom.

## RCA or issue handoff

When requested, use the repository's issue/PR format with these facts:

| Field | Content |
| --- | --- |
| Impact and trigger | User-visible problem and exact conditions |
| Cause | Proven mechanism; distinguish inference |
| Fix | Behavior changed |
| Verification | Reproduction and observed result |
| Remaining work | Concrete gaps or prevention work, if any |

Use plain language. Omit abandoned theories and unrelated chronology. Do not imply checks ran or a
fix was deployed without evidence. Reuse the verification packet rather than restating it.

## Cross-agent brief

For a requested transfer, provide the task, constraints, source paths, excluded work, expected
artifact, unresolved decisions and return location. Link existing evidence and accepted decisions.
State investigation versus implementation scope and completed work. The brief grants no additional
permissions or authority to message external services.
