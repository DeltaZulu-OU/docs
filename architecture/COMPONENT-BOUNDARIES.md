# Component boundaries and qualification

This register consolidates surviving component requirements without
replacing detailed library API documentation or accepting new Decisions.

## Parse and LogCluster

Parse owns structural extraction of plaintext through the liblognorm v2
PDAG model, not semantic normalization. Qualify priority, backtracking,
tie behavior, malformed input and typed extraction against pinned upstream
fixtures and deliberate documented divergences. Unspecified upstream ties
are not evidence of a portable ordering guarantee. A passing corpus does
not establish coverage of every parser combination.

LogCluster owns deterministic candidate mining and reviewable parser
suggestions, not automatic production rule deployment or detection.
Preserve exact support counting and distinguish candidate identity,
gap bounds, merge semantics, ranking and rule rendering. Do not claim
full C/Perl parity from a limited fixture. DEC-0035 remains Proposed;
qualify merge behavior and bounded execution under C15. The Suggester
consumes Parse's parser catalogue; verify packed dependency lineage
and generated rules against the actual parser. Human review remains
the promotion boundary.

## LocalStream and DurableBuffer

DEC-0033 governs the node-local stream substrate. LocalStream retains
payload-opaque records independently of consumer completion, with
partition-local order and bounded replay. Query operators and durable
state adapters are separate from core and receive bound operations.
See [NRT pipeline](NRT-PIPELINE.md) and
[detection result contract](DETECTION-RESULT-CONTRACT.md) for recovery,
temporal, resource and persistence qualification. A historical processor
design is not evidence of implementation.

DurableBuffer is an optional single-buffer edge queue, not a required
LocalStream dependency or a broadcast stream. Its documented durability
boundary is sealed chunks; open in-memory records are not thereby durable.
Application code owns forwarding, retry decisions and terminal outcomes.
Verify sealing, recovery, quarantine, backpressure and outcome transitions
before relying on the queue for a positive delivery acknowledgement.
A reactive facade does not change the underlying durability contract.
Historical wrapper acceptance criteria do not authorize a new pub-sub
implementation or change LocalStream retention.

## Qualification boundary

C03/C10/C12 govern typed extraction and Agent integration; C05/C07 govern
delivery and state recovery; C14 governs reproducible builds, package
lineage and compatibility; C15 governs mining correctness. Local
development and CLI references remain useful at pinned revisions.
See the [component reconciliation report](../reports/2026-11-27-component-documentation-reconciliation.md) for scope and
limitations.
