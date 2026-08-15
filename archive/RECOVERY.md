# Recovery

What is worth pulling back out of the archive, and what should be distrusted
before it is reused.

This is the archive's highest-value content. An archived decision is cheap to
read and expensive to re-derive; a *wrong* archived decision that still reads as
authoritative is more expensive still, because it gets cited.

---

## Part 1 — Recoverable rejections

Ideas that were considered and declined. Each was declined for stated reasons,
and in each case the reasons are conditional on something that could change. They
are recorded here so that reopening one is a decision rather than a rediscovery.

### Avro as the agent-to-collector wire format

**Rejected by** Agent ADR 0014, which supersedes the wire-serialisation choice in
ADR 0010. ADR 0010 had *chosen* Avro; 0014 reversed it in favour of MessagePack.

**Recoverable if** the wire needs a schema registry with out-of-band schema
distribution — the property Avro has and MessagePack does not. Note that ADR
0010's original rejection of MessagePack ("self-describing tags do not provide a
catalog authority, sink DDL, or query-translation contract") was written before
the envelope design existed; see Part 2.

### Arrow as the collector's internal representation

**Rejected by** Agent ADR 0015, which supersedes the internal-representation
choice in ADR 0010.

**Recoverable if** the collector becomes columnar-analytical in its own right
rather than a row-at-a-time landing path. Arrow's cost was a conversion boundary
that bought nothing at the row rates in question; that arithmetic changes with
the access pattern, not with taste.

### The semantic view layer

**Not an ADR-5 — there is no Parse ADR 0005.** The semantic view layer is
deferred future work reserved in **Parse ADR-1** (which reserves the word
"normalization" exclusively for it) and narrowed in **Parse ADR-3** (*the
semantic view layer does not do schema mapping*).

Recording the correct citation matters here: a search for "ADR-5" in Parse finds
nothing and has never found anything, and the layer is easy to conclude was
deleted when in fact it was never built.

**Recoverable if** consumers need field-name normalisation across sources. ADR-3
already fixes its boundary: whatever it does, it does not do schema mapping.

### DeltaZulu.Normalize

Deleted at `bd4a734` (2026-08-12, *"Removed references to deleted projects"*),
taking three public types with it: `NormalizedField`, `NormalizedRecord`,
`RecordNormalizer`, plus `DeltaZulu.Normalize.Tests`. Recoverable from history.
This deletion is the one already known; see Part 3 for the others.

---

## Part 2 — Decisions made on rationale that outlived its conditions

**These four are why the Revisit-trigger section is mandatory on every Decision.**

Each was correctly reasoned when written. Each then kept its `Accepted` status
after the thing it depended on stopped being true, because nothing in the
document said what to watch, and so nobody watched.

### 1. Agent ADR 0012's factual error about the Proton REST API, propagating into ADR 0016

ADR 0012 rejected the REST ingest API on the grounds that it is *"documented as a
Timeplus Enterprise feature"* and that request-per-batch HTTP semantics fit the
near-real-time path poorly. It chose a Kafka-API-compatible intermediate instead.

ADR 0016 then superseded 0012 *in full*, adopting a bespoke native Proton sink —
carrying 0012's framing forward rather than re-examining it.

**The estate now ships `ProtonHttpExecutor`** in
`DeltaZulu.Platform.Data.Proton`, alongside `ProtonSchemaApplier` and
`ProtonDetectionDeployer`. HTTP-based Proton interaction is in production code
while the ADR that rejected it, and the ADR that superseded that one, both remain
`Accepted`. The premise and the shipped reality disagree, and the documents do
not know it.

**Retire ADR 0016's bespoke-native-sink premise** against the shipped code before
either document is cited again.

### 2. ADR 0010's MessagePack rejection, argued against pre-envelope requirements

ADR 0010 rejected MessagePack because *"self-describing tags do not provide a
catalog authority, sink DDL, or query-translation contract."*

True of bare MessagePack. Not true of MessagePack inside the envelope the estate
subsequently designed, where catalog authority lives in the envelope rather than
in the encoding. ADR 0014 reached the right answer later — but by reversing the
decision, not by noticing that the rejection had been evaluated against
requirements that no longer described the system.

### 3. ADR 0010's Arrow decision, recorded as final when it was an alternative

Arrow was recorded in 0010 as the settled internal representation. It was in
substance one option among several, and was superseded by ADR 0015.

The failure here is one of register rather than reasoning: a document that states
a tentative choice in settled language is read as settled, and the tentativeness
is unrecoverable from the text.

### 4. Platform ADR 0014, reversing Forward alignment the day the Agent ratified it

Platform ADR 0014 (*HTTP ingestion and type-fidelity registry*) reverses
alignment work on the same day the Agent ratified its own ADR 0014. Two
repositories, two `Accepted` decisions, the same number, opposite directions, one
day apart — and each internally consistent.

This is the case that most directly justifies both global numbering and the
`repos:` front-matter field. Neither document was wrong on its own terms. Nothing
existed that could see both.

---

## Part 3 — Deleted projects and public types

`git log --diff-filter=D` across all seven repositories. Deletions of whole
projects are listed; the source-file counts indicate where to look further.

### Deleted projects

| Repo | Commit | Date | Project |
|---|---|---|---|
| Parse | `bd4a734` | 2026-08-12 | `DeltaZulu.Normalize`, `DeltaZulu.Normalize.Tests` |
| Parse | `825ae3a` | 2026-07-14 | `src/tools/LogCluster.Cli` (extracted to its own repo) |
| Platform | `a0ccffc` | 2026-08-13 | `DeltaZulu.Blazor.Interop` (folded into Web) |
| Platform | `c72efeb` | 2026-06-11 | `DeltaZulu.Blazor.Components`, `DeltaZulu.Hunting.Core`, `DeltaZulu.Hunting.Render`, `DeltaZulu.Hunting.Schema`, `DeltaZulu.Hunting.Web`, `DeltaZulu.Platform.Web.Abstractions`, `DeltaZulu.Workbench.Application` |
| Forward | `8f7ab19` | 2026-07-21 | `DeltaZulu.Relp.Examples.Client`, `DeltaZulu.Relp.Examples.Server` (renamed Relp → Forward per ADR-7) |
| Agent | `1d54142` | 2026-07-23 | `src/DeltaZulu.LocalStream`, `src/DeltaZulu.Parse` (git submodules replaced by NuGet references) |

### Deleted source files, by repository

| Repo | Deleted `.cs` files |
|---|---|
| Platform | 118 |
| Forward | 16 |
| Agent | 15 |
| Parse | 11 |
| DurableBuffer | 10 |
| LocalStream | 1 |
| LogCluster | 1 |

**Platform's 118 is the number that deserves attention.** The bulk falls in the
`c72efeb` consolidation of seven projects, which is a plausible cause — but seven
projects' worth of public surface disappearing in one commit is exactly the
event the deletion rule exists to make traceable, and no Decision records it.

The Agent's deletions at `1d54142` are benign: submodules became package
references, so the code did not stop existing, it stopped being vendored.

The Forward deletions at `8f7ab19` are a rename, similarly benign.

**Not yet assessed:** whether the remaining deletions removed public types that
some Decision still governs. That is what `governs-check` answers going forward,
but it cannot answer it retroactively for Decisions that were never written.
