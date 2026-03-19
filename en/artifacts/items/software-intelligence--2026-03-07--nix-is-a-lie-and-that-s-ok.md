---
source: hn
url: https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok
published_at: '2026-03-07T23:25:21'
authors:
- todsacerdoti
topics:
- nix
- reproducible-builds
- linux-graphics
- runtime-linking
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Nix is a lie, and that's ok

## Summary
This article argues that although Nix claims to break away from FHS paths to achieve pure reproducibility, in graphics driver scenarios it actually depends on a global convention path, so its “purity” has exceptions. The author sees this not as a failure, but as a pragmatic compromise made to stay compatible with real hardware and preserve cache efficiency.

## Problem
- One of Nix’s core promises is to avoid FHS convention paths such as `/usr/lib` and `/lib64` in order to improve reproducibility and isolation.
- But in the GPU graphics stack, `libGL.so` must match the host machine’s kernel module and physical hardware, so it cannot be packaged in advance into most derivations at build time.
- If NixOS injected the correct `libGL.so` into every derivation, it would cause massive rebuilds and weaken the value of the binary cache; on non-NixOS Linux systems, this instead leads to a long-standing runtime missing-library problem that hurts practical usability.

## Approach
- NixOS and Home Manager adopt an **intentionally introduced impurity**: they provide a global path, `/run/opengl-driver/lib`, where programs look for `libGL.so` at runtime.
- This essentially reintroduces an FHS-like “find libraries by convention” mechanism, but only for the graphics-driver boundary condition that is hard to make pure.
- For non-NixOS users, common community practices include using `nixGL` to inject driver libraries at runtime via `$LD_LIBRARY_PATH`, manually modifying `$LD_LIBRARY_PATH`, or creating `/run/opengl-driver` yourself and symlinking the host system drivers into it.
- The core mechanism can be understood simply as: **don’t bake GPU driver libraries into every package ahead of time; instead, borrow the correct version from a conventional host location at runtime**.

## Results
- The article **does not provide formal experiments or benchmark numbers**.
- The most concrete factual result given is that when non-NixOS users run graphics-dependent Nix applications, a common error is `libGL.so.1: cannot open shared object file: No such file or directory`.
- The article notes that the related problem has been documented in issue `#9415` since **2015**, showing that this is a long-running compatibility issue that has not been fully resolved.
- The author’s main conclusion is that by using a global path such as `/run/opengl-driver/lib`, Nix reaches a pragmatic balance between avoiding “triggering massive rebuilds for all users and all derivations” and keeping graphics programs runnable.

## Link
- [https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok](https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok)
