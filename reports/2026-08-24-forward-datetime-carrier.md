# `DeltaZulu.Forward`'s datetime carrier contradicts CON-0001

Date: 2026-08-24. Checked against `DeltaZulu.Forward` at `ab4a9f0`, which declares
`Version 0.3.1` — the version `DeltaZulu.Agent` pins.

The check was motivated by ordinary work, not suspicion: adding agent-health
telemetry to the Agent's Forward transport demonstrator meant putting two
timestamps into `ForwardLogRecord.Fields`. `CLAUDE.md` and `CON-0001` both say
the carrier for a KQL `datetime` is `System.DateTime` with `Kind = Utc`, never
`DateTimeOffset`. The question was simply which type to write.

## Headline: a caller cannot comply. Forward converts `DateTime` to `DateTimeOffset` unconditionally, and `FWD-CONTRACT-v1` tells it to.

This is not an implementation slip that a caller can route around by choosing the
right type, and not one that can be fixed in the library alone. The wire
specification names `DateTimeOffset` as the canonical form. Both the code and the
document say the same thing, and both contradict `CON-0001`.

Two distinct contradictions, verified separately.

| # | `CON-0001` says | Forward 0.3.1 does | Verdict |
|---|---|---|---|
| 1 | The carrier is never `DateTimeOffset`, because it carries an offset KQL cannot express | Normalizes every datetime field value **to** `DateTimeOffset`, and the offset survives encode and decode | **CONFIRMED** |
| 2 | `Kind = Unspecified` is not convertible and must be rejected, not assumed | Silently treats `Unspecified` as UTC | **CONFIRMED** |

## What was run

A batch was encoded through `ForwardLogBatchCodec.Encode` and decoded back, with
three field values: a `DateTime` of `Kind = Utc`, a `DateTimeOffset` at `+03:00`
naming the same instant, and a `DateTime` of `Kind = Unspecified`.

```
fromDateTimeUtc      -> DateTimeOffset   08/24/2026 12:00:00 +00:00
fromDateTimeOffset   -> DateTimeOffset   08/24/2026 15:00:00 +03:00
fromUnspecifiedKind  -> DateTimeOffset   08/24/2026 12:00:00 +00:00

on wire as ISO-8601 text: 2026-08-24T12:00:00.0000000+00:00
on wire as ISO-8601 text: 2026-08-24T15:00:00.0000000+03:00
```

Three things follow from those six lines.

**`DateTime` does not survive as `DateTime`.** Every input came back as
`DateTimeOffset`. A caller who obeys `CON-0001` and writes `System.DateTime`
has it widened by the library before it reaches the wire, so obedience is not
available at the call site.

**The offset survives.** `12:00:00+00:00` and `15:00:00+03:00` are the same
instant, and they remain distinguishable after a round trip. This is precisely
the information `CON-0001` says KQL cannot express. Per `CON-0008`, an Rx.Kql
comparison of those two values reads their local wall-clock components — 12:00
against 15:00 — and finds the same moment unequal.

**`Unspecified` was assumed, not rejected.** It decoded as `+00:00` with no
error. `CON-0001` calls this inventing a fact.

## Where it is written

The behaviour is specified, not incidental. In `FORWARD_PROTOCOL_SPECIFICATION.md`
(`DeltaZulu.Agent`, `docs/`):

- §10 lists `DateTimeOffset` as tag `4` of the ten permitted scalar types,
  encoded as "MessagePack string, ISO 8601 round-trip (`o`) format".
- The same section's normalization table reads: `DateTime` → `DateTimeOffset`,
  "`Local` kind converts with its offset; any other kind (`Utc`, `Unspecified`)
  is treated as UTC".

In the library, `ForwardValueNormalizer.Normalize` passes `DateTimeOffset`
through and sends `DateTime` to `NormalizeDateTime`, which returns a
`DateTimeOffset` in both branches. `ForwardObjectFormatter` then writes it with
`dto.ToString("o", CultureInfo.InvariantCulture)`.

`ForwardLogRecord.CreatedAt` is itself typed `DateTimeOffset`, so the model
carries the same type outside the field dictionary, where no normalizer change
would reach it.

`CON-0010` anticipated the encoding consequence exactly — "a `DateTimeOffset` on
the wire would have to be encoded as something other than the native timestamp
extension". Confirmed: these values travel as ISO-8601 text, not MessagePack's
timestamp extension type.

## Scope

Every `DeltaZulu.Forward` caller inherits this, not only the Agent. `DEC-0001`
governs the wire format and cites `CON-0010`; it does not mention the carrier.

Not checked, and deliberately left open:

- **Rx.Kql's comparison behaviour was not re-executed.** `CON-0008` is cited as
  the existing record, not re-verified here.
- **Consumers other than the Agent were not surveyed.** Whether any live
  detection path currently evaluates a Forward-sourced datetime through Rx.Kql —
  which is what would turn this from a contract defect into a wrong answer — is
  unanswered.
- **The Agent's own use is narrow.** The health telemetry that prompted the check
  renders to a terminal panel and reaches no query engine.

## What this report does not decide

The fix is a wire-contract change, not a code change: `FWD-CONTRACT-v1` §10 would
have to stop naming `DateTimeOffset` as tag 4, which is a versioned wire break
affecting every deployed peer. The alternatives — amend the contract, supersede
`CON-0001`, or record that Forward is knowingly exempt — are an estate choice
with rejected alternatives and a revisit trigger, so they belong in a Decision
rather than in this report.

Nothing was changed in `DeltaZulu.Forward` or in `FWD-CONTRACT-v1` on the
strength of this check.
