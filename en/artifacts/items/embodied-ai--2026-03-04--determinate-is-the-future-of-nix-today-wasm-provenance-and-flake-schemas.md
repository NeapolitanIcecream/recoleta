---
source: hn
url: https://determinate.systems/blog/determinate-nix-future/
published_at: '2026-03-04T23:20:21'
authors:
- biggestlou
topics:
- nix
- webassembly
- software-supply-chain
- provenance
- flake-schemas
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Determinate is the future of Nix today: Wasm, provenance, and flake schemas

## Summary
This article introduces three key updates to Determinate Nix: Wasm/WASI, build artifact provenance, and flake schemas, with the goal of advancing Nix from a “build tool” into a more general-purpose, more secure, and more extensible platform. The core value lies in improving the ability to express complex logic, strengthening supply-chain verifiability, and relaxing the structural constraints of flakes.

## Problem
- The traditional Nix ecosystem is seen as stagnant and lacking a unified, clear roadmap for the future.
- It is difficult to write high-performance, testable, and complex evaluation and build logic in the Nix language, especially in large enterprises and monorepo scenarios.
- Existing Nix supply-chain information mainly remains at the dependency-graph level and lacks verifiable provenance for build origins; meanwhile, the output structure of flakes is too rigid.

## Approach
- Introduce **Wasm** for evaluation and **WASI** for realization, allowing users to move complex logic that is hard to implement in Nix into mature languages such as Rust, and then call it seamlessly from Nix.
- With Wasm/WASI support, directly implement things such as parsing `go.mod/go.sum`, processing YAML, and handling more complex system logic within Nix workflows, without relying on large amounts of Nix expressions or wrapper layers.
- Add experimental **provenance** support: automatically record and sign origin information for store paths, and store this metadata when pushing to FlakeHub Cache.
- Introduce **flake schemas**, allowing developers to customize flake output structures and enabling tools like `nix flake show` to display these custom outputs semantically.

## Results
- The article does not provide standard benchmarks, datasets, or performance metrics, so there are **no quantitative results** to report.
- The strongest concrete release claim is that three capabilities are launching this week: **Wasm/WASI support**, **experimental provenance storage and signing**, and **flake schemas**.
- The author claims that Wasm/WASI will significantly expand Nix’s applicability, enabling complex logic to be implemented in languages such as Rust and to cover both the evaluation and realization stages, but **does not provide numbers for throughput, latency, or developer productivity**.
- On provenance, it is currently possible to attach build-origin information such as a **GitHub Actions workflow**, with plans to further extend this to machine identity and state verification at the **TPM attestation** level, but **no quantified results are yet provided for coverage or security benefits**.
- flake schemas are described as a “major improvement” to the structural flexibility of flakes, capable of turning outputs previously displayed as `unknown` into interpretable semantic structures, but **there is no user research or compatibility statistics data**.

## Link
- [https://determinate.systems/blog/determinate-nix-future/](https://determinate.systems/blog/determinate-nix-future/)
