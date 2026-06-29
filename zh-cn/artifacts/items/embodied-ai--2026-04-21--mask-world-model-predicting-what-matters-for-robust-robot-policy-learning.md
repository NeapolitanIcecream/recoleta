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
Mask World Model 用未来语义掩码预测替代 RGB 视频预测，让机器人世界模型学习物体几何和接触动态，而不是纹理和光照。论文称，这样能让策略学习更稳健，并在仿真和真实机器人上提高成功率，同时在测试时仍然使用原始 RGB。

## 问题
- 标准机器人世界模型通常预测未来 RGB 帧，这会把容量放在纹理、光照、反射和背景变化上，而这些因素对动作选择没有帮助。
- 这些外观因素会在闭环控制中造成预测漂移，进而损害泛化能力，使策略在视觉变化下更脆弱。
- 有用的机器人策略需要与物体身份、空间布局和接触相关运动绑定的特征，尤其是在长时程操作任务中。

## 方法
- MWM 训练世界模型去预测未来**语义掩码**，而不是未来像素。掩码覆盖任务相关物体和机器人本体，形成一个几何瓶颈，去掉光度噪声。
- 训练分两阶段。阶段 1 用一个基于 diffusion / flow-matching 的骨干网络，在过去的多视角 RGB 和语言条件下学习掩码动态。阶段 2 训练一个 diffusion 策略头，读取骨干网络的预测特征并输出动作。
- 语义掩码只在训练时作为离线监督使用。推理时，系统输入原始多视角 RGB 和语言，不需要外部分割模型。
- 模型为 RGB 帧和渲染出的掩码图像共用一个视频 VAE，然后把掩码预测骨干网络中的 transformer 特征作为策略上下文。

## 结果
- 在 **LIBERO** 上，MWM 报告 **98.3% 的平均成功率**，超过 **GE-ACT 的 96.5%**、**pi0 的 94.2%**、**CogACT 的 93.6%**、**Cosmos w/ Latent IDM 的 91.9%** 和 **OpenVLA 的 76.5%**。
- 在更难的 **LIBERO-10** 子集上，MWM 达到 **96.0%**，对比 **GE-ACT 的 94.4%**、**pi0 的 85.2%**、**Cosmos w/ Latent IDM 的 84.2%** 和 **Cosmos w/ IDM 的 48.8%**。
- 基于掩码的消融结果支持了主要结论：**MWM-C1** 相比 **Cosmos w/ IDM**，平均 SR 从 **67.5%** 提升到 **81.0%**；**MWM-C2** 相比 **Cosmos w/ Latent IDM**，平均 SR 提升到 **91.8%**。
- 在 **RLBench** 上，MWM 报告 **68.3% 的平均成功率**，高于 **FiS-VLA 的 50.0%**、**CogACT 的 42.5%**、**GE-ACT 的 30.8%**、**pi0 的 33.3%** 和 **OpenVLA 的 23.3%**。
- 论文还提到，在真实 **Franka** 机器人上，MWM 在四个任务上的平均成功率为 **67.5%**，并且在背景、光照、物体颜色变化和随机 token 剪枝下，都比基于 RGB 的基线更稳。
- 真实世界 OOD 测试的定量鲁棒性细节在给出的摘录里只部分可见，所以最完整、最稳妥的结论是上面的基准成功率提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19683v2](http://arxiv.org/abs/2604.19683v2)
