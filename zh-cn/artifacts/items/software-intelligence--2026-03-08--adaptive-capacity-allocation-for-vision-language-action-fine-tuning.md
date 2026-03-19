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
language_code: zh-CN
---

# Adaptive Capacity Allocation for Vision Language Action Fine-tuning

## Summary
本文提出 LoRA-SP，一种面向视觉-语言-动作模型（VLA）微调的自适应容量分配方法，用输入级、层级的动态秩替代固定秩 LoRA。它针对机器人迁移中秩需求高且随任务变化的问题，在真实机器人多任务适配上以更少可训练参数达到或超过全量微调。

## Problem
- 现有 PEFT/LoRA 依赖固定 rank，但机器人/VLA 迁移的“内在秩”明显高于语言模型，且会随任务、层、机器人本体与环境变化。
- 固定全局 rank 在多任务设置下会让不同任务被迫共享同一低秩子空间，导致跨任务干扰、性能不稳定，并需要昂贵的 rank 网格搜索。
- 这很重要，因为预训练 VLA 部署到**未见过的机器人本体、环境或任务**时，若无法高效适配，就会限制 Physical AI 的落地能力。

## Approach
- 核心方法是 **LoRA-SP (Select-Prune)**：不用固定的低秩更新 \(\Delta W=BA\)，而是改成 SVD 风格的输入条件更新 \(\Delta W(x)=U\,\mathrm{diag}(s(x))\,V\)。
- 其中 \(U,V\) 是共享“向量库”，一个小型 router 对每个输入、每一层输出非负分数 \(s(x)\)，这些分数可理解为“当前输入需要哪些方向、强度多大”的奇异值。
- 再按累计能量 \(E_k(x)=\sum_{i\le k}s_i(x)^2 / \sum_j s_j(x)^2\) 选择最小的有效秩 \(k\)，满足 \(E_k(x)\ge \eta\)；其余向量被剪枝。简单说：只保留解释大部分更新能量的少数方向。
- 作者还加入谱损失 \(\mathcal{L}_{spec}=1-E_k(x)\)，把能量进一步集中到更少的向量上，从而在不明显损失精度的情况下学到更紧凑的适配器。
- 理论上，方法把 rank 选择与低秩近似误差直接关联：相对 Frobenius 误差约为 \(\sqrt{1-E(k)}\)，因此 \(\eta\) 成为可解释的容量/误差控制旋钮。

## Results
- 论文在 **4 个真实机器人操作任务**、**未见过的 AgileX PiPER 7-DoF 机械臂**、共 **480 条示范**、**2 个 VLA 骨干（\(\pi_0\) 与 SmolVLA）** 上评测。
- 关键结论：VLA 对 rank 更敏感，\(\pi_0\)-3.5B 需要大约 **\(r\approx128\)** 才接近全量微调；对比之下，LLaMA-7B 在 **\(r\in\{4,8\}\)** 已接近全量微调表现。
- 在多任务设置下，作者声称 LoRA-SP 相比标准 LoRA **最高提升 31.6% 成功率**，并且对 rank 选择更鲁棒。
- **\(\pi_0\) 多任务**：LoRA-SP 用 **9.2%** 可训练参数、平均激活秩 **76**，总体成功率 **80.0%**；对比 Full FT **80.0%**、LoRA \(r=128\) **73.3%**、LoRA-MoE(top-1) **13.3%**、LoRA-MoE(weighted) **46.7%**、AdaLoRA **20.0%**。
- **SmolVLA 多任务**：LoRA-SP 用 **17.1%** 可训练参数、平均激活秩 **60**，总体成功率 **86.7%**；对比 Full FT **73.3%**、LoRA \(r=128\) **40.0%**、LoRA-MoE(top-1) **33.3%**、LoRA-MoE(weighted) **60.0%**、AdaLoRA **6.7%**。
- 分任务数字也显示 LoRA-SP 具备竞争力：例如在 SmolVLA 多任务上，Open/Pour/Press/Pick-Place 分别为 **86.7/86.7/100.0/93.3**，而 Full FT 为 **73.3/86.7/100.0/86.7**。此外文中还声称谱损失可在接近减半的激活向量数下保持稳定成功率，但节选未完整给出全部消融表数值。

## Link
- [http://arxiv.org/abs/2603.07404v1](http://arxiv.org/abs/2603.07404v1)
