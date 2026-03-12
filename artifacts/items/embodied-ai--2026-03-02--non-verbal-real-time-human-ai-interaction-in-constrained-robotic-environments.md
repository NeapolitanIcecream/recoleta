---
source: arxiv
url: http://arxiv.org/abs/2603.01804v1
published_at: '2026-03-02T12:38:43'
authors:
- Dragos Costea
- Alina Marcu
- Cristina Lazar
- Marius Leordeanu
topics:
- human-ai-interaction
- nonverbal-communication
- motion-forecasting
- synthetic-data-pretraining
- edge-ai
relevance_score: 0.5
run_id: materialize-outputs
---

# Non-verbal Real-time Human-AI Interaction in Constrained Robotic Environments

## Summary
本文提出一个基于2D人体关键点的双任务框架，让AI在受限机器人环境中实时理解并回应人的非语言肢体动作。核心发现是：合成动作预训练能提升真实数据上的运动预测，但人类动作与AI生成动作之间仍存在可测量的统计差距。

## Problem
- 解决的问题：在算力、能耗、隐私和连接受限的机器人/边缘环境中，如何仅凭**非语言全身动作**实现实时的人机互动，包括**短时未来动作预测**和**情绪识别**。
- 为什么重要：这类能力有助于**主动避碰、交接时机判断、相机/机器人动作自适应**，并让人机协作更自然，而不依赖语音或文本。
- 研究还关注一个更深层问题：**AI生成动作数据是否足够接近真实人类动作**，以支持可靠训练和泛化。

## Approach
- 输入为过去 **60帧（2秒）** 的 **17个COCO 2D关键点**；输出同时包括未来 **30帧（1秒）** 的关键点预测，以及 **3类情绪** 分类（"enthusiastic"、"laughing"、"happy to see you"）。
- 使用一个**共享编码器 + 两个任务头**的联合学习框架：一个头做未来动作回归，另一个头做情绪分类；训练损失为 **MSE + 0.3 × Cross-Entropy**。
- 对比了四种轻量模型：**MLP、LSTM、CNN-LSTM、Transformer**，目标是在边缘设备上闭环实时运行。
- 先在真实数据上训练基线，再用 **MotionLCM** 生成的合成骨架序列做预训练（**9k / 45k / 90k**），最后在真实数据上微调。
- 额外用 **SORA** 和 **VEO3** 生成视频并提取关键点，测试模型对“纯合成视频动作”的泛化，从而衡量 synthetic-to-real gap。

## Results
- 实时性：四个模型都可在 **NVIDIA Orin Nano** 上超过实时运行；推理延迟分别约为 **1.643ms (MLP)**、**3.371ms (LSTM)**、**4.844ms (CNN-LSTM)**、**9.294ms (Transformer)**，最慢模型也约 **100 FPS**。
- 数据规模：真实数据仅 **437段视频**，经滑窗扩增为 **6992个样本**；合成预训练数据来自 MotionLCM，共 **90k样本**（每类 **30k**）。
- 动作预测：论文明确声称，**序列模型**（LSTM / CNN-LSTM / Transformer）在经过合成预训练后，真实测试集上的 **MAE持续下降**，且随着预训练数据从 **9k → 45k → 90k** 增长而继续改善；但摘录中**未给出完整MAE数值表**。
- 情绪识别在人类测试集上接近天花板：基线准确率为 **100 / 100 / 91.71 / 100**（CNN-LSTM / LSTM / MLP / Transformer），预训练后为 **100 / 100 / 94.78 / 100**，其中 **MLP提升 +3.07 个点**。
- 在 **SORA_Human** 上，预训练后准确率从 **45.76→38.28 (CNN-LSTM, -7.48)**、**45.54→44.31 (LSTM, -1.23)**、**47.99→36.72 (MLP, -11.27)**、**46.65→45.98 (Transformer, -0.67)**，说明某些SORA重渲染的人类动作会伤害泛化。
- 在 **SORA_AI** 上，预训练对部分模型帮助明显：**LSTM 32.66→50.00 (+17.34)**、**Transformer 35.74→48.15 (+12.41)**，而 **CNN-LSTM 31.25→28.35 (-2.90)**；在 **VEO** 上结果更接近真实分布，如 **CNN-LSTM 39.27→51.67 (+12.40)**、**Transformer 53.12→53.65 (+0.53)**，支持作者关于“**时间一致性比图像逼真度更重要**”的结论。

## Link
- [http://arxiv.org/abs/2603.01804v1](http://arxiv.org/abs/2603.01804v1)
