---
id: CON-0007
status: Accepted
subject: Rx.Kql binding and dispatch
---

# CON-0007 — Rx.Kql binding and dispatch behaviour

`Microsoft.Rx.Kql` 3.5.3, as shipped:

- Binds against `IDictionary<string, object>`.
- `GetProperty` throws `KeyNotFoundException` on a missing key — absence is an
  exception, not a null.
- `ComparisonExpression` dispatches on the **CLR runtime type** of the value.
- `Project` and `Extend` return `ExpandoObject`, discarding whatever declared
  type information entered the operator.

## Consequences

- Rx.Kql is a type-*inspecting* engine embedded inside a type-*declaring*
  estate. That inversion is the reason an adapter exists rather than a direct
  reference: the adapter is where declared types are unwrapped on the way in and
  re-attached on the way out.
- Missing-key semantics must be reconciled deliberately. A typed null and an
  absent field are different facts, and Rx.Kql collapses one into an exception.
- Because `Project`/`Extend` return `ExpandoObject`, declared types do not
  survive a projection. Anything downstream that needs them must have them
  re-attached, not re-inferred.
