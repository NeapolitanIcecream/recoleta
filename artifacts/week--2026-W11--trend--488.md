---
kind: trend
trend_doc_id: 488
granularity: week
period_start: '2026-03-09T00:00:00+00:00'
period_end: '2026-03-16T00:00:00+00:00'
topics:
- robotics
- VLA
- data-engine
- active-perception
- dexterous-manipulation
- long-horizon
- deployment
run_id: 83a94555-49f1-456e-8e7a-73d57da2b973
aliases:
- recoleta-trend-488
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/data-engine
- topic/active-perception
- topic/dexterous-manipulation
- topic/long-horizon
- topic/deployment
pass_output_id: 55
pass_kind: trend_synthesis
---

# 机器人VLA走向闭环造数、主动感知与部署级系统优化

## Overview
本周机器人研究的共识更清晰了：VLA不再只追求更大，而是补齐数据、恢复、感知和部署这几块最影响落地的短板。一条最强主线是闭环造数。Seed2Scale说明，具身数据不必持续重度依赖人工示教。随后RADAR、RoboClaw进一步把任务生成、执行、验证和复位并入系统流程，意味着“收数据”本身正在变成自动化能力，而不是训练前的人力准备。第二条主线是VLA增强重心后移。本周有效的方法不只来自预训练。

## Evolution

与prev1相比，本周延续了“更稳、更省、更能部署”的总方向，但内部重心已明显移动。持续存在的是部署链优化：按需计算的思路还在，只是从单点插件扩展为压缩、报警与服务栈协同。变化最大的两条线，一是长时程能力从记忆评测与插件化，转向未来预测、进度验证和失败恢复；二是闭环造数快速升温，数据采集、验证与环境复位开始被系统化。

### 部署稳健性与按需计算继续推进

- 变化：延续
- 历史窗口：[机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md)

相较 [机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md) 中以 Tri-System 和 TempoFit 为代表的“按需推理 + 记忆插件”路线，本周“稳态部署”这条线继续存在，但证据更靠近完整执行链。DepthCache 给出1.07×–1.28×推理加速且成功率几乎不掉，RC-NF 把异常报警压到100 ms以内，OxyGen 则把统一KV缓存管理做进多任务服务栈。这说明关注点仍是省算力与稳运行，但对象已从单个记忆或调度插件，扩展到压缩、报警和服务编排的整链路优化。

### 长时程能力从记忆插件转向未来预测与恢复

- 变化：转向
- 历史窗口：[机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md)

相较 [机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md) 里 RoboMME 对机器人记忆类型的评测拆解，以及 TempoFit 这类可插拔时序记忆，本周长时程研究的重心发生转移。AR-VLA 开始强调连续动作历史，SPR 强调可验证子目标与回退，而 DiT4DiT 和 FutureVLA 更进一步，直接预测动作后的世界变化，分别在 LIBERO 达到98.6%，在 LIBERO Long 达到96.0%，后者还在真实 Franka 四任务平均70.0%。本周不再只问“记住了什么”，而是更关心“接下来会发生什么、偏航后如何纠正”。

### 自进化数据引擎与自复位采集成为新增长点

- 变化：新出现
- 历史窗口：[机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md)

相较 [机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md) 中世界模型更强调结构化动态表示与安全接口，本周出现了更强的“闭环造数”信号。Seed2Scale 只用4条种子示范就把平均成功率拉到68.57%；RADAR 把任务生成、执行、验证与自主复位串成自动采集系统；RoboClaw 则把数据采集、策略学习和部署代理统一起来。世界模型和数据引擎开始从辅助训练的组件，变成能持续产出、筛选并复位环境的生产基础设施。

### 主动感知成为VLA的新能力层

- 变化：新出现
- 历史窗口：[机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md)

