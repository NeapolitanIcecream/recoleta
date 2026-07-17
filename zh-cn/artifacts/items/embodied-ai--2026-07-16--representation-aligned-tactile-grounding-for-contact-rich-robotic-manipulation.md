---
source: arxiv
url: https://arxiv.org/abs/2607.14609v1
published_at: '2026-07-16T06:12:05'
authors:
- Ruilin Chen
- Jingkai Jia
- Tong Yang
- Xinyu Zhou
- Qiao Sun
- Jiangwei Zhong
- Shizeng Zhang
- Nuo Chen
- Bailin He
- Wei Li
- Wenqiang Zhang
topics:
- robot-foundation-model
- vision-language-action
- tactile-grounding
- contact-rich-manipulation
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Representation-Aligned Tactile Grounding for Contact-Rich Robotic Manipulation

## Summary
## 摘要
论文表明，在接触丰富的机器人操作中，只有当未来触觉预测对中间动作专家表征施加监督时，才能最有效地提升操作性能。其潜在触觉预测器（LTP）将现实世界平均成功率提高到74%，且不增加推理时的计算量。

## 问题
- 视觉无法可靠观测压力、滑移、阻力和插入对齐等接触状态，这限制了VLA策略在插入、擦拭、拧下螺钉和可变形抓取等任务中的表现。
- 未来触觉预测可以为动作引起的接触动力学提供监督，但目前尚不清楚VLA的哪种内部表征应接收这种监督。
- 将损失施加于感知侧VLM特征或最终运动特征，可能造成与表征不匹配的监督；而原始触觉目标可能会放大传感器噪声和校准伪影。

## 方法
- 作者冻结VLA策略，并在其动作路径的不同位置训练线性探针来预测未来触觉测量值，利用探针误差确定未来接触信息最容易被获取的位置。
- 研究选择中间动作专家特征，因为这些特征已经受到动作条件的影响，但尚未被压缩为专门用于即时运动解码的表征。
- LTP使用可学习查询，根据该中间表征预测紧凑的未来触觉嵌入，而不是直接预测含噪的原始触觉信号。
- 训练时将潜在触觉损失与原生动作损失结合；推理时移除LTP分支，因此部署路径和推理成本保持不变。

## 结果
- 在使用ARX R5机器人、PaXini触觉传感器、每项任务50次示范和每项任务20次评估试验的五项现实世界接触丰富任务中，采用SmolVLA骨干网络的中间表征对齐方法取得了74%的平均成功率。
- 74%的结果比VLM侧未来触觉预测的58%高16个百分点，比最终动作状态预测的62%高12个百分点。
- 在\(\pi_{0}\)骨干网络上，标准策略、触觉条件策略、VLM侧预测策略和最终动作预测策略的平均成功率分别为40%、54%、58%和59%；表征对齐的触觉 grounding方法达到73%。
- 在SmolVLA的五项任务中，该方法有四项取得最佳结果，并在可变形物体抓取任务上并列最佳；其任务平均成功率为74%，而不使用未来触觉预测、仅输入触觉的方案为41%，三种多接口 grounding变体分别为38%、48%和60%。
- 将潜在触觉目标替换为原始触觉预测后，插入任务的成功率从80%降至55%。
- 证据仅限于报告中的现实世界任务套件和两种VLA骨干网络；摘录无法证明该方法在更广泛的机器人、数据集或更长期部署条件下的表现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14609v1](https://arxiv.org/abs/2607.14609v1)
