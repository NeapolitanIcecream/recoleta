---
source: arxiv
url: http://arxiv.org/abs/2603.05355v2
published_at: '2026-03-05T16:34:53'
authors:
- Pei Qu
- Zheng Li
- Yufei Jia
- Ziyun Liu
- Liang Zhu
- Haoang Li
- Jinni Zhou
- Jun Ma
topics:
- humanoid-robotics
- lidar-perception
- visuomotor-policy
- diffusion-policy
- teleoperation
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception

## Summary
OmniDP提出一种基于全景LiDAR点云的端到端人形机器人操作策略，用360°三维感知把操作范围扩展到相机视野之外。核心价值是减少因窄视场、遮挡和频繁挪动底座带来的失败、碰撞与部署复杂度。

## Problem
- 传统RGB-D/深度相机视场窄、易自遮挡，导致人形机器人只能在眼前小范围内稳定操作，视野外目标和障碍物常被漏检。
- 在空间受限、机器人不便转身或移动底座的场景中，这种感知瓶颈会直接造成任务失败、碰撞风险和控制不确定性增加。
- 现有扩展感知的方法如主动视觉或第三视角相机，往往带来额外机械复杂度、标定依赖和实时性问题。

## Approach
- 方法核心是把头部全景LiDAR生成的360°点云，直接输入一个端到端模仿学习策略，而不是依赖窄视角RGB-D图像。
- 感知编码器使用3D点云金字塔卷积，并加入**Time-Aware Attention Pooling (TAP)**：把短时间窗内的点云叠加起来，给每个点附上相对时间戳，再用注意力更重视最近观测，从而平滑LiDAR稀疏、闪烁的时序噪声。
- 编码得到的全局特征送入Diffusion Policy解码器，直接生成上半身28维关节动作；同时输入43维全身本体状态以支持协调控制。
- 为了训练策略，论文构建了一个基于XR头显与手柄的全身遥操作系统，在Unitree G1上高效采集带有全身协调的大工作空间示范数据。
- 部署时点云始终在LiDAR自身坐标系中表示，因此不需要额外外参标定，提升跨环境适应性。

## Results
- **总体任务表现（6个任务，总计120次试验）**：OmniDP达到**82/120**，显著高于DP **18/120**、DP3 **22/120**、iDP3 **25/120**。
- **视野外（OV）任务优势最明显**：仿真Pour (OV)中，OmniDP **12/20**，而DP/DP3/iDP3均为**0/20**；真实Hand Over (OV)中，OmniDP **12/20**，三种基线均为**0/20**；真实Pour (OV)中，OmniDP **11/20**，基线均为**0/20**；真实Wipe (OV)中，OmniDP **16/20**，基线均为**0/20**。
- **非OV任务也更强**：仿真Pick & Place上，OmniDP **16/20**，优于DP **10/20**、DP3 **13/20**、iDP3 **14/20**；真实Pick & Place上，OmniDP **15/20**，优于DP **8/20**、DP3 **9/20**、iDP3 **11/20**。
- **碰撞规避实验**：在障碍物位于相机视野外的场景，OmniDP成功率**14/20**、碰撞率**5/20**；DP为**0/20**成功、**20/20**碰撞，DP3为**0/20**成功、**18/20**碰撞，iDP3为**0/20**成功、**18/20**碰撞。
- **泛化能力**：在Pick & Place变体上，OmniDP在不同实例/光照/场景下分别为**13/20、15/20、12/20**；对应iDP3为**12/20、12/20、10/20**，DP3为**7/20、8/20、7/20**，DP为**3/20、4/20、2/20**。
- **消融实验**：Hand Over任务中，完整OmniDP为**12/20**；去掉全景观测后降到**0/20**；去掉TAP后降到**9/20**，表明360°感知和时间感知池化都关键。

## Link
- [http://arxiv.org/abs/2603.05355v2](http://arxiv.org/abs/2603.05355v2)
