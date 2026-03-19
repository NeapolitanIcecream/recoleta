---
source: arxiv
url: http://arxiv.org/abs/2603.03045v2
published_at: '2026-03-03T14:38:05'
authors:
- Inhoe Koo
- Hyunho Cha
- Jungwoo Lee
topics:
- quantum-compilation
- unitary-synthesis
- gflownet
- transformer-policy
- sparse-reward
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# QFlowNet: Fast, Diverse, and Efficient Unitary Synthesis with Generative Flow Networks

## Summary
QFlowNet proposes a generative method for **exact unitary synthesis** of quantum circuits, combining a GFlowNet with a Transformer encoder to learn **fast and diverse** circuit decompositions under extremely sparse terminal rewards. The paper’s core contribution is to uniformly reformulate the synthesis of any target unitary matrix as a path-generation problem of “moving from a residual state to the identity matrix,” thereby reusing a single policy.

## Problem
- The problem it addresses is: how to decompose a target unitary matrix into a sequence of quantum gates and efficiently find the correct circuit when the **combinatorial search space is enormous** and the **reward is extremely sparse**.
- This is important because unitary synthesis is a foundational step in quantum compilation; if executable circuits cannot be found quickly, quantum algorithms are difficult to map onto real hardware.
- Existing methods involve clear trade-offs: RL is typically slow to train, sample-inefficient, and tends to converge to a single solution; diffusion-based generative models can produce diverse solutions, but inference requires many sampling steps and is therefore slow.

## Approach
- Core mechanism: define the state as the **unitary residual** $s_t = U V_t^\dagger$. In other words, it measures how far the currently generated circuit still is from the target; when the residual becomes the identity matrix $I$, synthesis has succeeded.
- Use a **GFlowNet** to learn a step-by-step gate-selection policy, so that it samples solutions in proportion to reward rather than learning only a single optimal solution; this naturally supports diverse circuit generation and enables credit assignment under terminal rewards via Trajectory Balance.
- Use a **CNN+Transformer encoder** to read high-dimensional unitary/residual matrices, capture long-range global correlation structure in the matrix, and then use an MLP to output the distribution over the next quantum gate.
- The reward design is minimal: a binary reward is given only at termination. If the final fidelity $F(U,V_f) > 0.999$, the reward is $10^2$; otherwise it is $10^{-4}$; no complex reward shaping or pretraining is required.
- Training runs for 100,000 steps with batch size 2048 in the 3-qubit experiments; during evaluation, at most 1024 candidate circuits are sampled per target, and success is declared as long as one of them reaches the threshold.

## Results
- The **overall 3-qubit success rate** reaches **99.7%**, with evaluation covering random unitary circuits of **lengths 1–12**; even on the hardest **length-12** instances, the success rate remains **96%**.
- **4-qubit scalability** drops significantly: simple circuits can still reach **100%**, but performance falls to **48%** at **length 5**, and is **below 10% for length 8 and above**, showing that the current method is limited by the $O(4^n)$ input complexity.
- **Inference efficiency** is better than the diffusion model genQC: for targets of **length 8 and above**, genQC requires noticeably more samples, reaching nearly **70 attempts on average** at **length 12**; QFlowNet requires only **1–2 attempts on average** across the entire complexity range.
- **Training time** is also better than the RL baseline: on the **3-qubit** task, QFlowNet converges in about **2 days**, whereas the compared **Gumbel AlphaZero** requires **more than 10 days**; the figure caption also summarizes overall training as about **1–2 days vs. 6.5–10 days**.
- In terms of **circuit compactness**, the generated results often match the baseline length after Qiskit optimization, and the paper claims that a substantial number of samples are **shorter than the Qiskit baseline**, though the excerpt does not provide an exact proportion.
- In terms of **solution diversity**, based on **1024 samples**, the model can often find **dozens to over a hundred** distinct and correct decompositions for a single target; the excerpt does not provide more detailed mean or distribution statistics.

## Link
- [http://arxiv.org/abs/2603.03045v2](http://arxiv.org/abs/2603.03045v2)
