---
source: arxiv
url: https://arxiv.org/abs/2605.15040v1
published_at: '2026-05-14T16:35:12'
authors:
- Baolin Peng
- Wenlin Yao
- Qianhui Wu
- Hao Cheng
- Xiao Yu
- Rui Yang
- Tao Ge
- Alessandrio Sordoni
- Xingdi Yuan
- Yelong Shen
- Pengcheng He
- Tong Zhang
- Zhou Yu
- Jianfeng Gao
topics:
- agentic-llm-training
- code-intelligence
- software-agents
- reinforcement-learning
- kubernetes-sandboxes
- gui-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Orchard: An Open-Source Agentic Modeling Framework

## Summary
## 摘要
Orchard 是一个开源智能体训练系统，核心是一个轻量的 Kubernetes 环境服务。它使用可复用的沙箱基础设施，以及 SFT 和 RL 训练方案，在软件工程、浏览器使用和个人助理智能体上报告了强结果。

## 问题
- 智能体式 LLM 训练需要大量隔离环境，用于代码执行、网页任务和工具使用；封闭或高度耦合的沙箱系统会让结果更难复现和复用。
- 软件工程智能体需要大量轨迹数据，并且需要更好地从失败尝试中学习，因为 SWE-bench 类奖励很稀疏。
- 开放研究需要更低的沙箱成本和更高的 rollout 吞吐量，让较小团队也能大规模训练和评估智能体。

## 方法
- Orchard Env 作为 Kubernetes 原生沙箱服务运行，提供 REST API，用于创建沙箱、执行命令、文件 I/O、网络策略和清理。
- 它在运行时向用户 Docker 镜像注入轻量级 pod 内执行代理，因此任务镜像不需要重建。
- 执行请求直接发往沙箱 Pod IP，避开热路径上的 Kubernetes exec 和 WebSocket 开销。
- Orchard-SWE 蒸馏 107K 条软件工程轨迹，通过信用分配 SFT 保留未解决轨迹中的有用部分，并使用 Balanced Adaptive Rollout 处理稀疏奖励 RL。
- Orchard-GUI 和 Orchard-Claw 复用同一环境层，用于浏览器导航和生产力工具任务，并结合 SFT 与 RL。

## 结果
- 使用 Qwen3-30B-A3B-Thinking 的 Orchard-SWE 在 mini-swe-agent 下，SFT 后在 SWE-bench Verified 上达到 64.3%，SFT+RL 后达到 67.5%；论文称这是同等规模开源模型中的新最佳结果。
- Orchard-GUI 用 0.4K 条蒸馏轨迹和 2.2K 个开放式任务训练一个 4B 视觉语言智能体，在 WebVoyager 上达到 74.1%，在 Online-Mind2Web 上达到 67.0%，在 DeepShop 上达到 64.0%，平均为 68.4%。
- Orchard-Claw 在 0.2K 个合成任务上训练，在 Claw-Eval 上达到 59.6% pass@3；使用 ZeroClaw harness 时达到 73.9% pass@3。
- Orchard Env 报告平均命令延迟为 0.280 s；在引用的基准设置中，E2B 为 0.747 s，Modal 为 2.046 s。
- 在 1,000 个沙箱的压力测试中，Orchard Env 报告成功率为 100%，端到端时间为 26 s，平均创建时间为 11.75 s，平均 exec 延迟为 0.28 s。
- 128 个并行 2-vCPU、8-GiB 沙箱运行 240 小时的估算成本为按需 $3,362，使用 Spot 实例为 $673；Daytona 或 E2B 为 $7,078。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15040v1](https://arxiv.org/abs/2605.15040v1)
