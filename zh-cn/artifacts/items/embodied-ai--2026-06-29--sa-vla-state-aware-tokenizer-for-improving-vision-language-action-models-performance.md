---
source: arxiv
url: https://arxiv.org/abs/2606.30113v1
published_at: '2026-06-29T10:45:53'
authors:
- Tengyue Jiang
- Chunpu Xu
- Jiayue Kang
- Yao Mu
topics:
- vision-language-action
- action-tokenization
- state-conditioned-decoding
- sim2real
- robot-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance

## Summary
## 摘要
SA-VLA 通过结合机器人当前的本体感知状态来解码动作 token，改进了用于 VLA 机器人策略的离散动作 tokenizer。论文报告称，该方法在 RoboTwin 操作任务和零样本仿真到真实实验中取得了更高成功率。

## 问题
- 离散 VLA 策略需要从动作 token 还原连续机器人动作，但常见 tokenizer 会把每个 token 映射到一个固定动作原型。
- 操作任务受关节构型、物体位姿和接触状态影响，因此同一个 token 在不同状态下可能需要不同的连续控制。
- 这种压缩差距会影响效果，因为即使视觉语言模型预测了有用的动作 token，较差的动作重建也会降低任务成功率。

## 方法
- SA-VLA 在动作解码时以当前机器人状态为条件，通常使用关节角，同时为基于 LLM 的 VLA 策略保留离散动作 token 接口。
- 方法 A 在 VQ-VAE 编码器和解码器内部，通过状态特征与动作特征之间的交叉注意力注入状态。
- 方法 B 使用轻量级 MLP adapter，根据状态预测每个动作维度的缩放因子；量化前用该缩放因子除以动作，解码后再乘回。
- 方法 B 让一个码本 token 解码为一组依赖状态的连续动作，从而扩大有限 VQ 码本的有效支持范围。
- 该 VLA 使用文本 token、256-bin 离散化状态 token、来自 224×224 图像的 SigLIP 图像 token，以及用于自回归或并行解码的固定长度动作 token。

## 结果
- 在 12 个 RoboTwin 任务上，每个任务使用 1,600 条轨迹和 100 次 rollout，方法 B 在自回归解码下达到 0.56 平均成功率，在并行解码下也达到 0.56。
- RoboTwin 表中最强基线 VQ-BET 的平均成功率为 0.29；binning 为 0.24，FAST 为 0.17。
- 方法 A 也优于基线，在 RoboTwin 上自回归解码的平均成功率为 0.55，并行解码为 0.52。
- 状态消融显示，相比不使用状态的 tokenizer，加入状态带来提升：no-state PD 为 0.43，no-state AR 为 0.51，方法 A 为 0.52 PD 和 0.55 AR，方法 B 在 PD 和 AR 下均为 0.56。
- 在 Click Bell、Place Container Plate 和 Pick Diverse Bottles 的零样本仿真到真实测试中，每项 20 次试验，方法 B AR 的平均成功率为 0.33，高于 VQ-BET 的 0.15、binning 的 0.10 和 FAST 的 0.08。
- 真实世界实验中，方法 B AR 在 Click Bell 上为 10/20，在 Place Container Plate 上为 7/20，在 Pick Diverse Bottles 上为 3/20；方法 B PD 的平均成功率为 0.27。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30113v1](https://arxiv.org/abs/2606.30113v1)
