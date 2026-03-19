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
- build-systems
- provenance
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# Determinate is the future of Nix today: Wasm, provenance, and flake schemas

## Summary
This article introduces three new capabilities in Determinate Nix: Wasm/WASI, artifact provenance, and flake schemas, with the goal of advancing Nix from a "build tool" into a more general-purpose, trustworthy, and extensible platform. The core claim is that these address Nix's long-standing bottlenecks in expressing complex logic, supply-chain verifiability, and flakes extensibility.

## Problem
- The author argues that the Nix ecosystem has long been stagnant, lacking a clear future direction and struggling to meet the complex needs of large-scale teams.
- Complex evaluation/build logic is difficult to express and test directly in Nix, making high-performance, maintainable implementations of custom logic costly.
- Existing Nix emphasizes reproducibility, but lacks sufficient provenance capabilities for answering "where exactly an artifact came from, who built it, when, and on which machine"; at the same time, the flakes output structure is too rigid, limiting project expressiveness.

## Approach
- Introduce support for **Wasm** and **WASI**: move logic that is hard to write well in Nix into mature languages such as Rust, then call it seamlessly from Nix; Wasm is mainly used for evaluation, while WASI is used for realisation and provides filesystem access.
- Through Wasm/WASI, users can implement more complex tasks in Nix, such as parsing `go.mod`/`go.sum`, processing YAML, and implementing IP address management in a flake.
- Add an experimental **provenance** mechanism: automatically record and sign provenance data for store paths, and store that information when pushing to FlakeHub Cache.
- Introduce **flake schemas**: allow teams to define their own flake output structures so that tools like `nix flake show` can display non-standard outputs semantically instead of just showing `unknown`.

## Results
- The article does not provide systematic benchmark tests or standard dataset results, so there are **no quantitative performance improvement numbers**.
- The clear shipped result is that **Wasm/WASI support has been released in Determinate Nix**, and is described as "the most radical change" and "one of the most transformative sets of changes."
- **provenance has experimental support**: provenance data can be stored for store paths, and paths pushed to **FlakeHub Cache** are automatically signed and saved with provenance information.
- A specific in-use case: the author says they have already attached **GitHub Actions workflow data** to build artifacts internally to track "when and where something was built."
- Future enhancement directions include **TPM-attestable machine information**, to support trust/distrust decisions based on the identity and state of the build machine.
- **flake schemas are shipping this week with the product release**; the key improvement is that flakes can express outputs beyond predefined categories such as `packages`, `nixosConfigurations`, and `devShells`, and have them displayed meaningfully in tools.

## Link
- [https://determinate.systems/blog/determinate-nix-future/](https://determinate.systems/blog/determinate-nix-future/)
