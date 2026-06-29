---
source: arxiv
url: https://arxiv.org/abs/2605.17558v1
published_at: '2026-05-17T17:38:17'
authors:
- Yuxuan Lu
- Ziyi Wang
- Yingzhou Lu
- Yisi Sang
- Jiri Gesi
- Xianfeng Tang
- Yimeng Zhang
- Zhenwei Dai
- Hui Liu
- Hanqing Lu
- Chen Luo
- Qi He
- Benoit Dumoulin
- Jing Huang
- Dakuo Wang
topics:
- tool-calling-agents
- verified-data-generation
- mcp-servers
- offline-rl
- api-simulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs

## Summary
## 总结
FireFly 先执行真实的 MCP API，再根据观察到的输出编写任务，从而生成可验证的工具调用训练数据。论文声称，基于这批数据进行 RL 后，一个 4B 模型在留出的工具调用测试集上接近 Claude Sonnet 4.6 的表现。

## 问题
- 工具调用代理需要轨迹，其中中间 API 调用正确，最终答案也能检查，但人工标注成本高，而且很难覆盖大量 API。
- 许多合成数据集会先生成用户任务，而在此之前并没有已知可达结果，这会产生不可执行的调用、过时响应，或没有执行来源的标签。
- 真实 API 会变化、失败并触发速率限制，因此直接在真实服务器上反复做 RL rollout 很难复现。

## 方法
- FireFly 从 Smithery 抓取 MCP 服务器，然后筛选出无状态、无需用户认证、JSON schema 清晰且行为不平凡的工具。筛选后剩下 240 个服务器和 993 个工具。
- 它构建一个有向工具图，其中由 LLM 判断的边表示一个工具的输出可以作为另一个工具的输入。这个图大约有 83K 条有向边，其中 64K 条是中等或更高置信度的边。
- 一个强 LLM 在这个图采样出的子 DAG 中探索真实 API，生成可执行的工具调用 DAG，并记录工具名、参数、输出和数据流边。
- 任务生成器从已观察到的输出反向生成：在正确值已经出现在已执行的工具结果中之后，再写自然语言任务和结构化答案 schema。
- 检索增强模拟器缓存所有观察到的调用，并返回精确的缓存输出、带有 LLM 辅助的模糊检索输出，或对未见过的工具返回错误。随后 RL 使用离线 GRPO，并结合字段匹配和 LLM 评判得到二元奖励。

## 结果
- 数据集包含 5,144 个已验证任务和 9,749 条轨迹，覆盖 240 个服务器和 993 个工具。训练集用 4,944 个任务，测试集用 200 个任务。
- 任务统计包括平均 3.0 次工具调用、1–10 次调用范围、平均 4.6 个答案字段、77.0% 的中等难度任务，以及 38.5% 的多服务器任务。
- 在 FireFly 测试集上，Qwen3-4B 经过 FireFly RL 后，pass@1 从 28.1% 提升到 41.5%，提升 13.4 个百分点。pass@16 从 43.0% 提升到 57.0%。
- 训练后的 4B 模型在 pass@1 上接近 Claude Sonnet 4.6，分别为 41.5% 和 42.2%；在 pass@8 上超过它，分别为 52.8% 和 50.3%。
- 公共基准的提升包括：Tau2-Bench Retail 从 0.491 到 0.627，Airline 从 0.365 到 0.525，Telecom 从 0.189 到 0.204，MCP-Atlas 从 19.4% 到 26.0%，MCPMark File System 从 40.0% 到 60.0%，Postgres Easy 从 70.0% 到 80.0%，Postgres Std 从 9.5% 到 13.3%。
- 在完整训练过程中，模拟器调用中 42.2% 为精确匹配，57.8% 为模糊匹配，0% 为无数据。数据集生成大约用了 23.5B 个 token，成本约为 47K 美元。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17558v1](https://arxiv.org/abs/2605.17558v1)
