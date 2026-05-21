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
AI Harness Engineering 将自主编码表现视为模型、运行时 harness 和软件环境共同产生的属性。论文定义了 harness 组件和一套评估协议，用于让智能体的软件工作可审计。

## 问题
- 软件智能体在完整代码库任务中经常失败，即使它们能写出看起来合理的局部补丁；失败包括选错文件、测试薄弱、故障诊断错误、任务状态丢失，以及过早声称成功。
- 这个问题很重要，因为人类开发者目前在补足缺失的运行时支持：代码库上下文、工具选择、反馈解释、验证、权限控制和清理。
- 标准的通过/失败评估看不出智能体是否真正验证了变更、保留了既有行为，或依赖了隐藏的人类帮助。

## 方法
- 核心机制是在基础模型和代码库之间加入一个运行时 harness。它控制智能体能看到什么、能使用哪些工具、如何记录状态，以及如何证明任务完成。
- 论文定义了 11 项 harness 职责：任务规范、上下文选择、工具访问、项目记忆、任务状态、可观测性、故障归因、验证、权限、熵审计和干预记录。
- 论文提出了一个从 H0 到 H3 的 4 级阶梯，分阶段增加运行时支持：最小代码库访问、工具支持、上下文和记忆支持，最后是可观测性和验证支持。
- 论文定义了基于轨迹的 episode package，包含 8 类轨迹：动作、工具、上下文、验证、故障归因、干预、熵和结果。
- 评估关注完整的模型-harness-环境系统，并把人类干预作为可测量信号，通过 missing-harness human intervention rate，即 M-HIR，进行记录。

## 结果
- 摘录中没有报告任务成功率、pass@k 分数、基准胜率或大规模定量评估。
- 论文称，一项受控验证任务在 4 个 harness 级别上产生了不同的 episode 证据，较高级别比低级别产生了更丰富的审计记录。
- H0 主要产生最终补丁，而 H3 增加了复现日志、故障归因、确定性需求检查和结构化验证报告。
- 该方法给出 11 项命名的运行时职责，并将每一项映射到一种失败模式和一个证据制品。
- 评估协议为每个 episode 记录 8 类证据，并将失败分为 8 类：上下文、工具、反馈、验证、恢复、熵、模型和未知。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13357v1](https://arxiv.org/abs/2605.13357v1)
