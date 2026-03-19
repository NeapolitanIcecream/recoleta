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
language_code: en
---

# Open Weights isn't Open Training

## Summary
This article does not propose a new model; rather, it is an engineering retrospective on post-training an ultra-large open-weights model: the author attempted to perform LoRA fine-tuning on the 1T-parameter Kimi-K2-Thinking, only to find that “open weights” does not mean “open training.” The core conclusion is that the current open-source training stack contains many hidden failure points in ultra-large-scale, quantized, and MoE settings, and can only be made to run with a large number of low-level patches.

## Problem
- The problem to solve is: **how to perform practical post-training on an open 1T-scale quantized MoE model at relatively low cost**, and verify that the model’s behavior actually changes in the direction implied by the dataset.
- This matters because many “open-source models” release only weights, without providing a truly reproducible, scalable, and modifiable training path; for companies and researchers, this directly limits customization, alignment, and continual training capabilities.
- The article shows that in the HuggingFace / PEFT / Accelerate / quantization stack, features that appear usable for 8B models may fail at 1T+ scale due to issues with loading, VRAM, LoRA compatibility, MoE routing, and dequantization.

## Approach
- The author chose **Kimi-K2-Thinking** (a 1T-parameter MoE whose expert weights are quantized to 4-bit), targeting LoRA post-training on **8×H200**; to verify that training was effective, they constructed a **1,000-sample** Yoda-style Q&A dataset.
- They first wrote a standard HuggingFace + PEFT training script, then investigated failure points layer by layer, including: recompressing already-quantized weights, GPU memory allocation stalls during the `dispatch_model` stage, uneven VRAM distribution caused by `device_map='auto'`, incompatibility between quantized weights and LoRA, assertion failures in the MoE gate in train mode, and persistent VRAM accumulation because dequantized weights were not released.
- For each issue, the author applied the most direct engineering fix: remove the unnecessary `compress_model` call; set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`; manually assign layers to GPUs; avoid attaching LoRA to quantized experts and train only shared experts and attention-related projections; set the model to eval mode to bypass the training assertion on the non-differentiable gate.
- The most critical patch was modifying the forward pass of the quantized linear layer: **instead of registering dequantized weights as persistent parameters, dequantize on the fly, perform the linear computation, and then explicitly delete them**, thereby preventing continuous VRAM accumulation during each layer’s forward pass.

## Results
- Training was ultimately made to run: after patching, the training log showed loss decreasing from **1.7443 → 1.5071** (first 5 steps: 1.7443, 1.7749, 1.7258, 1.6842, 1.5071), indicating that at least in a small-scale experiment, the optimization objective began to improve.
- The achieved training configuration was: **batch size 8, sequence length 2048, 45 seconds per step, 364 train tokens/s**, on **8×H200** hardware.
- Qualitatively, after training the model could clearly produce **Yoda-style** responses, indicating that its behavior did in fact change in the direction implied by the dataset, satisfying the second part of the author’s original success criteria.
- But the limitations are also clear: **expert parameters still could not be trained**; only shared experts and some projection layers could be trained. So this is not a complete MoE post-training solution in the full sense.
- In terms of cost, the author claims that although the approach “works,” the **cost per token is about 6–9× higher than Tinker**, showing that the engineering viability is still far from ideal.
- The article does not report SOTA benchmark gains on standard datasets; its strongest substantive claim is that, through a series of low-level monkey patches, the author enabled runnable LoRA post-training for an open 1T quantized MoE model that was originally untrainable, and demonstrated that “open weights ≠ open training.”

## Link
- [https://www.workshoplabs.ai/blog/open-weights-open-training](https://www.workshoplabs.ai/blog/open-weights-open-training)
