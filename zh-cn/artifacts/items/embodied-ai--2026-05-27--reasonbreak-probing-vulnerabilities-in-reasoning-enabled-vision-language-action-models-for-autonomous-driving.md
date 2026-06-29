---
source: arxiv
url: https://arxiv.org/abs/2605.29114v1
published_at: '2026-05-27T21:21:37'
authors:
- Mohammadreza Teymoorianfard
- Jean-Philippe Monteuuis
- Jonathan Petit
- Amir Houmansadr
topics:
- vision-language-action
- autonomous-driving
- vla-safety
- adversarial-robustness
- closed-loop-simulation
- reasoning-models
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# ReasonBreak: Probing Vulnerabilities in Reasoning-Enabled Vision-Language-Action Models for Autonomous Driving

## Summary
## 总结
ReasonBreak 表明，轻微且保持原意的文本扰动会改变 NVIDIA Alpamayo VLA 驾驶模型的推理和行驶轨迹。论文在黑盒的开环和闭环设置下测试这一点，并把失败和碰撞、驶离道路、错误车道事件联系起来。

## 问题
- 带推理的 VLA 驾驶系统把文本指令和传感器输入一起使用，所以语音转文本和预处理噪声会改变文本表面形式。
- 中间推理的变化会影响生成的轨迹，这很重要，因为驾驶错误会导致碰撞或交通规则违规。
- 以往关于 VLA 脆弱性的研究主要看操控任务或没有显式推理输出的模型，对带推理的自动驾驶测试还不够。

## 方法
- 攻击只修改文本输入，视觉输入保持不变。允许的扰动包括大小写变化、词语打乱和字符级噪声，只要仍保留原本指令的含义即可。
- 威胁模型是基于查询的黑盒攻击：攻击者能看到模型输出，但不能访问参数、logits、架构或内部状态。
- 开环测试使用 Best-of-N 扰动查询，估计模型在搜索下能被操控到什么程度。
- 闭环测试在 AlpaSim 中每个仿真步使用一条随机损坏的文本输入，然后测量驾驶过程中错误如何累积。
- 评估检查语义推理字段、推理长度膨胀、推理输出缺失、轨迹偏移、碰撞率、近距离遭遇率、碰撞前时间、驶离道路率和错误车道率。

## 结果
- 在 195 个开环样本上，Alpamayo1 的语义推理 ASR 在关系为 0.889、蕴含为 0.850、规划为 0.832、对象为 0.765，整体为 0.836。
- Alpamayo1.5 在开环测试中更难攻击，语义推理 ASR 在关系为 0.626、蕴含为 0.520、对象为 0.436、规划为 0.429，整体为 0.422。
- 开环结构攻击也有效：Alpamayo1 的 slowdown ASR 为 0.248，DoS ASR 为 0.047；Alpamayo1.5 的 slowdown ASR 为 0.102，DoS ASR 为 0.088。
- 开环轨迹偏移 ASR 在 Alpamayo1 上为 0.336，在 Alpamayo1.5 上为 0.115，使用相对真实轨迹的 ADE 恶化来衡量。
- 在 50 段视频的闭环仿真中，论文报告轨迹操控的 ASR 最高达 72%，语义推理操控的 ASR 最高达 62%。
- 论文报告推理变化和轨迹偏移之间相关性较弱，而且在攻击成功时，碰撞、驶离道路和错误车道失败更多。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29114v1](https://arxiv.org/abs/2605.29114v1)
