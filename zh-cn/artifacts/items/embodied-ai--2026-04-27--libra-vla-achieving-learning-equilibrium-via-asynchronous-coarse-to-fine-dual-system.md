---
source: arxiv
url: https://arxiv.org/abs/2604.24921v1
published_at: '2026-04-27T19:02:46'
authors:
- Yifei Wei
- Linqing Zhong
- Yi Liu
- Yuxiang Lu
- Xindong He
- Maoqing Yao
- Guanghui Ren
topics:
- vision-language-action
- generalist-robot-policy
- robot-manipulation
- hierarchical-control
- diffusion-policy
- asynchronous-inference
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System

## Summary
## 摘要
Libra-VLA 是一种用于机器人操作的视觉-语言-动作策略，将动作生成拆分为粗粒度离散意图和连续精细控制。论文称，该方法在 LIBERO 和 LIBERO-Plus 上取得了更高成功率，同时降低了高成本 VLM 规划器的运行频率。

## 问题
- 许多 VLA 策略把图像和语言直接映射到高频电机指令，导致一个模型同时处理语义推理和精确控制。
- 这一点很关键，因为操作任务有天然层级：机器人先需要大致方向或目标，然后需要精确调整姿态以完成接触和对齐。
- 以往的时间层级方法缩短了长任务，但每个低层步骤仍要完成从语言-视觉特征到连续动作的高难度转换。

## 方法
- Libra-VLA 将策略分解为 `P(fine action | coarse action, observation) * P(coarse action | observation, instruction)`。
- Semantic Planner 使用 InternVL2.5-2B VLM，并配备并行的粗粒度动作头，从量化归一化动作中预测离散宏观方向 token。
- Action Refiner 使用扩散 transformer 和 SigLIP 视觉编码器，将粗粒度意图转换为连续机器人动作。
- 训练将粗粒度 token 的交叉熵与精细动作的扩散 MSE 结合起来，并使用课程学习，从真实粗粒度 token 逐步过渡到规划器预测的 token。
- 推理时，规划器会预测更长的粗粒度时域并写入 FIFO 意图缓冲区；当 `M=2` 且动作块大小为 `5` 时，它会预测 `10` 个粗粒度步骤，而 refiner 按控制频率运行。

## 结果
- 在 LIBERO 上，Libra-VLA 报告的平均成功率为 `97.2%`，相比之下，pi0.5 为 `96.9%`，GE-Act 为 `96.5%`，DD-VLA 为 `96.3%`。
- LIBERO 各套件得分为：Spatial `98.6%`、Object `99.4%`、Goal `98.0%`、Long `92.8%`。
- 在 LIBERO-Plus 零样本迁移上，Libra-VLA 报告的平均成功率为 `79.5%`，相比之下，OpenVLA-OFT 为 `69.6%`，pi0-Fast 为 `61.6%`。
- LIBERO-Plus 零样本类别得分为：Camera `68.9%`、Robot `48.8%`、Language `92.7%`、Light `97.9%`、Background `93.4%`、Noise `86.3%`、Layout `77.5%`。
- 论文称仿真和真实世界实验没有使用大规模机器人数据预训练；摘录未给出真实世界成功率数字。
- 论文称动作分解粒度与性能之间呈倒 U 形关系，并且当规划器和 refiner 的学习难度达到平衡时性能最佳；摘录未给出支持这一说法的消融数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24921v1](https://arxiv.org/abs/2604.24921v1)
