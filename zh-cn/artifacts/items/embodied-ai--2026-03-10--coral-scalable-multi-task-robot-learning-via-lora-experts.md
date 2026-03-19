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
- vision-language-action
- multi-task-learning
- lora-adapters
- robot-policy
- continual-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# CORAL: Scalable Multi-Task Robot Learning via LoRA Experts

## Summary
CORAL提出一种面向多任务机器人学习的参数隔离框架：冻结一个预训练VLA主干，并为每个任务添加一个轻量LoRA专家。它试图同时解决多任务负迁移、持续新增任务时的遗忘，以及边缘部署下的存储开销问题。

## Problem
- 多任务机器人联合微调时，不同任务梯度会相互冲突，导致负迁移，尤其在细粒度语言指令容易混淆时更严重。
- 若每个任务都保存一份完整模型检查点，存储与部署成本会随任务数线性爆炸，不适合真实机器人系统。
- 顺序学习新任务还会覆盖旧知识，引发灾难性遗忘，因此需要一种既能扩展又不互相干扰的方案。

## Approach
- 冻结一个通用的预训练VLA基础模型，只训练每个任务各自独立的LoRA适配器，把任务特有知识放进小型“专家”里。
- LoRA同时注入到视觉语言编码器和动作头的注意力层，让专家既能调整感知/语言特征，也能调整控制策略。
- 推理时由CORAL Manager根据语言指令直接确定任务并加载对应专家，不需要学习式gating网络或外部LLM路由。
- 通过先恢复干净主干、再合并目标LoRA权重的方式实现在线切换；合并后按原模型执行，因此作者声称没有额外推理FLOPs或时延开销。
- 由于不同任务参数完全隔离，新任务可顺序加入而不覆盖旧任务参数，从机制上缓解干扰与遗忘。

## Results
- **LIBERO（40任务）**：CORAL with **SimVLA** 达到 **99.3%** 平均成功率，相比 **SimVLA baseline 98.6%** 提升 **+0.7**，并高于文中列出的 **X-VLA 98.1%**；在 **LIBERO-Long** 上为 **98.8% vs 96.4%**，提升 **+2.4**。
- **LIBERO（同一框架换主干）**：CORAL with **π0.5** 达到 **98.4%**，相比 **π0.5 baseline 96.9%** 提升 **+1.5**；其中 **Long** 子集 **95.8% vs 92.4%**，提升 **+3.4**。
- **WidowX / Simpler-Bridge**：CORAL with **SimVLA** 平均 **97.9%**，高于 **SimVLA baseline 95.8%**，提升 **+2.1**；在 **Stack** 与 **Eggplant** 任务上分别提升 **+4.1**，且 **Spoon/Carrot** 达到 **100%/100%**。
- **Google Robot / Simpler-Fractal**：CORAL with **SimVLA** 平均 **84.9%**，相比 **SimVLA baseline 77.0%** 提升 **+7.9**；相较 **X-VLA 75.7%** 也更高。分项上 **Pick 85.9 (+3.6)**、**Move 92.8 (+11.8)**、**Open 75.9 (+8.2)**。
- **效率与存储**：针对 **0.8B** 主干，单个 **rank-16 LoRA** 专家约 **26MB**，作者称约比完整模型小 **100×**；40个LIBERO任务的专家库约 **1GB**，而单个完整微调检查点约 **3GB**。专家切换时间约 **100ms**，且声称 **zero additional inference FLOPs**。
- **真实机器人**：论文声称在 **Galaxea R1 Lite** 上验证了跨场景泛化、新任务获取和抗遗忘能力，但给定摘录未提供该部分的完整量化表格，因此无法从摘录中列出更具体真实世界数值。

## Link
- [http://arxiv.org/abs/2603.09298v1](http://arxiv.org/abs/2603.09298v1)
