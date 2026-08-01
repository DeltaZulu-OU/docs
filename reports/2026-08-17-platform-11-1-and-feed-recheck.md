# Package feed recheck, and the two confirmed §11.1 items

Date: 2026-08-17. Continues `2026-08-16-session-handoff.md`.

## 1. The feed is still blocked, and the evidence is sharper than last time

The handoff's first instruction was to restore a project referencing
`DeltaZulu.Kql 1.1.0-preview.1` from the org feed before doing anything that
depends on it. **It still returns 401**, so the dependent work was not started.

What is new is a probe that separates the possible causes, because "401" alone
does not distinguish a broken token from a missing scope:

| Endpoint | Result |
|---|---|
| `api.github.com/user` | **200** — the token is valid |
| `nuget.pkg.github.com/DeltaZulu-OU/index.json` | **200** — permissionless service index |
| `nuget.pkg.github.com/.../download/deltazulu.kql/index.json` | **401** |
| `nuget.pkg.github.com/DeltaZulu-OU/query?q=DeltaZulu.Kql` | **401** |
| `dotnet restore` against the feed | **401**, `NU1301` |

The token authenticates fine against the GitHub API and reaches the one Packages
endpoint that requires no authentication. Every Packages endpoint that *does*
require authentication rejects it. That is a missing `packages` permission on the
installation, not an expired credential, a proxy fault or a NuGet configuration
error — the three things a bare 401 would otherwise leave open.

`X-Oauth-Scopes` is empty on the response, which is expected for an installation
token and therefore not evidence either way. The endpoint split above is the
evidence.

A new session did not pick the grant up. Session tokens are minted at session
start, so a grant made *during* a session cannot appear in it — but this session
started after the grant was requested and still has no `packages` access, so the
grant had not taken effect at session start.

**Unchanged from the handoff:** `packages:read` for the Claude Code GitHub App
installation on `DeltaZulu-OU`, or a PAT with `read:packages` supplied through
the remote environment settings rather than pasted into a conversation.

**Still blocked by it:** FWD-CONTRACT-v2's two remaining items, and Parse
type-system commits B and D.

**Not blocked by it, and worth recording:** `DeltaZulu.Platform` references no
`DeltaZulu.*` package at all, so it restores, builds and tests with no feed
access whatsoever. That is why the work below could proceed.

## 2. §11.1 item 8 — `Uuid`/`IpAddress` cross-engine divergence

Confirmed by `2026-08-16-schema-divergence-verification.md` and now closed.
`ToDuckDbType` mapped both families to `VARCHAR` while Proton used native
`uuid`/`ipv6`, so equality, ordering and comparison differed per engine for the
same logical field.

Verified before changing anything, because the handoff records gap 19 attributing
a test failure to an `inet` extension download returning HTTP 403: **the
extension installs and loads here and `'127.0.0.1'::INET` round-trips.** The 403
does not reproduce. `DuckDbConnectionFactory` already ran `INSTALL inet;LOAD
inet;` on every connection and `DuckDbValueReader` already normalised `UUID` and
`INET` to strings, so the read path needed no change — the mapping was the only
thing holding the divergence open.

`DuckDbType` gained `Uuid` and `Inet`, appended so existing ordinals stay stable.
The registry's declared mappings and `ToDuckDbType` now agree on the native
types, and the legacy `DuckDbType`-keyed Proton path no longer degrades either to
`string`.

`ToSql`'s `_ => throw` default was removed rather than extended, per the estate
rule and item 7 of the same report. Adding a member to an enum guarded by a
fallthrough is exactly when the fallthrough costs something. The build reports no
CS8509, so every switch over `DuckDbType` covers the new members.

Six tests. One executes the emitted `CREATE TABLE` and reads `typeof()` back as
`UUID` and `INET`, so a mapping naming a type DuckDB rejects would fail rather
than pass silently. One shows `'192.168.001.010'` and `'192.168.1.10'` comparing
equal as `INET` and unequal as text — the divergence itself, made executable.

## 3. §11.1 item 11 — `ParserCanonicalization` applied, not just validated

Recorded as PARTIAL: the canonicalisation was declared on the field and its
consistency validated — `Utc` is rejected on a non-`Timestamp` family — but
nothing performed it.

`ParserCanonicalizer` renders the DuckDB expression, and
`LogicalSchemaProjection.ToCanonicalizedProjection` applies it across a schema's
top-level fields using the same column-selection rule as `ToSilverTable`, so the
projection and the table it feeds cannot disagree about which columns exist. The
canonicalisation is read from the declaration and never inferred from a value.

Semantics were measured against DuckDB before being written:

- `MacLowerColon` strips non-hex characters and regroups into colon pairs, so the
  Cisco dotted form, the dashed form and the colon form converge. A plain
  separator replace leaves `aabb.ccdd.eeff` as `aabb:ccdd:eeff`.
- `Ipv6Compressed` casts to `INET`, which stores an address rather than a
  spelling: the expanded `2001:0db8:...:0001` reads back as `2001:db8::1`.
- `Utc` casts through `TIMESTAMPTZ` onto a zoneless `TIMESTAMP`, so CON-0001 holds
  and no `DateTimeOffset` is created on the path.

### A defect wider than the item

The `Utc` arm exposed something the item does not mention. DuckDB reads
offset-bearing timestamp text correctly whatever the session timezone, but reads
**offsetless** text *in the session timezone*. Measured: the same literal
`'2026-01-01T12:00:00'` yields `12:00:00` under `Etc/UTC` and `17:00:00` under
`America/New_York`.

CON-0001 makes KQL `datetime` UTC-only, so a DuckDB session inheriting the host's
zone silently shifts every offsetless timestamp by the host's offset — the
local-wall-clock error CON-0008 exists to prevent, arriving through a different
door. The default happened to be `Etc/UTC` on this machine, which is not
something to depend on. `DuckDbConnectionFactory` now pins `SET TimeZone='UTC'`
on every connection.

A test asserts the shifted result under `America/New_York` deliberately, so the
pin is recorded as load-bearing and can be revisited if DuckDB's behaviour
changes, rather than carried forward as folklore.

## 4. A finding that constrains what "applied" can mean

`LogicalSchemaProjection` and `BuiltInLogicalSchemas` have **no production
consumers anywhere under `src/`** — only tests reference them. This is the same
shape as the `ILogicalSchemaRegistry` finding in `DEC-0012` and PIPELINE-ERRATA,
and it was not previously recorded for the projection itself.

So the canonicalisation is now performed by the projection, but the projection is
not yet performed by anything. That is the honest statement. The alternative —
wiring it into an ingest path invented for the purpose — would have been a larger
and less reversible change than the item called for. The canonicalisation now
travels with the projection, so whatever first consumes it applies it rather than
re-deriving it.

This strengthens rather than weakens the §11.1 headline: the divergences persisted
unobserved because nothing executes the code path they describe.

## 5. `DEC-0023` accepted

Accepted so DQM wave 2a — canary emitter, reconciler, receiver-side source
inventory — has a settled position to build against. It depends on nothing that
is blocked.

Acceptance settles the measurement principle and its two non-optional properties.
It does not settle the two questions the decision records as open, and the status
note keeps both visible so silence is not mistaken for resolution.

One of them blocks the emitter rather than the principle: **whether canaries are
filtered from Bronze or retained and marked.** `DEC-0010` makes Bronze
write-once, so filtering is a content-based routing judgement taken at write time
and cannot be undone, while retaining and marking is reversible at query time.
That asymmetry is recorded as an argument, not as a decision. It needs its own
Decision before the emitter writes anything.

`repos` and `governs` stay empty. `governs_check --collect` reports five governed
repositories and no warning for `DEC-0023`, which is the checker's documented
treatment of a principle-level Decision.

## 6. State

| Repository | Branch | Result |
|---|---|---|
| `DeltaZulu.Platform` | `claude/deltazulu-corrections-waves-l7ly9k` | Two commits pushed; suite **1338 passing**, from 1319 |
| `docs` | `claude/deltazulu-corrections-waves-l7ly9k` | `DEC-0023` accepted; this report |

The other seven repositories were attached with push access but not modified,
because the work that touches them is the work the feed blocks.

## 7. Next

**With the feed:** FWD-CONTRACT-v2's two remaining items, then Parse commits A–D,
remembering that commit D's plan to drop the `v2-iptables` and
`cisco-interface-spec` motifs costs 20 cases of committed parity coverage rather
than the 1 an earlier undercount suggested.

**Without it:** the Bronze canary-handling Decision above, which wave 2a needs;
and §11.1's remaining ordinary work — implement dynamic-bag routing (item 10,
whose silent loss is already pinned by a characterisation test), and make the
remaining closed-enum switches exhaustive. `KustoType`'s two switches still carry
`_ => throw`; they were left alone here because this session extended
`DuckDbType`, not `KustoType`, and widening the change would have blurred what
the tests were pinning.

Items 1 and 2 from that report remain Decisions rather than repairs: implementing
or deleting `ILogicalSchemaRegistry`, and adding `Ticks` to `LogicalDurationUnit`
per CON-0014.
