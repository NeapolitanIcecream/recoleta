---
source: arxiv
url: https://arxiv.org/abs/2607.19191v1
published_at: '2026-07-21T15:26:50'
authors:
- Fan Jiang
- Zhaoxu Sun
- Mengchao Wang
- Ziyu Zhu
- Chiyu Wang
- Yunpeng Zhang
- Wenlin Liu
- Yun Wang
- Xue Zheng
- Rui Sun
- Junfeng Ni
- Hongyu Pan
- Zhongxu Sun
- Fei Yu
- Zengye Ge
- Mengmeng Du
- Nianfei Fan
- Mingchao Sun
- Yu Liu
- Yongchang
- Yanqing Zhu
- Jiahang Wang
- Ning Ying
- Yuze Xuan
- Di Yang
- Zhicheng Liu
- Zhe Gao
- Tingbing Xu
- Jiacheng Sui
- Wenjin Yang
- Junnan Lai
- Shufeng Liu
- Yuan Liu
- Zheng Zhou
- Yingliang Peng
- Dawei Cao
- Kaifeng Sheng
- Yuxiang Cai
- Fei Lu
- Mu Xu
- Ning Guo
topics:
- world-model
- interactive-video-generation
- long-horizon-rollout
- real-time-inference
- robot-data-scaling
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# ABot-World-0: Infinite Interactive World Rollout on a Single Desktop GPU

## Summary
## 摘要
ABot-World-0 是一种以动作作为条件的视频世界模型，旨在单张桌面级 GPU 上进行持久、交互式 rollout。它结合多源数据采集、长时域 rollout 训练、基于键盘的控制和低比特流式推理，以最高 16 FPS 生成 720P 视频。

## 问题
- 交互式世界模型必须在用户动作持续改变环境的长时域闭环 rollout 中，保持视觉状态的一致性。
- 现有系统面临同步动作数据、可控性、自回归漂移、延迟、吞吐量和 GPU 显存等相互耦合的限制；解决这些问题对于本地仿真、智能体学习和具身 AI 研究具有重要意义。

## 方法
- WorldExplorer 收集同步的游戏和仿真轨迹，互联网视频则补充视觉多样性；统一数据管线执行 14 项确定性质量检查，并进行 VLM 评估、动作标注和文本注释。
- 模型采用帧同步的共享键盘动作空间，同时控制摄像机移动和角色行为，并通过参考角色记忆在第三人称 rollout 中保持角色身份一致。
- 通过教师强制和 ODE 蒸馏，将双向动作条件教师模型逐步蒸馏为因果学生模型。
- LongForcing 在扩展时域教师模型的监督下，让学生模型基于自身的长时域 rollout 进行训练，目标是减少累积的自回归漂移。
- 部署栈结合轻量级 VAE 解码器、显存感知调度、低比特 DiT 推理、高效注意力机制和有界 KV 缓存，以支持流式生成。

## 结果
- 在单张 NVIDIA RTX 5090 上，该系统以最高 16 FPS 流式生成 720P 视频，动作到首帧延迟为 1.2 秒，峰值显存占用约为 19 GiB。
- 对于采集的视频、控制信号、摄像机参数和环境状态，WorldExplorer 报告在 30 FPS 下的跨模态对齐误差低于 33 ms。
- 在 WorldRoamBench 和扩展交互式 rollout 上的实验表明，该系统具备可控性、视觉质量、物理合理性和时间记忆一致性；论文摘录将这些结果描述为具有竞争力。
- 所提供的文本没有报告 WorldRoamBench 的数值分数、消融实验或逐一基线比较，因此无法根据该摘录量化 LongForcing 和完整系统的相对性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19191v1](https://arxiv.org/abs/2607.19191v1)
