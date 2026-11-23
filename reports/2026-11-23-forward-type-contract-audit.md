# C03 — Forward type contract: source-level verification

**Date:** 2026-11-23. **Forward revision:** [fba0c5c](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/tree/fba0c5c63a1ee506373012ad458276ec807e542a).
**Platform revision:** [60d6588](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f).
No code was changed or executed; these are source observations.

| ID | Observed source behavior | Implication |
|---|---|---|
| FWD-01 | `ForwardValueNormalizer.NormalizeDateTime` converts `DateTime` to `DateTimeOffset`; `Unspecified` is treated as UTC | KQL field-value contract needs a versioned correction or explicit owner decision |
| FWD-02 | `ForwardObjectFormatter` tag 4 writes `DateTimeOffset` as round-trip text and reads with `ParseExact("o")` | Changing tag 4 requires reader/writer compatibility tests; transport metadata `CreatedAt` is a separate concern |
| FWD-03 | Tag 5 writes `TimeSpan.Ticks` and reads `new TimeSpan(ticks)` | **Forward's TimeSpan codec already uses canonical ticks**; do not conflate with Platform's microsecond-default registry |
| FWD-04 | Platform `LogicalDurationUnit` lacks Ticks and defaults to Microseconds; `RegistryProjectionTarget` still includes Proton | Registry migration and consumer audit required under DEC-0033 and CON-0014 |
| FWD-05 | `ForwardLogRecord` declares `CollectionTier`, `NullReasons`, `MatrixVersion` | Fields exist; propagation into Gold and retention across replay are unverified |

Required regression fixtures: UTC/local/Unspecified `DateTime`;
offset-bearing `DateTimeOffset`; old/new tag-4 payloads; positive,
negative and sub-microsecond `TimeSpan`; nested values; missing/null
reason and tier/version round trips; replay and Gold provenance linkage.
Verify unsupported types reject rather than silently coerce.

**Owner choice still open:** UTC `DateTime` field contract migration and
version compatibility. This audit does not authorize a wire change.
