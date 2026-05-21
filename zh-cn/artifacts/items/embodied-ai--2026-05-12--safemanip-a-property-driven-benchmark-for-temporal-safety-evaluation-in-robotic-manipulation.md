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
## 摘要
SafeManip 是一个用于检查机器人操作 rollout 中时序安全性的基准，使用 LTL_f 监视器，而不是只看任务成功率。它表明，当前 VLA 策略可以完成任务，但在执行过程中仍会违反安全规则。

## 问题
- 标准操作基准按任务完成情况打分，因此可能漏掉最终状态之前发生的不安全执行。
- 许多故障取决于事件顺序：污染后接触清洁表面、物体进入固定装置之前就释放，或撞到机构后未能恢复。
- 这对家用和厨房机器人很重要，因为成功的最终状态仍可能包含不安全接触、溢洒、不稳定放置或卫生违规。

## 方法
- SafeManip 使用有限轨迹上的线性时序逻辑定义可复用的时序安全模板，模板写在 `Collision`、`StableGrasp`、`Sanitized`、`Contained` 和 `FixOpen` 等谓词之上。
- 它使用仿真器状态、物体姿态、接触、夹爪状态、固定装置状态和任务动作信号，将每个 rollout 映射为符号谓词轨迹。
- 每个任务把通用模板绑定到具体物体、固定装置、区域和技能，然后用编译为有限自动机的 LTL_f 监视器检查 rollout。
- 该属性套件包含 8 类安全问题和 10 个模板：碰撞/接触、抓取稳定性、释放稳定性、交叉污染、动作起始、机构恢复、容纳，以及封闭空间/访问。
- 该基准分别报告任务成功率、安全违规率、成功且安全、成功但不安全、失败但安全、失败且不安全，以及不安全状态暴露。

## 结果
- 评估使用 50 个 RoboCasa365 任务、6 个 VLA 策略或变体，并且每个任务运行 50 个 rollout。
- 测试的策略包括 `pi_0`、`pi_0.5`、GR00T N1.5，以及 3 个 GR00T N1.5 训练变体。
- `pi_0.5` 将任务成功率从 `pi_0` 的 8.1% 提高到 9.3%，同时安全违规率也从 69.7% 升至 82.8%。
- 论文报告称，GR00T-tpt 的任务成功率高于其他 GR00T 变体，但违规率仍然很高；摘录未给出确切的 GR00T 数值。
- 摘录中的分类结果显示，碰撞/接触和释放稳定性是主要故障来源；释放稳定性的不安全状态暴露也较高，因为失败的放置可能在许多时间步内保持未稳定状态。
- 较低的容纳和封闭空间/访问违规率部分与监视器激活有关：容纳在检测到转移后检查，封闭空间/访问通常只在伸手进入或访问内部固定装置事件期间触发。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12386v1](https://arxiv.org/abs/2605.12386v1)
