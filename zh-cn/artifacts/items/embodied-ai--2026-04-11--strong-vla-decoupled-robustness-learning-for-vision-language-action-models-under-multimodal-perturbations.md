---
source: arxiv
url: http://arxiv.org/abs/2604.10055v2
published_at: '2026-04-11T06:37:47'
authors:
- Yuhan Xie
- Yuping Yan
- Yunqi Zhao
- Handing Wang
- Yaochu Jin
topics:
- vision-language-action
- robot-robustness
- multimodal-perturbations
- curriculum-learning
- sim-benchmark
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations

## Summary
## 总结
STRONG-VLA 通过把微调拆成“扰动增强”阶段和“干净数据重新对齐”阶段，提高了视觉-语言-动作模型的鲁棒性。论文还提出了一个包含 28 种扰动类型的多模态扰动基准，并在 LIBERO、真实机器人设置以及 OpenVLA、OpenVLA-OFT 和 pi0 上展示了性能提升。

## 问题
- 当相机输入被污染，或者指令里出现噪声、干扰项或对抗性编辑时，视觉-语言-动作模型会失效。在机器人任务里，早期的小错误会扩散成整个任务失败。
- 现有鲁棒性训练通常把干净数据和扰动数据放进同一个目标里一起优化。论文认为，这会带来冲突梯度：干净数据需要模型对细节敏感，扰动数据则把策略推向不变性。
- 这对部署很重要，因为真实机器人会同时面对传感器噪声、遮挡、几何偏移和指令污染。

## 方法
- STRONG-VLA 不用单一的联合鲁棒性目标，而是采用两个训练阶段。
- Stage I 在扰动数据上训练，并使用课程式安排，随着时间推移提高扰动难度。它先强化语言，再强化视觉。
- 这个课程用简单的模态特定分数衡量扰动强度：语言用文本污染比例，视觉用归一化图像失真、遮挡面积或几何位移。
- Stage II 在干净任务数据上对 Stage I 的模型做微调，以恢复任务执行精度，同时保留在扰动中学到的鲁棒性。
- 论文还构建了一个包含 28 种扰动类型的基准：12 种文本扰动和 16 种视觉扰动，其中包括只用于评测、用于零样本鲁棒性测试的留出扰动。

## 结果
- 在 LIBERO 上，STRONG-VLA 在三种骨干模型上都提高了见过和未见扰动下的平均任务成功率：OpenVLA 最高提升 +12.60%（见过）和 +7.77%（未见）；OpenVLA-OFT 提升 +14.48%（见过）和 +13.81%（未见）；pi0 提升 +16.49%（见过）和 +5.58%（未见）。
- 干净输入上的表现大体保持：OpenVLA 相比基线下降 1.00 分，OpenVLA-OFT 下降 0.75 分，pi0 上升 2.75 分。
- 文本攻击上的单项提升很大。例子包括：OpenVLA-OFT 在前缀对抗注入上提升 +84.75，在角色伪装上提升 +82.50；pi0 在角色伪装上提升 +58.25；OpenVLA 在后缀语言污染上提升 +39.50。
- 视觉和多模态场景也有提升。例子包括：pi0 在图像偏移上提升 +36.25，在后缀污染加随机遮挡上提升 +44.75；OpenVLA-OFT 在前缀注入加随机遮挡上提升 +44.00；OpenVLA 在后缀污染加随机遮挡上提升 +26.75。
- 留出扰动上的零样本鲁棒性也有改善，包括语义漂移、上下文干扰项和动态视觉伪影。部分扰动仍然有小幅下降，例如 OpenVLA 在动态均匀噪声上下降 -6.25，OpenVLA-OFT 在动态均匀噪声上下降 -2.75。
- 摘要说，AIRBOT 平台上的真实世界实验支持了该方法的实用价值，但摘录里没有给出这些数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10055v2](http://arxiv.org/abs/2604.10055v2)
