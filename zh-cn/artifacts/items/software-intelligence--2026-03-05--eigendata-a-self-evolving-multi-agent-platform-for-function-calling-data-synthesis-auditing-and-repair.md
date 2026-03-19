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
- multi-agent-systems
- function-calling
- data-synthesis
- benchmark-repair
- outcome-aware-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# EigenData: A Self-Evolving Multi-Agent Platform for Function-Calling Data Synthesis, Auditing, and Repair

## Summary
EigenData 是一个面向函数调用型智能体的数据基础设施，用多智能体自动生成、审计、修复数据库、工具环境和多轮轨迹。论文重点展示它如何修复 BFCL-V3 基准，并提出更贴近真实任务成功与否的 outcome-aware 评测。

## Problem
- 函数调用智能体需要高质量、领域化训练数据，但人工构造数据库、工具实现和多轮轨迹成本高、速度慢、且难以保持全局一致性。
- 现有合成数据/基准常有系统性问题：函数 schema 或实现有 bug、用户意图含糊、参考轨迹不可靠，导致训练和评测信号失真。
- 传统按回合匹配函数调用的评测不一定反映任务是否真正完成；模型可能“调用看起来对”，但数据库状态和最终结果是错的。

## Approach
- 提出一个自演化多智能体平台，由顶层调度器 **EigenCore** 协调三个子系统：**DatabaseAgent** 生成真实一致的领域数据库，**CodingAgent** 生成并测试可执行工具/环境，**DataAgent** 合成并优化多轮函数调用轨迹。
- 系统是端到端的：从数据库 schema 与数据填充，到 API/环境代码，再到 SFT/RL 轨迹生成；各模块之间有交叉反馈，发现不一致时可定向回修，而不是整条流水线重跑。
- CodingAgent 采用“生成→单测→调试→集成测试”的双阶段闭环，并用 JudgeAgent 判断失败是代码错还是测试错，以提高自动生成环境的可靠性。
- DataAgent 采用分层多智能体生成和自演化提示优化：先在小规模 pilot 上根据评审反馈优化 prompt，再在大规模生成时持续质量监控与修正。
- 在案例中，EigenData 用于系统审计和修复 BFCL-V3：同时修正函数 schema、代码实现、参考轨迹和意图歧义，并新增 outcome-aware 评测，重点看数据库最终状态、关键函数调用和关键信息处理是否正确。

## Results
- 论文的核心实证结论是：**修复后的 BFCL-V3 + outcome-aware 指标** 能得到与人工对“功能正确性”判断**显著更一致**的模型排序；但摘录中**未给出具体相关系数、准确率或排名变化数值**。
- 作者声称 EigenData 能**系统性识别并自动修复** BFCL-V3 中的 schema、实现和参考轨迹错误，并对含糊意图进行消歧；但摘录中**没有提供错误数量、修复比例或覆盖率的定量统计**。
- 相比原始 BFCL-V3 的 turn-level function matching，新评测会关注**数据库状态是否正确变化**、**关键函数是否真正调用**、以及**关键信息是否被正确处理/传达**，从而暴露出“原评测看不见”的失败模式。
- 论文还提供了可用性产物：发布了 **corrected BFCL-V3** 数据与 **CLI**，支持数据生成、schema refinement、审计和修复；但摘录中**没有报告运行成本、吞吐量或人工节省比例**。

## Link
- [http://arxiv.org/abs/2603.05553v1](http://arxiv.org/abs/2603.05553v1)
