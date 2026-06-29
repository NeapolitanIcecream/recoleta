---
source: arxiv
url: https://arxiv.org/abs/2605.26563v1
published_at: '2026-05-26T05:24:37'
authors:
- Minxing Wang
- Xiaofei Xie
- Yintong Huo
topics:
- agentic-coding
- failure-diagnosis
- code-intelligence
- software-maintenance
- llm-agents
- benchmark
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems

## Summary
## 概要
TrajAudit 通过找出让代理走偏的最早步骤，诊断仓库级编码代理运行中的失败。它结合测试错误提示、轨迹过滤和基于工具的检查，处理长而嘈杂的执行轨迹。

## 问题
- 编码代理会在多文件软件维护任务中失败，开发者需要知道第一个决定性的错误步骤，才能修复代理、提示词、工具或工作流。
- 现有的 LLM 诊断方法会读取整段轨迹或固定分块，因此在仓库级轨迹上准确率会下降；这类轨迹通常有 20 到 100 多个步骤，单步观测内容可占到超过 70% 的内容。
- 先前基准低估了这种难度；Who&When 的平均步数为 22.24，每步平均字符数为 1,384.11，而 RootSE 的平均步数为 50.94，每步平均字符数为 5,830.71。

## 方法
- TrajAudit 先使用失败测试代码和错误信息生成初步诊断，包括可能的失败阶段和原因。
- 它通过语义显著性折叠压缩轨迹观测：没有失败相关模式或关键词的内容会被替换为折叠标记，而更可能有用的代码、补丁和错误信号会保留可见。
- 一个调查代理读取任务、初步诊断和折叠后的轨迹，然后在需要时调用 API 查看被隐藏的观测内容。
- 输出结果是预测的最早决定性错误步骤，以及一段自然语言说明。
- 论文还引入了 RootSE，这是一个基准，包含来自 SWE-agent、OpenHands 和 AutoCodeRover 在 SWE-bench 与 SWE-bench Pro 任务上的真实失败编码代理轨迹。

## 结果
- 在 RootSE 上，TrajAudit 的定位准确率比最强的现有基线高出 24.4 个百分点以上。
- TrajAudit 使用的 token 数至少比基线少 18%。
- RootSE 包含 93 个失败执行实例、4,500 多个执行步骤，以及约 2700 万个字符。
- RootSE 的任务描述平均为 8,223.51 个字符，而 Who&When 为 240.47 个字符；RootSE 任务平均修改 2.9 个文件，而 Who&When 为 1.7 个文件。
- RootSE 覆盖 3 种编程语言；Who&When 覆盖 1 种。
- 标注质量报告显示，用于识别最早决定性错误步骤的 Cohen’s kappa 为 0.78，经过仲裁后最终一致率为 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26563v1](https://arxiv.org/abs/2605.26563v1)
