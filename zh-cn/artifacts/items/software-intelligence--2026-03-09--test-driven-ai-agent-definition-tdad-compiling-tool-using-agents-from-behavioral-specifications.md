---
source: arxiv
url: http://arxiv.org/abs/2603.08806v1
published_at: '2026-03-09T14:04:54'
authors:
- Tzafrir Rehan
topics:
- llm-agents
- test-driven-development
- prompt-compilation
- behavioral-specification
- mutation-testing
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications

## Summary
TDAD把“做一个可用的工具型智能体”变成类似测试驱动开发的编译流程：先把行为规格转成测试，再反复改提示词直到通过测试。它的目标是让生产级智能体的合规性、回归安全和测试强度都能被量化，而不再依赖人工抽查。

## Problem
- 生产中的LLM工具智能体很难**验证是否真正符合规格**：小的提示词改动可能导致静默回归、错误用工具、泄露敏感信息或违反流程。
- 现有做法多靠手工试错和抽样检查，**缺少像软件工程那样可接入CI/CD的可执行行为契约**。
- 一旦把测试作为优化目标，又会出现**specification gaming**：智能体可能学会“过测试”而不是真的满足需求。

## Approach
- 把智能体开发视为“编译”：输入是YAML规格（工具、策略、决策树、响应契约等），输出是编译后的提示词和工具描述。
- 用两个编码代理协作：**TestSmith**先把规格转成可执行测试；**PromptSmith**根据可见测试失败反复最小化修改提示词，直到通过。
- 为防止“只会刷题”，引入三种机制：**visible/hidden test split**（只用可见测试编译，隐藏测试只评估泛化）、**semantic mutation testing**（生成有意出错但看似合理的提示词变体，看测试能否抓住）、**spec evolution**（v1→v2需求变化后，用隐藏的旧版不变量测试衡量回归安全）。
- 测试尽量确定性：使用固定fixture、脚本化多轮对话、结构化`respond`工具和工具调用轨迹断言，而不是依赖LLM裁判打分。
- 在 **SpecSuite-Core** 上评估，该基准含4个深规格化场景：SupportOps、DataInsights、IncidentRunbook、ExpenseGuard。

## Results
- 在 **24次独立试验**（4个规格 × 2个版本 × 3次）中，TDAD报告 **v1编译成功率 92%**，**v2编译成功率 58%**。
- 对成功运行，平均 **隐藏测试通过率(HPR)** 为 **v1 97%**、**v2 78%**，说明在仅见可见测试的情况下仍有一定泛化能力，但规格演化后的难度明显更高。
- **语义变异得分(MS)** 达到 **86%–100%**，表明可见测试通常能杀死大部分“看似合理但行为错误”的提示词变体；文中还提到跨实验 **87% 的mutation intents能成功激活**，其余被排除为非激活变异。
- **规格更新回归安全分数(SURS)** 平均 **97%**，表示v2在不直接看到v1不变量测试的情况下，仍大体保留旧行为。
- 失败案例中，作者称**多数失败运行只差1–2个可见测试未过**，意味着流程常能接近完成但在复杂演化需求下仍会卡住。
- 基准规模方面，4个规格各有 **10–14个决策节点**；每个版本大致包含 **34–53个可见测试**、**42–45个隐藏测试**、**6–7个变异意图**（中位数，跨3次试验波动约±10–30%）。

## Link
- [http://arxiv.org/abs/2603.08806v1](http://arxiv.org/abs/2603.08806v1)
