---
source: arxiv
url: http://arxiv.org/abs/2603.08993v1
published_at: '2026-03-09T22:29:47'
authors:
- Tony Mason
topics:
- llm-agents
- prompt-analysis
- coding-agents
- multi-model-evaluation
- system-prompt-testing
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Arbiter: Detecting Interference in LLM Agent System Prompts

## Summary
本文提出 Arbiter，用于把 LLM 编码代理的 system prompt 当作可测试的软件制品来分析，并检测其中的“指令干扰/冲突”。作者在 Claude Code、Codex CLI、Gemini CLI 三个厂商提示词上做了跨模型、跨架构分析，声称能以极低成本发现不同类型的结构性失败模式。

## Problem
- LLM 代理的 system prompt 实际上决定代理行为，但不像传统软件那样有类型检查、lint 或测试；内部自相矛盾时，模型会“悄悄圆过去”，导致不稳定和不可审计的行为。
- 让同一个执行 prompt 的 LLM 来审计 prompt 本身不可靠，因为它会用自身启发式掩盖冲突；这对代码代理尤其重要，因为 prompt 控制工具使用、状态管理、工作流和安全边界。
- 现有研究多关注提示工程或 prompt injection，而不是 system prompt 自身作为软件架构时的内部一致性与组合缺陷。

## Approach
- Arbiter 分两阶段：**directed evaluation** 先把 prompt 拆成带标签的块（层级、类别、语气、作用域），再用形式化规则检查块对之间的干扰，如 mandate/prohibition 冲突、作用域重叠、优先级歧义、隐式依赖、逐字重复。
- 为避免穷举成本，作者对规则加预过滤，把 Claude Code 上理论上的约 15,680 个块对-规则组合缩到 100–200 个相关检查。
- **undirected scouring** 则让多个不同 LLM 用非常开放的指令去“找有意思的问题”，每一轮继承前面轮次已发现的内容，鼓励后续模型探索新的区域；当连续 3 个模型都认为无需继续时停止。
- 核心思想是“外部审计 + 多模型互补”：不同模型带来不同分析偏差，因此不是求共识，而是利用差异发现单模型看不到的漏洞类别。
- 另外作者还构建了 prompt AST，把文档解析成结构树并做结构哈希/差分，用于量化 prompt 架构和跨版本变化。

## Results
- 跨三个代理的 undirected scouring 共得到 **152 个 findings**：Claude Code **116**、Codex CLI **15**、Gemini CLI **21**；收敛轮数分别为 **10/2/3**，总 API 成本仅 **$0.27**（其中分别约 **$0.236 / $0.012 / $0.014**）。
- 在 Claude Code 的 directed analysis 中，作者把 **56** 个块做人工分类，并标注出 **21** 个 interference patterns：**4** 个关键直接冲突、**13** 个作用域重叠、**2** 个优先级歧义、**2** 个隐式依赖；其中 **20/21（95%）** 被声称可静态检测。
- 严重度分布上，Claude Code 的 scourer 结果为 **34 curious (29%) / 36 notable (31%) / 34 concerning (29%) / 12 alarming (10%)**；Codex CLI 为 **3/7/5/0**；Gemini CLI 为 **4/9/6/2**。作者据此称更长、更单体化的 prompt 有更大的严重冲突表面积。
- 作者的核心经验结论是：**prompt architecture 与 failure class 强相关，但与 severity 不强相关**。单体式 Claude 更容易在子系统边界出现增长型冲突；扁平式 Codex 更一致但能力受限；模块化 Gemini 则在模块组合缝隙出现设计级 bug。
- Gemini CLI 上最强的案例是记忆压缩链路中的**结构性数据丢失**：`save_memory` 保存的偏好不会进入压缩后的 XML `state_snapshot`，作者称这意味着压缩发生时偏好会被“结构性保证删除”。论文还称 Google 后续独立提交并修复了相关压缩症状 bug，但**未修复其指出的 schema 级根因**。
- 方法论上，作者强调多模型确实发现了**类别上不同**的问题，而不只是更多问题；例如 Claude 偏结构/安全，Kimi 偏经济与资源耗尽，GLM 偏数据完整性。对 Claude Code，**116 个 findings 对应 107 个唯一类别**，被用来支撑“模型互补而非冗余”的主张。

## Link
- [http://arxiv.org/abs/2603.08993v1](http://arxiv.org/abs/2603.08993v1)
