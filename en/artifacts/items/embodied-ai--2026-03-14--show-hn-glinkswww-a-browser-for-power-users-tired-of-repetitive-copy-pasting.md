---
source: hn
url: https://github.com/rio719/gLinksWWW-browser
published_at: '2026-03-14T22:37:19'
authors:
- glinkswww
topics:
- web-browser
- productivity-tools
- privacy
- clipboard-manager
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: GLinksWWW – A browser for power users tired of repetitive copy-pasting

## Summary
This is not a research paper, but a browser project introduction aimed at users who perform high-frequency web operations. It highlights a multi-slot clipboard, fast search engine switching, and privacy protection, but does not provide systematic experiments or academic evaluation results.

## Problem
- It aims to solve the problems heavy web users face with repeated copy-pasting, frequently switching search engines, and the cumbersome management of site data.
- It emphasizes privacy needs: common browsers save history and continuously accumulate cookies, increasing exposure risk and management costs.
- This matters because these frequent small actions continuously drain efficiency, and privacy leakage risk is related to the accumulation of local traces.

## Approach
- It proposes a **multi-slot clipboard browser**: offering up to 18 concurrent slots, with keyboard shortcuts that directly bind copy, cut, and paste to specific slots.
- It includes a built-in clipboard manager, allowing users to view and manage text snippets or links in each slot rather than relying only on a single system clipboard.
- It provides **one-click search engine switching** within the interface, covering Google, Bing, Yahoo, Startpage, Yandex, Perplexity, and others.
- It adopts a “**no history storage**” zero-footprint approach: browsing history is not written to local disk, and no browsing traces are retained after the session is closed.
- It supports **per-website cookie management**, enabling users to view, edit, and destroy cookies for specific sites without affecting other sites.

## Results
- The specific feature numbers given in the text include **18 concurrent clipboard slots**, while the description also mentions **9-Slot Multi-Copy & Paste**; these two statements are inconsistent.
- The browser supports **up to 7 tabs** and claims cross-platform support for **Windows, Linux (AppImage/DEB), MacOS**.
- It provides explicit shortcut mappings: copy is **Ctrl+Shift+0~9/F1~F8**, cut is **Alt+Shift+0~9/F1~F8**, and paste is **Ctrl+Alt+0~9/F1~F8**.
- **No quantitative experimental results are provided**: there are no speed benchmarks, user studies, privacy evaluations, comparison metrics against other browsers, datasets, or standard benchmarks.
- The strongest concrete claims are: reducing repetitive copy-pasting through the multi-slot clipboard, reducing local traces through the no-history policy, and improving control through site-level cookie management.

## Link
- [https://github.com/rio719/gLinksWWW-browser](https://github.com/rio719/gLinksWWW-browser)
