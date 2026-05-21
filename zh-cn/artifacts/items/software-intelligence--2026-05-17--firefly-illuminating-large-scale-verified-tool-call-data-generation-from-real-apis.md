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
## 摘要
FireFly 先执行真实 MCP API，再根据观测到的输出编写任务，用这种方式生成经过验证的工具调用训练数据。论文称，在这些数据上进行 RL 训练后，一个 4B 模型在其留出的工具调用测试中接近 Claude Sonnet 4.6 的表现。

## 问题
- 工具调用智能体需要包含正确中间 API 调用和可检查最终答案的轨迹，但人工标注成本高，也难以扩展到大量 API。
- 许多合成数据集会在已知可达结果出现之前生成用户任务，这可能产生不可执行的调用、过期响应，或没有执行来源的标签。
- 实时 API 会变化、失败并触发速率限制，因此很难在真实服务器上复现反复进行的 RL rollout。

## 方法
- FireFly 从 Smithery 抓取 MCP 服务器，然后筛选出无状态、无需用户认证、JSON schema 清晰且行为有一定复杂度的工具。筛选后保留 240 个服务器和 993 个工具。
- 它构建一个有向工具图，其中由 LLM 判断的边表示一个工具的输出可以输入另一个工具。该图约有 83K 条有向边，其中包括 64K 条中等或更高置信度的边。
- 一个强 LLM 在从该图采样的子 DAG 中探索实时 API，生成可执行的工具调用 DAG，并记录工具名称、参数、输出和数据流边。
- 任务生成器从观测到的输出反向工作：在正确值已经存在于已执行的工具结果之后，它编写自然语言任务和结构化答案 schema。
- 一个检索增强模拟器缓存所有观测到的调用，并返回精确缓存输出、在 LLM 帮助下模糊检索到的输出，或对未见工具返回错误。随后 RL 使用离线 GRPO，并通过字段匹配和 LLM 判断给出二元奖励。

## 结果
- 数据集包含来自 240 个服务器和 993 个工具的 5,144 个已验证任务和 9,749 条轨迹。其中 4,944 个任务用于训练，200 个用于测试。
- 任务统计包括平均 3.0 次工具调用、1–10 次调用范围、平均 4.6 个答案字段、77.0% 中等难度任务，以及 38.5% 多服务器任务。
- 在 FireFly 测试集上，Qwen3-4B 经过 FireFly RL 后，pass@1 从 28.1% 提升到 41.5%，增幅为 13.4 个百分点。pass@16 从 43.0% 提升到 57.0%。
- 训练后的 4B 模型在 pass@1 上接近 Claude Sonnet 4.6，分别为 41.5% 和 42.2%；在 pass@8 上超过它，分别为 52.8% 和 50.3%。
- 公开基准上的提升包括：Tau2-Bench Retail 从 0.491 到 0.627，Airline 从 0.365 到 0.525，Telecom 从 0.189 到 0.204，MCP-Atlas 从 19.4% 到 26.0%，以及 MCPMark File System 从 40.0% 到 60.0%，Postgres Easy 从 70.0% 到 80.0%，Postgres Std 从 9.5% 到 13.3%。
- 在完整训练运行期间，模拟器调用的解析结果为 42.2% 精确匹配、57.8% 模糊匹配、0% 无数据。数据集生成使用约 23.5B tokens，成本约 $47K。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17558v1](https://arxiv.org/abs/2605.17558v1)
