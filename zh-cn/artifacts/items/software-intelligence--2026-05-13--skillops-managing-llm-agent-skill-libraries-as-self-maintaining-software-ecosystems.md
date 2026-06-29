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
SkillOps 在任务执行前维护 LLM 代理的技能库，识别过时、重复、不安全和不兼容的技能。在 ALFWorld 上，它的任务成功率高于多个检索、规划、图和自修复基线，同时在库维护阶段几乎不增加 LLM 成本。

## 问题
- LLM 代理会在多步任务中复用技能库，但这些技能库会累积持久性缺陷，例如冗余技能、缺失验证器、过时实现和接口漂移。
- 任务时修复可以修好一次失败的回合，但损坏的技能仍留在库里，因此同样的缺陷会影响后续检索、组合或执行。
- 这会影响自动化软件生产和面向代码的代理，因为不断增长的技能库会像需要维护的软件一样运行：损坏的接口和未验证的输出会把失败扩散到各个工作流。

## 方法
- 每个技能都存为一个带类型的契约 `(P,O,A,V,F)`：前置条件、可执行操作、生成的制品、验证器和已知失败模式。
- SkillOps 构建一个分层技能生态图，连接技能之间的依赖、兼容、冗余和替代关系。
- 库维护阶段会从效用、冗余、兼容性、失败风险和验证缺口几个维度给库打分，然后执行 `merge`、`repair`、`retire`、`add_validator` 和 `add_adapter` 等带类型的动作。
- 在任务时，其可选规划器用 BM25 加语义评分检索技能，按前置条件过滤，只通过依赖和兼容边拼接计划，插入验证器或适配器，并在失败后尝试局部修复。
- 插件路径很直接：`run_maintenance(raw_library)` 返回一个清理后的库，现有检索或规划代理可以直接使用，不需要改代码。

## 结果
- 在带有 200 个技能的 ALFWorld 上，SkillOps_Full 的任务成功率达到 79.5%，Wilson 95% 置信区间为 [75.9, 82.6]；对比对象分别是 LLM_Skill_Planner 的 70.6%、GoS_Style 的 61.1%、Hybrid_Retrieval 的 58.2%、SkillWeaver 的 50.3% 和 ReAct 的 12.8%。
- 相比表 1 中最强的基线 LLM_Skill_Planner，SkillOps 的任务成功率高出 8.9 个百分点；摘要里写的是 8.8 个百分点。
- 作为 200 技能规模下的即插即用维护层，它把 Hybrid Retrieval 从 38.2% 提高到 41.1%（+2.90pp），把 BM25 Only 从 41.8% 提高到 42.8%（+1.00pp），把 Dense Only 从 32.3% 提高到 33.4%（+1.12pp），把 GoS Style 从 42.8% 提高到 43.6%（+0.80pp），把 LLM Skill Planner 从 49.8% 提高到 50.3%（+0.50pp），把 SkillWeaver 从 41.3% 提高到 43.8%（+2.46pp）；ReAct 保持在 11.9%。
- 论文报告称，在最多 2,000 个技能的不同库规模下，库维护阶段的 LLM 调用几乎为零。
- 任务时 token 使用量在 35 个测量单元里有 24 个下降，4 个几乎不变，7 个上升；报告中的最大降幅是库规模 1,000 时 Dense_Only 的 -3.95%，最大增幅是库规模 500 时 BM25_Only 的 +5.56%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13716v1](https://arxiv.org/abs/2605.13716v1)
