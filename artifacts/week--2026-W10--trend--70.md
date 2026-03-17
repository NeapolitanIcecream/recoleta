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
---

# 机器人VLA迈向可部署系统：按需推理、记忆插件与安全世界模型

## Overview
本周机器人研究高度收敛。中心问题很明确：怎样把VLA和世界模型从“能做”推进到“能稳、能省、能上线”。一条主线是按需推理。不少系统不再默认每一步都调用大模型，而是让高层推理只在关键节点出现。这样既省算力，也更适合长时程任务。Tri-System是这一思路的代表：它在高层视觉语言模型和低层控制器之间加入Critic监控，执行正常时保持快速闭环，遇到停滞或异常再触发重规划。

## Clusters

### VLA转向按需推理与失败恢复

本周最强主线是把视觉-语言-动作模型（VLA）从演示系统推向可部署系统。方法不再追求每一步都做重推理，而是强调按需唤醒、异步调度和失败恢复。代表工作是 Tri-System：用视觉 Critic 监控执行，只在子任务完成、事故或停滞时唤醒高层 VLM，在真实长任务中明显优于单系统与双系统方案。

#### Representative sources
- [Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation](../Inbox/2026-03-05--critic-in-the-loop-a-tri-system-vla-framework-for-robust-long-horizon-manipulation.md) — Pengfei Yi; Yingjie Ma; Wenjiang Xu; Yanan Hao; Shuai Gan; Wanting Li; …


### 机器人记忆从概念走向评测与插件化增强

记忆不再只是“给模型加历史”。本周更强调两件事：先把记忆需求测清楚，再用更轻的方式补上时序能力。RoboMME把记忆拆成 temporal、spatial、object、procedural 四类，并显示不存在通吃方案。TempoFit则走插件路线，直接复用层级 K/V 缓存，在不训练的前提下提升长时程操作成功率。

#### Representative sources
- [RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies](../Inbox/2026-03-04--robomme-benchmarking-and-understanding-memory-for-robotic-generalist-policies.md) — Yinpei Dai; Hongze Fu; Jayjun Lee; Yuejiang Liu; Haoran Zhang; Jianing Yang; …
- [TempoFit: Plug-and-Play Layer-Wise Temporal KV Memory for Long-Horizon Vision-Language-Action Manipulation](../Inbox/2026-03-08--tempofit-plug-and-play-layer-wise-temporal-kv-memory-for-long-horizon-vision-language-action-manipulation.md) — Jun Sun; Boyu Yang; Jiahao Zhang; Ning Ma; Chencheng Wu; Siqing Zhang; …


### 世界模型走向结构化动态表示与安全接口

世界模型的关注点明显变化。重点不再是生成更像的视频，而是学到对控制有用的动态表征，并把这种表征接到安全监测和决策上。CoWVLA用潜在运动链替代冗余未来帧重建，在 LIBERO 上达到 0.956。另一条线则把概率世界模型用于运行时异常检测，在双臂失效检测上做到 92.0±6.4% 总体准确率。

#### Representative sources
- [Chain of World: World Model Thinking in Latent Motion](../Inbox/2026-03-03--chain-of-world-world-model-thinking-in-latent-motion.md) — Fuxiang Yang; Donglin Di; Lulu Tang; Xuancheng Zhang; Lei Fan; Hao Li; …
- [Foundational World Models Accurately Detect Bimanual Manipulator Failures](../Inbox/2026-03-07--foundational-world-models-accurately-detect-bimanual-manipulator-failures.md) — Isaac R. Ward; Michelle Ho; Houjun Liu; Aaron Feldman; Joseph Vincent; Liam Kruse; …


### 轻量适配与视角鲁棒成为部署补丁层

真实部署的另一条主线是少改模型、多补接口。AnyCamVLA在不加示教、不微调策略的前提下，把测试视角实时变回训练视角，显著提升相机扰动鲁棒性。同期的轻量适配工作也在减少任务迁移成本，说明社区正把“如何低成本上线”放到和“如何提分”同等重要的位置。

#### Representative sources
- [AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models](../Inbox/2026-03-06--anycamvla-zero-shot-camera-adaptation-for-viewpoint-robust-vision-language-action-models.md) — Hyeongjun Heo; Seungyeon Woo; Sang Min Kim; Junho Kim; Junho Lee; Yonghyeon Lee; …
