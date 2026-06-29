---
source: arxiv
url: https://arxiv.org/abs/2606.24884v1
published_at: '2026-06-23T17:59:01'
authors:
- Maggie Wang
- Lars Osterberg
- Stephen Tian
- Ola Shorinwa
- Jiajun Wu
- Mac Schwager
topics:
- vision-language-action
- robot-skill-acquisition
- steerable-policies
- continual-learning
- manipulation-primitives
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# InSight: Self-Guided Skill Acquisition via Steerable VLAs

## Summary
## 摘要
InSight 训练一个 VLA 执行有名称的操作原语，然后通过 VLM 引导的机器人 rollout 添加缺失原语，目标技能不需要人工演示。这让机器人在部署后扩展已学策略，而不是只依赖最初的演示集。

## 问题
- VLA 学到的是演示数据中已有的操作行为，所以一个只训练过拾取放置、打开抽屉或舀取的机器人，可能无法完成翻转、关闭、倾倒、扭转或清扫。
- 为每个新目标技能收集人工演示成本高，强化学习在真实机器人上可能需要过多试验。

## 方法
- InSight 先用 VLM 计划、夹爪状态转换、末端执行器运动和主导运动轴，把遥操作演示切分成带标签的原语片段。
- 每个原语片段成为一个单独的训练 episode，VLA 使用原语标签作为语言提示进行微调，并学习一个用于终止的进度信号。
- 对于新任务，VLM 编写原语计划，并标记 VLA 词表中缺失的原语标签。
- 已知原语通过可操控的 VLA 执行。缺失原语通过低层控制器执行，该控制器使用 VLM 选择的单轴平移或旋转以及带符号幅度。
- VLM oracle 检查任务是否成功，成功的新原语片段会加入数据集，VLA 随后重新训练，使这些原语成为可复用的策略动作。

## 结果
- 在仿真的方块翻转任务中，该方法使用 150 个拾取放置演示，切分出 7 类原语的 700 多个原语 episode。在总共 479 次尝试中获取 246 次 rotate-block 原语 rollout 后，翻转成功率达到 75%；在相同 rollout 预算下，SAC 的完整翻转成功率为 0%，但 reaching 达到 23%，grasp 达到 10%。
- 在仿真的抽屉关闭任务中，它从 50 个打开抽屉演示开始，这些演示被切分为 3 个原语。它从 82 个 episode 中收集到 70 个成功的 close-drawer 原语，然后在 25 次评估试验中以 100% 成功率关闭抽屉，同时保留打开抽屉能力。
- 在真实 xArm 扭转和倾倒任务中，基础 VLA 使用 50 个拾取放置演示训练，InSight 添加了 20 个成功获取的原语 episode。它达到 92% 的扭转成功率和 96% 的倾倒成功率；相比之下，CaP-X 分别为 32% 和 16%，没有新原语的 pi_0.5 基线为 0%。
- 在真实长时程“先扭转再倾倒”任务中，它在没有端到端演示的情况下串联 14 个原语并达到 80% 成功率；CaP-X 为 4%。
- 真实世界获取需要 23 次试验和 39.7 分钟实际时间来得到 20 个成功的扭转原语，需要 31 次试验和 85.3 分钟实际时间来得到 20 个成功的倾倒原语。
- 添加扭转和倾倒后，统一 VLA 在 15 次试验中对原始顶部拾取放置和侧向拾取放置技能保持 100% 成功率；清扫任务在只使用舀取演示的情况下，在 5/5 次评估试验中成功。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24884v1](https://arxiv.org/abs/2606.24884v1)
