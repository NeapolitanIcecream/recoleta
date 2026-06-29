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
LongAct 是一个用于自由形式、长时程家庭任务执行的基准，HoloMind 是为它设计的基于 VLM 的智能体。论文测试了规划、记忆和错误恢复，任务步数可以超过 2,000 步。

## 问题
- 现有具身 AI 基准大多测试短程导航或操作任务，因此没有覆盖跨房间、跨物体、带依赖关系的多阶段家庭流程。
- LongAct 之所以重要，是因为用户会提出书桌整理、厨房复位这类复合家务，这些任务需要状态跟踪、物体区分和在长动作序列中的重新规划。

## 方法
- LongAct 在 100 多个 ProcTHOR/AI2-THOR 房屋中设置了 300 个 episode，覆盖四种家庭场景。每个任务都有自由形式指令，平均约 9 个目标，输入包含 RGB-D 和语义分割，动作采用 ALFRED 风格，并设置 16,000 步上限。
- 它评估 Success Rate、Goal-Condition Success、步数，以及 Improvement Rate，这个指标基于执行过程中评分效率是否提升。
- HoloMind 把任务拆成一个由依赖目标组成的 DAG，然后先用记忆细化每个目标，再生成可执行的子目标。
- 它维护一个多模态空间记忆，包含 3D 语义地图、物体记录、基于 CLIP 的检索和 VLM 验证；情景记忆保存状态、已完成子目标和可复用规则。
- Critic 监控规划器和执行器的输出，发现错误时发出 Pass、Refine 或 Replan 指令。

## 结果
- 在 LongAct detailed 划分上，纯 Qwen3-VL-8B 的 Goal-Condition Success (GC) 只有 0.74%，Success Rate (SR) 为 0%；纯 Qwen3-VL-32B 的 GC 为 6.14%，SR 为 0%。
- 加上 HoloMind 后，Qwen3-VL-8B 的 GC 升至 24.5%，SR 升至 3.00%；Qwen3-VL-32B 的 GC 升至 51.2%，SR 升至 15.0%。
- 结合 GPT-5 的 HoloMind 给出了摘录中的最佳模型结果：表中 GC 为 59.0%，SR 为 16.0%，导航步数为 1,982，操作步数为 25.3，Improvement Rate (IR) 为 1.70。
- 人类表现报告为 93% 的目标完成率，而 GPT-5 为 59.0%。
- 纯 VLM 基线的 IR 为负值（Qwen3-VL-8B：-0.08；Qwen3-VL-32B：-0.32），而 HoloMind 变体的 IR 为正值（Qwen3-VL-2B：0.59；Qwen3-VL-8B：0.99；Qwen3-VL-32B：1.61；GPT-5：1.70）。
- 摘录说，去掉 Critic 会让准确率下降约 40%，并且操作效率和 IR 最多会下降 90%，但展示的表格没有这些消融行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14504v1](https://arxiv.org/abs/2605.14504v1)
