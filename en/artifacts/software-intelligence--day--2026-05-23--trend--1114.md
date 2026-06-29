---
kind: trend
trend_doc_id: 1114
granularity: day
period_start: '2026-05-23T00:00:00'
period_end: '2026-05-24T00:00:00'
topics:
- AI coding agents
- enterprise software engineering
- agent guardrails
- device sandboxes
- AI product due diligence
- software supply chain security
run_id: materialize-outputs
aliases:
- recoleta-trend-1114
tags:
- recoleta/trend
- topic/ai-coding-agents
- topic/enterprise-software-engineering
- topic/agent-guardrails
- topic/device-sandboxes
- topic/ai-product-due-diligence
- topic/software-supply-chain-security
language_code: en
pass_output_id: 186
pass_kind: trend_synthesis
---

# AI engineering tools are being judged by retention, guardrails, and control paths

## Overview
The day’s strongest signal is operational proof for AI engineering tools. Gemini for Google reports measured gains inside one company; The Polyglot Protocol encodes review habits; Resident narrows device agents to sandboxed local apps. The same corpus treats update channels, admin controls, churn, and source maps as part of the technical evaluation.

## Clusters

### Enterprise coding agents
Gemini for Google (GfG) is the only item with a large measured deployment result. The paper adapts Gemini to Google’s internal engineering data through continued pre-training and post-training, with a mid-training method to reduce catastrophic forgetting. In a blind A/B study with 29,000 developers, it reports 23% fewer mean iterations per turn and about 17% higher code survival rates.

The Polyglot Protocol is weaker as performance evidence, because it reports no task-success benchmark or baseline comparison. Its value is procedural: it tells coding agents to inspect the repository, choose languages under explicit rules, verify APIs and tools, check dependencies and security, and label unsupported checks. The repository covers 22 languages and includes adapters for Codex, Claude Code, and OpenCode.

#### Evidence
- [Customizing an LLM for Enterprise Software Engineering](../Inbox/2026-05-23--customizing-an-llm-for-enterprise-software-engineering.md): Summary and results for GfG customization, 29,000-developer blind A/B study, 23% iteration reduction, and 17% code-survival gain.
- [The Polyglot Protocol – senior-engineer guardrails for AI coding agents](../Inbox/2026-05-23--the-polyglot-protocol-senior-engineer-guardrails-for-ai-coding-agents.md): Summary of Polyglot Protocol guardrails, 22-language coverage, validation claims, and lack of benchmarked agent-performance gains.

### Sandboxed device apps
Resident applies agent-written code to physical devices with a tight safety boundary. It embeds a Lua runtime on ESP32 devices and exposes selected driver APIs, such as button events and display writes. Apps arrive over Wi-Fi through a websocket and run without compiling or flashing firmware.

The design keeps the live device loop local. The author cites 150 ms as the response limit for an interaction to feel instant, while cloud large language model calls add latency and often need remote personal context. The release is alpha v0.5.0, and the corpus gives no benchmark for load latency, memory use, safety tests, or device coverage. The concrete claim is hot loading inside a sandbox that blocks unrestricted capabilities such as the network stack.

#### Evidence
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): Summary of Resident’s ESP32 Lua sandbox, websocket hot loading, driver API model, 150 ms interaction motivation, and missing benchmarks.

### Agent product due diligence
Two items treat AI-agent products as systems with financial, operational, and security attack surfaces. The Polsia article audits a claimed autonomous company-builder through a public API and shipped source map. It says the public dashboard’s $9.70M annualized figure includes only about $4.63M in subscription revenue, with about 48% monthly paid churn and daily AI cost equal to about 57% of subscription run-rate. It also reports 1,355 public source modules, admin controls, human QA labels, and exposed owner or operational data for showcased companies.

The GSD incident focuses on the update path. The post says the original maintainer still controlled the npm packages `get-shit-done-cc` and `@gsd-build/sdk` after a reported token rug pull. Because these agents can run with shell and bash permissions, the guidance is to uninstall old packages, check npm and Claude directories, and use the audited community fork only if users still want that workflow.

#### Evidence
- [Polsia raised $30M; source map: fake ARR, dead users, god-mode over your company](../Inbox/2026-05-23--polsia-raised-30m-source-map-fake-arr-dead-users-god-mode-over-your-company.md): Summary of Polsia claims about ARR quality, churn, compute costs, source map reconstruction, admin controls, and privacy/security exposure.
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): Summary of the GSD npm update-channel risk, uninstall guidance, community fork, and shell-permission concern.
