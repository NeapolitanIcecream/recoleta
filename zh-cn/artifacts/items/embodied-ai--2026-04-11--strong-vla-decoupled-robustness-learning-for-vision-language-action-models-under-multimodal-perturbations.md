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
## 摘要
STRONG-VLA 通过将微调拆分为扰动强化阶段和干净数据重新对齐阶段，提升了视觉-语言-动作模型的鲁棒性。论文还提出了一个包含 28 种类型的多模态扰动基准，并在 LIBERO 和真实机器人环境中展示了 OpenVLA、OpenVLA-OFT 和 pi0 的性能提升。

## 问题
- 当相机输入受损，或指令中包含噪声、干扰项或对抗性编辑时，视觉-语言-动作模型会失效。在机器人场景中，前期的小错误可能演变为整个任务失败。
- 现有的鲁棒性训练通常将干净数据和扰动数据混合在同一个目标中。论文认为这会产生相互冲突的梯度：干净数据需要对细节保持敏感，而扰动数据会推动策略追求不变性。
- 这关系到部署效果，因为真实机器人会同时面对传感器噪声、遮挡、几何偏移和指令损坏。

## 方法
- STRONG-VLA 使用两个训练阶段，而不是单一的联合鲁棒性目标。
- 第一阶段在扰动数据上训练，并使用课程式安排，随着时间提高扰动难度。它先强化语言，再强化视觉。
- 该课程用简单的模态专用分数来衡量扰动强度：语言使用文本损坏比例，视觉使用归一化图像失真、遮挡面积或几何位移。
- 第二阶段在干净任务数据上对第一阶段得到的模型进行微调，在保留扰动条件下学到的鲁棒性的同时，恢复任务执行保真度。
- 论文还构建了一个包含 28 种扰动类型的基准：12 种文本扰动和 16 种视觉扰动，其中包括仅用于评估的留出扰动，用于零样本鲁棒性测试。

## 结果
- 在 LIBERO 上，STRONG-VLA 在三种骨干模型上都提高了已见和未见扰动下的平均任务成功率：OpenVLA 最高提升已见 +12.60%、未见 +7.77%；OpenVLA-OFT 提升已见 +14.48%、未见 +13.81%；pi0 提升已见 +16.49%、未见 +5.58%。
- 干净输入下的性能大多得以保持：OpenVLA 相比基线变化 -1.00 点，OpenVLA-OFT 为 -0.75，pi0 为 +2.75。
- 在文本攻击上，单项扰动的提升幅度很大。例子包括：OpenVLA-OFT 在前缀对抗注入上提升 +84.75，在角色伪装上提升 +82.50；pi0 在角色伪装上提升 +58.25；OpenVLA 在后缀语言损坏上提升 +39.50。
- 在视觉和多模态场景中也有提升。例子包括：pi0 在图像偏移上提升 +36.25，在后缀损坏加随机遮挡上提升 +44.75；OpenVLA-OFT 在前缀注入加随机遮挡上提升 +44.00；OpenVLA 在后缀损坏加随机遮挡上提升 +26.75。
- 在标记为仅评估的留出扰动上，零样本鲁棒性也有提升，包括语义漂移、上下文干扰项和动态视觉伪影。不过部分扰动仍有小幅下降，例如 OpenVLA 在动态均匀噪声上为 -6.25，OpenVLA-OFT 在动态均匀噪声上为 -2.75。
- 摘要称，在 AIRBOT 平台上的真实世界实验支持了该方法的实际价值，但这段摘录没有给出具体数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10055v2](http://arxiv.org/abs/2604.10055v2)
