---
source: hn
url: https://www.workshoplabs.ai/blog/open-weights-open-training
published_at: '2026-03-09T23:37:08'
authors:
- addiefoote8
topics:
- open-source-ml-infra
- llm-post-training
- mixture-of-experts
- quantization
- lora
- training-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Open Weights isn't Open Training

## Summary
这篇文章不是提出新模型，而是一次对超大开源权重模型进行后训练的工程复盘：作者尝试给 1T 参数的 Kimi-K2-Thinking 做 LoRA 微调，却发现“开放权重”并不等于“开放训练”。核心结论是，现有开源训练栈在超大规模、量化、MoE 场景下存在多处隐藏失效点，必须靠大量底层补丁才能勉强跑通。

## Problem
- 要解决的问题是：**如何以较低成本对一个开源的 1T 级 MoE 量化模型进行可用的后训练**，并验证模型行为确实按数据集方向改变。
- 这很重要，因为很多“开源模型”只开放了权重，却没有真正可复现、可扩展、可修改的训练路径；对企业和研究者而言，这直接限制了定制化、对齐和持续训练能力。
- 文章表明，在 HuggingFace / PEFT / Accelerate / quantization stack 上，面向 8B 模型看似可用的功能，到 1T+ 模型时可能会因为加载、显存、LoRA 兼容性、MoE 路由和反量化等问题失效。

## Approach
- 作者选用 **Kimi-K2-Thinking**（1T 参数 MoE，专家权重量化为 4-bit），目标是在 **8×H200** 上做 LoRA 后训练；为验证训练是否生效，构造了一个 **1000 条样本**的“Yoda 风格”问答数据集。
- 先写出一套标准 HuggingFace + PEFT 训练脚本，然后逐层排查失败点，包括：重复压缩已量化权重、`dispatch_model` 阶段的 GPU 内存分配卡顿、`device_map='auto'` 导致显存分布不均、量化权重与 LoRA 不兼容、MoE gate 在 train 模式下断言失败、以及反量化后权重未释放导致显存持续累积。
- 对每个问题，作者都采用最直接的工程修补：删除不必要的 `compress_model` 调用；设置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`；手工指定层到 GPU 的映射；避免对量化 experts 挂 LoRA，仅训练 shared experts 和注意力相关投影；将模型置于 eval 模式以绕过不可微 gate 的训练断言。
- 最关键的补丁是修改量化线性层前向：**不再把反量化后的权重注册成持久 parameter，而是即时反量化、完成线性计算后显式删除**，从而阻止每层前向时显存不断累积。

## Results
- 训练最终被跑通：在修补后，训练日志显示 loss 从 **1.7443 → 1.5071**（前 5 个 step：1.7443, 1.7749, 1.7258, 1.6842, 1.5071），说明至少在小规模实验中优化目标开始下降。
- 可用训练配置达到：**batch size 8、sequence length 2048、每 step 45 秒、364 train tokens/s**，运行硬件为 **8×H200**。
- 定性结果上，模型在训练后能明显输出 **Yoda 风格**回答，表明行为确实按数据集方向发生改变，这是作者最初成功标准中的第二项。
- 但限制也很明确：**专家参数仍然无法训练**，只能训练 shared experts/部分投影层；因此这不是完整意义上的 MoE 后训练方案。
- 成本方面，作者声称该方案虽然“能用”，但**每 token 成本约比 Tinker 高 6–9 倍**，说明工程可行性远未达到理想状态。
- 文章没有给出标准 benchmark 数据集上的 SOTA 指标提升；最强的量化主张是：作者通过一系列底层 monkey-patch，使一个原本无法训练的开源 1T 量化 MoE 模型实现了可运行的 LoRA 后训练，并证明“开源权重 ≠ 开放训练”。

## Link
- [https://www.workshoplabs.ai/blog/open-weights-open-training](https://www.workshoplabs.ai/blog/open-weights-open-training)
