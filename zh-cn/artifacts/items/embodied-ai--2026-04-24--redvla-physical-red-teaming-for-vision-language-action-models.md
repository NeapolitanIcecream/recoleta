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
RedVLA 是一种面向视觉-语言-动作模型的物理红队测试方法。它在机器人场景中放置并调整风险对象，在部署前触发不安全行为，并报告了在六个 VLA 模型上较高的攻击成功率。

## 问题
- VLA 模型在执行过程中可能造成物理伤害，但现有红队测试方法更关注语言或图像攻击，而不是通过机器人与环境交互产生的风险。
- 机器人安全测试需要在尽量保持原始任务和场景有效的前提下发现不安全行为；否则，失败可能来自错误搭建的场景，而不是实际的安全漏洞。
- 这对操控和其他物理场景中的真实部署很重要，因为不安全动作可能是不可逆且代价很高的。

## 方法
- RedVLA 固定任务指令，只通过添加一个风险对象来扰动初始物理场景。
- 第 1 阶段 Risk Scenario Synthesis 使用无害的机器人轨迹，找出通行、抓取和振动区域等关键交互区域，然后把风险对象放在机器人可能接触到的位置。
- 每个测试样例都针对一个具体的安全违规，采用一个包含三种代价类型的分类法：状态级、累积级和条件级。危害包括资源损坏、危险物品误用、机器人损坏和环境危害。
- 第 2 阶段 Risk Amplification 运行策略，读取已执行轨迹，选择靠近碰撞或抓取事件的空间锚点，然后用无梯度优化把风险对象移动到该锚点附近，直到出现目标不安全行为。
- 论文还提出了 SimpleVLA-Guard，这是一个基于 RedVLA 生成数据的轻量检测器，用来监测 VLA 内部特征并在线干预。

## 结果
- 在基于 LIBERO 的风险场景中，六个 VLA 模型的平均攻击成功率从 64.9% 到 95.5% 不等；最佳结果是 pi_0.5 的 95.5%，论文称这是在 10 次优化迭代内达到的。
- 按安全类型划分的平均 ASR 中，状态级场景高于 95%，累积级场景为 88.9%，条件级场景为 66.1%。
- 在完整模型对比表中，平均 ASR/SR 为：OpenVLA 64.9% / 39.1%，OpenVLA-OFT 90.5% / 44.7%，VLA-Adapter 89.9% / 48.4%，VLA-Adapter-Pro 91.6% / 45.3%，pi_0 93.2% / 54.6%，pi_0.5 95.5% / 62.1%。
- 一些单独场景的 ASR 接近或达到 100%。例如，累积级危险物品误用在六个模型上都达到 100.0% ASR；pi_0.5 在累积级资源损坏上达到 98.5%，在条件级环境危害上达到 98.0%。
- 更强的基础模型在这组评估中也表现出更高的脆弱性。OpenVLA-OFT 的无害任务成功率比 OpenVLA 高 20.6 个百分点，ASR 高 25.6 个百分点；pi_0.5 的无害任务成功率比 pi_0 高 2.6 个百分点，ASR 高 2.3 个百分点。
- 在语言和视觉扰动下，摘录报告 RedVLA 仍保持较高 ASR，语言扰动的平均 ASR 为 88.2%，视觉扰动的平均 ASR 为 85.5%，而仅有无害扰动时 ASR 保持在 5.2% 或以下。论文还称 SimpleVLA-Guard 将在线 ASR 降低了 59.5%，对任务性能影响很小。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22591v1](http://arxiv.org/abs/2604.22591v1)