[机器人VLA迈向可部署系统 (2026-W10)](week--2026-W10--trend--70.md) 已经讨论了可部署系统，但本周新增了一条更鲜明的主动感知路线。VLA-Thinker 允许模型在推理中重新查看局部区域，在 LIBERO 达到97.5%，比 OpenVLA-OFT 高6.5个百分点，在 Long 子集高10.4个百分点；SaPaVe 也指出失败常源于“没先看清楚”。这类结果表明，机器人VLA的改进点正从被动编码观察，转向运行时主动补充视觉证据。

## Clusters

### 闭环造数与自复位系统升温

本周最稳定的主线，是把数据生产做成机器人自己能跑的闭环。Seed2Scale 只用4条种子示范，就通过“小模型采集 + 大模型验真 + 目标策略学习”把平均成功率拉到68.57%。随后 RADAR 与 RoboClaw 又把任务生成、执行、验证、复位和部署代理串成系统，说明“复位”和“失败恢复”正从人工劳动变成训练基础设施。

#### Representative sources
- [Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation](../Inbox/2026-03-09--seed2scale-a-self-evolving-data-engine-for-embodied-ai-via-small-to-large-model-synergy-and-multimodal-evaluation.md) — Cong Tai; Zhaoyu Zheng; Haixu Long; Hansheng Wu; Zhengbin Long; Haodong Xiang; …
- [RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset](../Inbox/2026-03-12--radar-closed-loop-robotic-data-generation-via-semantic-planning-and-autonomous-causal-environment-reset.md) — Yongzhong Wang; Keyu Zhu; Yong Zhong; Liqiong Wang; Jinyu Yang; Feng Zheng
- [RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks](../Inbox/2026-03-12--roboclaw-an-agentic-framework-for-scalable-long-horizon-robotic-tasks.md) — Ruiying Li; Yunlang Zhou; YuYao Zhu; Kylin Chen; Jingyuan Wang; Sukai Wang; …
- [RoboRouter: Training-Free Policy Routing for Robotic Manipulation](../Inbox/2026-03-09--roborouter-training-free-policy-routing-for-robotic-manipulation.md) — Yiteng Chen; Zhe Cao; Hongjia Ren; Chenjie Yang; Wenbo Li; Shiyi Wang; …
- [MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation](../Inbox/2026-03-09--metaworld-x-hierarchical-world-modeling-via-vlm-orchestrated-experts-for-humanoid-loco-manipulation.md) — Yutong Shen; Hangxu Liu; Penghui Liu; Jiashuo Luo; Yongkang Zhang; Rex Morvley; …
- [TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation](../Inbox/2026-03-10--tiptop-a-modular-open-vocabulary-planning-system-for-robotic-manipulation.md) — William Shen; Nishanth Kumar; Sahit Chintalapudi; Jie Wang; Christopher Watson; Edward Hu; …


### VLA从预训练竞赛转向后训练与主动感知

VLA（视觉-语言-动作模型）的增强点，已明显从单次预训练扩展到后训练、运行时和主动感知。AtomVLA 用原子子任务与潜在世界模型奖励补长时程执行；OmniGuide 在不重训的情况下加入几何与语义引导；VLA-Thinker 允许推理中重新查看局部图像，在 LIBERO 达到97.5%，比 OpenVLA-OFT 高6.5个百分点，在 Long 子集高10.4个百分点。

#### Representative sources
- [AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models](../Inbox/2026-03-09--atomvla-scalable-post-training-for-robotic-manipulation-via-predictive-latent-world-models.md) — Xiaoquan Sun; Zetian Xu; Chen Cao; Zonghe Liu; Yihan Sun; Jingrui Pang; …
- [NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models](../Inbox/2026-03-10--ns-vla-towards-neuro-symbolic-vision-language-action-models.md) — Ziyue Zhu; Shangyang Wu; Shuai Zhao; Zhiqiu Zhao; Shengjie Li; Yi Wang; …
- [VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning](../Inbox/2026-03-15--vla-thinker-boosting-vision-language-action-models-through-thinking-with-image-reasoning.md) — Chaoyang Wang; Wenrui Bao; Sicheng Gao; Bingxin Xu; Yu Tian; Yogesh S. Rawat; …
- [FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model](../Inbox/2026-03-11--futurevla-joint-visuomotor-prediction-for-vision-language-action-model.md) — Xiaoxu Xu; Hao Li; Jinhui Ye; Yilun Chen; Jia Zeng; Xinyi Chen; …
- [AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control](../Inbox/2026-03-15--aerialvla-a-vision-language-action-model-for-uav-navigation-via-minimalist-end-to-end-control.md) — Peng Xu; Zhengnan Deng; Jiayan Deng; Zonghua Gu; Shaohua Wan
- [AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models](../Inbox/2026-03-10--ar-vla-true-autoregressive-action-expert-for-vision-language-action-models.md) — Yutong Hu; Jan-Nico Zaech; Nikolay Nikolov; Yuanqi Yao; Sombit Dey; Giuliano Albanese; …


