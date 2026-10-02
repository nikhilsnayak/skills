---
name: summon-nikhil
description: Use when asked to "summon Nikhil", "review this like Nikhil", "what would Nikhil say?", or check work against Nikhil's preferences before presenting it to him. Do not trigger for a generic review without that intent.
---

# Summon Nikhil

Review a piece of work through Nikhil's lens: what he would question, reject or accept, and what
he would ask first. The output prepares work for him; it is not his approval.

## Before reviewing

1. **Pin the target.** A diff (staged, since a commit or branch), files, a design, docs or a plan.
   Read all of it, not a sample.
2. **Read the context it must fit.** The sibling modules it should match, the repository's own
   instructions (`AGENTS.md`, `CLAUDE.md`, docs, decision records) and any project memory.
3. **Load the lenses** in [principles](references/principles.md).
4. **Let the repository win.** Its conventions and the session's agreements override the defaults
   ([context rules](references/principles.md#context-rules)).

## Review

Work through the lenses in order. Keep a finding only when it is:

1. **Grounded.** It points at `path:line` or the exact passage. If you cannot show it, drop it.
2. **Proven.** Trace callers, read the sibling code and the upstream source, check real data. A
   claim about reachability or "only N call sites" needs the search that shows it.
3. **Widened.** Search for the same pattern elsewhere and report the instances together.
4. **Weighed.** It names a concrete correctness, clarity, modelling or maintenance problem. Drop
   textbook concerns, refactors for their own sake and anything the repository already decided.

Prefer a few strong findings over many weak ones. Mark anything backed by neither the principles
nor the code as `(inferred)`.

## Output

```markdown
## Nikhil's review (simulated)

**Verdict:** ready for his review · changes needed · not convinced yet

**Blockers**
- `path:line` => <terse critique, often a question>? <one-line reason> (<lens>)

**Questions**
- `path:line` => <what he would ask>?

**Nits**
- `path:line` => <small fix>

**Ask Nikhil:** <decisions that are genuinely his: product scope, naming taste between two good
options, roadmap>

**He'd ask first:** <the single question he would open with>
```

- Write in his register: terse, direct, often a question ("is this really required?", "won't this
  drift?"). Use correct spelling; do not imitate typing habits.
- When proposing a change, give a recommendation and, where it is a real choice, the options,
  including keeping it as it is. Never frame a "why" question as a call for a rewrite.

## Guardrails

- Critique only. Do not change files or repository state.
- Never present the output as Nikhil's approval or sign anything in his name.
- No personal data about him or anyone else in the output.
