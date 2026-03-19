---
source: hn
url: https://github.com/rio719/gLinksWWW-browser
published_at: '2026-03-14T22:37:19'
authors:
- glinkswww
topics:
- web-browser
- privacy
- clipboard-manager
- power-user-tools
- search-switching
relevance_score: 0.24
run_id: materialize-outputs
language_code: en
---

# Show HN: GLinksWWW – A browser for power users tired of repetitive copy-pasting

## Summary
gLinksWWW is a privacy browser aimed at efficiency-focused power users, featuring a multi-slot clipboard, fast search engine switching, zero history storage, and per-site cookie management. Its main value lies in reducing repetitive copy-pasting and enhancing local privacy control, but it reads more like a product feature description than a research paper.

## Problem
- Addresses the problem of **inefficient repetitive copy-pasting** in browsers: traditional clipboards usually store only one item at a time, and frequently switching between text or links disrupts workflow.
- Addresses the problem of **privacy and residual session traces**: conventional browsers save history and site data, creating a burden for users who care about local privacy.
- Addresses the problem of **inconvenient search entry switching and site data control**: users often need to switch search engines manually and find it difficult to manage cookies granularly by website.

## Approach
- The core mechanism is a **multi-slot clipboard system**: users can copy/cut different text or links into designated numbered slots, then paste from the corresponding slot, avoiding repeated overwriting of the single system clipboard.
- It provides **18 concurrent slots** (the text mentions both 9-Slot and 18 Concurrent Slots, so the wording is somewhat inconsistent), and maps copy, cut, and paste directly to slot numbers through hotkeys.
- It integrates **one-click search engine switching** within the browser interface, supporting Perplexity, Google, Bing, Yahoo, Startpage, Yandex, and more, reducing the need to manually change settings or modify address bar behavior.
- It adopts a **zero history storage** policy: browsing history is not written to disk, and traces disappear once the session is closed, improving local privacy in the simplest and most direct way.
- It provides a **per-website cookie manager** and a multi-tab system with up to **7 tabs**, balancing site isolation, data control, and basic multitasking browsing.

## Results
- The text **does not provide formal experiments, benchmarks, or academic evaluation results**; there are no precise throughput, latency, user studies, or quantitative comparisons with Chrome/Firefox/Edge.
- The clearest functional result is support for **18 concurrent clipboard slots**, with targeted copy, cut, and paste via `Ctrl+Shift` / `Alt+Shift` / `Ctrl+Alt` plus number keys or `F1-F8`.
- It supports multi-tab browsing with **up to 7 tabs** and claims to offer “high-speed performance,” but provides no figures for startup time, memory usage, or page load speed.
- On privacy, the specific claim is that it **does not save browsing history to the local disk** and clears traces after the session closes; however, it provides no threat model, security audit, or privacy validation results.
- For cross-platform support, it claims compatibility with **Windows, Linux（AppImage/DEB）, MacOS**; this is a concrete deployment-related selling point, but not a quantitatively validated research breakthrough.

## Link
- [https://github.com/rio719/gLinksWWW-browser](https://github.com/rio719/gLinksWWW-browser)
