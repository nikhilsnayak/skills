# Principles

Nikhil's recurring review preferences. These are defaults, not bans: a finding needs a concrete
correctness, clarity, modelling or maintenance consequence. Current user instructions and repository
conventions take precedence. Questions below illustrate his reasoning, not mandatory output.

## Review lenses

| Lens | What earns a finding | Characteristic question |
| --- | --- | --- |
| Necessity | Forwarding-only wrappers, speculative options, unused surface, dependencies or unrelated refactors without a current responsibility or known roadmap need | “Is this really required? Can existing features do it?” |
| Naming | Ambiguous terms, duplicate segments, synonyms for established domain terms, or names that conflict with known planned uses | “What does this mean? Is it consistent elsewhere?” |
| Modelling | Invalid combinations, duplicated facts kept in sync, unclear absence, or casts without a proven invariant | “Can this state exist? Won't these get out of sync?” |
| Built-ins and patterns | Bespoke mechanisms where platform/library capabilities or established sibling patterns already fit | “Did we invent this? What does the source recommend?” |
| Readability | Clever types, nested control flow, incidental formatting churn, or explanations compensating for avoidable complexity | “Can this read top to bottom?” |
| Proof and root cause | Symptom patches, speculative guards, unverified claims, or temporary fixes that leave the actual cause intact | “Can you reproduce it? Which change introduced it, and why?” |
| Boundaries and locality | Related logic scattered across modules, leaking dependencies, test-only production code, or two owners of one rule | “Does this belong here? Is the abstraction doing its job?” |
| Roadmap fit | A design that blocks a known next use, or implementation of unplanned features | “How does this look with the next planned feature?” |
| Correctness | Reachable failures involving empty/missing inputs, retries, concurrency, dates, money, authorization or uncertain outcomes | “What happens when this fails or two requests race?” |
| Tests | Tautological or library-only assertions, excessive mocking, or missing coverage of consequential behavior | “What real behavior does this test protect?” |
| Communication | Vague diagnostics, misleading UI claims, redundant documentation or explanations requiring unexplained internals | “Can the reader understand what happened and what to do?” |

## Applying the lenses

- An abstraction may earn its place through an accepted roadmap even with one implementation.
  Design for that roadmap without implementing features early.
- Model alternatives explicitly using the language's idioms. Store each fact once, derive the rest,
  and enforce invariants at their owning boundary. Booleans suit genuinely binary facts; casts need
  an invariant the type system cannot express, not convenience.
- Naming examples: `order.total.total` repeats a concept; an `EmailNotifier` may be too narrow for
  an accepted multi-channel design. Judge against actual domain vocabulary and planned use.
- An “idiomatic” claim needs a named sibling, library source or reference implementation.
  Repetition can be clearer than an abstraction with no independent responsibility.
- Comments explain non-obvious reasons concisely, following local convention. Length alone is not
  a defect; investigate whether a complicated explanation exposes a simpler design.
- Probe relevant failure paths and asymmetries between callers, not every hypothetical edge case.
  Distinguish source reasoning, reproduced behavior and unknowns.
- Prefer tests of meaningful behavior with appropriate seams. Match the repository's mocking and
  test policy; do not demand new tests merely to repeat a schema or framework guarantee.
- Diagnostics need useful, safe context without routine noise. UI copy should be accurate and
  direct. Docs should serve their audience and purpose; preserve required rationale and history.
  Explanations should use plain language and examples when they clarify the point.

## Stack-specific preferences

Apply only to targets using the named technology, subject to repository conventions.

**TypeScript:** prefer string-literal/discriminated unions over enums and independent optional-field
combinations; prefer `interface … extends` where appropriate. Consider one object argument for more
than two parameters or multiple parameters of the same type.

**React:** derive values rather than synchronizing copies with effects. Use effects for genuine
external synchronization. Prefer discriminated state/props where alternatives differ; consider a
reducer when transitions form a coherent state model.

## Context rules

Discover these from the current repository and session rather than inferring a universal policy:

- Test ownership, required gates and whether permanent tests are wanted.
- Compatibility guarantees and release status; being unreleased alone does not waive a contract.
- Comments, documentation, accessibility and supported environments.
- Interactive versus delegated review, and separate authority to implement or commit.

## How he decides

Understanding is part of acceptance: working code the reviewer cannot follow is not done.
Scrutiny focuses on naming, structure and necessity. When feedback is vague (“feels off”), diagnose
the concern and offer a few distinct options instead of repeatedly tweaking the same approach.
Keep ambitious proposals easy to compare and discard. Change recommendations when evidence changes;
accepted decisions are revisable with a reason. Before acceptance, check completeness and remaining
loopholes without inventing new scope.
