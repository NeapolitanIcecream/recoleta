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
---

# Adaptive Capacity Allocation for Vision Language Action Fine-tuning

## Summary
本文提出 LoRA-SP，一种面向视觉-语言-动作模型微调的自适应容量分配方法，用动态激活秩替代固定秩 LoRA。它针对机器人跨任务、跨本体迁移时固定低秩容量不足且难调的问题，在真实机器人多任务实验中以更少可训练参数达到或超过全量微调表现。

## Problem
- 预训练 VLA 部署到**新环境、新机器人本体、和新任务**时，通常仍需适配；而标准 LoRA 依赖一个固定 rank，但机器人迁移的**内在秩更高且随任务变化更大**。
- 语言模型常用很小秩（如 $r\in\{4,8\}$）即可接近全量微调，但文中指出 VLA 在 OOD 机器人迁移中常需**$r\approx128$ 甚至接近满秩**，固定 rank 很难统一兼顾效率和精度。
- 多任务训练时，不同任务被迫共享同一低秩子空间，会带来**跨任务干扰**，导致 LoRA 对 rank 很敏感，往往需要昂贵的网格搜索。

## Approach
- 提出 **LoRA-SP (Select-Prune)**：不用固定的 $\Delta W=BA$，而是改成 **SVD 风格**的输入条件更新 $\Delta W(x)=U\,\mathrm{diag}(s(x))\,V$，其中 $U,V$ 是共享向量库，路由器输出非负分数 $s(x)$，相当于“每个方向该用多大力度”。
- 对每个输入、每一层，按照分数平方的累计能量选择最小活跃秩 $k$，满足 $E_k(x)\ge \eta$；只保留这些方向，其余剪掉。可把它理解为：**先准备一组足够宽的候选方向，再按当前样本自动挑出最必要的几个**。
- 文中给出谱分析：若累计能量为 $E(k)$，最佳 rank-$k$ 近似的相对 Frobenius 误差为 $\sqrt{1-E(k)}$，因此 $\eta$ 直接控制近似误差；例如文中说明 $\eta=0.99$ 对应误差上界约 **0.1**。
- 训练时加入谱损失 $\mathcal{L}_{\text{spec}}=1-E_k(x)$，鼓励能量集中到更少向量上，从而在**不明显损伤任务精度**的情况下自动压缩活跃秩。
- 方法使用单个共享适配器，而非为每个任务建立多个专家，因此相比 LoRA-MoE 更容易部署，也更利于跨任务共享有用方向。

## Results
- 在 **4 个真实机器人操作任务**、**未见过的 AgileX PiPER 7-DoF 机械臂**、共 **480 条示教**、**双 RGB 视角**上评测，覆盖两种 VLA 骨干：**$\pi_0$** 和 **SmolVLA**。
- 关键结论：LoRA-SP 在多任务上**最多比标准 LoRA 提升 31.6% 成功率**，同时“匹配或超过”全量微调，且对 rank 选择更稳健。
- **$\pi_0$ 多任务**：LoRA-SP 平均成功率 **80.0%**，与 **Full FT 80.0%** 持平；优于 **LoRA r=128 的 73.3%**（+6.7 个点）、**LoRA-MoE weighted-sum 的 46.7%**、**AdaLoRA 的 20.0%**。其活跃秩 **76**，可训练参数 **9.2%**，而 Full FT 为 **100%**。
- **SmolVLA 多任务**：LoRA-SP 平均成功率 **86.7%**，超过 **Full FT 73.3%**（+13.4 个点），显著优于 **LoRA r=128 的 40.0%**（+46.7 个点，相对提升约 116.8%）、**LoRA-MoE weighted-sum 的 60.0%**、**AdaLoRA 的 6.7%**。其活跃秩 **60**，可训练参数 **17.1%**，远低于 Full FT 的 **100%**。
- 固定秩 LoRA 的 rank 敏感性很强：例如在 **$\pi_0$ 多任务**中，LoRA 从 **r=8/16/32/64/128** 的平均成功率约为 **0.0/0.0/6.7/46.7/73.3%**；在 **SmolVLA 多任务**中对应约 **0.0/0.0/13.3/26.7/40.0%**，显示 VLA 迁移确实需要更高且更灵活的容量。
- 文中还报告：LLaMA-7B 在 **$r\in\{4,8\}$** 就接近全量微调，而 **$\pi_0$-3.5B** 要到 **$r\approx128$** 才接近全量微调；此外达到 **99% 能量** 所需秩在不同模块/数据域中可从**满秩的 0.2 到 0.9** 不等，说明层间和任务间容量需求高度异质。

## Link
- [http://arxiv.org/abs/2603.07404v1](http://arxiv.org/abs/2603.07404v1)
