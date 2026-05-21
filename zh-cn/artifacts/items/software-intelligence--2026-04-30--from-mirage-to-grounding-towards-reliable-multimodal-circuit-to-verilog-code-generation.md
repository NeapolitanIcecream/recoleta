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
## 摘要
这篇论文表明，许多多模态代码模型在电路转 Verilog 任务中可以取得高分，但它们依赖模块头名称，没有读取电路图像。论文提出 C2VEval 来暴露这个问题，并提出 VeriGround，这是一个 4B 模型，训练目标是使用可视电路拓扑并拒绝无效输入。

## 问题
- 电路图编码硬件行为，因此错误的视觉到 Verilog 翻译可能造成代价高昂的 RTL 和硅片错误。
- 标准评测会给模型一个模块头，`sum`、`cout`、`clk` 或 `fsm_3state` 等名称可能在不依赖图像的情况下泄露目标电路。
- 这会产生 Mirage 故障：把电路图替换为空白图像后，Pass@k 保持不变或更高，从而掩盖较弱的视觉 grounding。

## 方法
- C2VEval 包含 169 个电路转 Verilog 样本，这些样本由经过验证的 Verilog 通过 netlistsvg 渲染得到，图像和代码精确对应。
- 该基准使用配对的 Normal 和 Anony 变体。Normal 保留语义标识符；Anony 用占位符替换模块名、端口名和参数名，同时保留拓扑。
- 模型在 Original 模式下使用真实电路图测试，在 Mirage 模式下使用空白图像测试，同时保留相同的模块头。
- VeriGround 使用混合 Normal 和 Anony 的监督微调训练，加入针对空白或不匹配图像的拒绝示例，并使用 D-ORPO 对齐，对早期生成或拒绝 token 赋予更高权重。

## 结果
- 在 C2VEval Normal 上，Mirage 模式在所有 8 个被评测 MLLM 的报告指标中都追平或超过 Original 模式，说明空白图像性能可以等于或超过真实图像性能。
- 在 Anony 下，前沿模型的 Functional Pass@1 大幅下降：GPT-5.4 从 45.51% Normal Original 降至 24.55% Anony Original，Opus-4.6 从 52.69% 降至 11.38%。
- 对 167 个样本的样本级分析发现，Original-only 成功率在 Normal 中为 8.2%，在 Anony 中为 8.8%，因此论文估计真正的视觉 grounding 约覆盖 8-9% 的样本。
- VeriGround 4B 在 Normal 上达到 46.11% 的 Functional Pass@1，在 Anony 上达到 42.51%。
- VeriGround 在 Normal Functional Pass@1 上接近 GPT-5.4，分别为 46.11% 和 45.51%；在 Anony 上超过报告的基线，McNemar's test 得到 p < 0.001。
- VeriGround 在 Normal 有效输入上的 False Refusal Rate 为 1.20%，在 Anony 有效输入上为 0.00%，同时在空白图像上保持至少 92% 的 Refusal Rate。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27969v2](https://arxiv.org/abs/2604.27969v2)
