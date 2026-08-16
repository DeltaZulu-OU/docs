# Package publishing is blocked, and what it blocks

Date: 2026-08-16. Measured, not inferred.

## The finding

`DeltaZulu.Kql` 1.0.0-preview.1 builds, packs, and passes 58 conformance tests
against both halves of the version span. It cannot be published from an agent
session.

```
dotnet nuget push DeltaZulu.Kql.1.0.0-preview.1.nupkg \
  --source https://nuget.pkg.github.com/DeltaZulu-OU/index.json
→ 401 Unauthorized
  "Your request could not be authenticated by the GitHub Packages service."
```

The session's GitHub App installation token carries **no `packages` scope at
all** — not read, not write. The same token reads and writes repository contents
without difficulty, so this is a scope boundary rather than a broken credential.

This is the same wall the Wave 0 pre-flight hit from the other side: item 7 could
not verify a `deltazulu-github` restore from a clean container, for the identical
reason.

## What it blocks

| Work | Blocked because |
|---|---|
| FWD-CONTRACT-v2 items 3–11 | `DeltaZulu.Forward` must reference `DeltaZulu.Kql` to replace `ForwardValueNormalizer` with `KqlTypes.TryNormalize` and re-type `Fields` as `IReadOnlyDictionary<string, KqlValue>` |
| Parse type-system commits B and D | `ScalarSymbol` replaces `KqlType`, on `ParserInfo`, on `SyslogEnvelope`, and in the rewritten fixtures |
| Platform consuming the catalogue | Would surface the undefined-source defect that is currently latent there |

The security half of FWD-CONTRACT-v2 (items 1–2) was independent of this and has
already landed.

## What was done instead

`DeltaZulu.Kql` had no publish workflow. One now exists
(`.github/workflows/publish.yml`, `workflow_dispatch`), so a maintainer can
release with one dispatch using the repository's own `GITHUB_TOKEN`, which does
carry `packages: write`.

Three gates in it are deliberately stronger than the estate's existing publish
workflows:

**A forward-version guard.** The other repositories check only that the release
tag is free. That is exactly what let LocalStream's declared version move from an
implicit `1.0.0` down to an explicit `0.1.0` *after* 1.0.0 had been published: the
tag `v0.1.0` was genuinely unused, so the guard passed while its intent inverted,
and consumers pinned at 1.0.0 would never have resolved the result. The new guard
compares against the highest existing tag and refuses anything that does not move
forward.

It implements SemVer prerelease ordering rather than using `sort -V`, which ranks
`1.0.0-preview.1` *above* `1.0.0` and would get precisely the interesting case
backwards. Nine cases were checked, including the LocalStream one.

**Both halves of the span are tested as separate publish steps.** Publishing an
assembly exercised against only 9.2.0 would ship CON-0006's span unverified.

**The packed nuspec is asserted to carry Kusto.Language as an open-ended
minimum.** A bracket pin would make the assembly unloadable in one of the two
host processes, so it fails the publish rather than shipping. Verified against
the actual built package.

## What a maintainer needs to do

Either run the `Publish NuGet package` workflow in `DeltaZulu-OU/DeltaZulu.Kql`,
or supply a PAT with `write:packages` (and `read:packages` for the consuming
side) to whatever runs the publish.

Until one of those happens, the three blocked items above stay blocked, and no
amount of local work moves them.

## Recommendation beyond the immediate fix

The forward-version guard should be backported to the publish workflows in
`DeltaZulu.Parse`, `DeltaZulu.LocalStream` and `DeltaZulu.DurableBuffer`. All
three carry the weaker tag-free check, and LocalStream has already demonstrated
what that check misses. DurableBuffer is a separate case of the same underlying
gap: it has never declared a `<Version>`, so it relies on the SDK default of
`1.0.0` — which is already published, meaning its next publish cannot proceed at
all without an explicit version.
