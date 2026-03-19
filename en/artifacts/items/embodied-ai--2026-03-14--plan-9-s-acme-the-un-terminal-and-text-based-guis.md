---
source: hn
url: https://www.danielmoch.com/posts/2025/01/acme/
published_at: '2026-03-14T22:47:21'
authors:
- birdculture
topics:
- text-based-gui
- acme-editor
- plan-9
- developer-tools
- unix-integration
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Plan 9's Acme: The Un-Terminal and Text-Based GUIs

## Summary
This is a technical article introducing the design philosophy of Plan 9's Acme editor, not a robotics or machine learning research paper. It argues for a highly consistent, text-centered GUI that integrates command-line tools as an alternative path between traditional terminal TUIs and modern IDEs.

## Problem
- The problem the article addresses is that modern GUIs/IDEs are often closed off from one another, use inconsistent interaction patterns, and have high learning costs, making the overall computer experience bloated and overwhelming.
- For developers, the appeal of terminal tools is not simply that they are "in the terminal," but that they are text-centered, highly regular in behavior, and easy to compose and transfer learning across.
- This matters because if a development environment can reduce configuration burden, unify interaction styles, and better reuse the existing Unix toolchain, it can reduce cognitive overhead and unnecessary interface complexity.

## Approach
- The core mechanism is a "textual GUI" like Acme: the interface is graphical, but the primary objects of interaction are still text rather than large numbers of icons or separate widget systems.
- Users can select any text and "pipe" it to command-line programs; the command output either replaces the original text or appears directly in a new Acme window, naturally embedding CLI tools into the editing environment.
- Under the hood, Acme exposes its interaction interface via the 9P protocol, which can be used on POSIX systems through Unix domain sockets; this allows external "helper programs"/plugins to cooperate with the editor in a very free and lightweight way.
- It is deliberately minimalist: almost no configuration options, no theming system, no syntax highlighting by default, and only limited auto-indentation, in order to reduce the time users waste on appearance and editor "tuning."
- The author summarizes it as an "integrating development environment" rather than a traditional "integrated development environment": the emphasis is not on packing every feature into one all-in-one application, but on integrating external tools through a unified text interface.

## Results
- The article **does not provide experimental data, benchmarks, or quantitative metrics**, so there are no reportable accuracy figures, speed measurements, datasets, or numerical comparisons with baselines.
- The strongest concrete claim is that Acme has "aged gracefully" for about **30 years**, and the author uses its long-term usability as evidence of the success of its design.
- The article claims that Acme has less configuration burden than conventional modern IDEs; for example, phenomena like "hundreds of lines of config files" are basically absent in Acme, though no quantitative statistics are provided.
- The article also gives capability examples: it can be extended through helper programs, and there is even an **LSP client (acme-lsp)** and plugins for things like "format on save," showing that its minimalist core does not preclude functional extension, though again there are no quantitative comparison results.

## Link
- [https://www.danielmoch.com/posts/2025/01/acme/](https://www.danielmoch.com/posts/2025/01/acme/)
