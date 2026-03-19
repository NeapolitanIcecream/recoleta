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
language_code: en
---

# Open Weights isn't Open Training

## Summary
This article does not propose a new model; rather, it is an empirical dissection of the “trainability” of ultra-large open-weight models: the author attempted LoRA post-training on the 1T-parameter Kimi-K2-Thinking, only to find that “open weights” are far from equivalent to “open training.” The core conclusion is that existing open-source training stacks have multi-layer implementation flaws in ultra-large-scale, quantized, and MoE settings, often requiring manual patches just to barely run.

## Problem
- The article addresses the question: **although open large models release their weights, can external developers वास्तवապես continue training/post-training them reliably and at low cost**. This matters because without trainability, the value of open weights for customization, controllable deployment, and ecosystem innovation is greatly diminished.
- The specific case is post-training **Kimi-K2-Thinking (1T parameters, MoE, INT4 expert quantization)**, with the goal of seeing **loss decrease** and getting the model to learn to answer questions in the style of Yoda.
- The author found that the main obstacles were not the algorithm itself, but infrastructure issues: hidden bugs or trillion-scale-inappropriate implementations across model loading, quantization handling, VRAM allocation, device mapping, LoRA compatibility, MoE forward logic, and more.

## Approach
- Use a small dataset with **verifiable behavioral change**: take questions from TriviaQA, then have another LLM generate answers in a “Yoda tone,” yielding about **1,000** training samples.
- Using HuggingFace Transformers + PEFT LoRA as the base, attempt to directly load and train **moonshotai/Kimi-K2-Thinking** on **8×H200 (1128 GB total VRAM)**.
- After encountering problems, the author investigated layer by layer and applied patches. The core changes included:
  - Remove the step that **runs compress_model again on an already quantized model**, avoiding meaningless and extremely slow “compression.”
  - Enable `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` to mitigate long stalls caused by GPU memory allocation/fragmentation issues.
  - Manually specify a more balanced `device_map` to avoid the severe single-GPU VRAM skew caused by `device_map='auto'`.
  - Avoid the parts where **LoRA is incompatible with quantized expert weights**, and apply LoRA only to shared experts and some attention/projection layers.
  - Set the model to `eval()` to bypass assertions in the MoE gate under train mode; and rewrite the compressed linear layer forward pass so it **dequantizes on the fly per layer and immediately frees weights**, preventing leak-like cumulative VRAM OOM.
- The ultimate goal is not to propose a new training algorithm, but to show whether a series of low-level monkey patches can make the existing open-source stack “barely train” an ultra-large open-weight model.

## Results
- After removing the duplicate compression call, the model went from being stuck at **“Compressing model” for over 1 hour** to successfully completing loading of **62 checkpoint shards**, a significant improvement in the loading stage.
- After setting `expandable_segments:True`, the `dispatch_model` issue—which previously remained stuck for **about 20 more minutes** after shard loading—was eliminated, allowing the model to move to the next step **immediately** after checkpoint loading finished.
- With `device_map='auto'`, 7 GPUs were at about **62.7 GB**, while **GPU 7 reached 120.9/140 GB**; after manually balancing the layer placement, the forward pass succeeded, showing that automatic placement was clearly imbalanced for this model.
- After fixing the dequantization logic of the compressed linear layer, training truly ran end-to-end for the first time: in the example, loss went from **1.7443 → 1.7749 → 1.7258 → 1.6842 → 1.5071** (first 5 steps, step 0-4), meeting the success criterion of “loss decreases.”
- The working configuration could be scaled to **batch size 8, sequence length 2048, 45 seconds/step, 364 train tokens/s**, but the author notes that this setup still **cannot train experts**, and costs roughly **6–9× more than Tinker** on a per-token basis.
- Qualitatively, the model did learn the target style: for example, its answers to “who are you?” and “Can you give some advice?” clearly showed **Yoda-style inverted phrasing**. However, the article **does not provide standard benchmarks, test-set metrics, or rigorous comparison experiments with other training frameworks**; the strongest conclusion remains: “it can barely be trained, but both efficiency and completeness are unsatisfactory.”

## Link
- [https://www.workshoplabs.ai/blog/open-weights-open-training](https://www.workshoplabs.ai/blog/open-weights-open-training)
