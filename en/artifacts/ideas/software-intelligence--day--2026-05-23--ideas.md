---
kind: ideas
granularity: day
period_start: '2026-05-23T00:00:00'
period_end: '2026-05-24T00:00:00'
run_id: f4d60be8-002e-44a7-a834-d55624705ca0
status: succeeded
topics:
- AI coding agents
- enterprise software engineering
- agent guardrails
- device sandboxes
- AI product due diligence
- software supply chain security
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/enterprise-software-engineering
- topic/agent-guardrails
- topic/device-sandboxes
- topic/ai-product-due-diligence
- topic/software-supply-chain-security
language_code: en
pass_output_id: 187
pass_kind: trend_ideas
upstream_pass_output_id: 186
upstream_pass_kind: trend_synthesis
---

# Production Controls for AI Engineering

## Summary
AI engineering adoption is moving toward measurable production behavior and explicit control surfaces. The clearest work to copy is code-survival measurement for coding-agent pilots, update-path review for local agent packages, and sandboxed app loading for small device interfaces.

## Code-survival telemetry for internal coding-agent rollouts
Engineering teams testing coding agents can add two product metrics to pilot dashboards: the number of back-and-forth iterations needed to finish a request, and whether assisted code remains after review and later edits. Gemini for Google reports both measures at large scale, with a blind A/B study across 29,000 developers showing 23% fewer mean iterations per turn and about 17% higher code survival rates.

A practical version does not require a custom foundation model on day one. An internal pilot can tag agent-assisted pull requests, connect chat or IDE sessions to review outcomes, and sample code survival after a fixed window such as 30 or 60 days. Multi-language repositories also need a pre-change checklist: inspect the repository, verify APIs and tooling, check dependencies and security rules, and label checks the agent could not run. The Polyglot Protocol is useful here as a procedural template, especially because it names repository discovery and validation failures that teams already see in code review.

### Sources
- [Customizing an LLM for Enterprise Software Engineering](../Inbox/2026-05-23--customizing-an-llm-for-enterprise-software-engineering.md): GfG reports a 29,000-developer blind A/B study with fewer iterations and higher code survival rates.
- [The Polyglot Protocol – senior-engineer guardrails for AI coding agents](../Inbox/2026-05-23--the-polyglot-protocol-senior-engineer-guardrails-for-ai-coding-agents.md): The Polyglot Protocol defines repository discovery, API verification, dependency checks, testing, security review, and final validation for coding agents.

## Update-path inventory for local AI agent packages with shell access
Teams using local coding agents need an inventory of package names, maintainers, install locations, and permissions for tools that can run shell commands. The GSD incident shows the specific failure mode: an npm package can keep its publish path even after social trust in the maintainer collapses, and agent packages may run with bash or shell permissions on a developer machine.

The immediate workflow is small enough for a security team or developer-experience team to run this week. List globally installed and project-local AI agent packages, check `~/.npm/_npx/` and `.claude` for leftovers, pin approved package names, and require a maintainer-control review before agents receive shell permissions. For tools installed through npm, the review should include who can publish, whether a fork changed the update path, and how developers can remove stale packages. This is supply-chain review applied to agent tooling, where an update can become a local code-execution path.

### Sources
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): The post identifies retained npm publish access for original GSD packages and the risk created by shell-capable local agents.
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): The post gives concrete cleanup locations and commands, including npm installs, `~/.npm/_npx/`, and `.claude` directories.

## Sandboxed hot-loaded Lua apps for ESP32 device prototypes
Device teams can test AI-authored microcontroller behavior by exposing a narrow driver API and running generated Lua apps inside an on-device sandbox. Resident shows a concrete pattern on ESP32: app code is pushed over Wi-Fi through a websocket, runs without compiling or flashing firmware, and can use selected capabilities such as button events and display writes while blocked from unrestricted access such as the network stack.

This fits prototypes where the interaction loop must feel local. The author cites 150 ms as the response limit for an interface to feel instant, which is hard to meet when every button press waits on a cloud model. A useful first test is a small device with a screen and buttons, such as an M5StickS3-style kit, plus two measurements Resident does not yet publish: app load latency and memory use under repeated hot loads. Safety testing should include attempts to reach blocked APIs, especially networking and hardware controls outside the exposed driver surface.

### Sources
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): Resident is described as an ESP32 Lua sandbox for hot-loading AI-authored apps without compiling or flashing firmware.
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): The source cites 150 ms as the threshold for instant interaction and explains why cloud calls are too slow for live device loops.
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): The source describes the safety concern around unrestricted firmware control and motivates sandboxed device code.
