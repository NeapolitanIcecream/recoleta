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
- package-security
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Dependency cooldowns would be a good idea for Go

## Summary
This article argues that Go should introduce a dependency "cooldown" mechanism to prevent developers from upgrading immediately when a new dependency version is released. The author believes this would reduce supply-chain risk, especially in the real-world environment where automated dependency update tools are widely used.

## Problem
- The problem to solve is that Go projects upgrade to new dependency versions too quickly, making malicious, faulty, or retargeted module versions easier to spread in a short period of time.
- This matters because although Go has protections such as "minimum version selection," in practice many automated tools and manual workflows still update dependencies as soon as a new version appears.
- For widely used dependencies, as long as enough developers are monitoring updates, there will almost always be someone who pulls the new version immediately after release, amplifying the impact of supply-chain attacks or release mistakes.

## Approach
- The core idea is simple: do not let a new dependency version "take effect" immediately, but instead require it to wait for some period before projects are allowed to upgrade to that version.
- This cooldown period creates a window for automated checks or manual review, making suspicious releases, mistaken releases, or version tampering easier to detect.
- The author argues that optional support from tools like Dependabot alone is not enough, because not everyone uses such platforms, and some people also perform dependency upgrades manually.
- Therefore, a better mechanism should be supported directly by the Go toolchain, and preferably enabled through persistent configuration in `go.mod`, so that default behavior is consistent and team members are less likely to miss it.

## Results
- The article does not provide experiments, benchmarks, or formal quantitative results.
- The strongest specific claim is that even though Go uses minimum version selection, in practice dependency upgrades still happen "fast enough" that the short-term risk window after a dependency release is real.
- Based on observing quite a few Go project repositories, the author notes that many dependency updates are triggered by automation tools such as Dependabot, but provides no numerical statistics.
- The article's main contribution is an argument about security and tool design, rather than a new algorithm or system implementation validated by data.

## Link
- [https://utcc.utoronto.ca/~cks/space/blog/programming/GoDependencyCooldownsGood](https://utcc.utoronto.ca/~cks/space/blog/programming/GoDependencyCooldownsGood)
