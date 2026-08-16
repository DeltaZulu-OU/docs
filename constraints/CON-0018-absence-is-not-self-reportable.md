---
id: CON-0018
status: Accepted
subject: Absence detection
---

# CON-0018 — A component cannot report its own absence

A metric emitted by a component is silent exactly when that component stops.
`last_record_age` reported by an agent goes quiet at the precise moment it
becomes interesting, and an outage in the path that carries metrics suppresses
the evidence of that outage.

## Consequences

- Every *positive* signal is safe on a shared telemetry path. Every *absence*
  signal is not, and the two must be designed differently.
- Absence must be computed at the **receiver**, against an expected-source
  inventory the sender does not control. This requires nothing from the silent
  party, which is the point.
- A minimal liveness heartbeat must travel a path independent of the data plane.
  The control-plane channel already exists and already survives a transport
  outage.
- This does not argue for a second metrics pipeline. It argues for three narrow
  properties — receiver-side inventory, a separable heartbeat, and an external
  canary path — which preserve the shared-path design's advantages without its
  blind spot.

Without these, a total outage looks like a quiet night.
