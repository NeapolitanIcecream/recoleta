---
source: arxiv
url: http://arxiv.org/abs/2603.05553v1
published_at: '2026-03-05T04:58:38'
authors:
- Jiaao Chen
- Jingyuan Qi
- Mingye Gao
- Wei-Chen Wang
- Hanrui Wang
- Di Jin
topics:
- function-calling
- synthetic-data
- multi-agent-systems
- benchmark-repair
- evaluation-metrics
relevance_score: 0.12
run_id: materialize-outputs
---

# EigenData: A Self-Evolving Multi-Agent Platform for Function-Calling Data Synthesis, Auditing, and Repair

## Summary
EigenData 是一个面向函数调用智能体数据的多智能体平台，覆盖数据库构建、可执行环境生成、轨迹合成、审计与修复的全流程。论文重点展示其对 BFCL-V3 基准的系统性审计与修复，并提出更贴近真实任务成功的 outcome-aware 评测。

## Problem
- 函数调用智能体需要高质量、领域化、可执行的数据，但人工构建数据库、工具实现和多轮轨迹既昂贵又易出错。
- 现有合成数据/基准常有三类问题：函数 schema 或实现有 bug、用户意图与标注存在歧义、评测只看逐轮函数匹配而不看任务结果是否真的正确。
- 这些问题会误导训练和模型选择：模型可能“调用格式对了”，却没有把数据库状态改对，也没有真正完成用户目标。

## Approach
- 核心方法是一个由 **EigenCore** 协调的多智能体平台，把数据生命周期拆成三块：**DatabaseAgent** 生成真实且一致的领域数据库，**CodingAgent** 生成并测试可执行工具/环境，**DataAgent** 生成和优化多轮函数调用轨迹。
- 系统的关键机制是“生成→测试→调试→再生成”的自演化闭环：代码侧用单元测试、集成测试和 judge 做故障归因；数据侧用评审与程序化验证不断修正提示词和样本。
- 各组件之间有交叉反馈：下游若发现 schema、代码、数据库或轨迹不一致，EigenCore 会把结构化反馈发回上游，只修复相关部分而不是整条流水线重跑。
- 在 BFCL-V3 案例中，EigenData 不只是生成新数据，还会审计已有 benchmark，定位并自动修复函数 schema、实现、参考轨迹和用户意图中的系统性错误。
- 论文还提出 outcome-aware evaluation：不再主要比较逐轮轨迹是否与参考答案完全一致，而是检查最终数据库状态、关键函数调用和关键信息处理是否正确。

## Results
- 论文声称 EigenData 成功**系统性识别并自动修复** BFCL-V3 中的 schema、实现、参考轨迹与用户意图错误，但摘录中**未提供具体修复数量或比例**。
- 论文声称修复后的 benchmark 加上 outcome-aware 指标，得到的模型排序与**人工对功能正确性的判断相关性显著更高**，但摘录中**未给出相关系数或具体数值**。
- 论文明确指出，新评测会导致与原始 BFCL-V3 **“显著不同”的模型排名**，说明传统 turn-level match 可能掩盖真实功能失败；但摘录中**没有列出具体模型名次变化数字**。
- 架构层面给出了一套可落地系统：支持从零生成数据库、环境和轨迹，也支持只对现有基准做审计/修复，并已发布 CLI 与修复版 BFCL-V3 代码仓库。
- 量化结果方面，当前提供文本中**没有可引用的明确实验数字、数据集规模、提升幅度或与具体 baseline 的百分比比较**。

## Link
- [http://arxiv.org/abs/2603.05553v1](http://arxiv.org/abs/2603.05553v1)
