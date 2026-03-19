---
source: hn
url: https://www.workshoplabs.ai/blog/open-weights-open-training
published_at: '2026-03-09T23:37:08'
authors:
- addiefoote8
topics:
- open-weights
- llm-training
- mixture-of-experts
- quantization
- lora
- ml-infrastructure
relevance_score: 0.67
run_id: materialize-outputs
language_code: zh-CN
---

# Open Weights isn't Open Training

## Summary
这篇文章不是提出新模型，而是一次对超大开源权重模型“可训练性”的实证拆解：作者尝试对 1T 参数的 Kimi-K2-Thinking 做 LoRA 后训练，却发现“开放权重”远不等于“开放训练”。核心结论是，现有开源训练栈在超大规模、量化、MoE 场景下存在多层实现缺陷，往往需要手工补丁才能勉强跑通。

## Problem
- 文章要解决的问题是：**开源大模型虽然开放了权重，但是否真的能被外部开发者低成本、可靠地继续训练/后训练**。这很重要，因为没有可训练性，开放权重对定制化、可控部署和生态创新的价值会大幅缩水。
- 具体案例是对 **Kimi-K2-Thinking（1T 参数、MoE、INT4 专家量化）** 进行 post-training，目标是看到 **loss 下降**，并让模型在行为上学会像 Yoda 一样回答问题。
- 作者发现主要障碍不是算法本身，而是基础设施问题：模型加载、量化处理、显存分配、设备映射、LoRA 兼容性、MoE 前向逻辑等多个环节都存在隐藏 bug 或不适合 trillion-scale 的实现。

## Approach
- 用一个**可验证行为变化**的小型数据集做实验：从 TriviaQA 取问题，再让另一个 LLM 生成“Yoda 口吻”的答案，形成约 **1000 条**训练样本。
- 以 HuggingFace Transformers + PEFT LoRA 为基础，尝试在 **8×H200（总显存 1128 GB）** 上直接加载并训练 **moonshotai/Kimi-K2-Thinking**。
- 遇到问题后，作者逐层排查并打补丁，核心修改包括：
  - 删除对**已量化模型再次执行 compress_model** 的步骤，避免无意义且极慢的“压缩”。
  - 打开 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`，缓解 GPU 内存分配/碎片问题导致的超长卡顿。
  - 手工指定更均匀的 `device_map`，避免 `device_map='auto'` 造成单卡显存严重倾斜。
  - 避开 **LoRA 与 quantized expert 权重不兼容** 的部分，只对 shared experts 和部分注意力/投影层加 LoRA。
  - 将模型设为 `eval()` 以绕过 MoE gate 在 train 模式下的断言；并重写压缩线性层前向，使其**按层即时反量化并立即释放权重**，防止显存累积泄漏式 OOM。
- 最终目标不是提出新训练算法，而是证明：通过一系列底层 monkey-patch，现有开源栈能否把超大开源权重模型“勉强训起来”。

## Results
- 在删除重复压缩调用后，模型从卡在 **“Compressing model” 超过 1 小时**，变为正常完成 **62 个 checkpoint shard** 加载，加载阶段显著推进。
- 设置 `expandable_segments:True` 后，原本在 shard 加载后还要额外卡住 **约 20 分钟** 的 `dispatch_model` 问题被消除，模型可以在 checkpoint 加载完成后**立即**进入下一步。
- 使用 `device_map='auto'` 时，7 张卡约为 **62.7 GB**，而 **GPU 7 达到 120.9/140 GB**；手工均匀分层后，前向通过，说明自动分配在该模型上明显失衡。
- 修复压缩线性层的反量化逻辑后，训练首次真正跑通：示例中 loss 从 **1.7443 → 1.7749 → 1.7258 → 1.6842 → 1.5071**（前 5 步，step 0-4），满足“loss 下降”的成功标准。
- 跑通配置可提升到 **batch size 8、sequence length 2048、45 秒/step、364 train tokens/s**，但作者指出该方案仍然**不能训练 experts**，且按 token 计费约比 **Tinker 贵 6–9 倍**。
- 定性结果上，模型确实学会了目标风格：如对 “who are you?”、“Can you give some advice?” 的回答明显呈现 **Yoda 式倒装口吻**。不过文中**没有给出标准 benchmark、测试集指标或与其他训练框架的严格对照实验**，最强结论仍是“可以勉强训练起来，但效率和完整性都不理想”。

## Link
- [https://www.workshoplabs.ai/blog/open-weights-open-training](https://www.workshoplabs.ai/blog/open-weights-open-training)
