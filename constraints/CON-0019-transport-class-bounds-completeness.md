---
id: CON-0019
status: Accepted
subject: Transport delivery guarantees
---

# CON-0019 — Transport class bounds what a completeness figure can mean

Delivery guarantees differ per transport, and a completeness figure inherits the
weakest guarantee on its path. Averaging completeness across transport classes
produces a number that means nothing.

| Transport class | Delivery property |
|---|---|
| Buffered agent over Forward | At-least-once, ACK on durable append; bounded by `agent.output` retention |
| File and journal tail | At-least-once, bounded by offset persistence |
| Windows channel and ETW | Provider-side buffering with its own drop counters, which precede the agent |
| Syslog TCP or RELP | Ordered, but no acknowledgement reaches the original producer |
| **Syslog UDP** | **No delivery guarantee at all** |
| API polling | Provider-controlled availability, pagination and rate limits |

## Consequences

- Completeness is reported **per transport class** before it is reported in
  aggregate, or not reported at all.
- **A UDP source has no obtainable completeness figure.** It must be rendered as
  *unmeasurable*, not as an assumed rate. Any dashboard showing a percentage for
  a UDP source is presenting a fabricated number. Agent Phase 3 includes a
  `syslog-udp` adapter, so this is a live case and not a hypothetical.
- For Windows channels and ETW, provider drops must be **read from the provider**
  rather than inferred, because they happen before the agent sees anything.
- The proportion of sources on unmeasurable transports should itself be a
  reported figure, so the limit of the completeness claim is visible rather than
  a footnote.
