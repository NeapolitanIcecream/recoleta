---
source: hn
url: https://charm.land/blog/v2/
published_at: '2026-03-05T23:26:52'
authors:
- atkrad
topics:
- terminal-ui
- ai-agent-tooling
- rendering-engine
- developer-tools
- ssh-optimization
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# The next generations of Bubble Tea, Lip Gloss, and Bubbles are available now

## Summary
This article announces the stable v2 releases of the terminal UI libraries Bubble Tea, Lip Gloss, and Bubbles, with a focus on making the terminal a first-class runtime environment for AI agents and modern developer tools. Its core value is providing faster, more stable, and more predictable rendering and input capabilities to support production-grade terminal applications.

## Problem
- The terminal is shifting from a "somewhat niche developer preference" into a primary platform for AI agents, coding tools, and operating system interaction, but the previous generation of terminal UI capabilities struggled to handle higher loads and more complex interactions.
- Existing terminal application development needs a lower barrier to high-quality interaction while also balancing performance, composability, scripting, and deep OS access, which is important in production environments.
- In remote scenarios such as SSH, rendering efficiency directly affects cost; therefore, more efficient terminal rendering is not just an experience issue, but also a practical resource and money issue.

## Approach
- The core mechanism is the introduction of the **Cursed Renderer**, whose design references the rendering algorithm of **ncurses**, updating terminal output more efficiently and thereby significantly reducing rendering overhead.
- v2 provides more optimized rendering, advanced compositing, higher-fidelity input handling, and a more declarative API to achieve "very predictable" output.
- The new version makes deeper use of modern terminal capabilities, including richer keyboard support, inline images, synchronized rendering, and clipboard transfer over SSH.
- These capabilities have already been used in production for a long time in the author's own AI coding agent **Crush**, indicating that the design is not experimental but an engineering solution validated under real-world constraints.

## Results
- The ecosystem has broad adoption: the Bubble Tea ecosystem already supports **25,000+** open-source applications and is used by teams at **NVIDIA, GitHub, Slack, Microsoft Azure** and others.
- The author claims that v2 rendering is "**faster and more efficient by orders of magnitude**," meaning speed and efficiency improved by **orders of magnitude**; however, the excerpt **does not provide specific benchmark numbers, datasets, or baselines**.
- For applications running over **SSH**, the author says the gains from the improvements are "**monetarily quantifiable**," meaning they can translate into clear cost savings; however, the excerpt **does not provide specific savings amounts or percentages**.
- The v2 branches have been running in production from the very beginning in the AI coding agent **Crush**, and have been used in real products for **months**, which is the strongest engineering validation presented.
- The article also emphasizes that throughout the project's history, it has "**never pushed a breaking change**," and that this v2 is a generational upgrade made in response to significant shifts in platform requirements.

## Link
- [https://charm.land/blog/v2/](https://charm.land/blog/v2/)
