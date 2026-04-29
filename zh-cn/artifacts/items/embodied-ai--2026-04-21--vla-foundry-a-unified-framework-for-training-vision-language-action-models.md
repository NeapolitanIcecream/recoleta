---
source: arxiv
url: http://arxiv.org/abs/2604.19728v1
published_at: '2026-04-21T17:51:51'
authors:
- Jean Mercat
- Sedrick Keh
- Kushal Arora
- Isabella Huang
- Paarth Shah
- Haruki Nishimura
- Shun Iwase
- Katherine Liu
topics:
- vision-language-action
- robot-foundation-model
- multimodal-training
- robot-data-scaling
- sim-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# VLA Foundry: A Unified Framework for Training Vision-Language-Action Models

## Summary
## 摘要
VLA Foundry 是一个开源代码库，用一套统一的堆栈训练语言模型、视觉语言模型和视觉语言动作模型。论文的主要结论是，这条统一流水线让 VLA 研究更容易控制，而更强的 VLM 骨干模型，例如 Qwen3-VL，可以提升下游机器人策略性能。

## 问题
- 开源 VLA 项目通常集中在最后的动作训练阶段，并依赖彼此独立的预训练流水线，这使得骨干模型、数据混合方式和训练配方研究很难在干净的条件下进行。
- 与文本和图文数据相比，机器人数据较少，因此上游 LLM 和 VLM 的训练选择会显著影响下游机器人性能。
- 研究人员需要一个系统，支持全流程实验、骨干模型和数据集的模块化替换，以及可复现的大规模训练。

## 方法
- 该框架用一个共享代码库完成 LLM、VLM 和 VLA 训练，提供 YAML/dataclass 配置、可插拔注册表、共享训练循环，并同时支持从零开始训练和使用 Hugging Face 骨干模型。
- 它统一了多模态数据处理：文本、图像字幕和机器人数据集可以按权重采样混合；机器人数据还带有专门的归一化、动作分块、位姿处理，以及预处理为 WebDataset shards 的流程。
- 为了支持大规模训练，它支持基于 DDP/FSDP2 的分布式训练、混合精度、梯度检查点，以及多节点运行；文中基准测试最高覆盖 16 个节点上的 128 张 GPU。
- 论文用两类模型展示了这个框架：通过 LLM→VLM→VLA 流水线从零训练的 Foundry-VLA-1.7B，以及基于预训练 Qwen3-VL 2B 骨干模型构建的 Foundry-Qwen3VLA-2.1B-MT。
- VLA 模型在 VLM 序列中加入一个 observation token，并将其隐藏状态输入一个 3.25 亿参数的 flow-transformer 动作头；该动作头用 flow matching 训练，对动作序列去噪。

## 结果
- 从零训练的 LLM 是一个 12 亿参数模型，在 DCLM 上用 5 亿样本 / 1 万亿 token 训练。在标准多项选择基准上，1 万亿 token 检查点报告 HellaSwag **66.7**、MMLU **26.6**、ARC-e **71.7**、ARC-c **39.3**、PIQA **77.5**、WinoGrande **62.6**、OpenBookQA **40.8**、BoolQ **65.4**。
- 从零训练的 VLM 将该 LLM 与一个 8600 万参数 ViT 结合，并在 **2 亿** 个 DataCompDR-1B 样本上训练。在 COCO_VAL 图像描述任务上，2 亿样本检查点报告 BLEU-1 **58.64**、BLEU-2 **38.62**、BLEU-3 **24.49**、BLEU-4 **15.57**、ROUGE-L **38.17**、CIDEr **55.14**。
- VLA 堆栈在 VLM 之上加入一个 3.25 亿参数的 transformer 动作头，使完整的从零训练 VLA 模型达到 **17 亿** 参数；基于 Qwen 的多任务模型为 **21 亿** 参数。
- 评测基准 lbm_eval_oss 在 Drake 仿真中包含 **49** 个双臂桌面操作任务。
- 摘要称，在 LBM Eval 的标称闭环评测设置下，完全开放的从零训练模型与作者此前的闭源工作表现相当，而将骨干模型替换为 Qwen3-VL 后，结果比他们的基线高出很多。
- 给出的摘录没有包含主要的 VLA 闭环成功率表，因此这里无法提供相对基线提升的确切机器人策略数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19728v1](http://arxiv.org/abs/2604.19728v1)
