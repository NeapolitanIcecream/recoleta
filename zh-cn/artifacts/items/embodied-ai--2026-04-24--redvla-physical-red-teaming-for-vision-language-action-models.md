---
source: arxiv
url: http://arxiv.org/abs/2604.22591v1
published_at: '2026-04-24T14:18:23'
authors:
- Yuhao Zhang
- Borong Zhang
- Jiaming Fan
- Jiachen Shen
- Yishuai Cai
- Yaodong Yang
- Jiaming Ji
topics:
- vision-language-action
- robot-safety
- physical-red-teaming
- embodied-ai
- simulated-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# RedVLA: Physical Red Teaming for Vision-Language-Action Models

## Summary
## 摘要
RedVLA 是一种面向视觉-语言-动作模型的物理红队测试方法。它在机器人场景中放置并迭代调整风险物体，在部署前触发不安全行为；论文报告称，该方法在六个 VLA 模型上都取得了较高的攻击成功率。

## 问题
- VLA 模型在执行过程中可能造成物理伤害，但现有红队方法主要关注语言或图像攻击，而不是通过机器人与环境交互产生的风险。
- 机器人安全测试需要在尽量保持原始任务和场景有效的前提下发现不安全行为；否则，失败可能来自被破坏的测试设置，而不是真实的安全弱点。
- 这对操作等物理领域的实际部署很重要，因为不安全动作可能不可逆，代价也很高。

## 方法
- RedVLA 固定任务指令，只通过加入一个风险物体来扰动初始物理场景。
- 第一阶段“风险场景合成”使用正常机器人轨迹找出关键交互区域，例如经过区、抓取区和振动区，然后把风险物体放在机器人可能接触到它的位置。
- 每个测试样例都针对一种具体的安全违规类型，论文使用的分类包括三类代价：状态级、累积级和条件级。对应危险包括资源损坏、危险物品误用、机器人损坏和环境损害。
- 第二阶段“风险放大”运行策略，读取执行轨迹，在碰撞或抓取事件附近选取一个空间锚点，然后用无梯度优化把风险物体朝该锚点移动，直到出现目标不安全行为。
- 论文还提出了 SimpleVLA-Guard，这是一种基于 RedVLA 生成数据构建的轻量检测器，可监控 VLA 的内部特征并在线干预。

## 结果
- 在基于 LIBERO 的风险场景中，RedVLA 在六个 VLA 模型上的平均攻击成功率达到 64.9% 到 95.5%；最好结果出现在 pi_0.5，上限为 95.5%，论文称这一结果在 10 次优化迭代内达到。
- 按安全类型划分，状态级场景的平均 ASR 超过 95%，累积级场景为 88.9%，条件级场景为 66.1%。
- 在完整模型对比表中，平均 ASR/SR 分别为：OpenVLA 64.9% / 39.1%，OpenVLA-OFT 90.5% / 44.7%，VLA-Adapter 89.9% / 48.4%，VLA-Adapter-Pro 91.6% / 45.3%，pi_0 93.2% / 54.6%，pi_0.5 95.5% / 62.1%。
- 若干单独场景的 ASR 接近或达到 100%。例如，累积型危险物品误用在全部六个模型上都达到 100.0% ASR；pi_0.5 在累积型资源损坏上达到 98.5%，在条件型环境损害上达到 98.0%。
- 在这组评估中，能力更强的基础模型也表现出更高的脆弱性。与 OpenVLA 相比，OpenVLA-OFT 的正常任务成功率提高了 20.6 个百分点，ASR 提高了 25.6 个百分点；与 pi_0 相比，pi_0.5 的正常任务成功率提高了 2.6 个百分点，ASR 提高了 2.3 个百分点。
- 在语言和视觉扰动下，摘录称 RedVLA 仍保持较高 ASR：语言扰动下平均 ASR 为 88.2%，视觉扰动下为 85.5%；而单独的良性扰动将 ASR 保持在 5.2% 或以下。论文还称，SimpleVLA-Guard 可将在线 ASR 降低 59.5%，同时对任务表现影响较小。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22591v1](http://arxiv.org/abs/2604.22591v1)
