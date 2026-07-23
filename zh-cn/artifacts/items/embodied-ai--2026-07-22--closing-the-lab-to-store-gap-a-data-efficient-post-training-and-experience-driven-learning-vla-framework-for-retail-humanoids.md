---
source: arxiv
url: https://arxiv.org/abs/2607.20345v1
published_at: '2026-07-22T16:30:51'
authors:
- "Roger Sala Sis\xF3"
- "Tiago Silv\xE9rio"
- Jakob Sand
- Tran Nguyen Le
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- real-world-deployment
- experience-driven-learning
- ood-detection
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Closing the Lab-to-Store Gap: A Data-Efficient Post-Training and Experience-Driven Learning VLA Framework for Retail Humanoids

## Summary
## 摘要
DEED 是一个系统框架，用于在机器人数据有限的情况下，将 GR00T N1.6 视觉-语言-动作模型适配到现实零售环境中的人形机器人补货任务。该框架结合了高数据效率的后训练、经验驱动的优化，以及在 Unitree G1-Edu 上进行的潜在空间分布监测。

## 问题
- VLA 策略在基准测试中通常表现良好，但部署时会因执行错误、分布偏移、示范不一致和环境变化而失效。
- 离线模仿策略无法从自身的部署经验中学习，这限制了其在超市补货等长时程任务中的恢复能力和持续改进能力。
- 这一问题之所以重要，是因为在人类设计的环境中实现可靠的人形机器人操作，不仅取决于基础模型架构，也同样取决于实际的数据、控制和监测选择。

## 方法
- 对齐相机、录制和控制频率；整理示范数据，使其覆盖均衡的状态范围、高效行为和一致动作，同时包含恢复行为，并限制不受控的变化。
- 使用改编后的 IA-VLA 掩码突出与任务相关的视觉区域，采用二值手部控制，使用 Butterworth 滤波器平滑预测动作，并记录连续的多子任务回合。
- 针对解耦的 GR00T 架构改编 RECAP：加入“Advantage=True/False”文本前缀，并训练视觉-语言价值函数，根据预期进展为动作标注；人工纠正干预被强制标记为正样本。
- 每轮优化都从原始 GR00T 检查点重新初始化，并收集自主运行轨迹和人工恢复操作，用于进一步训练。
- 在 VLA 的潜在状态空间中拟合高斯混合模型，并使用最近成分的马氏距离、关节级分数和经验阈值来识别分布偏移。

## 结果
- 评估使用配备 Dex-3 灵巧手的 Unitree G1-Edu，在实体超市芯片补货任务上进行，模型从 GR00T-N1.6-G1-PnPAppleToPlate 检查点初始化。
- 初始数据集包含 81 段遥操作示范，约 51.5 分钟的操作数据，以及一个 20 维动作空间；其中三路 RGB 相机以 30 FPS 录制，控制信号以 25 Hz 记录。
- 两轮优化新增了 116 段自主运行回合，其中 41 段成功、75 段失败，自主运行总时长约为 56.9 分钟。
- 遥操作数据与自主运行数据合计包含约 108.4 分钟的机器人操作数据；所有训练、价值估计和推理均在一台配备 NVIDIA RTX 5090 的工作站上运行。
- 摘要所提供的节选指出，有针对性的数据设计和后训练将一个在朴素微调下失败的策略转变为能够胜任现实任务的系统，但没有提供与基线相比的成功率指标，也没有量化 DEED 各组成部分分别带来的改进。
- 研究还报告了一个实际限制：当自生成的运行轨迹主导训练分布时，反复优化可能导致性能下降，因此需要重新初始化检查点并进行分布监测。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.20345v1](https://arxiv.org/abs/2607.20345v1)