### 灵巧操作转向共享表示与接触基础设施

灵巧操作不再只比策略分数，而是同时补共享表示、人在回路纠错、接触建模和采集仿真。XL-VLA 将不同灵巧手动作映射到共享潜在空间，在4种灵巧手、10个任务上把总体成功率从约0.32提升到0.72。FAR-Dex 则把少样本示教扩增与残差控制结合，在4个任务上达到83%–95%成功率，并把每步延迟压到3.0–4.3 ms。

#### Representative sources
- [FAR-Dex: Few-shot Data Augmentation and Adaptive Residual Policy Refinement for Dexterous Manipulation](../Inbox/2026-03-11--far-dex-few-shot-data-augmentation-and-adaptive-residual-policy-refinement-for-dexterous-manipulation.md) — Yushan Bai; Fulin Chen; Hongzheng Sun; Yuchuang Tong; En Li; Zhengtao Zhang
- [Cross-Hand Latent Representation for Vision-Language-Action Models](../Inbox/2026-03-10--cross-hand-latent-representation-for-vision-language-action-models.md) — Guangqi Jiang; Yutong Liang; Jianglong Ye; Jia-Yang Huang; Changwei Jing; Rocky Duan; …
- [DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation](../Inbox/2026-03-10--dexhil-a-human-in-the-loop-framework-for-vision-language-action-model-post-training-in-dexterous-manipulation.md) — Yifan Han; Zhongxi Chen; Yuxuan Zhao; Congsheng Xu; Yanming Shao; Yichuan Peng; …
- [Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation](../Inbox/2026-03-11--contact-coverage-guided-exploration-for-general-purpose-dexterous-manipulation.md) — Zixuan Liu; Ruoyi Qiao; Chenrui Tie; Xuanwei Liu; Yunfan Lou; Chongkai Gao; …
- [Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA](../Inbox/2026-03-09--towards-human-like-manipulation-through-rl-augmented-teleoperation-and-mixture-of-dexterous-experts-vla.md) — Tutian Tang; Xingyu Ji; Wanli Xing; Ce Hao; Wenqiang Xu; Lin Shao; …
- [Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation](../Inbox/2026-03-09--seed2scale-a-self-evolving-data-engine-for-embodied-ai-via-small-to-large-model-synergy-and-multimodal-evaluation.md) — Cong Tai; Zhaoyu Zheng; Haixu Long; Hansheng Wu; Zhengbin Long; Haodong Xiang; …


### 长时程控制走向未来预测与显式恢复

长时程能力的重点，已从“有没有记忆模块”转向“能否预测后果、识别偏航并及时纠错”。DiT4DiT 与 FutureVLA 直接把未来动力学放进控制模型，分别在 LIBERO 达到98.6%，在 LIBERO Long 达到96.0%，后者还在真实 Franka 四任务上做到70.0%。AR-VLA、SPR 和 VLA-Thinker 则从动作历史、进度验证和再观察机制补上恢复链路。

