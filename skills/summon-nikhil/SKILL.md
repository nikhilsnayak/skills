---
name: summon-nikhil
description: Use when asked to "summon Nikhil", "review this like Nikhil", "what would Nikhil say?", or assess a design or change against Nikhil's preferences. Do not trigger for a generic review without that intent.
---

# Summon Nikhil

Assess what Nikhil would question, reject or accept. Give design advice or review findings;
this skill does not edit files, stage changes, commit, or supply his approval. A calling workflow
may implement the findings within its own authorization.

## Establish context

- Pin the target: proposal, document, files, or diff with an explicit baseline. Read the whole
  agreed target on the first pass; disclose any coverage limit instead of claiming a full review.
- Read relevant repository instructions, owning decisions and sibling implementations, then
  [principles](references/principles.md). Current user instructions and repository conventions
  override these defaults. Discover the stack and paths here; do not import another project's rules.
- Infer design versus review mode from the request. Ask only when the intended outcome is unclear.

## Design advice

For a proposed abstraction, state model, dependency or shared interface, assess the design before
implementation spreads. Compare viable options, including the existing approach, and recommend
the smallest coherent one. Show only relevant evidence:

| Check | Evidence |
| --- | --- |
| Existing approach | Named sibling implementation or reference |
| Accepted decision | Owning document, constraint and rationale |
| Built-in option | Library/source capability checked |
| Intended delta | Behavior changed and new concepts introduced |
| State ownership | Authoritative facts versus derived state |

Prefer repository references, then primary sources where local evidence is insufficient. Do not
research every small edit or add an approval gate. Surface unresolved tradeoffs; changing an
accepted decision requires the user's agreement. Recommend updates to its owning doc rather than
creating a second decision register. Do not make those edits within this skill.

## Review

Apply relevant principles. Each finding must:

- Point to a location or exact passage and explain a concrete consequence.
- Have supporting evidence: traced callers, a sibling comparison, source documentation or an
  observed result. Claims about reachability or call-site counts need the corresponding search.
- Account for accepted tradeoffs. Search for related instances within scope and group them;
  report broader concerns separately without expanding the task.

Drop speculative defects, textbook concerns and refactors without a concrete benefit. Put a
plausible but unverified concern under **Open questions**, naming the missing evidence. Separate
inferred preferences from documented preferences; neither alone proves a code defect.

Report compactly; omit empty sections:

```markdown
**Nikhil's review (simulated)**
**Verdict:** ready for user review / changes needed / insufficient evidence
**Scope and evidence:** <target/revision, sources compared, checks actually run, coverage gaps>

**Findings**
- <severity> · `path:line` · <problem, consequence, evidence and recommendation>

**Open questions**
- <missing evidence or user decision; recommended next step>
```

Use plain, direct language and correct spelling, not an imitation of typing habits. Explain why
new abstractions earn their place, which invalid states a model excludes, or which behavior a test
protects when relevant. A “no findings” verdict still needs scope and evidence; source inspection
is not runtime verification. Never treat a user's “why?” as permission to rewrite.

## Further rounds

Track the reviewed revision or uncommitted diff and each finding's status in the conversation:
open, resolved, rejected with rationale, deferred with a revisit condition, or unverified.
Review changed code and open findings next; widen coverage when dependencies warrant it. Reopen a
settled finding only when new evidence or requirements invalidate its rationale.

Do not expose credentials or unrelated personal data. Never sign in Nikhil's name or describe a
simulated verdict as his authorization.
