---
source: arxiv
url: https://arxiv.org/abs/2606.18632v1
published_at: '2026-06-17T03:03:16'
authors:
- Zhuowen Yin
- Chongyang Liu
- Wenzhang Yang
- Renjue Li
- Yinxing Xue
topics:
- embodied-foundation-models
- robot-safety
- vision-language-action
- synthetic-data
- hazard-benchmark
- refusal-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models

## Summary
## 摘要
RoboShackles 是一个合成安全数据集，用于测试具身基础模型是否会拒绝可能伤人的机器人动作。它基于真实 DROID 观测构建了 10,000 个危险机器人视频片段，并发现 6 个受测 EFM 在每个测试类别中都会生成不安全动作。

## 问题
- EFM 可以把模型输出转成实体机器人动作，因此错误回答可能造成直接伤害，或在家庭环境中制造危险。
- 机器人伤人或造成危险情况的真实视频无法以安全、合乎伦理的方式收集，这使伤害预防训练和评估缺少数据。
- 现有 EFM 安全研究常测试攻击或控制约束，但对直接伤害和延迟危险的覆盖有限，例如火灾、溢水、触电和物体坠落。

## 方法
- 流水线从真实 DROID 机器人观测开始，使用约 90,000 个经过筛选的第三人称机器人片段作为源材料。
- Qwen3-VL 分析每个场景，并编写特定类别的图像编辑指令；Qwen-Image 编辑初始帧，加入安全关键状态。
- 随后 Qwen3-VL 编写时序视频提示，Wan2.7 根据编辑后的帧和提示，一次生成未来机器人执行过程。
- 人类审核员过滤掉存在严重伪影、标签错误、机器人运动不可信、物体身份漂移或提示与视频不匹配的样本。
- 评估采用严格的拒绝规则：只有当模型拒绝指令或不生成可执行动作时，才判定为安全。

## 结果
- RoboShackles 包含 10,000 个机器人视频片段，覆盖 6 个类别：2 个直接伤害类别，即手部伤害和人体伤害；4 个间接伤害类别，即火灾、电气、水和坠落风险。
- 测试集包含 1,200 个样本，每个类别 200 个样本。
- 自动视频检查报告显示，所有 6 个类别的 PSP = 1.000、TAC = 1.000；所有 6 个类别的 RSS = 1.000；MSS 从电气危险的 0.946 到手部和人体直接伤害的 1.000 不等。
- 运动幅度因类别而异：机器人 MA-R 从手部伤害的 0.184 到人体伤害的 0.491 不等；物体 MA-O 从用水安全的 0.122 到人体伤害的 0.403 不等。
- 6 个受评估的 EFM，Cosmos-Policy、DreamZero、LingBot-VA、FastWAM、VLA-JEPA 和 World Guidance，在全部 6 个类别中的不安全动作生成率均为 100%。
- 摘录没有给出训练后安全性提升的定量结果，因此有数据支持的主要结论是：在该数据集上，所有受测模型都未通过基于拒绝的安全标准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18632v1](https://arxiv.org/abs/2606.18632v1)
