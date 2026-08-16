---
id: CON-0017
status: Accepted
subject: Completeness evidence
---

# CON-0017 — Volume is not loss; completeness requires evidence from outside the pipeline

A fall in event rate is equally consistent with three causes: data loss, a
genuine fall in source activity, and an intentional filter change. **Nothing
internal to the pipeline distinguishes them**, because all three look identical
from inside — fewer records arrive, and every internal counter agrees.

## Consequences

- Internal conservation accounting (`in = out + dropped + failed + buffered +
  residual`) proves that the pipeline did not lose what it received. It cannot
  prove that it received what was produced. Those are different claims and only
  the second is completeness.
- Establishing completeness requires evidence originating **outside** the
  pipeline: source-side sequence numbers, producer counters, or injected
  canaries with known emission rates.
- Any figure presented as "completeness" that derives only from pipeline
  telemetry is measuring conservation and mislabelling it.
