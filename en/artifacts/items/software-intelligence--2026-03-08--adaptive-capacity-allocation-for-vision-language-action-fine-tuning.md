---
source: arxiv
url: http://arxiv.org/abs/2603.07404v1
published_at: '2026-03-08T01:33:01'
authors:
- Donghoon Kim
- Minji Bae
- Unghui Nam
- Gyeonghun Kim
- Suyun Lee
- Kyuhong Shim
- Byonghyo Shim
topics:
- vision-language-action
- parameter-efficient-finetuning
- lora
- adaptive-rank
- robot-learning
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# Adaptive Capacity Allocation for Vision Language Action Fine-tuning

## Summary
This paper proposes LoRA-SP, an adaptive capacity allocation method for fine-tuning vision-language-action models (VLAs), replacing fixed-rank LoRA with dynamic rank at the input and layer levels. It targets the problem that rank requirements in robotic transfer are high and vary by task, achieving performance on real-robot multi-task adaptation that matches or exceeds full fine-tuning with fewer trainable parameters.

## Problem
- Existing PEFT/LoRA methods rely on a fixed rank, but the “intrinsic rank” of robot/VLA transfer is clearly higher than that of language models and varies across tasks, layers, robot embodiments, and environments.
- A fixed global rank forces different tasks to share the same low-rank subspace in multi-task settings, causing cross-task interference, unstable performance, and requiring expensive rank grid search.
- This matters because when deploying a pre-trained VLA to **unseen robot embodiments, environments, or tasks**, the inability to adapt efficiently limits the real-world deployment of Physical AI.

## Approach
- The core method is **LoRA-SP (Select-Prune)**: instead of using a fixed low-rank update \(\Delta W=BA\), it uses an SVD-style input-conditioned update \(\Delta W(x)=U\,\mathrm{diag}(s(x))\,V\).
- Here, \(U,V\) are a shared “vector bank,” and a small router outputs nonnegative scores \(s(x)\) for each input and each layer. These scores can be understood as singular values indicating “which directions the current input needs and with what strength.”
- It then selects the minimum effective rank \(k\) according to cumulative energy \(E_k(x)=\sum_{i\le k}s_i(x)^2 / \sum_j s_j(x)^2\), such that \(E_k(x)\ge \eta\); the remaining vectors are pruned. In simple terms: only the few directions explaining most of the update energy are kept.
- The authors also introduce a spectral loss \(\mathcal{L}_{spec}=1-E_k(x)\), further concentrating energy into fewer vectors so that more compact adapters can be learned without noticeably sacrificing accuracy.
- Theoretically, the method directly links rank selection to low-rank approximation error: the relative Frobenius error is approximately \(\sqrt{1-E(k)}\), so \(\eta\) becomes an interpretable knob for controlling capacity/error.

## Results
- The paper evaluates on **4 real-robot manipulation tasks**, an **unseen AgileX PiPER 7-DoF robotic arm**, a total of **480 demonstrations**, and **2 VLA backbones (\(\pi_0\) and SmolVLA)**.
- Key conclusion: VLAs are more sensitive to rank; \(\pi_0\)-3.5B requires about **\(r\approx128\)** to approach full fine-tuning, whereas LLaMA-7B is already close to full fine-tuning performance at **\(r\in\{4,8\}\)**.
- In the multi-task setting, the authors claim that LoRA-SP improves success rate by **up to 31.6%** over standard LoRA, while also being more robust to rank choice.
- **\(\pi_0\) multi-task**: LoRA-SP uses **9.2%** trainable parameters with an average active rank of **76**, achieving an overall success rate of **80.0%**; compared with Full FT **80.0%**, LoRA \(r=128\) **73.3%**, LoRA-MoE(top-1) **13.3%**, LoRA-MoE(weighted) **46.7%**, and AdaLoRA **20.0%**.
- **SmolVLA multi-task**: LoRA-SP uses **17.1%** trainable parameters with an average active rank of **60**, achieving an overall success rate of **86.7%**; compared with Full FT **73.3%**, LoRA \(r=128\) **40.0%**, LoRA-MoE(top-1) **33.3%**, LoRA-MoE(weighted) **60.0%**, and AdaLoRA **6.7%**.
- Per-task numbers also show LoRA-SP is competitive: for example, on SmolVLA multi-task, Open/Pour/Press/Pick-Place are **86.7/86.7/100.0/93.3**, while Full FT is **73.3/86.7/100.0/86.7**. In addition, the paper claims that spectral loss can maintain stable success rates with nearly half as many active vectors, though the excerpt does not provide the full ablation table values.

## Link
- [http://arxiv.org/abs/2603.07404v1](http://arxiv.org/abs/2603.07404v1)
