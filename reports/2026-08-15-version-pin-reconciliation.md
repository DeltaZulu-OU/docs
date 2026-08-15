# Version pin reconciliation — LocalStream and DurableBuffer

Date: 2026-08-15. Question: the Agent pins `DeltaZulu.LocalStream 1.0.0` and
`DeltaZulu.DurableBuffer 1.0.0`, while LocalStream's source declares `0.1.0` and
DurableBuffer declares no version at all. Are the published packages diverging
from source, or are the pins aspirational?

## Answer: neither. The pins are correct, and LocalStream's source has since gone backwards.

Both packages were published exactly once each, both from a manual
`workflow_dispatch` rather than a tag push, and both runs succeeded:

| Package | Run | Date | Commit | Version published |
|---|---|---|---|---|
| DeltaZulu.DurableBuffer | 29861111418 | 2026-07-21 | `5574911` (current HEAD) | **1.0.0** |
| DeltaZulu.LocalStream | 30011960723 | 2026-07-23 | `ce7d95a` (= tag `v1.0.0`) | **1.0.0** |

Both publish workflows resolve the package version from source via
`dotnet msbuild -getProperty:Version`. At each of those commits **no `<Version>`
was declared anywhere**, so MSBuild returned the SDK default `1.0.0` — which is
what shipped, and what the Agent pins. The pins match published reality exactly.

## The actual defect: LocalStream's declared version is below its published version

On 2026-08-13, commit `7899423` ("Updated versions") **added**
`<Version>0.1.0</Version>` to `Directory.Build.props` — three weeks after 1.0.0
was published. Verified by reading the file at both points:

- at tag `v1.0.0` (`ce7d95a`, 2026-07-23): no `<Version>` element
- at `HEAD` (`7899423`, 2026-08-13): `<Version>0.1.0</Version>`

So the source now declares a version *lower* than what is on the feed. Two things
follow, both of which fire on the next publish rather than today:

1. The workflow would pack and push `0.1.0`. Consumers pinned at `1.0.0` — the
   Agent among them — would never resolve it, and NuGet would not treat it as an
   upgrade for anyone.
2. LocalStream's publish workflow guards on the tag already existing
   (*"Tag 'v1.0.0' already exists; update Directory.Build.props to an unpublished
   version"*). The `0.1.0` edit satisfies that guard's letter — the version is
   unpublished — while inverting its intent. The guard checks for *unpublished*,
   not for *forward*.

The plausible reading is that `0.1.0` was chosen to get past that guard, and
downwards was as good as upwards for that purpose. That is a guard defect as much
as an edit mistake: nothing in the workflow compares the new version to the
highest already published.

## DurableBuffer is differently stuck

DurableBuffer has never declared a `<Version>` — confirmed by running the
workflow's own resolution command, which returns `1.0.0` today. It has no git
tags at all. Since 1.0.0 is already on the feed, the next publish would attempt
to push a version that exists, and cannot proceed without an explicit `<Version>`
being added first.

## Not fixed here

Per the session's instruction this is a report. Neither repository was modified.
Both fixes are one line each, but they are version decisions rather than
corrections — LocalStream needs a version above 1.0.0, DurableBuffer needs an
explicit one — and picking the numbers is a release call, not a repair.

Worth folding into whichever Decision governs release mechanics: the publish
guard should compare against the highest published version, not merely assert
that the tag is free.
