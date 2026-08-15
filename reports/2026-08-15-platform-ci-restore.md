# Platform CI restore — what was actually wrong

Date: 2026-08-15. Concerns the two items recorded as gaps 1 and 2, both rated P0
because they gate publishing `DeltaZulu.Kql` to a feed Platform can consume.

## Gap 1's stated symptom is refuted; the underlying defect is real and worse

The gap was recorded as: `RestorePackagesWithLockFile=true`, `.gitignore`
excludes `packages.lock.json`, no lock files committed, CI runs
`dotnet restore --locked-mode` on three operating systems — therefore **restore
cannot succeed on a clean checkout**.

Restore succeeds. Verified on .NET SDK 10.0.110 against Platform's pre-fix tree
with an empty package cache: `dotnet restore --locked-mode` exits 0 and
**generates all 13 lock files during the run**.

That is not the good news it sounds like. Locked mode's purpose is to fail when
the resolved graph does not match a committed lock file. With no lock file
present, NuGet writes one and proceeds — so CI was asserting nothing at all. The
flag was decorative, and every run silently re-resolved dependencies while
appearing to verify them.

A failing CI job announces itself. A no-op does not, which is why this was worth
correcting even though nothing was red.

This is the same failure mode already documented in the Agent's
`Directory.Packages.props`, where four `PackageVersion` entries were silently
ignored by Central Package Management and a known-vulnerable
`SQLitePCLRaw.lib.e_sqlite3` shipped despite the file appearing to pin it. A
configuration that looks like enforcement and is not.

## What was changed

- Removed the `packages.lock.json` exclusion from `.gitignore`.
- Committed all 13 lock files.
- Verified from a clean checkout with an isolated, empty `NUGET_PACKAGES`
  directory that `dotnet restore --locked-mode` succeeds against the committed
  lock files.

## Gap 2 confirmed, and it is broader than Platform

`NuGet.config` declared a `packageSourceMapping` entry for `deltazulu-github`
without ever defining that source in a `<packageSources>` section. Confirmed.

Two qualifications the gap did not carry:

1. **It is latent in Platform, not breaking.** Platform consumes no `DeltaZulu.*`
   packages today — no `PackageReference` and no `PackageVersion` entry — so
   nothing requests the undefined source. It breaks the moment Platform consumes
   `DeltaZulu.Kql`, which is exactly what this work is building toward.
2. **The same defect is in the Agent and in Parse.** In the Agent it is *not*
   latent: `dotnet restore` from a clean checkout fails with NU1100 for all five
   `DeltaZulu.*` packages, because they are mapped to a source that does not
   exist.

The instruction to use Parse's `NuGet.config` as the correct reference does not
hold — Parse has the identical defect in its committed file. Parse restores in CI
only because `publish.yml` builds a temporary config at run time and calls
`dotnet nuget add source` with `GITHUB_TOKEN`. That run-time injection is the
working pattern; the committed file is not.

Platform's config now defines both sources explicitly, with `<clear />` ahead of
them so restore does not depend on whatever machine-level sources a runner
happens to have.

## Still open

- The Agent's and Parse's `NuGet.config` have the same undefined-source defect
  and were not touched here.
- Restoring `DeltaZulu.*` packages from a clean container still requires a PAT
  with `read:packages`. This session's GitHub App token returns 401 against
  `nuget.pkg.github.com`, so the end-to-end feed consumption path remains
  unverified from outside CI.
