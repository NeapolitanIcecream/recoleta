---
source: arxiv
url: https://arxiv.org/abs/2606.20246v1
published_at: '2026-06-18T13:57:12'
authors:
- Gia-Binh Nguyen
- Trong-Bao Ho
- Thien-Loc Ha
- Khoa Vo
- "Philip Lund M\xF8ller"
- Quang T. Nguyen
- Long Dinh
- Tuan Dam
- Vu Duong
- Tung M. Luu
- Trung Le
- Tran Nguyen Le
- Minh Vu
- An Thai Le
- Ngan Le
- Daniel Sonntag
- James Zou
- Jan Peters
- Duy M. H. Nguyen
- Ngo Anh Vien
topics:
- vision-language-action
- layer-pruning
- robot-finetuning
- model-compression
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Finetuning Vision-Language-Action Models Requires Fewer Layers Than You Think

## Summary
## 摘要
CLP 在微调前从预训练 VLA 机器人策略中移除冗余的 transformer 层。它降低训练和推理成本，同时保持操控成功率，有时还能提高成功率。

## 问题
- π0 和 GR00T-N1.5 等现代连续控制 VLA 模型有数十亿参数，导致下游微调成本高，机器人实时推理速度慢。
- 许多现有 VLA 提效方法主要降低推理成本、添加路由模块，或面向较早的自回归动作 token 模型，而不是当前的流式或扩散动作策略。
- 论文研究能否在微调前移除预训练 VLA 的层，使机器人实验室可以训练更小的策略，同时不牺牲任务成功率。

## 方法
- CKA-guided Layer Pruning（CLP）使用少量机器人 episode，对预训练 VLA 运行一次校准前向传播。
- 它计算 VLM backbone 和连续动作 head 中相邻 transformer 层之间的 Centered Kernel Alignment。CKA 高表示两个相邻层产生相似的隐藏表示。
- CLP 将连续的高相似度层分组，保留每组中的第一层作为锚点，移除其余层中冗余程度最高的层，并重新连接保留下来的 block。
- 剪枝后的模型随后使用原始 VLA 训练目标进行微调，不使用辅助 router、蒸馏损失或运行时层选择器。

## 结果
- 在 LIBERO 上，CLP 用于 π0、GR00T-N1.5 和 SmolVLA 时，将模型大小减少 21.3% 到 25.9%，将可训练参数减少 25.8% 到 37.0%。
- 在 LIBERO 上训练 60,000 步时，π0 的训练时间从 15.5 小时降至 11.2 小时，GR00T-N1.5 从 10.7 小时降至 7.4 小时，SmolVLA 从 24.75 小时降至 8.83 小时。
- 在 RTX 4070 上，π0 的推理延迟从 211 ms 降至 152 ms，GR00T-N1.5 从 121 ms 降至 85 ms，SmolVLA 从 201 ms 降至 137 ms。
- GFLOPs 方面，π0 从 3073 降至 2196.5，GR00T-N1.5 从 1010 降至 512.4，SmolVLA 从 598.4 降至 536.1。
- 仅使用 10% 的 LIBERO 数据时，CLP 报告 π0 的平均成功率为 84.6%，相比之下完整 π0 基线为 77.7%，π0-MoLe 为 79.7%，训练速度提升 1.38×。
- 在使用 GR00T-N1.5 的 SimplerEnv 上，平均成功率从 16.6% 升至 20.0%，训练时间从 22.9 小时降至 15.7 小时。论文还报告了在 4 种机器人本体的 10 个真实世界操控任务上的验证结果：使用 100 条演示时，相比完整模型提升 15% 到 20%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20246v1](https://arxiv.org/abs/2606.20246v1)
