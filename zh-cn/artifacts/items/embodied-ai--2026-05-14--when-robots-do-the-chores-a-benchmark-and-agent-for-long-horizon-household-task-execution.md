---
source: arxiv
url: https://arxiv.org/abs/2605.14504v1
published_at: '2026-05-14T07:47:53'
authors:
- Zilin Zhu
- Longteng Guo
- Yanghong Mei
- Bowen Pang
- Zongxun Zhang
- Xingjian He
- Ruyi Ji
- Jing Liu
topics:
- long-horizon-planning
- embodied-ai-benchmark
- household-robots
- vision-language-agents
- multimodal-memory
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution

## Summary
## 摘要
LongAct 是一个用于自由形式、长时程家庭任务执行的基准，HoloMind 是面向该基准的 VLM 智能体。论文测试了规划、记忆和错误恢复能力，任务长度可能超过 2,000 个智能体步骤。

## 问题
- 现有具身 AI 基准大多测试短程导航或操作任务，因此无法覆盖跨房间、跨物体且包含依赖关系的多阶段家庭流程。
- LongAct 的意义在于，用户可能会提出桌面布置或厨房复位这类复合家务请求，这需要在长动作序列中跟踪状态、区分物体并重新规划。

## 方法
- LongAct 在 100 多个 ProcTHOR/AI2-THOR 房屋中设置 300 个 episode，覆盖四类家庭场景。每个任务包含自由形式指令，平均约 9 个目标，提供 RGB-D 和语义分割，使用 ALFRED 风格动作，并设置 16,000 步上限。
- 它评估 Success Rate、Goal-Condition Success、步数和 Improvement Rate；Improvement Rate 是一种基于执行过程中评分效率是否上升的指标。
- HoloMind 将任务分解为由依赖目标组成的 DAG，然后在生成可执行子目标前，结合记忆细化每个目标。
- 它维护多模态空间记忆，包括 3D 语义地图、物体记录、基于 CLIP 的检索和 VLM 验证；情节记忆存储状态、已完成子目标和可复用规则。
- Critic 监控规划器和执行器输出，在检测到错误时发出 Pass、Refine 或 Replan 命令。

## 结果
- 在 LongAct detailed split 上，纯 Qwen3-VL-8B 达到 0.74% Goal-Condition Success (GC) 和 0% Success Rate (SR)；纯 Qwen3-VL-32B 达到 6.14% GC 和 0% SR。
- 使用 HoloMind 后，Qwen3-VL-8B 提升到 24.5% GC 和 3.00% SR，Qwen3-VL-32B 提升到 51.2% GC 和 15.0% SR。
- 搭配 GPT-5 的 HoloMind 在摘录中给出最佳模型结果：表中为 59.0% GC、16.0% SR、1,982 个导航步骤、25.3 个操作步骤，以及 1.70 Improvement Rate (IR)。
- 文中报告的人类表现为 93% 目标完成率，而 GPT-5 为 59.0%。
- 纯 VLM 基线的 IR 为负值（Qwen3-VL-8B：-0.08；Qwen3-VL-32B：-0.32），HoloMind 变体的 IR 为正值（Qwen3-VL-2B：0.59；Qwen3-VL-8B：0.99；Qwen3-VL-32B：1.61；GPT-5：1.70）。
- 摘录称，移除 Critic 会使准确率降低约 40%，并可能使操作效率和 IR 最多降低 90%，但所示表格未包含这些消融行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14504v1](https://arxiv.org/abs/2605.14504v1)
