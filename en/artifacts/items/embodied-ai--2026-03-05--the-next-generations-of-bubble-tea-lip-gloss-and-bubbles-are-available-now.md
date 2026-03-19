---
source: hn
url: https://charm.land/blog/v2/
published_at: '2026-03-05T23:26:52'
authors:
- atkrad
topics:
- terminal-ui
- rendering
- developer-tools
- ssh
- ai-agent
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# The next generations of Bubble Tea, Lip Gloss, and Bubbles are available now

## Summary
This is a product/engineering announcement about the official v2 releases of the terminal UI libraries Bubble Tea, Lip Gloss, and Bubbles, rather than an academic paper. Its core value lies in significantly improving the performance, input fidelity, and predictability of terminal applications through a new renderer and support for more modern terminal capabilities.

## Problem
- The previous generation of terminal UI tooling struggled to meet the production needs of AI agents and modern terminal applications in terms of performance, rendering efficiency, and the ability to compose complex interfaces.
- The terminal is shifting from a "niche preference" to a primary interaction platform, especially for AI coding agents and remote SSH scenarios, raising the bar for efficient, stable, low-bandwidth UI frameworks.
- Developers need APIs that make it easier to take advantage of new terminal capabilities, such as richer keyboard input, inline images, synchronized rendering, and clipboard transfer over SSH.

## Approach
- Introduces the core mechanism of v2, the **Cursed Renderer**, whose design is inspired by the **ncurses rendering algorithm** to update terminal display content more efficiently.
- At the simplest level, it improves speed and efficiency by "only doing the necessary screen updates and composing interface elements more intelligently," thereby reducing rendering overhead.
- Provides a more declarative API to achieve "more predictable output," reducing uncertainty when developing complex terminal interfaces.
- Makes deeper use of modern terminal features, including richer keyboard support, inline images, synchronized rendering, and clipboard transfer over SSH.
- These changes have been running for months under real production workloads in the authors' own product, Crush (an AI coding agent), serving as engineering validation.

## Results
- The article **does not provide a rigorous benchmark table, experimental setup, or specific quantitative metrics**, so standard academic-style quantitative results cannot be extracted.
- The strongest performance claim is that rendering is "**faster and more efficient by orders of magnitude**," but no specific multiplier, dataset, or comparison baseline is provided.
- For SSH scenarios, the authors claim the benefits of these improvements are "**monetarily quantifiable**," but they do not provide an amount or measurement method.
- In terms of ecosystem adoption, the article says the Bubble Tea ecosystem already powers **25,000+** open-source applications and is used by teams at **NVIDIA, GitHub, Slack, Microsoft Azure**, and others, but this reflects ecosystem impact rather than experimental results for v2.
- In terms of stability/maturity, the authors state that the v2 branches have been used in their production product **Crush** from the very beginning and have run under real-world constraints for **months**.

## Link
- [https://charm.land/blog/v2/](https://charm.land/blog/v2/)
