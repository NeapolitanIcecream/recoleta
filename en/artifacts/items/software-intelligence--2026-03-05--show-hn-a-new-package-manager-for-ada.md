---
source: hn
url: https://github.com/tomekw/tada
published_at: '2026-03-05T23:20:39'
authors:
- tomekw
topics:
- package-manager
- ada
- build-tooling
- dependency-management
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# Show HN: A new package manager for Ada

## Summary
Tada is a new package management tool for Ada, focused on using a simple manifest and default configuration to unify building, testing, running, and dependency installation. It is more like a lightweight, personally driven alternative aimed at reducing the burden of writing build scripts by hand.

## Problem
- Build and package management workflows in Ada development may rely on low-level tools and handwritten scripts, increasing the operational cost of project initialization, dependency management, testing, and running.
- Although existing solutions are more mature, the author wanted a simpler tool with clear defaults that fits their own workflow.
- This matters because lower toolchain friction can improve the usability and development efficiency of Ada projects, especially for small projects and ecosystem building.

## Approach
- Tada wraps **GPRbuild** and provides unified commands for Ada packages: `init`, `install`, `build`, `run`, `test`, `clean`, `cache`.
- It uses a simple manifest file, **`tada.toml`**, to declare package metadata, dependencies, and development dependencies, avoiding the need for developers to write complex build scripts directly.
- Toolchain discovery uses a fixed priority order: **local config -> global config -> PATH**, and allows explicit configuration of `gnat` and `gprbuild` paths.
- It provides “opinionated” default behavior and a local cache mechanism, allowing the current package to be installed into the local cache and then used as a dependency by other projects.

## Results
- The text **does not provide formal paper-style quantitative experimental results**, nor does it give benchmark numbers for performance, success rate, or comparisons with Alire.
- Specifically stated capabilities include support for **Linux x86_64, macOS ARM, and Windows x86_64**.
- Dependency and version management uses **Semantic Versioning (`MAJOR.MINOR.PATCH`)** and supports prerelease tags such as `0.1.0-dev`.
- The command set covers the core stages of the package lifecycle: **8 main commands** (the complete CLI set can be regarded as including `build`, `cache`, `clean`, `config`, `help`, `init`, `install`, `run`, `test`, `version`).
- The author explicitly positions it as **alpha software**; the strongest verifiable claim is that it can already “build itself” and can be used to create, build, test, run, and cache Ada packages.

## Link
- [https://github.com/tomekw/tada](https://github.com/tomekw/tada)
