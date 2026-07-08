---
kind: trend
trend_doc_id: 811
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
topics:
- "\u673A\u5668\u4EBA\u64CD\u4F5C"
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "\u4E16\u754C\u6A21\u578B"
- "\u957F\u65F6\u7A0B\u63A7\u5236"
- sim-to-real
- "\u53EF\u53D8\u5F62\u7269\u4F53"
run_id: materialize-outputs
aliases:
- recoleta-trend-811
tags:
- recoleta/trend
- "topic/\u673A\u5668\u4EBA\u64CD\u4F5C"
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "topic/\u4E16\u754C\u6A21\u578B"
- "topic/\u957F\u65F6\u7A0B\u63A7\u5236"
- topic/sim-to-real
- "topic/\u53EF\u53D8\u5F62\u7269\u4F53"
language_code: zh-CN
---

# 机器人策略正在加入显式前瞻、几何和任务记忆

## Overview
当天的主线是机器人操作研究把策略内部信号做得更显式：未来状态、潜在动作、相机位姿和子任务记忆。InternVLA-A1.5、Cortex 和 CamVLA 显示了当前重点：保持语言条件控制的速度，同时加入更长、更复杂任务所需的物理或时间信号。

## Clusters

### 潜在前瞻与动作代码
多篇论文训练视觉-语言-动作模型（VLA），让策略内部携带紧凑的动作相关信号。InternVLA-A1.5 使用 50 个前瞻 token，在训练时用它们调节一个冻结的视频生成器；推理时移除视频分支，并输出 50 步连续动作块。CAC-VLA 从图像和语言 token 预测潜在动作，再通过门控交叉注意力用这些动作调节连续动作专家。GeoMoLa 采用更偏几何的方法：它通过预测未来点云变化来学习离散运动代码，然后用这些代码执行 6-DoF 操作。

这些论文报告的提升在需要泛化的任务上最明显，而不只是在模仿任务上。CAC-VLA 报告 LIBERO 平均成功率为 98.3%，LIBERO-Plus 监督微调成功率为 89.5%。GeoMoLa 在单视角 RLBench 的 10 个任务、166 个变体上报告平均成功率为 84.7%，高于 RVT2 的 80.4%。InternVLA-A1.5 声称在六个仿真基准上取得最佳整体结果，但可用摘录没有给出具体基准表。

#### Evidence
- [InternVLA-A1.5: Unifying Understanding, Latent Foresight, and Action for Compositional Generalization](../Inbox/2026-07-06--internvla-a1-5-unifying-understanding-latent-foresight-and-action-for-compositional-generalization.md): 摘要描述了 InternVLA-A1.5 的前瞻 token、使用冻结视频生成器的训练方式、实时推理、数据规模，以及六个基准上的结果主张。
- [CAC-VLA: Context-Gated Action Conditioning for Vision-Language-Action Models](../Inbox/2026-07-06--cac-vla-context-gated-action-conditioning-for-vision-language-action-models.md): 摘要给出了 CAC-VLA 的潜在动作调节机制，以及 LIBERO / LIBERO-Plus 结果。
- [Geometry-Aware Motion Latents for Learning Robust Manipulation Policies](../Inbox/2026-07-06--geometry-aware-motion-latents-for-learning-robust-manipulation-policies.md): 摘要给出了 GeoMoLa 的几何感知运动潜变量和 RLBench 成功率。

### 用受限子任务做长时程控制
长任务正通过显式子任务状态和受限技能词表来处理。Cortex 使用高层视觉-语言模型维护文本记忆，并为低层 VLA 输出子任务。它的规划器被限制在 32 个标准操作原语内，并配有模板和可达性感知标注，让低层策略接收可执行命令。

DSWAM 使用类似的拆分。它的默认路径是一个世界动作模型执行器，用来预测双臂动作块。当粗粒度家务命令需要分解时，视觉-语言规划器会被激活。在与 DeMaVLA 匹配设置下的真实折叠测试中，DSWAM 将成功率从 92.5% 提高到 96.3%，并将平均完成时间从 2'18" 缩短到 1'44"。Cortex 在真实世界 14 步化学任务上的成功率为 65%，在 14 步清洗任务上的成功率为 55%；所引用的端到端基线在这些任务上得分为 0%。

#### Evidence
- [Cortex: A Bidirectionally Aligned Embodied Agent Framework for Long-horizon Manipulation](../Inbox/2026-07-06--cortex-a-bidirectionally-aligned-embodied-agent-framework-for-long-horizon-manipulation.md): 摘要详细说明了 Cortex 的子任务记忆、32 个原语、训练标注，以及真实世界化学和清洗任务结果。
- [DSWAM: A Dual-System World Action Foundation Model for Fine-Grained Robot Manipulation](../Inbox/2026-07-06--dswam-a-dual-system-world-action-foundation-model-for-fine-grained-robot-manipulation.md): 摘要详细说明了 DSWAM 的执行器-规划器设计、与 DeMaVLA 匹配的折叠对比，以及 RoboTwin 双臂结果。

### 部署缺口：相机位姿和场景特定数据
两篇论文针对训练后的策略离开原始设置后出现的失败。CamVLA 处理相机移动问题。它在相机坐标系中预测末端执行器动作，从一张 RGB 图像估计 6-DoF 手眼变换，并把动作转换到机器人基座坐标系。在 RLBench 未见视角上，加入 CamVLA 后，π0 的平均成功率从 33.2% 提高到 51.4%。在真实 Franka 测试中，π0 + CamVLA 在 5°、10° 和 15° 相机偏移下也保持了更高成功率。

PRISM 处理缺少场景匹配演示的问题。给定一张目标场景图像和一条指令，它构建多样化的仿真“数字近亲”场景，规划轨迹，并用生成的数据训练策略。在每个任务 400 条轨迹的 sim-to-sim 测试中，PRISM 搭配 π0.5 在 LIBERO 的“把牛奶放进篮子”任务上达到 98.0%，相比之下 X-Sim 为 48.0%，RoboTwin 2.0 为 14.0%。

#### Evidence
- [From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model](../Inbox/2026-07-06--from-fixed-to-free-cameras-calibration-free-view-robust-vision-language-action-model.md): 摘要给出了 CamVLA 的相机坐标系动作设计、单图像位姿估计和视角结果。
- [PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis](../Inbox/2026-07-06--prism-personalized-robotic-dataset-generation-via-image-based-scene-and-motion-synthesis.md): 摘要给出了 PRISM 的单图像数据集生成流程和 sim-to-sim 性能对比。

### 可变形物体世界模型需要触觉和密集 3D 跟踪
Deform360 为同一控制问题增加了一条重数据路线。它收集了 198 个可变形物体，覆盖 1,980 条交互序列，使用 41 台同步相机和带触觉的夹爪。该数据集包含布料状、绳索状和体积型物体，涵盖 17 个类别中的 13 种操作原语类型。

主要贡献是成对传感。该流程重建逐帧几何，每个视角最多跟踪 1,600 个点，把轨迹提升到 3D，并用触觉接触一致性进行细化。摘要报告，视觉-触觉跟踪的 Chamfer 距离误差为 2.71×10^-5 m²，纯视觉跟踪为 1.41×10^-4 m²。视觉到接触预测在 36 个筛选视角上的平均准确率达到 88.67%。这为未来机器人世界模型提供了一个面向富接触可变形操作的具体基准。

#### Evidence
- [Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models](../Inbox/2026-07-06--deform360-a-massive-multi-view-visuotactile-dataset-for-deformable-world-models.md): 摘要给出了 Deform360 的数据集规模、传感设置、跟踪流程，以及定量跟踪和接触结果。
