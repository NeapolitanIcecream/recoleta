---
source: arxiv
url: http://arxiv.org/abs/2604.19683v2
published_at: '2026-04-21T17:05:37'
authors:
- Yunfan Lou
- Xiaowei Chi
- Xiaojie Zhang
- Zezhong Qian
- Chengxuan Li
- Rongyu Zhang
- Yaoxu Lyu
- Guoyu Song
- Chuyao Fu
- Haoxuan Xu
- Pengwei Wang
- Shanghang Zhang
topics:
- world-model
- robot-policy-learning
- vision-language-action
- semantic-masks
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Mask World Model: Predicting What Matters for Robust Robot Policy Learning

## Summary
## 摘要
Mask World Model 用未来语义掩码预测替代 RGB 视频预测，让机器人世界模型学习物体几何和接触动力学，而不是纹理和光照。论文称，这种方法让策略学习更稳健，并提高了仿真和真实机器人上的成功率，同时在测试时仍然使用原始 RGB。

## 问题
- 标准机器人世界模型通常预测未来 RGB 帧，这会把模型容量更多用在纹理、光照、反射和背景变化上，而这些信息无助于动作选择。
- 这些外观因素会在闭环控制中造成预测漂移，损害泛化能力，并让策略在视觉变化下变得脆弱。
- 有用的机器人策略需要与物体身份、空间布局和与接触相关的运动有关的特征，尤其是在长时程操作任务中。

## 方法
- MWM 训练世界模型预测未来的**语义掩码**，而不是未来像素。掩码覆盖任务相关物体和机器人，形成一个几何瓶颈，去掉光度噪声。
- 训练分两个阶段。第一阶段用以 diffusion / flow-matching 为基础的骨干网络，在过去的多视角 RGB 和语言条件下学习掩码动力学。第二阶段训练一个 diffusion 策略头，读取骨干网络的预测特征并输出动作。
- 语义掩码只在训练期间作为离线监督使用。推理时，系统输入原始多视角 RGB 和语言，不需要外部分割模型。
- 该模型对 RGB 帧和渲染后的掩码图像复用同一个视频 VAE，然后将掩码预测骨干网络中的 transformer 特征作为策略上下文。

## 结果
- 在 **LIBERO** 上，MWM 报告的**平均成功率为 98.3%**，高于 **GE-ACT 的 96.5%**、**pi0 的 94.2%**、**CogACT 的 93.6%**、**Cosmos w/ Latent IDM 的 91.9%** 和 **OpenVLA 的 76.5%**。
- 在更难的 **LIBERO-10** 子集上，MWM 达到 **96.0%**，相比之下 **GE-ACT 为 94.4%**、**pi0 为 85.2%**、**Cosmos w/ Latent IDM 为 84.2%**、**Cosmos w/ IDM 为 48.8%**。
- 基于掩码的消融实验支持论文的主要结论：**MWM-C1** 相比 **Cosmos w/ IDM**，平均 SR 从 **67.5%** 提高到 **81.0%**；**MWM-C2** 相比 **Cosmos w/ Latent IDM** 提高到 **91.8% 平均 SR**。
- 在 **RLBench** 上，MWM 报告的**平均成功率为 68.3%**，高于 **FiS-VLA 的 50.0%**、**CogACT 的 42.5%**、**GE-ACT 的 30.8%**、**pi0 的 33.3%** 和 **OpenVLA 的 23.3%**。
- 论文还称，在四项任务上，真实 **Franka** 机器人取得了 **67.5% 的平均成功率**，并表示 MWM 比基于 RGB 的基线更能应对背景、光照、物体颜色变化和随机 token pruning。
- 提供的摘录只展示了真实世界 OOD 测试的部分定量细节，因此目前最完整、最有力的结论仍然是上面的基准成功率提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19683v2](http://arxiv.org/abs/2604.19683v2)
