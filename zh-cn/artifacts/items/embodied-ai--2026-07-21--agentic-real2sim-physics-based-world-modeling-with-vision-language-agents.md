---
source: arxiv
url: https://arxiv.org/abs/2607.19190v1
published_at: '2026-07-21T15:23:38'
authors:
- Guanxiong Chen
- Qianjun Xia
- Jiawei Peng
- Heng Zhang
- Bole Ma
- Justin Qian
- Ziyi Jiao
- Bingyang Zhou
- Luoxin Ye
- Kaifeng Zhang
- Kunyi Wang
- Weijia Zeng
- Yunuo Chen
- Pengzhi Yang
- Ziqiu Zeng
- Huamin Wang
- Chao Liu
- Alan Yuille
- Fan Shi
- Changxi Zheng
- Yunzhu Li
- Chenfanfu Jiang
- Peter Yichen Chen
topics:
- real-to-sim
- world-modeling
- vision-language-agents
- robot-manipulation
- simulator-in-the-loop
- digital-twins
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents

## Summary
## 摘要
Agentic Real2Sim 将记录的机器人—物体交互转换为基于物理的可仿真情节孪生体。该方法结合视觉语言智能体、确定性视觉感知、场景组装和仿真器闭环优化，支持刚体操作，并对可变形物体交互和人形机器人情节进行了定性扩展。

## 问题
- 从真实环境到仿真的转换需要恢复几何结构、物体状态、物理参数、相机与机器人的对齐关系、接触关系和轨迹；人工调参使这一过程缓慢且脆弱。
- 这一问题之所以重要，是因为可复用且与真实世界对齐的仿真情节能够支持多种交互类型中的机器人策略学习与评估。

## 方法
- 共享的情节契约存储观测、参与体、几何结构、仿真器状态、物理参数与对齐参数、仿真后端以及回放指标。
- 四个相互衔接的阶段使用智能体完成物体发现、关键帧和掩码选择、物理先验推断、场景准备与修复决策；确定性工具则执行分割、网格恢复、深度估计、位姿跟踪、标定和抓取优化。
- 系统将重建的情节载入 MuJoCo，并通过抓取扫描或智能体驱动的回放优化循环，根据仿真证据调整物体位置。
- 领域适配器复用该契约，以支持 PhysTwin 风格的可变形物体交互和 BFM-Zero 风格的人形机器人运动，但这些扩展仅进行了定性评估，没有汇总评分。

## 结果
- 在随机抽取的 100 个 DROID 操作情节上，Gemma 4 31B 后端获得了 48 次回放成功、8 次部分成功和 44 次失败；回放成功要求评审分数至少达到 8/10。
- 四个 VLM 后端的回放成功次数分别为：Gemma 4 31B 为 48/100，Qwen 3.6 35B 为 45/100，GPT-5.4 为 43/100，Claude Haiku 4.5 为 37/100。
- 模型费用从 Gemma 4 31B 的 $2.62 到 GPT-5.4 的 $82.30 不等；在报告的配置下，Claude、Qwen 和 GPT-5.4 的费用分别是 Gemma 的 3.5 倍、5.0 倍和 31.4 倍。
- 可变形物体和人形机器人转换展示了具有代表性的真实—仿真匹配结果及失败案例，但论文没有报告这些领域的定量汇总结果。
- 结果表明，开放权重的 31B VLM 可以取得与其他后端相当的实际回放结果；同时也显示，所有后端的绝对回放成功率均低于 50%，并且仍容易受到上游感知和仿真错误的影响。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19190v1](https://arxiv.org/abs/2607.19190v1)
