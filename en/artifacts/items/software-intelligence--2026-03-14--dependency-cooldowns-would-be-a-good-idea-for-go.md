---
source: hn
url: https://utcc.utoronto.ca/~cks/space/blog/programming/GoDependencyCooldownsGood
published_at: '2026-03-14T22:29:59'
authors:
- ingve
topics:
- go-modules
- dependency-management
- software-supply-chain
- devsecops
- automation
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Dependency cooldowns would be a good idea for Go

## Summary
This article argues for introducing dependency “cooldown periods” into the Go ecosystem to prevent developers from upgrading immediately after a dependency is released. The core point is that even though Go has a minimum version selection mechanism, real-world automated upgrades and manual checks still cause new versions to spread too quickly, increasing supply-chain risk.

## Problem
- The problem to solve is that Go projects may upgrade too quickly to newly released dependency versions, causing malicious or problematic versions to be widely adopted before sufficient review.
- This matters because modern dependency upgrades are often driven by automation tools such as Dependabot, and widely used packages will almost always be pulled by some projects immediately after release.
- The author argues that Go’s minimum version selection alone is not enough, because real-world upgrade behavior is not actually “slow” or “conservative.”

## Approach
- The proposal is to introduce dependency cooldowns for Go: after a new dependency version is released, projects must wait for some period of time before upgrading to it.
- The simplest mechanism is to use “version age” as a threshold for upgrades, so that both automated tools and manual upgrade workflows avoid versions that are too new by default.
- The author emphasizes relying on tool support that is “enabled by default and hard to get wrong,” rather than merely showing the version release time and leaving users to judge for themselves.
- The preference is to put this setting into project-level configuration such as `go.mod`, so the rule persists and automatically applies to all collaborators, rather than relying on environment variables.

## Results
- The article does not provide experiments, datasets, or benchmarks, so there are **no quantitative results** to report.
- The strongest empirical claim is that in practice developers update dependencies “fast enough” that if a module publisher changes what content corresponds to a particular version, other people will be affected very quickly.
- The author observes that many Go projects automate dependency updates, for example through Dependabot, and uses this as real-world evidence supporting the need for cooldown periods.
- The article claims that if automated update tools supported cooldown periods and projects enabled the mechanism, they could gain “a considerable portion” of the benefit without changing Go’s core mechanisms, but it does not quantify the magnitude of that benefit.

## Link
- [https://utcc.utoronto.ca/~cks/space/blog/programming/GoDependencyCooldownsGood](https://utcc.utoronto.ca/~cks/space/blog/programming/GoDependencyCooldownsGood)
