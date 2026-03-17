---
source: arxiv
url: http://arxiv.org/abs/2603.09298v1
published_at: '2026-03-10T07:28:41'
authors:
- Yuankai Luo
- Woping Chen
- Tong Liang
- Zhenguo Li
topics:
- robot-learning
- vision-language-action
- lora
- multi-task-learning
- continual-learning
relevance_score: 0.42
run_id: materialize-outputs
---

# CORAL: Scalable Multi-Task Robot Learning via LoRA Experts

## Summary
CORAL提出了一种面向多任务机器人学习的可扩展方案：冻结一个预训练VLA主干，并为每个任务分配一个独立LoRA专家。它旨在用很小的存储和几乎无推理额外开销的方式，减少多任务梯度冲突、支持持续增量扩展，并提升真实与仿真环境中的任务成功率。

## Problem
- 多任务机器人微调中，不同任务的梯度会相互冲突，导致负迁移，单一共享模型往往牺牲单任务性能。
- 为每个任务保存一个完整模型虽然能避免干扰，但存储与部署成本随任务数线性爆炸，不适合边缘机器人。
- 顺序加入新任务时，标准微调还会覆盖旧知识，引发灾难性遗忘，因此需要一种既可扩展又低开销的持续学习机制。

## Approach
- 冻结一个预训练的Vision-Language-Action主干模型，只训练任务专属的LoRA适配器，把通用能力与任务特化能力分离开。
- 每个任务对应一个独立LoRA专家，训练时只更新该专家参数，不与其他任务共享可训练参数，从结构上避免参数级任务干扰。
- LoRA同时注入到视觉语言编码器和动作头的注意力层，让专家既能调整感知/指令理解，也能调整低层控制策略。
- 推理时用CORAL Manager根据语言指令直接确定任务并加载对应专家，无需学习式gating网络；通过将LoRA权重合并进主干，实现零额外推理FLOPs。
- 该设计天然支持持续扩展：加入新任务时只需新增一个轻量LoRA专家，不必重训或覆盖旧任务参数。

## Results
- 在LIBERO 40任务基准上，CORAL在SimVLA主干下达到**99.3%**平均成功率，较SimVLA基线**98.6%**提升**+0.7**个百分点，并超过X-VLA的**98.1%**；其中LIBERO-Long从**96.4%**升至**98.8%**，提升**+2.4**。
- 在同一LIBERO基准上，CORAL用于\(\pi_{0.5}\)主干时达到**98.4%**，较\(\pi_{0.5}\)基线**96.9%**提升**+1.5**；在最难的LIBERO-Long上从**92.4%**提升到**95.8%**，增幅**+3.4**。
- 在WidowX任务上，CORAL_SimVLA平均成功率为**97.9%**，高于SimVLA基线的**95.8%**，提升**+2.1**；其中Stack和Eggplant分别提升**+4.1**到**95.8%**，Spoon与Carrot均为**100.0%**。
- 在Google Robot任务上，CORAL_SimVLA平均达到**84.9%**，较SimVLA基线**77.0%**提升**+7.9**，也高于X-VLA的**75.7%**与RT-2-X的**65.6%**；子任务Move从**81.0%**提升到**92.8%**（**+11.8**），Open从**67.7%**提升到**75.9%**（**+8.2**）。
- 效率方面，典型**0.8B**参数VLA模型上，一个rank-16专家仅约**26 MB**，约为完整模型的**100×**压缩；LIBERO的**40**个专家总存储约**1 GB**，而单个完整微调检查点约**3 GB**。
- 部署方面，专家切换在单GPU上可于**100 ms**内完成，并声明带来**零额外推理FLOPs/延迟**；LIBERO中每个任务LoRA只训练**50 steps**，强调其轻量适配特性。

## Link
- [http://arxiv.org/abs/2603.09298v1](http://arxiv.org/abs/2603.09298v1)
