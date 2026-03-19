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
- humanoid-manipulation
- lidar-perception
- diffusion-policy
- point-cloud-policy
- omnidirectional-perception
- teleoperation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception

## Summary
本文提出 OmniDP，一种面向类人机器人操作的端到端激光雷达驱动视觉运动策略，用 360° 点云替代窄视角 RGB-D 感知，以支持超出相机视野的大工作空间操作。其核心价值在于让机器人在难以频繁挪动底座的场景中，仍能稳定发现目标、避障并完成全身协调操作。

## Problem
- 现有 RGB-D/深度相机策略通常只有窄视场，目标或障碍物一旦位于相机视野外，就会导致抓取失败、碰撞或需要频繁重定位。
- 对类人机器人而言，额外的主动视觉机构、第三视角相机或多相机标定会带来机械复杂度、延迟、标定依赖和实时性问题。
- 这很重要，因为真实非结构化环境中的大范围操作、递交、擦拭、倒水等任务，往往要求机器人在不方便移动身体时仍具备全向环境感知与安全操作能力。

## Approach
- 作者提出 **OmniDP**：输入为头部全景 LiDAR 的 360° 点云和 43 维本体状态，输出上肢 28 维关节动作；下肢/腰部由预训练 HOMIE 控制，从而实现全身协同操作。
- 感知编码器采用点云金字塔卷积，并加入 **Time-Aware Attention Pooling (TAP)**：把短时间窗内的历史点云拼起来，为每个点附加相对时间戳，再用注意力更重视较新的观测，以缓解 LiDAR 稀疏、闪烁和单帧池化不稳定的问题。
- 点云预处理上，先按机械臂可达性裁剪 1.3 m 外的点，再统一下采样到 4096 点，以兼顾近场几何信息和实时推理效率。
- 为训练该策略，作者构建了基于 Meta Quest 3 的轻量级 XR 全身遥操作系统，在 Unitree G1 上采集包含行走、躯干调整、双臂和灵巧手协同的示范数据。
- 一个关键工程点是点云直接使用 LiDAR 自身坐标系表示，因此部署时不需要外参标定，提升了跨环境适应性。

## Results
- **总体任务成功率（6 个任务，含仿真与真实）**：OmniDP 为 **82/120**，显著高于 **DP 18/120、DP3 22/120、iDP3 25/120**。
- **超视野（OV）任务优势非常明显**：例如仿真 **Pour (OV)**，OmniDP **12/20**，而 **DP/DP3/iDP3 全为 0/20**；真实 **Hand Over (OV)** 为 **12/20 vs 全部基线 0/20**；真实 **Pour (OV)** 为 **11/20 vs 全部基线 0/20**；真实 **Wipe (OV)** 为 **16/20 vs 全部基线 0/20**。
- **常规可视任务也更强**：仿真 Pick & Place，OmniDP **16/20**，高于 **DP 10/20、DP3 13/20、iDP3 14/20**；真实 Pick & Place，OmniDP **15/20**，高于 **8/20、9/20、11/20**。
- **避障评测**：在障碍物位于相机视野外时，OmniDP 成功率 **14/20**、碰撞率 **5/20**；而 **DP 0/20, 20/20**，**DP3 0/20, 18/20**，**iDP3 0/20, 18/20**，说明全向感知显著提升了安全性。
- **泛化评测（Pick & Place）**：不同实例 **13/20**、不同光照 **15/20**、不同场景 **12/20**，均优于 **iDP3 的 12/20、12/20、10/20**，也优于更弱的 DP/DP3。
- **消融实验**：在 Hand Over 任务上，完整 OmniDP **12/20**；去掉全向观测后 **0/20**；去掉 TAP 后降为 **9/20**，表明 360° 感知和时间注意池化都对性能关键。

## Link
- [http://arxiv.org/abs/2603.05355v2](http://arxiv.org/abs/2603.05355v2)
