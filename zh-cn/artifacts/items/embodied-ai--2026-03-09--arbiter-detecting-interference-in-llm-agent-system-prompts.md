---
source: arxiv
url: http://arxiv.org/abs/2603.08993v1
published_at: '2026-03-09T22:29:47'
authors:
- Tony Mason
topics:
- llm-agents
- system-prompt-analysis
- prompt-interference
- multi-model-evaluation
- coding-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Arbiter: Detecting Interference in LLM Agent System Prompts

## Summary
本文提出 Arbiter，用于把 LLM 代理的 system prompt 当作“软件制品”来审计，检测其中的内部指令干扰与架构性失效模式。作者在 Claude Code、Codex CLI、Gemini CLI 三个编码代理提示词上做了跨厂商分析，强调多模型互补审查比单模型更能发现不同类别的问题。

## Problem
- 论文要解决的是：LLM 代理的 system prompt 往往很长、很复杂，却缺少像传统软件那样的类型检查、lint 和测试，因此内部矛盾会被执行模型悄悄“圆过去”，导致行为不稳定且难以定位。
- 这很重要，因为 system prompt 实际上规定了代理的工具使用、工作流、安全边界和记忆机制；一旦内部冲突，代理可能在不同调用中做出不一致甚至危险的决策。
- 作者还指出：负责执行 prompt 的同一个 LLM 不适合作为自己的审计员，因此需要外部、形式化、跨模型的检测机制。

## Approach
- 核心方法是一个两阶段框架 **Arbiter**：先做**定向分析**，再做**无向清查**。可把它理解为“先按规则系统查错，再让多个不同模型自由探索未知问题”。
- 定向分析会把 prompt 拆成若干块，并给每块标注层级、类别、语气和作用域；然后用 5 类规则检查块与块之间是否存在干扰，如 mandate-prohibition conflict、scope overlap redundancy、priority ambiguity、implicit dependency、verbatim duplication。
- 为了避免穷举所有块对，方法先用作用域和语气做预过滤，把 Claude Code 上约 15,680 个候选检查缩到 100–200 个相关对。
- 无向清查则把 prompt 交给多个不同 LLM，用故意模糊的指令让它们“读并找有意思的东西”；每一轮都会看到前几轮的发现，并尝试探索尚未覆盖的区域，直到连续 3 个模型都认为没必要继续为止。
- 作者还补充了一个 prompt AST 结构分析层，把 prompt 解析成文档树，用于结构画像、克隆检测和版本 diff，但这更像辅助分析工具，而非主结果来源。

## Results
- 跨 3 个厂商的无向清查共发现 **152** 个问题：Claude Code **116**、Codex CLI **15**、Gemini CLI **21**；收敛所需轮次分别为 **10 / 2 / 3**，总 API 成本仅 **$0.27**。
- 在 Claude Code 的定向分析中，作者把 prompt 分成 **56** 个块，找出 **21** 个干扰模式：**4** 个 critical 直接矛盾、**13** 个 scope overlap、**2** 个 priority ambiguity、**2** 个 implicit dependency；其中 **20/21 = 95%** 被认为可静态检测。
- 严重度分布上，Claude Code 的无向清查结果为 Curious **34 (29%)**、Notable **36 (31%)**、Concerning **34 (29%)**、Alarming **12 (10%)**；Codex CLI 为 **3/7/5/0**；Gemini CLI 为 **4/9/6/2**。作者据此声称提示词架构与“失败类别”强相关，但与“严重度”不强相关。
- 架构层面的主要结论是：**monolithic** 的 Claude Code 更易在子系统边界产生增长型矛盾，**flat** 的 Codex CLI 更一致但能力表达更少，**modular** 的 Gemini CLI 更容易在模块组合缝隙上出现设计级 bug。
- 一个最强的外部验证案例来自 Gemini CLI：清查器发现其 history compression 的 XML schema 缺少保存用户 memory 的字段，导致压缩后保存偏好会被结构性丢失。作者称 Google 后续独立提交并修补了相关 P0 压缩 bug，但**没有**修复其指出的 schema 级根因。
- 方法论上的突破性主张不是传统任务基准精度提升，而是“**多模型会发现类别上不同的问题**”：例如资源/经济风险、权限模式漏洞、数据完整性、信任架构缺陷等由不同模型分别擅长，单模型分析无法覆盖这种互补性。

## Link
- [http://arxiv.org/abs/2603.08993v1](http://arxiv.org/abs/2603.08993v1)
