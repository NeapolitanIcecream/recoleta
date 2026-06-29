---
source: arxiv
url: https://arxiv.org/abs/2606.12344v1
published_at: '2026-06-10T17:16:23'
authors:
- Mengyu Zheng
- Kai Han
- Boxun Li
- Haiyang Xu
- Yuchuan Tian
- Wei He
- Hang Zhou
- Jianyuan Guo
- Hailin Hu
- Lin Ma
- Chao Xu
- Guohao Dai
- Lixue Xia
- Yunchao Wei
- Yunhe Wang
- Yu Wang
topics:
- coding-agents
- swe-bench
- agent-harnesses
- code-intelligence
- benchmarking
- cost-evaluation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks

## Summary
## 摘要
Claw-SWE-Bench 在同一套 SWE-bench 风格评分协议下评估代码代理的 harness，因此可以在相同任务上比较模型选择、harness 选择和运行成本。它包含一个 350 个样本的多语言基准和一个 80 个样本的 Lite 子集，用于更便宜的开发运行。

## 问题
- OpenClaw 这类通用代理不能直接满足 SWE-bench 协议：评测器需要干净的 Docker 工作区、放在 `model_patch` 里的补丁，以及仓库测试，而不是开放式的代理对话记录。
- 之前的 SWE-bench 风格报告把模型、harness、提示词、预算、停止规则和补丁提取混在一起，难以判断提升来自 LLM 还是代理 harness。
- 成本很重要，因为代码代理会发起很多工具调用和模型调用；相同的 Pass@1 可能对应不同的 API 成本、墙钟时间和缓存行为。

## 方法
- 该基准固定任务集合、提示模板、Docker 工作区、墙钟预算、补丁提取、预测格式和 SWE-bench 评测器。
- 每个 harness 通过一个适配器连接，适配器包含 `create_agent`、`send_task`、`backup_session`、`delete_agent` 和 `get_docker_args` 等生命周期方法。
- 候选补丁取自 `/testbed` 下仓库的最终 diff，而不是从代理的最终文本回答里解析。
- 完整集合包含 350 个 GitHub issue 解决样本，覆盖 8 种编程语言和 43 个仓库，来源是 SWE-bench-Multilingual 和 SWE-bench-Verified-Mini，并在清理未来提交后得到。
- Claw-SWE-Bench Lite 选择 80 个样本，每种语言 10 个，选择过程基于 17 个校准列，兼顾成本和排名。

## 结果
- 在完整的 350 样本基准上，使用最小 direct-diff 适配器的 OpenClaw 只得到 19.1% 的 Pass@1，而在相同的 GLM 5.1 模型下，完整适配器达到 73.4%。
- 在 OpenClaw × 9 个模型的扫描中，模型选择让 Pass@1 变化 29.4 个百分点。
- 在 5 个 claw × 2 个模型的扫描中，在固定模型下，harness 选择让 Pass@1 最多变化 27.4 个百分点；GLM 5.1 上的差距是 12.5 个百分点，Qwen 3.6-flash 上是 27.4 个百分点。
- Lite-80 在 17 个校准列上与完整集合保持接近：full-350 的平均 Pass@1 为 0.639，Lite-80 为 0.643，相差 +0.4 个百分点。
- 在 5 claws × 2 models 的跨 claw 检查中，Lite-80 的平均绝对 full 差异为 1.88 个百分点，最大差异为 3.68 个百分点。
- Lite-80 的成本约为完整 350 样本运行的 22.9%；报告的比例分别是输入 token 22.2%、输出 token 23.6%、缓存读取 token 22.6% 和墙钟时长 23.0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12344v1](https://arxiv.org/abs/2606.12344v1)
