---
id: CON-0003
status: Accepted
subject: ScalarTypes.All membership
---

# CON-0003 — `ScalarTypes.All` membership differs between 9.2.0 and 12.4.1

**The membership is not stable across the version span.** This constraint was
drafted asserting twelve members including `Type` and `Null`; verification
refuted that as a single-version truth.

| | 9.2.0 | 12.4.1 |
|---|---|---|
| Count | **11** | **12** |
| Members | bool, datetime, decimal, dynamic, guid, int, long, real, string, timespan, type | the same, **plus `null`** |
| `type` present | yes | yes |
| `null` present | **no** | yes |
| `unknown` present | no | no |
| `ScalarTypes.Null` static member | **does not exist** | exists |
| `ScalarTypes.Unknown` static member | exists, excluded from `All` | exists, excluded from `All` |

`unknown` is an inference artefact (`ScalarFlags.All`), not a type a value can
have. It is excluded from `All` in both versions and must never be surfaced.

## Consequences

- Any code filtering `All` down to the estate's surfaced set must filter **by
  name** and tolerate `null` being absent. Referencing `ScalarTypes.Null` as a
  compile-time symbol does not build against 9.2.0.
- Filtering out `type` and `null` by name yields the identical ten-member set on
  both versions. The divergence is therefore absorbable, but only by code that
  never assumes the member exists.

## Verified

`reports/2026-08-15-kusto-language-preflight.md`, items 1 and 3.
