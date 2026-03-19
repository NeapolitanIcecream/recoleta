---
source: arxiv
url: http://arxiv.org/abs/2603.05185v1
published_at: '2026-03-05T13:55:33'
authors:
- Pengfei Yi
- Yingjie Ma
- Wenjiang Xu
- Yanan Hao
- Shuai Gan
- Wanting Li
- Shanlin Zhong
topics:
- robot-manipulation
- vision-language-action
- hierarchical-control
- anomaly-detection
- long-horizon-planning
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation

## Summary
该论文提出一个用于长时程机器人操作的三系统VLA框架：用VLM负责慢速规划、VLA负责快速执行、轻量Critic负责监控并决定何时切换。核心价值是在不频繁调用昂贵VLM的前提下，提高复杂操作任务中的鲁棒性、异常恢复和OOD泛化能力。

## Problem
- 现有机器人操作系统很难同时兼顾**高层语义推理**与**低层实时控制**：VLM会思考但太慢，VLA执行快但语义理解不够深。
- 传统双系统通常采用固定频率或僵硬的切换规则，导致在顺利执行时浪费算力、在出错时又反应不够快，尤其影响长时程任务。
- 真实环境中还会出现停滞、掉落、扰动和分布外场景；如果没有在线异常检测与恢复机制，机器人容易陷入无限重试或任务失败，这对实际部署很关键。

## Approach
- 提出**Tri-System**架构：System 2“Brain”用VLM生成语义子任务，System 1“Cerebellum”用flow-matching动作模型执行连续控制，System 3“Critic”持续看当前画面并评估进展。
- Critic被建模成一个轻量视觉问答器：输入图像和当前子任务，输出要么是**进度值**（离散化到101个bin，对应[-1,0]完成度），要么是异常标记`<aci>`。
- 调度机制是**事件驱动的异步切换**：正常情况下只让VLA高速闭环执行；只有在子任务完成、检测到异常、或长时间无进展（停滞）时，才唤醒VLM重新规划。
- 为避免无限卡死，系统加入**类人启发式规则**：若停滞帧数达到阈值`N_stag=180`，就重置机器人状态并带着“stagnation timeout”记忆重新规划。
- 还提出一个**自动子任务标注流水线**：先用末端轨迹和夹爪状态做关键帧提议，再用VLM检索语义标签，减少人工标注长时程演示数据的成本。

## Results
- 在真实机器人 **Arrange the Tableware** 任务上，Tri-System 在4个场景均优于基线：Ordered **10/10**（Single **8/10**, Dual **7/10**）；Scattered **9/10**（vs **0/10**, **6/10**）；Left cup OOD **7/10**（vs **0/10**, **1/10**）；Fallen **7/10**（vs **2/10**, **5/10**）。
- 在 **Tidy up the Desk** 长时程任务上，Tri-System 的分步成功数也最高：Open **9/10**（Single **7/10**, Dual **6/10**）；Bottle1 **8/10**（vs **5/10**, **5/10**）；Bottle2 **5/10**（vs **2/10**, **1/10**）；Overall **4/10**（vs **0/10**, **0/10**）。
- 论文声称该方法达到**state-of-the-art**真实世界长时程操作表现，并且在**分布外左臂抓杯**场景中，即使训练中没有该任务的左臂数据，仍能取得 **7/10** 成功率。
- 系统运行上，Critic支持约**20 Hz**异步监控；Critic使用约**0.2B**参数的 Florence-2-base，以较低开销实现在线进度跟踪和异常中断。
- 数据方面，每个任务收集**200**条遥操作轨迹；餐具任务额外加入**100**条“杯子被碰倒后恢复”的轨迹用于训练恢复能力。论文未提供比“VLM调用次数/延迟”更细的计算开销量化对比，但明确声称动态调度减少了昂贵VLM查询。

## Link
- [http://arxiv.org/abs/2603.05185v1](http://arxiv.org/abs/2603.05185v1)
