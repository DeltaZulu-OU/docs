# Constraints

External facts and historical records retained under their original identifiers. Original records are immutable; the authority classification below distinguishes external facts from dated observations and internal contracts. Accepted Decisions and current specifications govern internal choices.

Each constraint states what is true, how it was verified, and what it forbids or
forces. Constraints do not choose; Decisions choose, and cite these.

| ID | Subject |
|---|---|
| CON-0001 | KQL `datetime` is UTC-only |
| CON-0002 | Kusto.Language contains no CLR type mapping |
| CON-0003 | `ScalarTypes.All` membership differs between 9.2.0 and 12.4.1 |
| CON-0004 | Widening lattice per `IsWiderThan` |
| CON-0005 | Alias tables, both versions |
| CON-0006 | Rx.Kql pins 9.2.0; Platform runs 12.4.1; DeltaZulu.Kql must span both |
| CON-0007 | Rx.Kql binding and dispatch behaviour |
| CON-0008 | Rx.Kql compares `DateTimeOffset` via local wall clock |
| CON-0009 | `System.Decimal` is narrower than KQL `decimal` |
| CON-0010 | MessagePack timestamp extension is UTC, no offset |
| CON-0011 | `MessagePackWriter`/`Reader` are `ref struct` |
| CON-0012 | liblognorm's corpus is not committed |
| CON-0013 | LocalStream carries payload bytes verbatim |
| CON-0014 | Wire tag 5 is ticks; the registry defaults to microseconds |
| CON-0015 | `KqlNullReason` is closed and specified |
| CON-0016 | The collector has no repository |
| CON-0017 | Volume is not loss; completeness needs external evidence |
| CON-0018 | A component cannot report its own absence |
| CON-0019 | Transport class bounds what completeness can mean |
| CON-0020 | An integrity digest attests only if computed at write time |
| CON-0021 | `Kusto.Language.Syntax.SyntaxKind` member values differ across 9.2.0 and 12.4.1 |

**Historical-state caution (2026-11-23):** `CON-0016` was an August snapshot,
not an immutable external fact. `DEC-0022` has since established that the
collector belongs in `DeltaZulu.Platform`, and the Platform repo contains an
`Ingestion` project; existence of the required standalone executable remains
unverified. Do not treat `CON-0016`'s "no project or directory" wording as
current implementation evidence. This index clarification does not silently
reclassify or supersede the immutable Constraint; the approved authority classification below resolves that taxonomy issue.

## Current interpretation and correction register (2026-11-25)

The immutable records above preserve their original wording; the following qualifications govern how readers use the evidence. No original Constraint has been renumbered or edited. The owner approved the following index-level classification on 2026-11-27.

| Record | Qualification / work item |
|---|---|
| CON-0001 | KQL UTC semantics are distinct from the chosen UTC `DateTime` carrier. `ToUniversalTime()` may resolve ambiguity, accept invalid wall times or clamp to representable limits; unconditional losslessness is false ([Microsoft API](https://learn.microsoft.com/en-us/dotnet/api/system.datetime.touniversaltime)). C03 must verify known zone/offset, unique instant, range, and round-trip policy; reject rather than silently invent an instant. |
| CON-0006, CON-0012–CON-0016 | Version pins, corpus state, payload opacity, duration units, enumeration ownership and collector existence mix dated observations and internal policies with external facts. Preserve originals; use the approved classification below. |
| CON-0019 | ACK on durable append is a target pending C05 verification, not a proved end-to-end guarantee. UDP has no delivery guarantee but scoped measurement with independent ground truth is possible. C04 tracks the reporting-policy choice under DEC-0023. |
| CON-0020 | A digest or signed manifest is only as trustworthy as its independently protected reference and verification history. See DEC-0024 (Proposed) for deletion, rollback, key custody and restore-sampling questions. C04 remains open. |


## Approved authority classification

| Record | Current authority | Interpretation |
|---|---|---|
| CON-0006 | Compatibility requirement | Supported Kusto.Language span; verify current consumer compatibility under DEC-0032 and CON-0021. |
| CON-0012 | Historical observation | Corpus availability at inspection time; recheck upstream before relying on it. |
| CON-0013 | Architectural contract | Payload opacity is governed by DEC-0033, not an immutable external fact. |
| CON-0014 | Contract discrepancy | Historical ticks/microseconds mismatch; resolve under DEC-0003 and DEC-0038, not by assuming either implementation is authoritative. |
| CON-0015 | Internal type contract | Current Kql type declarations and DEC-0032 govern ownership; historical enumeration wording is not an external fact. |
| CON-0016 | Superseded historical observation | DEC-0022 establishes collector placement; verify implementation separately. |

The remaining records retain their existing interpretation, including the qualifications above. This classification changes neither accepted architectural requirements nor historical evidence.
