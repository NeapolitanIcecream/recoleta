---
source: arxiv
url: https://arxiv.org/abs/2606.25819v1
published_at: '2026-06-24T13:34:34'
authors:
- Yang Tian
- Zhengpeng Shi
- Bo Zhao
topics:
- tool-using-agents
- agent-benchmarks
- unreliable-tools
- recovery-evaluation
- llm-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability

## Summary
## 摘要
ToolBench-X 测试大语言模型代理在工具失败、漂移或相互矛盾时，能否完成多步骤工具任务。论文发现，当前代理经常在可恢复风险上失败，原因是它们误判工具问题，并选择了效果较弱的恢复动作。

## 问题
- 现有工具使用基准常在干净环境中给正确函数调用打分，但真实工具会出现文档过时、字段改名、超时、输出格式变化和来源冲突。
- 这一点很关键，因为代理即使调用了正确函数，如果信任不完整、偏移或相互矛盾的工具输出，仍会给出错误最终答案。
- 基准需要可恢复风险，这样失败才能对应到诊断、验证和恢复行为。

## 方法
- 作者构建了 ToolBench-X，包含 1,106 个可执行任务和 4,956 个 Python 工具，覆盖 7 个领域。每个任务都有确定性工具和标准最终答案，用于自动评测。
- 任务工作流分布均衡：378 个顺序任务（34.2%）、358 个并行任务（32.4%）和 370 个混合任务（33.5%）。
- 他们注入了 5 种可恢复风险类型：Specification Drift 141 个（12.7%）、Invocation Error 173 个（15.6%）、Execution Failure 265 个（24.0%）、Output Drift 264 个（23.9%）和 Cross-source Conflict 263 个（23.8%）。
- 每个注入后的任务都保留至少 1 条有效恢复路径，例如重试、使用备用工具、规范化输出、检查证据或解决来源冲突。
- 他们用最终任务准确率评测 12 个大语言模型，匹配方式为后端执行状态匹配或显式标准答案匹配。

## 结果
- 在 ToolBench-X 上，没有被评测模型的总体准确率达到 0.60。最佳模型是 Doubao-Seed-2.0-Lite，准确率为 0.513；之后是 GPT-5.4 的 0.453、DeepSeek-V4-Pro 的 0.425、GLM-5.1 的 0.420、Qwen-3.5-35B-A3B-Thinking 的 0.419，以及 Gemini-3.1-Flash 的 0.416。
- Qwen-3.5-35B-A3B-Thinking 得分为 0.419，高于 GPT-4o 的 0.359；相比 Qwen-3.5-35B-A3B 的 0.372，绝对准确率提高 0.047。
- 并行任务平均最容易，准确率为 0.421。论文报告称，顺序依赖比并行调用更容易造成错误累积。
- Output Drift 是最容易的风险，平均准确率为 0.581。Invocation Error 最难，平均准确率约为 0.260，差距约为 0.321。
- 在第一次工具响应失败后，代理在 44% 到 76% 的轨迹中会重试同一个工具，而直接终止保持在 12% 以下。高重试率与总体准确率并不一致，因此失败点在于诊断和恢复选择。
- 在一个包含 200 个任务的诊断子集上，干净工具 Oracle 准确率比注入异常的基线高 35 到 50 个百分点。定向提示使准确率提高 25.5 到 35.5 个百分点，并恢复约 60% 到 80% 的损失准确率；没有提示的 10 轮额外交互帮助较小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25819v1](https://arxiv.org/abs/2606.25819v1)
