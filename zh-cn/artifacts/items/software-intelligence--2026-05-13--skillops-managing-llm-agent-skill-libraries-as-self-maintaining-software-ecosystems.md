---
source: arxiv
url: https://arxiv.org/abs/2605.13716v1
published_at: '2026-05-13T16:02:25'
authors:
- Hongji Pu
- Xinyuan Song
- Liang Zhao
topics:
- llm-agents
- skill-libraries
- code-intelligence
- agent-maintenance
- technical-debt
- software-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems

## Summary
## 摘要
SkillOps 在任务执行前维护 LLM 智能体技能库，检测过时、重复、不安全和不兼容的技能。在 ALFWorld 上，它报告的任务成功率高于多个检索、规划、图和自修复基线，同时库维护阶段的 LLM 成本近乎为零。

## 问题
- LLM 智能体复用技能库来完成多步任务，但这些库会积累持续性缺陷，例如冗余技能、缺少验证器、实现过时和接口漂移。
- 任务执行阶段的修复可以修好一次失败的 episode，但受损技能仍留在库中，同一缺陷之后仍可能影响检索、组合或执行。
- 这对自动化软件生产和面向代码的智能体很重要，因为不断增长的技能库会像需要维护的软件一样运行：损坏的接口和未经验证的输出会把失败传播到多个工作流。

## 方法
- 每个技能都存为类型化合约 `(P,O,A,V,F)`：前置条件、可执行操作、产出工件、验证器和已知失败模式。
- SkillOps 构建 Hierarchical Skill Ecosystem Graph，用依赖、兼容、冗余和替代边连接技能。
- 库维护阶段会按效用、冗余、兼容性、失败风险和验证缺口给健康度打分，然后应用类型化动作，例如 `merge`、`repair`、`retire`、`add_validator` 和 `add_adapter`。
- 在任务执行阶段，它的可选规划器用 BM25 加语义评分检索技能，按前置条件过滤，只通过依赖和兼容边拼接计划，插入验证器或适配器，并在失败后尝试局部修复。
- 插件路径很简单：`run_maintenance(raw_library)` 返回清理后的库，现有检索或规划智能体无需改代码即可使用。

## 结果
- 在使用 200 个技能库的 ALFWorld 上，SkillOps_Full 达到 79.5% 的任务成功率，Wilson 95% CI 为 [75.9, 82.6]；相比之下，LLM_Skill_Planner 为 70.6%，GoS_Style 为 61.1%，Hybrid_Retrieval 为 58.2%，SkillWeaver 为 50.3%，ReAct 为 12.8%。
- 相比表 1 中最强的基线 LLM_Skill_Planner，SkillOps 的任务成功率提高 +8.9 个百分点；摘要报告为 +8.8 个百分点。
- 作为 200 个技能规模下的即插即用维护层，它将 Hybrid Retrieval 从 38.2% 提升到 41.1%（+2.90pp），BM25 Only 从 41.8% 提升到 42.8%（+1.00pp），Dense Only 从 32.3% 提升到 33.4%（+1.12pp），GoS Style 从 42.8% 提升到 43.6%（+0.80pp），LLM Skill Planner 从 49.8% 提升到 50.3%（+0.50pp），SkillWeaver 从 41.3% 提升到 43.8%（+2.46pp）；ReAct 保持在 11.9%。
- 论文报告，在技能库规模最高 2,000 个技能时，库维护阶段的 LLM 调用近乎为零。
- 在 35 个测量单元中，任务执行阶段的 token 使用量有 24 个下降，4 个几乎不变，7 个上升；报告的最大降幅是库规模 1,000 时 Dense_Only 的 -3.95%，最大增幅是库规模 500 时 BM25_Only 的 +5.56%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13716v1](https://arxiv.org/abs/2605.13716v1)
