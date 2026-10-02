# Principles

Nikhil's recurring judgements across several projects. Each lens gives the rule, what makes a
finding and what he typically asks. Quotes are his words, spelling corrected.

Every rule is a strong default, not a ban: report a breach only when it causes a concrete
correctness, clarity, modelling or maintenance problem in the target.

## 1. Necessity

Every module, layer, field, variant, helper, flag and dependency earns its place through a concrete
responsibility, a current need or a known roadmap item.

- **Finding:** a wrapper that only forwards, a speculative option, exported surface nothing uses,
  an unused dependency or asset, a refactor nobody asked for.
- **Not a finding:** an abstraction the known roadmap needs, even with one implementation ("follow
  the registry pattern now itself… even though we only have one adapter").
- **Asks:** "is this refactor really required?" · "do we have any real use cases for it? can't we
  achieve that with existing features?"

## 2. Naming

Names are unambiguous, use the project's established vocabulary and stay right once the known
roadmap lands.

- **Finding:** repeated segments (`order.total.total`, `price.amount.amount`, `error.error`), a
  term that already means something else in the domain, a near-synonym of an established term, a
  name that will clash with a planned feature (`EmailNotifier` when SMS notifications are planned).
- **Asks:** "send is ambiguous" · "nothing should be ambiguous" · "keep the convention consistent
  across the project, there should be 0 violations"

## 3. Modelling

The model cannot represent invalid states, and keeps states and moving parts minimal.

- **Defaults:** string-literal and discriminated unions over boolean and optional-field
  combinations; no TS `enum`; each fact stored once and the rest derived by one shared function;
  constraints in the schema or type, not at every call site; `interface … extends` over
  intersections; one object argument past two parameters or two of the same type.
- **Escape hatches** are fine when justified: a boolean for a genuinely two-valued fact, a cast
  where the type system cannot express a proven invariant ("keep booleans only as an escape
  hatch").
- **Finding:** a combination that admits an impossible state; two copies kept in sync by a check
  (then audit the model for the whole category); an unexplained cast or `as unknown as`.
- **Asks:** "won't this get out of sync?" · "what does `undefined` mean here?" · "our data model
  should be in such a way that we shouldn't be able to represent invalid state in the first place"

## 4. Built-ins and existing patterns

Use the platform, the framework's built-in module or the codebase's existing mechanism before
anything bespoke. Extend an existing pattern in the same shape, following the sibling module.

- **Finding:** a hand-rolled version of a library feature, a new concept for a solved problem,
  code shaped differently from its siblings.
- **Evidence:** "idiomatic" needs the library's source or a reference implementation, not an
  impression.
- **Asks:** "is this a well-known approach or did we invent it?" · "doesn't feel idiomatic" · "how
  do other well-known projects handle this?"

## 5. Readability

Code reads top to bottom and looks pleasant, not merely works.

- **Finding:** type gymnastics, nested ternaries, IIFEs, clever currying; code that needs a
  paragraph of comment; types that hurt inference or inflate type instantiations; restyling or
  reformatting unrelated code in the diff.
- Comments are for the genuinely non-obvious, one line.
- **Asks:** "not happy with this type gymnastics" · "if it needs a paragraph of comments to
  understand what's happening then the implementation is flawed"

## 6. Root cause and proof

Fix the cause, not the symptom, and prove a claim before making it.

- **Finding:** a hack, stopgap, half-built feature or patch a later change will overwrite; a
  speculative guard for a problem nobody reproduced; a claim without evidence (real data, upstream
  documentation or source, a reproduction, the traced call graph); "checks pass" that never ran.
- **Asks:** "did you check the prod data?" · "proof for your claim or a reliable way to reproduce
  first" · "which commit regressed this, and what was it trying to fix?" · "don't fall for quick
  hacks"

## 7. Boundaries and locality

Code lives with its concept, and layers do not leak.

- **Finding:** related code scattered across modules; a dependency escaping its abstraction (a
  service requirement in every method, DOM APIs in a platform-agnostic package, test-only code in
  a production bundle); two sources of truth for one rule or definition.
- **Asks:** "I like locality, all related code stays in one place" · "won't this leak into the
  methods and violate the purpose of using layers?"

## 8. Roadmap fit

Design for the known roadmap without building it.

- **Finding:** a shape that breaks when the next planned feature arrives, or work for a feature
  nobody planned.
- **Asks:** "now assume the next planned feature is also present, how does this look?" (a second
  client app on the same API, a second payment method in the checkout)

## 9. Correctness

- **Probe:** empty, zero, missing, repeated and concurrent inputs; asymmetry between paths ("why
  only on the mutation path?"); money, time zones and dates; security and abuse; failure paths
  that lose data or leave work uncertain; what the user sees when it fails.
- **Asks:** "what if two requests race?" · "is there a security or abuse risk? how do typical
  applications handle it?"

## 10. Tests

Tests prove meaningful behaviour, and validation stays proportional.

- **Finding:** a tautological test, a test that only confirms library behaviour, excessive
  mocking, a missing test for the failure or edge path that matters.
- Run what the change affects first; keep full and expensive suites for the final check.

## 11. Writing for the reader

- **Observability:** every failure diagnosable from the logs alone; no happy-path noise.
- **UI copy:** facts only, technically true; no reassurance or pleasantries.
- **Docs:** concise, written for their audience, describing the current state, not history.
- **Explanations:** concise and plain, with an example, assuming no knowledge of internals.

## React

When the target is React:

- `useEffect` is a last resort; derive state instead of synchronising copies.
- Unions over boolean and optional-prop combinations in props and state.
- Logic that reads as a pure transition function becomes `useReducer`.

## Context rules

These vary by project; the repository's conventions and the session's agreements decide:

- **Tests:** delegated to the agent in some projects, not written at all in others.
- **Backward compatibility:** none before launch or release; strict once a feature is released.
- **Comments and JSDoc:** match the surrounding file's convention.
- **Accessibility and browser support:** scoped per surface.
- **Working mode:** small reviewed slices, or an authorised end-to-end loop with reviewer agents.

## How he decides

- Understanding is part of acceptance: working code he cannot follow is not done.
- He often accepts a well-argued recommendation quickly; his scrutiny lands on naming, structure
  and necessity.
- Vague verdicts ("feels off", "ugly") usually come before the reason: diagnose them and offer two
  or three distinct options rather than tweaking the current one.
- He asks for ambitious ideas and keeps few; keep brainstorms short and easy to drop.
- He changes his mind when shown evidence, and expects the same.
- Before accepting: "is it complete? any loopholes left?"
