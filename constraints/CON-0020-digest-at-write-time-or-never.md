---
id: CON-0020
status: Accepted
subject: Evidence integrity
---

# CON-0020 — An integrity digest attests only if computed at write time

A digest computed when a payload is written attests to what was written. A digest
computed later attests only to what is there now — which is precisely the
question it was supposed to answer.

## Consequences

- Bronze payload digests must be computed at the write point (M12) or the
  evidence is permanently unattestable. This puts them in the same irreversible
  class as record-carried provenance.
- Parquet's per-page CRCs detect **corruption**, not **modification**. They are
  not an integrity control against a party who can rewrite a file, and the
  DuckLake catalogue database is itself unprotected.
- A per-record digest cannot detect **deletion**, because a removed record leaves
  no digest behind. Detecting deletion needs a signed per-partition manifest
  covering the file list and their digests.
- Retention duration is a configuration setting, not a control. Only a scheduled
  restore test — against the **oldest** retained partition, not the newest —
  demonstrates that the retention claim is true.
