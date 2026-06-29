---
source: arxiv
url: https://arxiv.org/abs/2606.24815v1
published_at: '2026-06-23T17:00:06'
authors:
- Pablo Valle
- Shaukat Ali
- Aitor Arrieta
- Lionel Briand
topics:
- vision-language-action
- robot-evaluation
- test-oracles
- failure-localization
- multi-agent-generation
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models

## Summary
## 概要
MANGO 根据自然语言指令，为 VLA 机器人任务自动生成细粒度测试预言机。它检查 open、pick、place、close 等有序原子步骤，而不只检查最终模拟器状态，因此能改进评估和调试。

## 问题
- VLA 机器人基准常使用手写的符号预言机，只检查最终状态，例如执行结束时某个物体是否在容器内。
- 这些预言机构建时需要领域工作，依赖 Python 或 .bddl 文件等基准专用格式，并且对长程操作任务给出的调试信号较弱。
- 机器人可能因为漏掉中间步骤、掉落物体，或按错误顺序执行步骤而失败；最终状态预言机通常只报告任务失败。

## 方法
- MANGO 从复杂的自然语言任务中构建可复用的原子任务库，包含 `Open(fridge)`、`Pick(bottle)`、`Place(bottle, fridge)` 和 `Close(fridge)` 等参数化动作。
- 它使用可用的模拟器函数，将每个原子任务映射到模拟器检查，例如打开状态、持有状态、接触关系和空间关系。
- 对于每条完整指令，它将指令分解为有序或部分有序的原子任务序列，并为每个步骤附加匹配的预言机。
- 三种智能体角色执行迭代检查：Generator 创建候选任务库和预言机，Assessor 智能体检查逻辑、对象落地、函数使用和执行可靠性，Judge 接受候选结果或发送修正指令。
- 每个生成循环在被接受后停止，或在 10 次迭代后停止。

## 结果
- 论文在 2 个基准上评估 MANGO：LIBERO_10 和 RoboCasa Humanoid Tabletop。
- 作者声称，MANGO 生成的可执行细粒度预言机检测到的失败数量与手写符号预言机相近。
- 生成的预言机还能通过识别失败的原子步骤和任务序列中的顺序违规来定位失败。
- 论文报告了关于组件贡献以及在保持预言机质量的同时减少初始任务集的消融研究，但该摘录没有给出定量消融值。
- 提供的摘录没有包含精确的成功率、失败计数、精确率、召回率、运行时间，或除 2 个具名基准和 10 次迭代上限之外的基线数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24815v1](https://arxiv.org/abs/2606.24815v1)
