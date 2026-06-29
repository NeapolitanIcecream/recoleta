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
Orchard 是一个开源的智能体训练系统，建立在一个轻量的 Kubernetes 环境服务之上。它通过可复用的沙箱基础设施，以及 SFT 和 RL 方案，在软件工程、浏览器操作和个人助理智能体上取得了很强的结果。

## 问题
- 智能体 LLM 训练需要大量隔离环境来做代码执行、网页任务和工具调用；封闭或强耦合的沙箱系统会让结果更难复现和复用。
- 软件工程智能体需要更大的轨迹数据集，也需要更好地从失败尝试中学习，因为 SWE-bench 风格的奖励很稀疏。
- 开放研究需要更低的沙箱成本和更高的 rollout 吞吐量，方便小团队在规模上训练和评估智能体。

## 方法
- Orchard Env 作为一个 Kubernetes 原生的沙箱服务运行，提供用于创建沙箱、执行命令、文件读写、网络策略和清理的 REST API。
- 它会在运行时把一个轻量级的、注入到 Pod 内的执行代理放进用户的 Docker 镜像里，所以任务镜像不需要重建。
- 执行请求直接发到沙箱 Pod 的 IP，这样就避开了 Kubernetes exec 和 WebSocket 在热路径上的开销。
- Orchard-SWE 蒸馏了 107K 条软件工程轨迹，保留未完成轨迹中有用的部分来做 credit-assignment SFT，并使用 Balanced Adaptive Rollout 处理稀疏奖励 RL。
- Orchard-GUI 和 Orchard-Claw 复用同一环境层来处理浏览器导航和生产力工具任务，并结合 SFT 和 RL。

## 结果
- 使用 Qwen3-30B-A3B-Thinking 的 Orchard-SWE 在 mini-swe-agent 设置下，SFT 后在 SWE-bench Verified 上达到 64.3%，SFT+RL 后达到 67.5%，论文将其称为同等规模模型中的新的开源最好结果。
- Orchard-GUI 用 0.4K 条蒸馏轨迹和 2.2K 个开放式任务训练了一个 4B 视觉语言智能体，在 WebVoyager、Online-Mind2Web、DeepShop 上分别达到 74.1%、67.0%、64.0%，平均 68.4%。
- Orchard-Claw 用 0.2K 个合成任务训练，在 Claw-Eval 上达到 59.6% 的 pass@3；配合 ZeroClaw harness 后达到 73.9% 的 pass@3。
- Orchard Env 报告的平均命令延迟是 0.280 秒；在所引 benchmark 设置下，E2B 为 0.747 秒，Modal 为 2.046 秒。
- 在 1,000 个沙箱的压力测试中，Orchard Env 报告 100% 成功率、26 秒端到端时间、11.75 秒平均创建时间和 0.28 秒平均执行延迟。
- 在 240 小时内并行运行 128 个 2 vCPU、8 GiB 的沙箱，按需估算成本为 3,362 美元，使用 spot 实例为 673 美元；Daytona 或 E2B 为 7,078 美元。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15040v1](https://arxiv.org/abs/2605.15040v1)
