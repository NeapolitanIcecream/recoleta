---
kind: trend
trend_doc_id: 70
granularity: week
period_start: '2026-03-02T00:00:00'
period_end: '2026-03-09T00:00:00'
topics:
- robotics
- vla
- world-models
- memory
- deployment
- adaptive-inference
- safety
- embodied-ai
run_id: materialize-outputs
aliases:
- recoleta-trend-70
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/world-models
- topic/memory
- topic/deployment
- topic/adaptive-inference
- topic/safety
- topic/embodied-ai
---

# VLA走向可部署机器人：按需推理、动力学建模与长时程记忆升温

## Overview
这一周的机器人研究很集中。主线很明确：把VLA从“能做”推向“能部署”，把世界模型从“会生成”推向“会控制”。记忆、鲁棒性和运行时效率，正在一起成为核心指标。趋势一：VLA进入可部署阶段这条线最清楚。研究者开始正面处理真实环境里的延迟、失败恢复和硬件约束。Tri-System代表了“按需推理”思路。

## Clusters

### VLA进入可部署阶段：按需推理、分层控制与边缘落地

本周最强主线是把视觉-语言-动作模型（VLA）从“会做演示”推向“能稳定部署”。工作集中在按需推理、失败恢复、边缘端运行和物理约束。Tri-System用Critic只在必要时唤醒慢速规划，真实长任务整体成功数明显高于单双系统。LiteVLA-Edge则证明256M量级模型可在Jetson Orin本地闭环运行。PhysiFlow把语义理解、高频动作生成和稳定跟踪拆开，说明人形全身控制也在走分层化。

#### Representative papers
- [Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation](../Inbox/2026-03-05--critic-in-the-loop-a-tri-system-vla-framework-for-robust-long-horizon-manipulation.md) — Pengfei Yi; Yingjie Ma; Wenjiang Xu; Yanan Hao; Shuai Gan; Wanting Li; …
- [LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics](../Inbox/2026-03-03--litevla-edge-quantized-on-device-multimodal-control-for-embedded-robotics.md) — Justin Williams; Kishor Datta Gupta; Roy George; Mrinmoy Sarkar
- [PhysiFlow: Physics-Aware Humanoid Whole-Body VLA via Multi-Brain Latent Flow Matching and Robust Tracking](../Inbox/2026-03-05--physiflow-physics-aware-humanoid-whole-body-vla-via-multi-brain-latent-flow-matching-and-robust-tracking.md) — Weikai Qin; Sichen Wu; Ci Chen; Mengfan Liu; Linxi Feng; Xinru Cui; …


### 动作表示转向连续动力学，世界模型开始直接服务控制

另一条持续升温的线索是，模型不再只学动作标签，而是更直接学习“动作之后世界如何变化”。Pri4R用3D点轨迹做训练期辅助监督，在不增加测试开销的前提下提升操控表现。CoWVLA则把世界模型压到潜在运动空间，减少对静态背景的浪费。这里的共同目标不是更像视频生成，而是让动力学表征真正服务控制。

#### Representative papers
- [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](../Inbox/2026-03-02--pri4r-learning-world-dynamics-for-vision-language-action-models-with-privileged-4d-representation.md) — Jisoo Kim; Jungbin Cho; Sanghyeok Chu; Ananya Bal; Jinhyung Kim; Gunhee Lee; …
- [Chain of World: World Model Thinking in Latent Motion](../Inbox/2026-03-03--chain-of-world-world-model-thinking-in-latent-motion.md) — Fuxiang Yang; Donglin Di; Lulu Tang; Xuancheng Zhang; Lei Fan; Hao Li; …


### 记忆从能力口号变成系统设计：多尺度、可压缩、面向长时程

本周长时程能力的讨论明显更具体。重点从“加更多历史”转向“需要什么记忆、怎样压缩、何时调用”。MEM把短期视频记忆和长期语言记忆分开处理，面向分钟级任务。日度综述也反复强调记忆评测、关键帧历史和插件式时间记忆，说明记忆正在从附属模块变成通用机器人策略的核心设计面。

#### Representative papers
- [MEM: Multi-Scale Embodied Memory for Vision Language Action Models](../Inbox/2026-03-04--mem-multi-scale-embodied-memory-for-vision-language-action-models.md) — Marcel Torne; Karl Pertsch; Homer Walke; Kyle Vedder; Suraj Nair; Brian Ichter; …


### 研究重心转向补短板：语言服从、视角鲁棒、杂乱场景与安全监测

部署短板修补成为高频主题。语言服从、相机视角变化、杂乱场景筛选和运行时安全都被单独拿出来做。IGAR揭示VLA会忽视矛盾指令，并用免训练注意力重校准修补。AnyCamVLA用测试时视角合成提升零样本相机适配。HSC-VLA则在高密度杂乱场景中先做场景清理再执行动作，显著提升双臂任务稳定性。世界模型一侧也开始被用于失效检测与安全接口。

#### Representative papers
- [Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration](../Inbox/2026-03-06--restoring-linguistic-grounding-in-vla-models-via-train-free-attention-recalibration.md) — Ninghao Zhang; Bin Zhu; Shijie Zhou; Jingjing Chen
- [AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models](../Inbox/2026-03-06--anycamvla-zero-shot-camera-adaptation-for-viewpoint-robust-vision-language-action-models.md) — Hyeongjun Heo; Seungyeon Woo; Sang Min Kim; Junho Kim; Junho Lee; Yonghyeon Lee; …
- [HSC-VLA: Hierarchical Scene-Clearing for Robust Bimanual Manipulation in Dense Clutter](../Inbox/2026-03-08--hsc-vla-hierarchical-scene-clearing-for-robust-bimanual-manipulation-in-dense-clutter.md) — Zhen Liu; Xinyu Ning; Zhe Hu; XinXin Xie; Yitong Liu; Zhongzhu Pu
