---
source: hn
url: https://xclif.readthedocs.io/en/latest/manifesto.html
published_at: '2026-03-15T23:56:35'
authors:
- thatxliner
topics:
- python-cli
- developer-experience
- framework-design
- code-organization
- plugin-architecture
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# The Xclif Manifesto

## Summary
Xclif advocates elevating large Python CLIs from a “argument parsing library” to a “full framework”: using the file system to map the command tree, using function signatures to directly define command interfaces, and integrating help, configuration, logging, and plugin mechanisms into one unified system. The core problem it aims to solve is not how to write a single command, but how to let code organization, developer experience, and startup performance scale together as a CLI grows into a multi-level, multi-function tool.

## Problem
- Existing Python CLI tools such as Click/Typer are well suited for small scripts, but when a CLI becomes a deep command tree like `git`, `cargo`, or `kubectl`, **the code organization model** becomes the main pain point.
- Developers have to manually register groups and subcommands, centrally import and assemble the command tree, causing the **CLI structure and code directory structure to drift apart**, which makes maintenance and expansion difficult.
- Modern CLIs also require DX capabilities such as beautiful help, man pages, shell completion, color control, configuration files, and automatic plugin discovery; in other libraries these often depend on multiple plugins or glue code, making **integration costly and prone to mismatch**.

## Approach
- Xclif borrows the idea from web routing frameworks: **the directory structure is the command structure**. For example, `routes/config/get.py` automatically becomes `myapp config get` without explicit registration.
- **Functions are commands**: developers only need to write a Python function; its signature directly defines the CLI contract. Parameters without default values become positional arguments, parameters with default values become options, docstrings become help text, and type annotations determine parsing behavior.
- The entry point is minimal: `__main__.py` only needs to build the CLI from the routes directory via `Cli.from_routes(routes)`, enabling a “zero-boilerplate” startup.
- The framework has common CLI capabilities built in and designed as a unified whole: Rich output, configuration management (priority: CLI flag > env var > config file > default), automatic `--verbose/-v` logging levels, and extensible implementations under a plugin-style architecture.
- For performance, Xclif **implements a custom parser from scratch**, rather than building on `argparse`, `Click`, or `getopt`, with the goal of reducing startup overhead while keeping the core lean.

## Results
- The core claim given in the documentation is an **improvement in the organizational model**: by making the “file tree the command tree,” it eliminates manual registration and centralized assembly, claiming to let developers understand the surface structure of the CLI directly from the file system.
- It claims the entry point can be reduced to **3 lines** (`Cli.from_routes(routes)`), significantly reducing boilerplate for large multi-command CLIs; however, it does not provide a code-line comparison experiment against Click/Typer.
- On performance, the text claims **Typer may add hundreds of milliseconds of startup latency**, while Xclif targets being “fast by default” and reduces overhead through on-demand imports and a custom parser; however, **it does not provide benchmark numbers, datasets, or reproducible experimental results**.
- In terms of feature integration, the author claims Xclif natively provides Rich help/error output, configuration loading, automatic logging arguments, and plugin-style extension, and emphasizes that these capabilities are designed as a unified whole rather than stitched on later; however, **no quantitative metrics or user study results are provided**.

## Link
- [https://xclif.readthedocs.io/en/latest/manifesto.html](https://xclif.readthedocs.io/en/latest/manifesto.html)
