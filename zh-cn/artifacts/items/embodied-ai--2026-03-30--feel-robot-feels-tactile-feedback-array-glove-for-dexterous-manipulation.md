---
source: arxiv
url: http://arxiv.org/abs/2603.28542v1
published_at: '2026-03-30T15:04:13'
authors:
- Feiyu Jia
- Xiaojie Niu
- Sizhe Yang
- Qingwei Ben
- Tao Huang
- Feng zhao
- Jingbo Wang
- Jiangmiao Pang
topics:
- dexterous-manipulation
- teleoperation
- tactile-feedback
- robot-data-collection
- haptic-glove
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Feel Robot Feels: Tactile Feedback Array Glove for Dexterous Manipulation

## Summary
## 摘要
TAG 是一款用于灵巧操作的低成本遥操作手套，结合了精确的 21-DoF 手部跟踪和高分辨率指尖触觉反馈。它面向接触密集型机器人遥操作和示教数据采集，在这些场景中，运动误差和缺失的触觉反馈会降低任务成功率和数据质量。

## 问题
- 灵巧遥操作仍受两个实际限制影响：人在到机器人运动映射中的手部跟踪误差，以及接触过程中较弱或缺失的触觉反馈。
- 基于视觉和 VR 的系统高度依赖相机视角、对齐和姿态估计，而许多手套传感器会发生漂移、磨损，或在电磁噪声附近失去精度。
- 对机器人学习来说，遥操作保真度不足会直接影响结果，因为质量差的示教会降低物理一致性，使采集到的数据更难用于模仿学习。

## 方法
- TAG 使用 21 个非接触式磁编码器来跟踪整只手的关节运动。每个关节角度都由三轴磁场测量恢复得到，这种方法可实现无漂移跟踪，并通过基于比值的角度计算抵消部分共模误差。
- 每个指尖都配有一个紧凑的 **32-actuator** 电渗触觉阵列，集成在 **2 cm²** 模块中。该模块支持空间触觉模式，因此操作者不仅能感知发生了接触，还能感知接触发生的位置。
- 手套提供两种反馈模式：**shape mapping**，将机器人指尖的接触模式映射到人的指尖；以及 **pressure mapping**，将更强的接触转换为更大的触觉激活区域。
- 该系统面向真实机器人使用和跨平台兼容性而设计。论文在多种机器人触觉传感方式和两种遥操作配置上进行了测试，包括 G1 + Inspire Hand 和 UR5e + XHand。
- TAG 的设计目标之一是低成本和可复现：文中称整套系统成本 **低于 $500**，而商用触觉手套通常 **高于 $5,000**。

## 结果
- 关节跟踪精度较高：论文报告了 **sub-degree error**，设计级精度低于 **0.8°**，实测最大跟踪误差在 **±0.35°** 以内，长时间运行误差分布为 **σ = 0.215°**。
- 在 **1000 s** 测试中，长期稳定性较好：首尾两个 **30 s** 时间窗口之间的平均差异约为 **0.02°**，说明漂移很低。
- 在文中报告的设置下，其抗电磁干扰能力明显优于商业基线：在运行中的 PC 机箱附近，**Manus glove** 的偏差达到 **5.69°**，而 **TAG** 保持在 **0.24°** 以内。
- 作为手套设备，其硬件密度较高：实现了 **21 DoF** 手部捕捉，以及每个指尖 **32 tactile actuators per fingertip**，模块尺寸为 **29 × 18.4 × 5.5 mm**。
- 在一项有 **5 participants** 参与的接触形状辨别用户研究中，**single-point contacts reached 100% accuracy**。摘录还指出，**two-point** 和 **plane** 接触各有 **23/25** 次被正确识别。
- 摘录称其提高了接触密集型遥操作任务的成功率，并为模仿学习提供了更可靠的示教数据，但给出的文本未包含最终任务成功率数字或学习指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28542v1](http://arxiv.org/abs/2603.28542v1)
