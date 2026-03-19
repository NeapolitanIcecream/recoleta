---
source: hn
url: https://www.danielmoch.com/posts/2025/01/acme/
published_at: '2026-03-14T22:47:21'
authors:
- birdculture
topics:
- text-based-gui
- developer-tools
- plan9
- editor-design
- unix-integration
relevance_score: 0.4
run_id: materialize-outputs
language_code: en
---

# Plan 9's Acme: The Un-Terminal and Text-Based GUIs

## Summary
This article introduces Plan 9's Acme editor and positions it as an "un-terminal," text-first GUI development environment. The core argument is that, compared with closed-off, fragmented modern GUIs, Acme provides a simpler, more durable development experience through unified text interaction and integration with system tools.

## Problem
- Modern GUI applications typically redesign their interaction model independently, lacking consistency and making the overall user experience complex, fragmented, and costly to learn.
- The reason traditional terminals/TUIs are popular with developers is not just that they are "in the terminal," but that they share a highly consistent text-based interaction model and make it easy to compose external tools.
- Common IDEs/editors often have too many configuration options, plugins, and visual customizations, making it easy for developers to spend their energy tuning the environment rather than doing actual work.

## Approach
- Acme uses a text-centered GUI: users can select text in any window, directly "pipe" it to command-line tools, and then write the output back to the selection or display it in a new window.
- It exposes its internal interaction interface through the 9P protocol, allowing external programs to communicate with the editor in a very simple and flexible way, forming an extension mechanism similar to plugins/helper programs.
- Unlike approaches that "embed a terminal in the editor," Acme deeply integrates CLI-style operations into the entire interface, so any text area can become a surface for commands and results.
- It intentionally remains minimalist: almost no configuration, no complex theme system, and no syntax highlighting by default, thereby reducing the cognitive burden of the toolchain and interface.

## Results
- The article is not an experimental paper and does not provide benchmark tests, accuracy, percentage efficiency gains, or quantitative results on datasets.
- The strongest concrete claim is that Acme has already "aged gracefully" for about **30 years** without needing to constantly chase new languages, compilers, terminals, or theme ecosystems.
- The author argues that its core advantage lies in deeper tool integration: compared with VS Code, which mainly "opens a terminal inside the editor," Acme supports directly executing standard CLI-style commands and processing results in **any window**.
- The article also claims that Acme's 9P/helper-program model is simple enough that extensions could even "in theory be written in shell scripts," indicating that its extension interface has a low barrier to entry.
- From a user-experience perspective, the author's conclusion is that removing syntax highlighting, themes, and extensive configuration comes at "almost no cost" while significantly reducing meaningless environment tuning, but this is a personal experiential claim rather than quantitative evidence.

## Link
- [https://www.danielmoch.com/posts/2025/01/acme/](https://www.danielmoch.com/posts/2025/01/acme/)
