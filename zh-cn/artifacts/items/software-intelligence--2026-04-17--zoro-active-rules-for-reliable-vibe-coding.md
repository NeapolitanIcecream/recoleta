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
Zoro 将 `AGENTS.md` 等规则文件从被动文本变成 AI 辅助编程过程中的主动控制。它把规则绑定到计划步骤，在所需规则得到证明前阻止流程继续，并让用户根据具体失败来修订规则。

## 问题
- 在 vibe coding 中，规则文件很常见，但随着会话推进，智能体经常不再遵守这些规则，因为规则只是作为静态上下文加载。
- 开发者很难看清哪些规则被应用了、是否被遵守，以及怎样改进薄弱或过时的规则。
- 这很重要，因为团队用这些规则来约束架构、工作流、UI 和安全；如果智能体跳过它们，开发者就得手动检查、修正并重复说明要求。

## 方法
- Zoro 在 Codex、Claude Code、Cline 和 Cursor 等现有编程智能体之上加入 **Enrich-Enforce-Evolve** 工作流。
- **Enrich：** 智能体生成初始计划后，Zoro 将规则匹配到具体的计划步骤，并且可以拆分或改写步骤，把规则附着到真正相关的位置。
- **Enforce：** 在执行过程中，智能体必须调用 Zoro CLI 命令来标记步骤进度，并提交每条必需规则已被遵守的证明；对于可测试的规则，它还必须先提供单元测试，才能继续。
- **Evolve：** 用户在 UI 中查看规则证据，在规则应用不当时直接添加现场备注，Zoro 再借助 LLM 汇总这些备注并细化规则集。
- 该系统通过 `ZORO.md` 指令文件和共享的 `.zoro` 目录实现与智能体无关，后者存储增强后的计划、规则元数据、证据和用户备注。

## 结果
- 论文报告称，与标准 vibe coding 相比，Zoro 使 **规则遵守率提高了 57%**。
- 技术评估覆盖 **36 次 vibe coding 会话**，称 Zoro 在 **保持功能完成能力** 的同时，相比标准编程智能体提高了规则遵守情况。
- 用户研究包含 **12 名参与者**，报告称人们控制智能体的方式发生了变化：用户从 prompt engineering 转向了 rule engineering。
- 前期设计研究包括 **10 次程序员访谈**，以及对 **3 名程序员** 的观察，每次会话持续 **2-3 小时**。
- 摘要未提供指标定义、数据集名称、方差，或除 57% 相对提升之外的确切基线分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15625v1](http://arxiv.org/abs/2604.15625v1)
