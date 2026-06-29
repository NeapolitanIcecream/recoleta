---
source: arxiv
url: https://arxiv.org/abs/2605.12386v1
published_at: '2026-05-12T16:49:28'
authors:
- Chengyue Huang
- Khang Vo Huynh
- Sebastian Elbaum
- Zsolt Kira
- Lu Feng
topics:
- robot-safety
- vision-language-action
- robot-manipulation
- temporal-logic
- benchmarking
- robocasa
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation

## Summary
## 总结
SafeManip 是一个用于检查机器人操作滚动轨迹中时间安全性的基准，它使用 LTL_f 监控器，而不只看任务是否完成。结果显示，当前的 VLA 策略可以完成任务，但在执行过程中仍然违反安全规则。

## 问题
- 标准操作基准按任务完成情况计分，因此可能漏掉在最终状态之前发生的不安全执行。
- 许多失败取决于事件顺序：污染后再接触干净表面、物体还没完全进入固定装置就提前释放，或者撞到机构后没有恢复。
- 这对家用和厨房机器人很重要，因为最终状态成功，也可能包含不安全接触、洒漏、放置不稳或卫生违规。

## 方法
- SafeManip 用有限轨迹上的线性时序逻辑定义可复用的时间安全模板，模板基于 `Collision`、`StableGrasp`、`Sanitized`、`Contained` 和 `FixOpen` 等谓词。
- 它结合模拟器状态、物体位姿、接触、夹爪状态、固定装置状态和任务动作信号，把每次 rollout 映射成符号谓词轨迹。
- 每个任务把通用模板绑定到具体的物体、固定装置、区域和技能，然后用编译成有限自动机的 LTL_f 监控器检查 rollout。
- 该属性集覆盖 8 类安全问题，共 10 个模板：碰撞/接触、抓取稳定性、释放稳定性、交叉污染、动作起始、机构恢复、容纳，以及封闭/访问。
- 基准将任务成功与安全违规率分开报告，并统计成功且安全、成功但不安全、失败但安全、失败且不安全，以及不安全状态暴露。

## 结果
- 评估使用了 50 个 RoboCasa365 任务、6 个 VLA 策略或变体，以及每个任务 50 次 rollout。
- 测试的策略包括 `pi_0`、`pi_0.5`、GR00T N1.5，以及 3 个 GR00T N1.5 训练变体。
- 与 `pi_0` 相比，`pi_0.5` 的任务成功率从 8.1% 提高到 9.3%，但安全违规率也从 69.7% 升到 82.8%。
- 论文提到，GR00T-tpt 的任务成功率高于其他 GR00T 变体，但违规率仍然很高；摘录没有给出 GR00T 的具体数值。
- 摘录中的类别结果指出，碰撞/接触和释放稳定性是主要失败来源；释放稳定性的不安全状态暴露也很高，因为失败的放置可能在很多时间步里都没有稳定下来。
- 容纳和封闭/访问的违规率偏低，部分原因是监控器触发条件：容纳在检测到转移后才检查，封闭/访问通常只在伸入或访问内部固定装置时触发。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12386v1](https://arxiv.org/abs/2605.12386v1)
