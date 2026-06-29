---
source: arxiv
url: http://arxiv.org/abs/2604.15625v1
published_at: '2026-04-17T02:06:55'
authors:
- Jenny Ma
- Sitong Wang
- Joshua H. Kung
- Lydia B. Chilton
topics:
- code-intelligence
- human-ai-interaction
- software-foundation-model
- automated-software-production
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ZORO: Active Rules for Reliable Vibe Coding

## Summary
## 摘要
Zoro 将 `AGENTS.md` 这类规则文件从被动文本变成 AI 辅助编码中的主动控制。它把规则绑定到计划步骤上，在必要规则被证明已遵守之前阻止进展，并让用户根据具体失败修改规则。

## 问题
- 在 vibe coding 中，规则文件很常见，但随着会话推进，代理往往不再遵守，因为规则只作为静态上下文加载。
- 开发者很难看出哪些规则被应用了、是否被遵守，以及如何改进薄弱或过时的规则。
- 这很重要，因为团队用这些规则来约束架构、工作流、UI 和安全要求；如果代理跳过这些规则，开发者就得手动检查、纠正并反复下达指令。

## 方法
- Zoro 在现有编码代理之上增加了一个 **Enrich-Enforce-Evolve** 工作流，适用于 Codex、Claude Code、Cline 和 Cursor 等工具。
- **Enrich：** 在代理生成初始计划后，Zoro 将规则匹配到具体的计划步骤，并且可以拆分或改写步骤，把规则放到真正相关的位置。
- **Enforce：** 在执行过程中，代理必须调用 Zoro CLI 命令来标记步骤进度，并提交证明，说明每条必需规则都已遵守；对于可测试的规则，它还必须在继续之前提供单元测试。
- **Evolve：** 用户在界面中查看规则证据，在规则应用不佳时添加现场备注，Zoro 再借助 LLM 汇总这些备注，改进规则集。
- 该系统通过 `ZORO.md` 指令文件和共享的 `.zoro` 目录实现与代理无关，目录中保存已增强的计划、规则元数据、证据和用户备注。

## 结果
- 论文报告称，与标准 vibe coding 相比，Zoro 的规则遵守率提高了 **57%**。
- 技术评估覆盖 **36 次 vibe coding 会话**，并指出与标准编码代理相比，Zoro 在提高规则遵守的同时**保持了完成功能的能力**。
- 用户研究包含 **12 名参与者**，结果显示人们控制代理的方式发生了变化：用户从提示工程转向规则工程。
- 前期设计工作包括 **10 次程序员访谈**，以及对 **3 名程序员** 的观察，每次会话持续 **2-3 小时**。
- 这段摘录没有给出指标定义、数据集名称、方差，或除 57% 相对提升之外的精确基线分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15625v1](http://arxiv.org/abs/2604.15625v1)
