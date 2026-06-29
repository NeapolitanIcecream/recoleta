---
source: arxiv
url: https://arxiv.org/abs/2604.27969v2
published_at: '2026-04-30T15:01:27'
authors:
- Guang Yang
- Xing Hu
- Xiang Chen
- Xin Xia
topics:
- multimodal-code-generation
- verilog-generation
- visual-grounding
- code-intelligence
- hardware-design
- benchmarking
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation

## Summary
## 总结
论文表明，许多多模态代码模型在电路转 Verilog 任务上看起来表现很好，但它们依赖模块头名称，而不是读取电路图像。论文提出 C2VEval 来暴露这个问题，并提出 VeriGround，一个训练成使用电路视觉拓扑并拒绝无效输入的 4B 模型。

## 问题
- 电路图编码的是硬件行为，因此错误的视觉到 Verilog 翻译会造成昂贵的 RTL 和硅片错误。
- 标准评估会给模型一个模块头，像 `sum`、`cout`、`clk` 或 `fsm_3state` 这样的名字，可能直接暴露目标电路，而不需要看图像。
- 这就产生了 Mirage 失效：把图替换成空白图像后，Pass@k 保持不变甚至更高，掩盖了薄弱的视觉对齐。

## 方法
- C2VEval 包含 169 个电路转 Verilog 样本，这些样本由经过验证的 Verilog 用 netlistsvg 渲染而成，图像和代码一一对应。
- 基准包含成对的 Normal 和 Anony 变体。Normal 保留语义标识符；Anony 将模块、端口和参数名替换为占位符，同时保留拓扑结构。
- 模型在 Original 模式下使用真实电路图，在 Mirage 模式下使用空白图像，同时保留相同的 header。
- VeriGround 使用混合 Normal 和 Anony 的监督微调、针对空白图或不匹配图像的拒答样本，以及 D-ORPO 对齐训练；该方法对前面的 generate-or-refuse token 赋予更高权重。

## 结果
- 在 C2VEval Normal 上，Mirage 模式在报告的所有指标上都与或超过了 8 个评测的 MLLM 的 Original 模式，说明空白图像上的表现可以等于甚至超过真实图像。
- 在 Anony 设置下，前沿模型的 Functional Pass@1 明显下降：GPT-5.4 从 45.51% 的 Normal Original 降到 24.55% 的 Anony Original，Opus-4.6 从 52.69% 降到 11.38%。
- 对 167 个样本的逐样本分析发现，Normal 中只有 8.2% 是 Original-only 成功，Anony 中是 8.8%，所以论文估计真正的视觉对齐大约只覆盖 8% 到 9% 的样本。
- VeriGround 4B 在 Normal 上的 Functional Pass@1 达到 46.11%，在 Anony 上达到 42.51%。
- VeriGround 在 Normal 的 Functional Pass@1 上接近 GPT-5.4，分别是 46.11% 和 45.51%，并且在 Anony 上以 McNemar 检验的 p < 0.001 优于报告的所有基线。
- VeriGround 在有效输入上的 False Refusal Rate 在 Normal 下为 1.20%，在 Anony 下为 0.00%，同时在空白图像上保持至少 92% 的 Refusal Rate。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27969v2](https://arxiv.org/abs/2604.27969v2)
