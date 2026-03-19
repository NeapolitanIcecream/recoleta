---
source: arxiv
url: http://arxiv.org/abs/2603.04819v1
published_at: '2026-03-05T05:10:47'
authors:
- Pradyumna Tambwekar
- Andrew Silva
- Deepak Gopinath
- Jonathan DeCastro
- Xiongyi Cui
- Guy Rosman
topics:
- embodied-assistance
- synthetic-data
- multimodal-learning
- open-set-generalization
- overcooked
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# On the Strengths and Weaknesses of Data for Open-set Embodied Assistance

## Summary
本文研究开放集具身辅助中的一个核心问题：仅靠合成交互数据训练的多模态助手，能否在**未见过的用户缺陷**和**新任务配置**上给出纠正动作或自然语言指导。论文在 Overcooked 中构建了开放集纠正辅助基准，并表明数据设计而非单纯模型调用，对泛化能力至关重要。

## Problem
- 要解决的是**开放集纠正辅助**：模型需要阅读长时序、多模态用户行为轨迹，在**没有固定纠错类别列表**的前提下，生成纠正动作或语言反馈。
- 这很重要，因为真实辅助机器人/交互式具身系统必须面对**新用户、新错误模式、新任务**，而真实长时交互数据又昂贵、噪声大、难采集。
- 现有方法通常依赖**封闭类别纠错**或**外部规划器**，难以检验模型是否真正学会了跨缺陷、跨任务泛化的辅助能力。

## Approach
- 作者在 Overcooked 中用**程序化地图 + 合成用户 + 缺陷注入**生成长时序轨迹：5种启发式用户策略、17类缺陷（含 no defect）、每步20%随机动作、450个程序生成地图。
- 模型采用**Llama-3 + ViT-base** 的投影式多模态结构：把整段轨迹的图像编码成视觉 token，与动作文本交错输入，再统一输出文本形式的**教练式反馈**或**纠正动作**。
- 训练数据分成两类：一类是**grounding 数据**，教模型看懂图像、时间变化和环境事件；另一类是**task-specific 数据**，教模型分析缺陷并给出辅助，包括 coaching、corrections、defect-delineation 三个任务。
- 教练文本、推理轨迹等监督信号由 GPT-4o 辅助合成，并带有自检/投票过滤，以提升标签质量与风格多样性。
- 核心机制可简化为：**先让模型学会“看懂发生了什么”，再学会“判断哪里出错了”，最后生成“怎么纠正”**，并测试它是否能迁移到没见过的错误和新配方任务。

## Results
- 在**未见缺陷泛化**上，作者方法优于 GPT-4o behavior critic 基线。Coaching：Behavior Critic 21.00，Behavior Critic + Summaries 55.70，Ours 1B 76.60，Ours 8B **77.80**。
- 在**未见缺陷的纠正动作**上，Ours 1B **55.70**，Ours 8B 54.60，显著高于 Behavior Critic 20.40 和 Behavior Critic + Summaries 19.80；说明该设定下性能在 1B 左右已趋于饱和。
- 在**新任务/新配方泛化**上，模型缩放更关键。Coaching：Behavior Critic 34.21，Behavior Critic + Summaries 71.05，Ours 1B 50.88，Ours 8B **85.96**。
- 在**新任务的纠正动作**上，Ours 8B **56.67**，优于 Ours 1B 50.83、Behavior Critic 9.17、Behavior Critic + Summaries 15.83。
- 数据规模与构成方面，论文明确给出训练集组成：Image-QA 55,000，Trajectory-QA 54,000，Video-QA 55,000，Coaching 26,000，Corrections 27,000，Defect-Delineation 20,000；最强结论是**多样且互补的数据覆盖（grounding、缺陷理解、场景多样性）是开放集辅助泛化的关键**。

## Link
- [http://arxiv.org/abs/2603.04819v1](http://arxiv.org/abs/2603.04819v1)
