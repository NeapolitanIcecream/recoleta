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
- uav-navigation
- vision-language-action
- end-to-end-control
- embodied-ai
- autonomous-landing
relevance_score: 0.24
run_id: materialize-outputs
---

# AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control

## Summary
AerialVLA提出一个面向无人机视觉-语言导航的极简端到端Vision-Language-Action框架，直接把双视角图像与模糊语言提示映射为连续控制与降落动作。核心主张是去掉密集oracle引导和外部目标检测器后，反而能得到更自主、更高效、且在未见环境中更稳健的导航策略。

## Problem
- 现有UAV视觉-语言导航方法常依赖**密集oracle方向提示**，使模型更像被动跟随器，而不是真正进行空间推理与自主导航。
- 许多方法还依赖**外部目标检测器**来决定何时降落，导致感知与控制割裂，鲁棒性和真实性不足。
- 无人机在3D开放环境中需要连续控制与精细视觉对齐，这比地面2D导航更难，对搜索救援、巡检等GPS不可靠场景很重要。

## Approach
- 使用**双视角极简感知**：仅保留前视与下视图，垂直拼接后送入OpenVLA-7B的视觉编码器，以减少多相机冗余和推理开销。
- 使用**模糊方向提示**：把机载IMU/GPS估计的相对方位离散成如“straight ahead”“forward-right”等粗粒度提示，替代逐步oracle guidance，迫使模型做主动视觉定位。
- 使用**数值token化动作输出**：将3-DoF动作\(\langle \Delta x, \Delta z, \Delta \psi \rangle\)离散到99个bin，并直接映射到LLM已有数字词表，而不是训练新的动作token。
- 通过**统一降落机制**把导航和停止合成一个策略：模型既可输出LAND，也可预测接近零位移来触发降落，无需外部检测器。
- 训练上采用**行为克隆**，并加入几何一致性过滤，移除模糊提示下会引入因果歧义的约4%训练帧。

## Results
- 在TravelUAV基准的**Seen**测试集上，AerialVLA达到**47.96% SR**和**38.54% SPL**，优于最强基线LongFly的**36.39% SR / 31.07% SPL**，分别提升**+11.57**和**+7.47**个百分点。
- 在Seen-Hard子集上，AerialVLA的**SR为46.30%**，LongFly为**33.94%**，提升**+12.36**个百分点；但NE为**93.16**，略逊于LongFly的**85.20**。
- 文中声称在**未见场景**中，AerialVLA取得“**接近领先基线3倍的成功率**”的更强泛化，但给定摘录未包含对应完整表格数字，无法逐项核对具体SR/SPL值。
- 计算效率方面，在RTX 4090上，AerialVLA总延迟**0.38s**、显存**17GB**，相比TravelUAV的**0.63s**、**20GB**更快更省；虽然其VLA主干耗时**0.35s**（vs. 0.26s），但省去了**0.37s**的Assist与Grounding DINO模块，仅模糊提示增加**0.03s**。
- 训练配置为TravelUAV上**7,922**条轨迹、约**420k**帧，LoRA仅训练约**2.98%**参数，使用**4×RTX 4090**训练**5个epoch**，约**35小时**。

## Link
- [http://arxiv.org/abs/2603.14363v1](http://arxiv.org/abs/2603.14363v1)
