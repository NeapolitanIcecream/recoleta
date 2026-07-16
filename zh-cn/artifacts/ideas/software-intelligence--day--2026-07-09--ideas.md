---
kind: ideas
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent harnesses
- test-time adaptation
- long-horizon evaluation
- repository verification
- small language models
tags:
- recoleta/ideas
- topic/agent-harnesses
- topic/test-time-adaptation
- topic/long-horizon-evaluation
- topic/repository-verification
- topic/small-language-models
language_code: zh-CN
---

# 代理工作流优化与验证

## 摘要
代理团队可以通过针对有界工作流调整控制程序来降低推理成本，通过基于轨迹的 harness 修改改善部署后的行为，并通过检查点级评分诊断长时间运行。每项改动都需要可执行的上线测试，因为代理指标、工作负载多样性和超时可能扭曲总体成功率。

## 小模型工作流迁移的 Harness 适配门槛
运行预算审批等重复性工作流的团队，应先用特定于任务的 harness 测试小型语言模型，再决定是否承担前沿模型的推理成本。Harness 优化器可以检查失败轨迹，并修改指令、工具可用性、上下文选择、钩子和编排循环。在报告的预算审批任务中，经过适配的 Gemma-4-26B-A4B 配置准确率达到 98.3%，高于默认 harness 的 75.0%，也高于报告中的 Gemini-3.1-Pro 的 97.3%。在 21 个任务-模型组合中，适配提升了其中 16 个的表现，并在 7 个组合中消除了测得的差距。

实际的采用门槛可以是一组来自单个高流量工作流的回放样本，并按实例多样性和操作边界情况进行划分。比较前沿模型代理、使用当前 harness 的小模型，以及经过适配的小模型代理在任务准确率、契约违规、延迟和每个完成案例的成本上的表现。对于超出已验证工作流范围的案例，保留前沿模型作为回退方案。研究发现，重复性任务和能力更强的小模型获得的收益更大，因此在将节省成本的估算用于容量规划前，需要使用多样化的留出集进行验证。

### 资料来源
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): 报告了优化器设计、21 个任务-模型组合的结果、预算审批对比、成本降低情况，以及与任务多样性和基础模型能力相关的限制。
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): 介绍了预算审批 harness 的具体变化：计划骨架、精简工具集，以及通过钩子强制执行约束。

## 基于无标签执行轨迹的影子模式 Harness 更新
代理运营人员可以利用 SQL、编码和数据工作流已经产生的轨迹，以影子模式运行候选 harness 修改。每个分支都应记录提示词、工具调用、输出、运行时错误、产物和恢复决策。提议器修改可执行 harness；选择器根据执行健康度、往返一致性或公开测试结果为候选方案评分。上线前应使用单独的带标签金丝雀集，因为这些代理指标可能会选出更差的分支。

TTHE 展示了在模型参数冻结时可能获得的收益：在 DeepSeek-V4-Flash 上，BIRD 从 12.0% 提升到 50.0%，SWE-bench Verified 从 20.0% 提升到 35.0%。同一组实验还发现了选择遗憾、评审器错误、候选覆盖有限，以及扩大搜索预算后收益不单调等问题。因此，初始部署可以限制分支数量和计算资源，保留每个代码差异，并只在代理指标和金丝雀结果同时改善时上线。由于适配后的状态就是 harness 程序，回滚可以按普通代码发布处理。

### 资料来源
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): 详细说明了 TTHE 的分支机制、轨迹收集、基于代理指标的选择、基准测试收益和已记录的选择限制。
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): 将 harness 定义为负责上下文构建、工具使用、验证和失败恢复的可执行代码，并介绍了根据无标签轨迹进行的持久化测试时更新。

## 长时间运行终端代理的检查点级评分
评估终端代理的开发人员应为有意义的中间状态添加可执行评分器，包括环境设置、产物创建、测试完成、模式有效性和最终验证。除了记录耗时、回合数、token 使用量、重试次数和最后一个已验证状态，还应按检查点记录奖励。这样可以区分早早停滞、取得实质进展，以及完成工作却未通过最终验证的代理。

Long-Horizon-Terminal-Bench 发现，690 次运行中有 433 次获得了部分奖励，其中 180 次的奖励达到 0.5 或更高。共有 73 次运行的得分在 0.75 到 0.95 之间，而在 0.95 阈值下完全通过的运行只有 30 次。未解决运行中有 79% 由超时导致；一次平均运行消耗 990 万个 token、231 个回合，并持续 85.3 分钟。一个成本较低的初步检查方法是，将 5 个有代表性的内部任务拆分为加权检查点，并在现有时间限制下重新运行当前代理。生成的轨迹可以显示工程工作应优先投入规划、状态恢复、验证还是运行时预算。

### 资料来源
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): 提供了部分奖励的分布、接近完成的运行次数、超时占比，以及 token、回合数和运行时长的平均测量值。
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): 介绍了该基准测试的细粒度评分子任务，以及针对未完成长时工作流的密集中间奖励。
