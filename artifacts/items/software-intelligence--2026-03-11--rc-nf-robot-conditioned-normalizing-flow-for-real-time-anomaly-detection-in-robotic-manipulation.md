---
source: arxiv
url: http://arxiv.org/abs/2603.11106v1
published_at: '2026-03-11T10:14:37'
authors:
- Shijie Zhou
- Bin Zhu
- Jiarui Yang
- Xiangyu Zhao
- Jingjing Chen
- Yu-Gang Jiang
topics:
- robot-anomaly-detection
- normalizing-flow
- vision-language-action
- real-time-monitoring
- ood-detection
- robot-manipulation
relevance_score: 0.35
run_id: materialize-outputs
---

# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

## Summary
本文提出 RC-NF，一种面向机器人操作的实时异常检测模块，用于监控 VLA 机器人执行是否偏离任务分布。它通过仅使用正常演示进行无监督训练，在仿真基准和真实机器人上实现了高精度、低延迟的 OOD 检测与干预触发。

## Problem
- 论文要解决的是：VLA 机器人在动态环境和分布外（OOD）情况下容易执行漂移或失败，但现有监控方法要么依赖穷举异常类别，要么推理延迟达到秒级，无法及时干预。
- 这很重要，因为机器人操作是闭环控制，若不能在早期发现抓取失败、物体滑落或空间目标错位，错误会快速累积并导致任务失败甚至安全风险。
- 现有基于分类的方法泛化差，基于大模型的监控又太慢，因此需要一个能实时、任务相关、无需异常标注的运行时监控器。

## Approach
- 核心方法是 **Robot-Conditioned Normalizing Flow (RC-NF)**：学习“正常任务执行时，机器人状态 + 物体运动轨迹”应当长什么样；运行时如果当前观测在这个分布下概率很低，就判为异常。
- 它只用成功示例训练，是无监督异常检测；推理时用负对数似然作为异常分数，分数越高表示越偏离正常执行。
- 输入由三部分组成：机器人本体状态、任务文本嵌入、以及从视频中经 SAM2 分割后得到的目标物体点集轨迹，而不是直接用原始图像。
- 论文提出新的耦合层 **RCPQNet**：把机器人状态和任务嵌入做成 query，把物体点集特征做成 memory，通过交叉注意力生成 flow 的缩放/平移参数，从而在“解耦处理”机器人与物体信息的同时保留交互关系。
- 系统作为即插即用监控模块并行挂在 VLA 控制环中；一旦异常分数超过阈值，就触发状态级回退（homing/rollback）或任务级重规划。

## Results
- 在新提出的 **LIBERO-Anomaly-10** 基准上，RC-NF 在三类异常上都达到最优：平均 **AUC 0.9309 / AP 0.9494**，优于 FailDetect 的 **AUC 0.7181 / AP 0.7700**，约提升 **+0.2128 AUC** 和 **+0.1794 AP**。
- 相比最强基线，论文声称平均约提升 **8% AUC** 和 **10% AP**；从表中看，RC-NF 相比最佳非本方法（按平均）GPT-5 的 **AUC 0.8500 / AP 0.8507**，提升约 **+0.0809 AUC**、**+0.0987 AP**。
- 分类别结果：**Gripper Open** 上 RC-NF 达到 **AUC 0.9312 / AP 0.9781**；**Gripper Slippage** 为 **0.9195 / 0.9180**；**Spatial Misalignment** 为 **0.9676 / 0.9585**。其中空间错位任务上，VLM 基线接近随机，如 GPT-5 仅 **AUC 0.4904 / AP 0.4015**。
- 真实机器人实验中，RC-NF 作为 VLA（如 **π0**）的插件式模块，异常响应延迟 **低于 100 ms**，可触发状态级回滚和任务级重规划。
- 训练数据使用原始 **LIBERO-10**，每个任务 **50** 条 demonstration；RC-NF 采用 **12** 个 flow steps、训练 **100** 个 epochs。论文同时发布 **LIBERO-Anomaly-10**，包含 **3** 类操作异常。

## Link
- [http://arxiv.org/abs/2603.11106v1](http://arxiv.org/abs/2603.11106v1)
