# Constraints

Facts about the world the estate does not control. Immutable: a constraint that
turns out to be false is superseded by a new one, never edited in place.

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
