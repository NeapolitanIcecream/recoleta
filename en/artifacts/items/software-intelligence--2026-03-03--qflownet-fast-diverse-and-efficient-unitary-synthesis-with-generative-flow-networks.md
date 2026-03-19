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
- gflownet
- transformer-policy
- unitary-synthesis
- sparse-reward
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# QFlowNet: Fast, Diverse, and Efficient Unitary Synthesis with Generative Flow Networks

## Summary
QFlowNet proposes a generative framework for exact unitary synthesis of quantum circuits, combining GFlowNet with a Transformer encoder to learn efficiently even under extremely sparse terminal rewards. Its goal is to maintain a high success rate while training faster than reinforcement learning, inferring faster than diffusion models, and generating diverse valid quantum circuits.

## Problem
- The paper addresses **unitary synthesis**: decomposing a target unitary matrix into a sequence of quantum gates. This is crucial for quantum compilation, but the search space grows combinatorially with circuit length and gate-set size.
- Existing RL methods often suffer from **sparse rewards**, requiring complex reward shaping and long training times, and they often converge to a single policy, making it difficult to provide multiple candidate solutions.
- Existing generative methods such as diffusion models can produce diverse solutions, but **inference is slow** and requires many samples, making them unsuitable for online or rapid compilation scenarios.

## Approach
- The core mechanism reformulates the synthesis process as a path search problem toward a unified target: the state is defined as the **residual unitary matrix** `s_t = U V_t^†`, so regardless of what the target `U` is, the endpoint is always the identity matrix `I`.
- Under this definition, the reward function no longer changes with the target; the model only needs to learn “how to reach `I` from any residual,” using a **general policy** to handle different target unitary matrices.
- It uses **GFlowNet** instead of standard RL: it learns to sample solutions in proportion to reward, so it is naturally inclined to generate multiple high-quality solutions rather than betting on only one optimum; the training objective uses Trajectory Balance to propagate sparse terminal rewards back through the entire trajectory.
- A **CNN+Transformer encoder** reads the `2 × d × d` unitary matrix tensor, captures non-local correlations in the matrix, and then an MLP policy head outputs the distribution over the next quantum gate.
- The reward design is very simple: if the fidelity `F(U, V_f) > 0.999` for the final circuit and target, a success reward of `100` is given; otherwise, an extremely small positive reward of `1e-4` is given, with no need for intermediate reward shaping or pretrained models.

## Results
- On the **3-qubit** benchmark (random unitaries, target circuit lengths **1–12**), QFlowNet achieves an overall success rate of **99.7%**.
- On the hardest **length-12** instances, the 3-qubit model still reaches a **96%** success rate; during evaluation, at most **1024** candidate circuits are sampled per target, and success is counted if any candidate has fidelity **>0.999**.
- Compared with the diffusion model **genQC**, QFlowNet is more stable in inference sampling efficiency: for circuits of length **8+**, the number of attempts required by genQC rises significantly, reaching an average close to **70 attempts** at **length 12**; QFlowNet, by contrast, requires only **1–2 attempts** on average across the full complexity range.
- In terms of training time, on the **3-qubit** task QFlowNet converges in about **2 days**, whereas the compared **Gumbel AlphaZero** method requires **more than 10 days**; the figure summarizes this as about **1–2 days** for QFlowNet versus about **6.5–10 days** for the baseline.
- On **4 qubits**, simple circuits can reach **100%** success, but performance drops markedly as complexity increases: about **48%** at length **5**, and below **10%** for lengths **8 and above**, showing that the main current bottleneck is memory/complexity scaling with qubit count.
- Beyond accuracy, the model can also generate **diverse and compact** circuits: the paper says that for a single target it can often find **dozens to hundreds** of different correct decompositions, and many results are even shorter than the baseline circuits optimized by **Qiskit transpile (optimization_level=1)**, though no more detailed per-case numeric table is provided here.

## Link
- [http://arxiv.org/abs/2603.03045v2](http://arxiv.org/abs/2603.03045v2)
