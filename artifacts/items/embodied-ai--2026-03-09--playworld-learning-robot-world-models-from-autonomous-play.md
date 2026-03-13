---
source: arxiv
url: http://arxiv.org/abs/2603.09030v2
published_at: '2026-03-09T23:58:07'
authors:
- Tenny Yin
- Zhiting Mei
- Zhonghe Zheng
- Miyu Yamane
- David Wang
- Jade Sceats
- Samuel M. Bateman
- Lihan Zha
- Apurva Badithela
- Ola Shorinwa
- Anirudha Majumdar
topics:
- robot-world-model
- autonomous-play
- video-diffusion
- policy-evaluation
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
---

# PlayWorld: Learning Robot World Models from Autonomous Play

## Summary
PlayWorld提出一种从机器人自主“玩耍”数据中学习动作条件视频世界模型的框架，目标是更真实地预测接触丰富的操控动态。核心主张是：比起成功偏置的人类示教，自动自玩数据更适合训练可扩展、物理一致的机器人世界模型。

## Problem
- 现有机器人视频世界模型多依赖人类示教数据，数据分布集中在**成功轨迹**，缺少失败、碰撞、打滑、形变等关键接触事件。
- 这会导致模型在闭环预测时出现物理幻觉，如物体重复、消失、非真实移动，从而削弱策略评估、规划和RL微调的可靠性。
- 这个问题重要，因为接触丰富的操控任务正是现实机器人落地的难点；如果世界模型无法可靠模拟这些动态，就很难成为真正有用的数据驱动模拟器。

## Approach
- 用一个**VLM任务提议器**根据当前场景图像自动生成多样化自然语言指令，再由预训练**VLA执行策略**去执行，从而在真实机器人上持续收集无监督自玩交互数据。
- 这种机制本质上是在让机器人“自己给自己出题并尝试完成”，通过指令扰动和不同初始物体状态，自然产生更丰富的成功与失败接触模式。
- 为支持长时间无人值守采集，系统加入了轻量安全过滤与场景重置机制，可连续运行长达**8小时**，包括夜间采集。
- 世界模型采用预训练的**stable video diffusion**动作条件视频骨干，联合预测**3个相机视角**，并在自玩数据上微调。
- 为了更好学习长尾交互，作者使用基于**CLIP到成功轨迹距离**的课程学习：先学接近成功的简单片段，再逐步加入更罕见、更难的探索性交互。

## Results
- 在交互中心基准上，**Robot Play (6h)** 相比 **Human Demo (6h)** 在多个接触失败模式上显著更好：例如**missed grasp** 的 LPIPS **0.080→0.066**、SSIM **0.875→0.883**；**slide** 的 LPIPS **0.090→0.077**；**slip** 的 LPIPS **0.090→0.078**；**collision** 的 LPIPS **0.086→0.074**、SSIM **0.852→0.888**。
- 将机器人自玩数据从 **6h 扩展到 30h** 后，性能继续提升：例如**success** 的 LPIPS **0.082→0.071**；**slide** 的 LPIPS **0.077→0.073**、SSIM **0.865→0.876**；说明自玩数据缩放后仍能带来收益。
- 加入课程学习后进一步提升：**Robot Play (Curriculum)** 在 **success** 上达到 LPIPS **0.070** / SSIM **0.880**，在 **slide** 上达到 LPIPS **0.071** / SSIM **0.890**，在 **collision** 上达到 LPIPS **0.072** / SSIM **0.893**，优于未加课程的 30h 自玩模型。
- 论文声称，基于PlayWorld训练的模型在**策略评估与失败预测**上，相比人类采集数据可带来**最高40%改进**。
- 论文还声称，利用该世界模型进行**模型内强化学习**后，真实机器人部署时策略成功率可提升**65%**（相对预训练策略）。
- 数据缩放方面，作者宣称PlayWorld的下游视觉精度在**人类示教数据已饱和的5×规模**下仍持续改进，强调其可扩展性与长尾交互覆盖优势。

## Link
- [http://arxiv.org/abs/2603.09030v2](http://arxiv.org/abs/2603.09030v2)