#### Representative sources
- [AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models](../Inbox/2026-03-10--ar-vla-true-autoregressive-action-expert-for-vision-language-action-models.md) — Yutong Hu; Jan-Nico Zaech; Nikolay Nikolov; Yuanqi Yao; Sombit Dey; Giuliano Albanese; …
- [AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control](../Inbox/2026-03-15--aerialvla-a-vision-language-action-model-for-uav-navigation-via-minimalist-end-to-end-control.md) — Peng Xu; Zhengnan Deng; Jiayan Deng; Zonghua Gu; Shaohua Wan
- [FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model](../Inbox/2026-03-11--futurevla-joint-visuomotor-prediction-for-vision-language-action-model.md) — Xiaoxu Xu; Hao Li; Jinhui Ye; Yilun Chen; Jia Zeng; Xinyi Chen; …
- [AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models](../Inbox/2026-03-09--atomvla-scalable-post-training-for-robotic-manipulation-via-predictive-latent-world-models.md) — Xiaoquan Sun; Zetian Xu; Chen Cao; Zonghe Liu; Yihan Sun; Jingrui Pang; …
- [NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models](../Inbox/2026-03-10--ns-vla-towards-neuro-symbolic-vision-language-action-models.md) — Ziyue Zhu; Shangyang Wu; Shuai Zhao; Zhiqiu Zhao; Shengjie Li; Yi Wang; …
- [EvoDriveVLA: Evolving Autonomous Driving Vision-Language-Action Model via Collaborative Perception-Planning Distillation](../Inbox/2026-03-10--evodrivevla-evolving-autonomous-driving-vision-language-action-model-via-collaborative-perception-planning-distillation.md) — Jiajun Cao; Xiaoan Zhang; Xiaobao Wei; Liyuqiu Huang; Wang Zijian; Hanzhen Zhang; …


### 部署效率与推理服务栈成为新焦点

部署层创新已成为独立赛道。DepthCache 用深度先验做免训练 token 压缩，带来1.07×–1.28×加速且几乎不掉成功率；RC-NF 把异常报警压到100 ms以内；OxyGen 通过统一 KV 缓存管理，减少共享观测的重复计算，在单卡上兼顾语言生成与高频动作控制。研究焦点正从“模型更大”转向“整条执行链更稳、更省、更实时”。

#### Representative sources
- [OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism](../Inbox/2026-03-15--oxygen-unified-kv-cache-management-for-vision-language-action-models-under-multi-task-parallelism.md) — Xiangyu Li; Huaizhi Tang; Xin Ding; Weijun Wang; Ting Cao; Yunxin Liu
- [DepthCache: Depth-Guided Training-Free Visual Token Merging for Vision-Language-Action Model Inference](../Inbox/2026-03-11--depthcache-depth-guided-training-free-visual-token-merging-for-vision-language-action-model-inference.md) — Yuquan Li; Lianjie Ma; Han Ding; Lijun Zhu
- [Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation](../Inbox/2026-03-09--seed2scale-a-self-evolving-data-engine-for-embodied-ai-via-small-to-large-model-synergy-and-multimodal-evaluation.md) — Cong Tai; Zhaoyu Zheng; Haixu Long; Hansheng Wu; Zhengbin Long; Haodong Xiang; …
- [RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA Models](../Inbox/2026-03-09--rapid-redundancy-aware-and-compatibility-optimal-edge-cloud-partitioned-inference-for-diverse-vla-models--655.md) — Zihao Zheng; Sicheng Tian; Hangyu Cao; Chenyue Li; Jiayu Chen; Maoliang Li; …
- [R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation](../Inbox/2026-03-15--r3dp-real-time-3d-aware-policy-for-embodied-manipulation.md) — Yuhao Zhang; Wanxi Dong; Yue Shi; Yi Liang; Jingnan Gao; Qiaochu Yang; …
- [GST-VLA: Structured Gaussian Spatial Tokens for 3D Depth-Aware Vision-Language-Action Models](../Inbox/2026-03-10--gst-vla-structured-gaussian-spatial-tokens-for-3d-depth-aware-vision-language-action-models.md) — Md Selim Sarowar; Omer Tariq; Sungho Kim
