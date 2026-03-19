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
- parameter-efficient-fine-tuning
- lora
- multi-task-learning
- robot-adaptation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Adaptive Capacity Allocation for Vision Language Action Fine-tuning

## Summary
This paper proposes LoRA-SP, an adaptive capacity allocation method for fine-tuning vision-language-action models, which replaces fixed-rank LoRA with dynamically activated rank. It targets the problem that fixed low-rank capacity is insufficient and hard to tune for cross-task and cross-embodiment robotic transfer, and in real-robot multi-task experiments it matches or exceeds full fine-tuning performance with fewer trainable parameters.

## Problem
- Deploying a pre-trained VLA to **new environments, new robot embodiments, and new tasks** usually still requires adaptation; however, standard LoRA relies on a fixed rank, while robotic transfer has a **higher intrinsic rank that varies more across tasks**.
- Language models can often use very small ranks (e.g., $r\in\{4,8\}$) to approach full fine-tuning, but the paper points out that VLA in OOD robot transfer often requires **$r\approx128$ or even near-full rank**, making it difficult for a fixed rank to balance efficiency and accuracy.
- In multi-task training, different tasks are forced to share the same low-rank subspace, causing **cross-task interference**, which makes LoRA highly sensitive to rank choice and often requires expensive grid search.

## Approach
- Proposes **LoRA-SP (Select-Prune)**: instead of using a fixed $\Delta W=BA$, it uses an **SVD-style** input-conditioned update $\Delta W(x)=U\,\mathrm{diag}(s(x))\,V$, where $U,V$ are a shared vector bank, and the router outputs nonnegative scores $s(x)$, indicating “how strongly each direction should be used.”
- For each input and each layer, it selects the minimum active rank $k$ according to the cumulative energy of squared scores, satisfying $E_k(x)\ge \eta$; only these directions are kept and the rest are pruned. This can be understood as: **first prepare a sufficiently wide set of candidate directions, then automatically pick the few most necessary ones for the current sample**.
- The paper provides a spectral analysis: if the cumulative energy is $E(k)$, the relative Frobenius error of the best rank-$k$ approximation is $\sqrt{1-E(k)}$, so $\eta$ directly controls approximation error; for example, the paper notes that $\eta=0.99$ corresponds to an error upper bound of about **0.1**.
- During training, a spectral loss $\mathcal{L}_{\text{spec}}=1-E_k(x)$ is added to encourage energy to concentrate on fewer vectors, thereby automatically compressing the active rank **without significantly harming task accuracy**.
- The method uses a single shared adapter rather than building multiple experts for each task, so compared with LoRA-MoE it is easier to deploy and better supports sharing useful directions across tasks.

## Results
- Evaluated on **4 real-robot manipulation tasks**, an **unseen AgileX PiPER 7-DoF robot arm**, with **480 demonstrations** and **dual RGB views**, covering two VLA backbones: **$\pi_0$** and **SmolVLA**.
- Key conclusion: LoRA-SP achieves **up to 31.6% higher success rate than standard LoRA** in multi-task settings, while “matching or exceeding” full fine-tuning and being more robust to rank choice.
- **$\pi_0$ multi-task**: LoRA-SP reaches an average success rate of **80.0%**, matching **Full FT at 80.0%**; outperforming **LoRA r=128 at 73.3%** (+6.7 points), **LoRA-MoE weighted-sum at 46.7%**, and **AdaLoRA at 20.0%**. Its active rank is **76**, with **9.2%** trainable parameters, whereas Full FT uses **100%**.
- **SmolVLA multi-task**: LoRA-SP reaches an average success rate of **86.7%**, exceeding **Full FT at 73.3%** (+13.4 points), and substantially outperforming **LoRA r=128 at 40.0%** (+46.7 points, about 116.8% relative improvement), **LoRA-MoE weighted-sum at 60.0%**, and **AdaLoRA at 6.7%**. Its active rank is **60**, with **17.1%** trainable parameters, far below Full FT’s **100%**.
- Fixed-rank LoRA shows strong rank sensitivity: for example, in **$\pi_0$ multi-task**, the average success rates for LoRA at **r=8/16/32/64/128** are about **0.0/0.0/6.7/46.7/73.3%**; in **SmolVLA multi-task**, they are about **0.0/0.0/13.3/26.7/40.0%**, showing that VLA transfer indeed requires higher and more flexible capacity.
- The paper also reports that LLaMA-7B approaches full fine-tuning at **$r\in\{4,8\}$**, whereas **$\pi_0$-3.5B** needs **$r\approx128$** to approach full fine-tuning; moreover, the rank required to reach **99% energy** varies across modules and data domains from **0.2 to 0.9 of full rank**, indicating highly heterogeneous capacity demands across layers and tasks.

## Link
- [http://arxiv.org/abs/2603.07404v1](http://arxiv.org/abs/2603.07404v1)
