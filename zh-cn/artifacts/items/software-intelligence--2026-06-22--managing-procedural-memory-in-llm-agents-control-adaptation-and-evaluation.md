---
source: arxiv
url: https://arxiv.org/abs/2606.23127v1
published_at: '2026-06-22T10:14:11'
authors:
- Julia Belikova
- Rauf Parchiev
- Evgeny Egorov
- Grigorii Davydenko
- Gleb Gusev
- Andrey Savchenko
- Maksim Makarenko
topics:
- llm-agents
- procedural-memory
- agent-benchmarks
- skill-transfer
- software-engineering
- enterprise-workflows
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation

## Summary
## 摘要
AFTER 是一个包含 382 个任务的基准，用于测试 LLM 智能体的程序性记忆能否在任务、角色和模型骨干之间变成可复用的技能知识。论文发现，技能更新可以提高工作场景智能体的准确率并降低 token 成本，但范围过窄的更新可能过拟合到某个角色或模型。

## 问题
- LLM 智能体经常重复执行工作流程，例如编辑电子表格、查询数据库、处理 PDF、配置基础设施和编写测试，因此可复用的程序性记忆可以减少反复试错。
- 现有智能体基准通常只在一个设置中衡量任务完成情况，没有把本地改进与跨任务、跨角色或跨模型骨干的迁移区分开。
- 这对生产环境智能体很重要，因为只在学习场景中有效的技能会增加维护成本，并在用户、工作流或模型变化时失效。

## 方法
- 作者构建了 AFTER，包含 382 个真实企业任务、6 个专业角色和 22 种程序性技能，覆盖文档、数据操作、ML/AI、基础设施和软件工程。
- 每个任务都有固定的技能标注，使基准可以在不混入检索错误的情况下测试技能质量。
- 他们评估两个属性：特异性，即在来源上下文中的改进；通用性，即迁移到留出任务、其他角色或其他模型的能力。
- 技能以带版本的 `SKILL.md` 工件存储。演化过程会收集执行轨迹、诊断失败、修订技能文本，并提升或回滚版本。
- 实验比较了无技能提示、人工编写技能、LLM 生成技能、一轮细化，以及几种基于轨迹的记忆更新系统。

## 结果
- AFTER 包含 382 个任务：318 个单技能任务和 64 个多技能工作流，覆盖 6 个角色和 22 种技能。
- 与无技能基线相比，静态程序性技能使全通过准确率平均提高 +2.8 个百分点；表 2 中列出的模型，单个聚合增益范围为 +0.4 到 +5.3 个百分点。
- 一轮 LLM 引导的细化在不同模型规模上带来 +3.7 到 +6.7 的聚合 M2 分数提升，论文报告的平均增益为 +5.2 个百分点。
- 当技能由多样化的多模型轨迹演化而来时，跨模型迁移最强：测试准确率为 73.1%，而单模型轨迹来源为 36.0% 到 59.4%，比最佳单模型来源至少高 +13.7 个百分点。
- 在使用 Qwen3.5-35B-A3B 对 pdf、xlsx 和 pptx 任务进行框架引导演化时，Hermes 在多样化轨迹下获得 +18.0 的测试 M1 增益；一些方法虽然训练增益较大，但测试准确率下降，例如 EvoSkill 在窄轨迹下训练增益为 +14.9、测试变化为 -2.7。
- 跨角色迁移可能造成损害：对于 pdf 技能，角色内演化为 PM 带来 +11.7 个百分点、为 DS 带来 +6.2 个百分点的增益，而在这两个角色之间迁移演化后的技能会损失 -4.8 到 -7.5 个百分点。在一个 Kafka Lag Anomaly Detection 任务上，演化后的技能使 Claude 减少 326k tokens、使 Hermes 减少 48k tokens。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23127v1](https://arxiv.org/abs/2606.23127v1)
