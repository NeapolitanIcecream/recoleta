---
source: arxiv
url: https://arxiv.org/abs/2605.16909v1
published_at: '2026-05-16T09:49:25'
authors:
- Zhiqiang Liu
- Wenhui Dong
- Yilang Tan
- Yuwen Qu
- Haochen Yin
- Chenyang Si
topics:
- tool-using-agents
- multimodal-benchmark
- mcp-tools
- agent-evaluation
- closed-loop-verification
- computer-use-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents

## Summary
## 摘要
TOBench 是一个面向智能体的基准和执行框架，这些智能体需要使用工具、处理多模态输入、检查生成的产物，并在最终提交前修正错误。论文称，当前模型在这些工作流上的表现仍远低于人类。

## 问题
- 现有工具使用和多模态基准通常把 API 调用、GUI 使用、感知或最终答案作为分离的技能来测试。
- 真实工作任务可能要求读取图像、文档、音频或视频，编辑文件，使用 MCP 工具，渲染输出，并检查结果是否符合任务规则。
- 这一点很重要，因为智能体在单项测试中可能看起来有能力，但在工具执行、多模态推理和自检需要协同工作时会失败。

## 方法
- TOBench 包含 100 个可执行任务，覆盖 2 个任务族：Customer Service 有 67 个任务，Intelligent Creation 有 33 个任务。
- 该基准覆盖 20 个子类别切片，并把智能体连接到 27 个 MCP 服务器上的 324 个工具。
- 每个任务向智能体提供用户请求、角色、领域规则、输入资产、可用工具、工作区状态和特定任务的验证器。
- 核心机制是闭环多模态验证：智能体使用工具，查看产物或工具输出，判断其是否满足任务要求，并在需要时修改。
- 评估使用特定任务的有依据检查器，结合格式检查、代码检查、工具日志检查、实时或时间敏感工具检查，以及基于 VLM 的检查。

## 结果
- 在全部 100 个任务上，报告中表现最好的模型是 Qwen3.5-Plus，任务成功率为 41.0%，人类基准为 94.0%。
- 闭源模型中的最佳结果是 Claude-Opus-4.6 和 Gemini-3-Pro，平均任务成功率为 32.0%。
- 困难任务大多仍未解决：Customer Service-Hard 的最高分为 20.00%，Intelligent Creation-Hard 的最高分为 15.38%。
- GPT-5 的平均成功率为 26.80%，GPT-5.2 为 22.00%，GPT-4o 为 6.12%。
- Qwen3.5-Plus 平均每个任务调用工具 25.0 次，使用 559.1k tokens，成本为 $0.17；Gemini-3.1-Pro 平均每个任务调用工具 21.5 次，使用 1506.6k tokens，成本为 $3.03。
- 论文报告了常见失败模式，涉及工具调用、工具参数、多模态推理，以及停止前缺少自我验证。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.16909v1](https://arxiv.org/abs/2605.16909v1)
