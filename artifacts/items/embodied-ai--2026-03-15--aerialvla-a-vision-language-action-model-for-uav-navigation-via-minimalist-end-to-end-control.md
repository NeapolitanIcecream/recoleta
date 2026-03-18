---
source: arxiv
url: http://arxiv.org/abs/2603.14363v1
published_at: '2026-03-15T13:02:13'
authors:
- Peng Xu
- Zhengnan Deng
- Jiayan Deng
- Zonghua Gu
- Shaohua Wan
topics:
- vision-language-action
- uav-navigation
- embodied-ai
- end-to-end-control
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
---

# AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control

## Summary
AerialVLA提出一个面向无人机视觉-语言导航的极简端到端VLA模型，把双视角图像和模糊语言提示直接映射为连续控制与降落动作。它试图摆脱现有UAV-VLN对oracle方向提示和外部目标检测器的依赖，在更自治的设定下实现导航与精确着陆。

## Problem
- 现有无人机VLN方法常依赖**密集oracle方向引导**，导致模型更像“跟提示走”，而不是真正进行空间推理与自主导航。
- 许多系统还依赖**外部目标检测器**来决定何时降落，造成感知与控制割裂，降低开放环境下的鲁棒性。
- UAV在3D动态环境中需要连续控制与精细视觉定位，这对实时性、稳定性和泛化都很关键，关系到搜救、巡检等GPS不可靠场景的可用性。

## Approach
- 使用**双视角极简感知**：仅保留前视和下视图像，垂直拼接后送入OpenVLA-7B的视觉编码器，以减少冗余输入和延迟，同时兼顾前向导航与降落对地对准。
- 使用**模糊方向提示**：把机载IMU/GPS得到的相对方位离散成粗粒度语言提示，如“straight ahead”“forward-right”，替代逐步oracle指令，迫使模型更多依赖视觉主动定位。
- 使用**数值token化动作输出**：将连续3-DoF动作 \(\langle \Delta x, \Delta z, \Delta\psi \rangle\) 离散为99个bin，并直接映射到LLM已有数字token，避免重新学习特殊动作词表。
- 将**导航与降落统一**到一个策略中：模型既可输出LAND，也可输出接近零位移动作作为停止信号，从而无需外部检测器触发着陆。
- 训练上采用**行为克隆**，并加入几何一致性过滤，去除模糊提示与专家动作之间明显矛盾的约4%训练帧。

## Results
- 在TravelUAV的Seen测试集上，AerialVLA达到**47.96% SR**、**38.54% SPL**、**65.88 NE**、**57.69% OSR**。
- 相比最强基线LongFly，在Seen集上提升到**+11.57 SR**（47.96 vs. 36.39）和**+7.47 SPL**（38.54 vs. 31.07）；论文还指出在Hard子集上SR优势为**+12.36**（46.30 vs. 33.94）。
- 与NavFoM相比，Seen集SR从**29.17%**提升到**47.96%**；与TravelUAV-DA相比，SR从**17.45%**提升到**47.96%**。
- 计算效率上，AerialVLA在RTX 4090上需要**17GB VRAM**、**0.38s总延迟**，优于TravelUAV的**20GB**、**0.63s**；其自身VLA推理为**0.35s**，模糊提示额外仅**0.03s**。
- 数据与训练规模：使用TravelUAV *UAV-Need-Help*任务，训练于**7,922条轨迹 / 420k帧**，测试包含Seen **1,418**条、Unseen Object **629**条、Unseen Map **958**条。
- 摘要声称在**unseen场景**中相对领先基线达到“**近3倍成功率**”，但当前给定摘录未包含对应完整表格数字，因此无法逐项核验。

## Link
- [http://arxiv.org/abs/2603.14363v1](http://arxiv.org/abs/2603.14363v1)
