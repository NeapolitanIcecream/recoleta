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
language_code: zh-CN
---

# AI engineering tools are being judged by retention, guardrails, and control paths

## Overview
当天最强的信号是 AI 工程工具的运营层证据。Gemini for Google 显示了某家公司内部的实测提升；The Polyglot Protocol 把审查习惯写成规则；Resident 把设备代理收进沙箱本地应用。同一组材料也把更新渠道、管理员控制、流失率和源码映射当作技术评估的一部分。

## Clusters

### Enterprise coding agents
Gemini for Google (GfG) 是唯一有大规模实测部署结果的条目。论文通过继续预训练和后训练，把 Gemini 适配到 Google 的内部工程数据，并用中期训练方法减少灾难性遗忘。在一项覆盖 29,000 名开发者的盲测 A/B 研究中，它报告平均每轮迭代次数减少 23%，代码存活率提高约 17%。

Polyglot Protocol 作为性能证据较弱，因为它没有报告任务成功基准或基线对比。它的价值在于流程：它要求编码代理先检查仓库，再按明确规则选择语言，验证 API 和工具，检查依赖和安全，并标注不受支持的检查。这个仓库覆盖 22 种语言，并为 Codex、Claude Code 和 OpenCode 提供适配器。

#### Evidence
- [Customizing an LLM for Enterprise Software Engineering](../Inbox/2026-05-23--customizing-an-llm-for-enterprise-software-engineering.md): Summary and results for GfG customization, 29,000-developer blind A/B study, 23% iteration reduction, and 17% code-survival gain.
- [The Polyglot Protocol – senior-engineer guardrails for AI coding agents](../Inbox/2026-05-23--the-polyglot-protocol-senior-engineer-guardrails-for-ai-coding-agents.md): Summary of Polyglot Protocol guardrails, 22-language coverage, validation claims, and lack of benchmarked agent-performance gains.

### Sandboxed device apps
Resident 把代理生成的代码应用到物理设备上，并把安全边界收得很紧。它在 ESP32 设备上嵌入 Lua 运行时，并开放部分驱动 API，例如按钮事件和显示写入。应用通过 websocket 经由 Wi‑Fi 到达，运行时不需要编译或刷写固件。

这个设计把实时设备循环留在本地。作者把 150 ms 说成让交互感觉即时的响应上限，而云端大语言模型调用会增加延迟，而且常常需要远程个人上下文。这个版本是 alpha v0.5.0，语料没有给出加载延迟、内存占用、安全测试或设备覆盖面的基准。它的明确主张是在一个沙箱里热加载，并阻止网络栈这类不受限制的能力。

#### Evidence
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): Summary of Resident’s ESP32 Lua sandbox, websocket hot loading, driver API model, 150 ms interaction motivation, and missing benchmarks.

### Agent product due diligence
有两篇条目把 AI 代理产品当作同时带有财务、运营和安全攻击面的系统。Polsia 这篇文章通过公共 API 和已发布的源码映射，审计了一个声称能自动搭建公司的产品。文章说，公开仪表盘上的 970 万美元年化数字里，只有大约 463 万美元来自订阅收入；月度付费流失率约 48%；每日 AI 成本约等于订阅运行率的 57%。它还报告了 1,355 个公开源码模块、管理员控制、人工 QA 标签，以及展示公司暴露出的所有者或运营数据。

GSD 事件关注的是更新路径。文章说，在一次被报告的 token rug pull 之后，原维护者仍然控制着 npm 包 `get-shit-done-cc` 和 `@gsd-build/sdk`。因为这些代理可以在 shell 和 bash 权限下运行，建议是卸载旧包，检查 npm 和 Claude 目录；如果用户仍想保留这套工作流，只使用经过审计的社区分支。

#### Evidence
- [Polsia raised $30M; source map: fake ARR, dead users, god-mode over your company](../Inbox/2026-05-23--polsia-raised-30m-source-map-fake-arr-dead-users-god-mode-over-your-company.md): Summary of Polsia claims about ARR quality, churn, compute costs, source map reconstruction, admin controls, and privacy/security exposure.
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): Summary of the GSD npm update-channel risk, uninstall guidance, community fork, and shell-permission concern.
