---
source: arxiv
url: https://arxiv.org/abs/2607.13021v1
published_at: '2026-07-14T17:58:09'
authors:
- Tanmay Singla
- James C. Davis
topics:
- code-intelligence
- automated-software-production
- software-supply-chain
- agentic-coding
- dependency-regeneration
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Software Supply Chains are Dead: Use-Case-Oriented Regeneration

## Summary
The paper proposes use-case-oriented regeneration: an agent locally reimplements only the dependency behavior a repository actually uses. Across 180 JavaScript/TypeScript repository–dependency pairs, the approach preserved nearly all repository-observed validation behavior while sharply reducing the exposed API surface, but it does not establish full semantic equivalence.

## Problem
- Package reuse forces repositories to inherit unused code, transitive dependencies, maintenance obligations, compatibility constraints, and supply-chain risk for narrow functionality.
- Generative coding agents reduce the cost of local implementation, making it important to reassess when dependency reuse is preferable to repository-owned code.
- The problem matters because dependency removal can reduce external trust and attack exposure, but regenerated code must still be validated for correctness and maintainability.

## Approach
- Treat the repository–dependency pair, rather than the upstream package, as the unit of replacement.
- Give an agent repository context and validation artifacts; have it identify dependency call sites, generate local replacements, update callers, remove the dependency, and iterate on validation failures.
- Target repository-observed equivalence: the replacement must preserve behaviors exercised by the repository, not every behavior supported by the original package.
- Evaluate 20 repositories for each of nine JavaScript/TypeScript dependencies, including nanoid, chalk, express, semver, lodash, axios, postcss, change-case, and zod.

## Results
- Across 180 pairs, regenerated code achieved a reported 99.8% aggregate validation pass rate; 166 of 180 pairs preserved all baseline validation checks.
- Generated replacements reduced the exported API surface by an average of 93.1%, from 82.1 original exports to 5.6 regenerated exports, with 6.9% of the original surface retained on average.
- Results were strongest for bounded uses: nanoid and zod had 20/20 pairs with perfect preservation, while lodash had 16/20 and accounted for the largest reported failure count, 104.
- The paper describes 14 failed regeneration attempts, involving semantic and edge-case mismatches, class-identity problems, and deep framework integrations such as express middleware and axios mock interceptors.
- The evidence is limited to existing repository validation artifacts and selected public repositories; passing those checks does not prove full semantic equivalence or coverage of future use cases.

## Link
- [https://arxiv.org/abs/2607.13021v1](https://arxiv.org/abs/2607.13021v1)
