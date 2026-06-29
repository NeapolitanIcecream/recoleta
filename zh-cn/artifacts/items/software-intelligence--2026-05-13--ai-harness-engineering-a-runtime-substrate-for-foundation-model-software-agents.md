---
source: arxiv
url: https://arxiv.org/abs/2605.13357v1
published_at: '2026-05-13T11:14:59'
authors:
- Hailin Zhong
- Shengxin Zhu
topics:
- software-agents
- code-intelligence
- agent-evaluation
- runtime-systems
- software-verification
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents

## Summary
## 摘要
AI Harness Engineering 将自主编码表现视为模型、运行时 harness 和软件环境共同决定的属性。论文定义了 harness 组件，并提出一套评估协议，用于让智能体软件工作可审计。

## 问题
- 软件智能体在完整仓库任务上经常失败，即使它们能写出看起来合理的局部补丁；失败包括选错文件、测试薄弱、故障诊断不佳、任务状态丢失，以及过早声称完成。
- 这个问题很重要，因为人类开发者目前在补充缺失的运行时支持：仓库上下文、工具选择、反馈解读、验证、权限控制和清理。
- 标准的通过/失败评估看不出智能体是否真的验证了改动、是否保留了先前行为，或者是否需要了隐藏的人类帮助。

## 方法
- 核心机制是在基础模型和代码仓库之间放置一个运行时 harness。它控制智能体能看到什么、能使用什么工具、如何记录状态，以及如何证明完成。
- 论文定义了 11 项 harness 职责：任务规范、上下文选择、工具访问、项目记忆、任务状态、可观测性、失败归因、验证、权限、熵审计和干预记录。
- 论文提出了一个 4 级阶梯 H0 到 H3，分阶段增加运行时支持：最小仓库访问、工具支持、上下文和记忆支持，然后是可观测性和验证支持。
- 论文定义了一个基于轨迹的 episode package，包含 8 类轨迹：动作、工具、上下文、验证、失败归因、干预、熵和结果。
- 评估关注完整的模型-harness-环境系统，并把人类干预当作一个可测量信号，通过缺失 harness 的人类干预率 M-HIR 来表示。

## 结果
- 摘录中没有报告任务成功率、pass@k 分数、基准胜率或大规模定量评估。
- 论文声称，在一个受控验证任务中，4 个 harness 级别产生了不同的 episode 证据，更高级别提供了比低级别更丰富的审计记录。
- H0 主要只产生最终补丁，而 H3 还加入了复现日志、失败归因、确定性的需求检查和结构化验证报告。
- 该方法提供了 11 项命名的运行时职责，并把每一项映射到一种失败模式和一种证据工件。
- 评估协议按每个 episode 记录 8 类证据，并把失败分成 8 类：上下文、工具、反馈、验证、恢复、熵、模型和未知。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13357v1](https://arxiv.org/abs/2605.13357v1)
