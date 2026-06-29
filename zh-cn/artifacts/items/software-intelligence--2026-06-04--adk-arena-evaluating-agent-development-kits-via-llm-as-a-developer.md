---
source: arxiv
url: https://arxiv.org/abs/2606.05548v1
published_at: '2026-06-04T01:00:54'
authors:
- Jintao Huang
- Xiaomin Li
- Gaurav Mittal
- Yu Hu
topics:
- agent-development-kits
- llm-as-developer
- code-intelligence
- software-agents
- benchmarking
- multi-agent-systems
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# ADK Arena: Evaluating Agent Development Kits via LLM-as-a-Developer

## Summary
## 摘要
ADK Arena 通过让同一个 LLM 代码代理为每个工具包构建基准代理，自动比较 51 个 Python Agent Development Kits。论文把生成成本当作 API 可用性的信号，把任务表现当作代理效果的衡量。

## 问题
- 开发者有很多 ADK 可选，但缺少关于哪些工具包能生成更好的代理、或降低开发成本的实证证据。
- 手工实现基准扩展性差：51 个框架跨 4 个基准需要 204 个专家编写的代理实现，还可能让结果偏向熟悉的 API。
- 现有代理基准多半是在固定 ADK 的情况下比较模型；开发者调研报告的是观点，而不是运行时行为。

## 方法
- 核心方法是 LLM-as-a-Developer：一个编码代理读取每个 ADK 的文档和源代码，编写带有 `solve(prompt, workdir)` 的 `agent.py` 文件，并在验证反馈后修复它。
- ADK Arena 在隔离的 Docker 镜像中运行每个框架，使用相同的提示、工具和预算，因此主要变量是 ADK 本身。
- 验证分三层：针对导入和框架使用的静态检查、一次真实 LLM 烟雾测试，以及一个真实基准任务和早停成功检查。
- 系统在 SWE-bench Verified、$\tau^2$-bench、Terminal-Bench 和 MCP-Atlas 上评估生成的代理，并用代理转发和测量 LLM 调用。

## 结果
- 这项研究覆盖 51 个 Python ADK 框架和 204 个代理-基准配对。
- 代理生成在 57% 的运行中成功。
- 生成成本在各框架之间相差 5.6 倍，每个生成的代理从 0.6 美元到 3.4 美元不等。
- 单一基准上表现最好的 ADK 代理能解决最多 80% 的任务，而中位数框架能解决 32%。
- 论文指出，一些 ADK 代理比通用前沿编码代理成本更低，表现更好。
- 信息来源消融显示，真实的框架使用率保持在 28% 到 40% 之间；即使没有任何参考材料，也有 33%，说明文档、源代码和模型先验知识常常可以互相替代。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05548v1](https://arxiv.org/abs/2606.05548v1)
