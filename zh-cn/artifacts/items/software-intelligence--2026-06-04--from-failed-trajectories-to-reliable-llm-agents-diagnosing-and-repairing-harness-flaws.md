---
source: arxiv
url: https://arxiv.org/abs/2606.06324v1
published_at: '2026-06-04T15:58:30'
authors:
- Mengzhuo Chen
- Junjie Wang
- Zhe Liu
- Yawen Wang
- Qing Wang
topics:
- llm-agents
- agent-harnesses
- trace-diagnosis
- automated-repair
- software-engineering-agents
- multi-agent-systems
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws

## Summary
## 摘要
HarnessFix 通过追踪失败执行中的具体运行时步骤和 harness 层来修复 LLM agent 的 harness，再生成有范围限制的补丁。论文声称，在 SWE-Bench Verified、Terminal-Bench 2.0 Verified、GAIA 和 AppWorld 上，相比初始 harness，未见测试性能提升了 15.2%–50.0%。

## 问题
- LLM agent 的失败原因不只来自基础模型，还包括工具 schema、上下文组装、编排、日志、验证、沙箱和策略检查。
- 现有自我改进方法通常只根据最终分数优化提示词或工作流，因此可能改错 agent harness 的部分，或者做出范围过大的修改。
- 可靠修复很重要，因为面向长时程的软件工程、终端、研究和应用自动化 agent 依赖外部工具和状态变化，细小的 harness 缺陷就可能导致最终提交出错。

## 方法
- HarnessFix 将原始轨迹和 harness 代码转换为 HTIR，这是一种步骤级表示，包含请求/响应消息、角色、执行状态、工件或状态影响、来源链接和控制流链接。
- 一个诊断 agent 使用 HTIR 定位负责的 TraceStep，或多个 TraceStep，把它们映射到 ETCLOVG 层，并写入诊断记录。
- 在任何编辑之前，系统会把相似的诊断记录归并为重复出现的缺陷记录。
- 一个修复 agent 把每条缺陷记录映射到有范围限制的修复算子，例如参数验证、上下文刷新、带验证门控的最终化或状态差分日志。
- 一个验证 agent 会检查补丁是否保持在作用范围内、是否减少目标缺陷，以及是否避免不可接受的回归。

## 结果
- 在 4 个基准上，SWE-Bench Verified、Terminal-Bench 2.0 Verified、GAIA 和 AppWorld，HarnessFix 相比初始 harness 将未见测试性能提高了 15.2%–50.0%。
- 论文说 HarnessFix 优于人工设计的 harness 和自我进化基线，但摘要没有给出具体基线分数。
- 该方法使用 4 个协作的 LLM agent：轨迹抽象、诊断、修复和验证。
- 分析覆盖 ETCLOVG 分类法中的 7 个 harness 层：Execution、Tooling、Context、Lifecycle、Observability、Verification 和 Governance。
- 消融实验测试了仅靠提示词修复、基于轨迹的诊断、有范围限制的修复算子，以及考虑回归的接受策略；摘要说每个组件都有帮助，但没有给出消融数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06324v1](https://arxiv.org/abs/2606.06324v1)
