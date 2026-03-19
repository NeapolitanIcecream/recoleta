---
source: hn
url: https://usage.jdx.dev/spec/
published_at: '2026-03-08T23:48:27'
authors:
- birdculture
topics:
- cli-specification
- developer-tools
- command-line-interface
- kdl
- documentation-generation
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Usage Specification

## Summary
Usage is a specification and CLI for defining command-line tools, allowing parameters, flags, environment variables, and config files to be described in a unified way. It aims to be for CLIs what OpenAPI is for Web APIs: a description layer that supports documentation, autocompletion, and cross-language scaffolding generation.

## Problem
- CLI tool parameters, subcommands, environment variables, and configuration logic are usually scattered across implementations in different languages/frameworks, making unified reuse difficult.
- Common needs in the CLI ecosystem—such as autocompletion, Markdown documentation, man pages, and cross-framework migration—often require repeated development, resulting in high cost and inconsistency.
- The lack of a standardized CLI specification hinders toolchain interoperability, which matters because both developers and framework authors need CLI definitions that are portable, generatable, and verifiable.

## Approach
- Proposes a declarative specification called Usage, using KDL to write CLI definitions and uniformly describe structures such as metadata, flags, args, subcommands, and aliases.
- Integrates environment variables, config files, default values, and command-line arguments into a single specification, and defines a clear precedence order, e.g. `CLI flag > env var > config file > default`.
- Provides a companion CLI tool that can generate autocompletion scripts, Markdown documentation, and man pages from the same specification, and supply richer argument-parsing input for any language.
- For CLI framework developers, Usage is positioned as something like an “LSP/OpenAPI for CLIs,” so frameworks only need to output a Usage definition to reuse common ecosystem capabilities.
- In terms of compatibility, it is mainly aimed at GNU-style CLIs; non-standard behavior may be considered for support, but with warnings that it is not recommended.

## Results
- The text **does not provide quantitative experimental results**; there are no benchmarks, datasets, or numerical metrics available for comparison.
- It explicitly states support for **3 types of generated outputs**: autocompletion scripts, Markdown documentation, and man pages.
- The specification can unify **4 types of input sources**: command-line arguments, environment variables, config files, and default values, while defining a deterministic precedence chain.
- The text provides **2 example specifications**: one basic CLI definition example and one more complex example with nested subcommands and aliases, showing that it can express common CLI structures.
- The strongest concrete claim is that developers can use a single Usage specification for scaffolding conversion and capability reuse across **different CLI frameworks and even different languages**, but the text does not provide quantitative validation.

## Link
- [https://usage.jdx.dev/spec/](https://usage.jdx.dev/spec/)
