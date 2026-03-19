---
source: hn
url: https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok
published_at: '2026-03-07T23:25:21'
authors:
- todsacerdoti
topics:
- nix
- reproducible-builds
- graphics-drivers
- fhs
- linux-packaging
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Nix is a lie, and that's ok

## Summary
This article argues that although Nix claims to escape FHS paths to achieve reproducibility, in the graphics driver scenario it actually reintroduces a global convention path similar to FHS. The core point is not to propose a new system, but to explain why this “impurity” is acceptable and necessary in engineering practice.

## Problem
- Nix’s design goal is to avoid depending on FHS convention paths such as `/usr/lib` and `/lib64` in order to improve build and runtime reproducibility.
- But `libGL.so` in the GPU graphics stack must match the host machine’s kernel module and actual hardware, and an application cannot predict the driver environment of the future machine it will run on at build time.
- If every derivation were made to bundle the correct `libGL.so`, it would cause massive rebuilds and greatly reduce the reuse value of the NixOS binary cache; on non-NixOS systems, this also directly leads to runtime errors like `libGL.so.1: cannot open shared object file`.

## Approach
- The article explains the practical engineering approach taken by Nix/NixOS: acknowledge that graphics drivers are a “hard boundary” between user space and kernel space that cannot be fully abstracted away through pure packaging.
- NixOS and Home Manager therefore introduce an intentional impure global path, `/run/opengl-driver/lib`, so that derivations can look up `libGL.so` there at runtime.
- This essentially reintroduces an FHS-like “find libraries by convention” mechanism, but avoids the cost of rebuilding all packages for every driver combination.
- For non-NixOS users, common alternatives include `nixGL` injecting libraries via `LD_LIBRARY_PATH`, manually setting `LD_LIBRARY_PATH`, or creating `/run/opengl-driver` yourself and symlinking system drivers into it.

## Results
- The article does not provide experimental data, benchmarks, or formal quantitative results.
- The strongest concrete claim is that graphics application issues on non-NixOS have existed for a long time, with issue `#9415` remaining open since **2015**.
- The key engineering conclusion given by the article is that, to avoid “massive rebuilds” for every user/driver combination, NixOS chooses to use the global path `/run/opengl-driver/lib` as a compromise.
- The specific failure mode is explicitly given: when running graphics-dependent Nix applications, `libGL.so.1: cannot open shared object file: No such file or directory` may occur.
- The concluding view is that Nix has not completely eliminated FHS-style conventions; in the GPU driver scenario, “allowing impurity when necessary” is more practical than insisting on absolute purity.

## Link
- [https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok](https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok)
