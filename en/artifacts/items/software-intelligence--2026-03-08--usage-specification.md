---
source: hn
url: https://usage.jdx.dev/spec/
published_at: '2026-03-08T23:48:27'
authors:
- birdculture
topics:
- cli-specification
- developer-tooling
- command-line-interface
- cross-language
- arg-parsing
relevance_score: 0.6
run_id: materialize-outputs
language_code: en
---

# Usage Specification

## Summary
Usage is a specification and CLI for defining command-line tools, aiming to unify a CLI's arguments, flags, environment variables, and configuration files into a portable declarative spec. It is analogous to OpenAPI/LSP for the CLI domain and can be used to generate completions, documentation, man pages, and serve as an intermediate representation for cross-language CLI frameworks.

## Problem
- The specification aims to solve the fact that CLI interface definitions are typically scattered across implementations in different languages and frameworks, leading to duplicated effort and difficulty in unifying documentation, completions, parsers, and configuration support.
- This matters because CLIs are a foundational interaction layer in software development and operations; without a unified spec, developers must separately maintain help text, completion scripts, and argument-parsing logic for each framework and shell.
- The existing CLI ecosystem lacks a standard description layer analogous to what OpenAPI provides for Web APIs, which hinders cross-language reuse, automatic toolchain generation, and a consistent human-computer interaction experience.

## Approach
- The core method is to define a declarative Usage spec: use KDL to describe CLI metadata, flags, positional arguments, subcommands, as well as environment variables, config files, and default-value mappings.
- The spec serves as the CLI's “single source of truth”: the same definition can be used to generate autocompletion scripts, Markdown documentation, man pages, or drive advanced argument parsers in different languages.
- The specification supports common GNU-style CLI structures such as nested subcommands, aliases, hidden aliases, global flags, and count flags, and explicitly expresses value-source precedence, such as `CLI flag > env var > config file > default`.
- For framework developers, it is positioned as something like “LSP/OpenAPI for CLIs”: frameworks only need to output a Usage definition to reuse the Usage CLI for generating multi-shell completions and documentation, without reimplementing these peripheral capabilities.
- The method explicitly limits its scope: it is primarily aimed at standard GNU-style CLIs and does not seek to cover all nonstandard command-line behaviors, though it allows compatibility and warnings for discouraged patterns.

## Results
- The text does not provide experimental data, benchmark results, or quantitative evaluation, so there are no concrete numerical improvements to report.
- It explicitly claims that **3 categories** of direct outputs can be generated from the same spec: autocompletion scripts, Markdown documentation, and man pages.
- It explicitly claims that the same specification can cover definitions for **4 categories** of input sources: arguments, flags, environment variables, and config files, and supports combining them with precedence.
- It explicitly claims that **1** spec can be scaffolded into different CLI frameworks, even across different programming languages, to reduce duplicated implementation.
- The strongest concrete compatibility claim is that it primarily supports standard GNU-style options; for some nonstandard behaviors it may in the future “allow but warn,” indicating that the design prioritizes practical consistency over complete expressiveness.

## Link
- [https://usage.jdx.dev/spec/](https://usage.jdx.dev/spec/)
