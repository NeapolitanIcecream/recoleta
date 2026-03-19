---
source: hn
url: https://github.com/tomekw/tada
published_at: '2026-03-05T23:20:39'
authors:
- tomekw
topics:
- ada
- package-manager
- build-tool
- developer-tooling
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: A new package manager for Ada

## Summary
Tada is a new package management tool for Ada, focused on handling building, testing, running, and dependency installation with a simple manifest and sensible defaults. It is an author-driven alpha project positioned as a lighter, more “opinionated” development experience than existing solutions.

## Problem
- Building and package management in Ada development often rely on low-level tools and extra scripts, increasing the complexity of project initialization, dependency management, and day-to-day development workflows.
- Although Alire already exists in the ecosystem, the author wants to provide a simpler alternative with more direct default configuration to reduce boilerplate work.
- This matters because reducing toolchain friction can improve the usability and development efficiency of Ada projects, especially for personal projects and small ecosystem building.

## Approach
- Tada wraps GPRbuild and provides a simple `tada.toml` manifest file to describe package information and dependencies, thereby reducing the need to hand-write build scripts.
- It unifies common development tasks into a small set of commands: `init`, `install`, `build`, `run`, `test`, `clean`, `cache`.
- The toolchain discovery mechanism looks for `gnat` and `gprbuild` in the order of local configuration, global configuration, and system PATH, balancing default ease of use with customizability.
- Dependencies are declared using semantic versioning in `[dependencies]` and `[dev-dependencies]`, then installed by `tada install` into the local cache for project use.

## Results
- The text does not provide benchmark tests, performance improvements, success rates, or quantitative comparison results versus Alire/GPRbuild.
- The declared and tested supported platforms total **3**: Linux x86_64, MacOS ARM, Windows x86_64.
- The tool covers about **9** core workflow commands: `build`, `cache`, `clean`, `config`, `help`, `init`, `install`, `run`, `test` (plus a `version` information command).
- Dependency and version management uses **SemVer (`MAJOR.MINOR.PATCH`)**, and supports prerelease labels such as `0.1.0-dev`.
- The author explicitly states that the software is in the **alpha** stage; the main breakthrough claim is not performance metrics, but completing Ada package building, testing, running, and dependency management with less configuration.

## Link
- [https://github.com/tomekw/tada](https://github.com/tomekw/tada)
