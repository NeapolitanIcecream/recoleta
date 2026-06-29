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
VLA Foundry 是一个开源代码库，用于在同一套代码中训练语言模型、视觉语言模型和视觉语言动作模型。论文的核心主张是，这条统一管线让 VLA 研究更容易控制，而且更强的 VLM 骨干（例如 Qwen3-VL）能提升下游机器人策略表现。

## 问题
- 现有开源 VLA 项目常把重点放在最后的动作训练阶段，并依赖彼此分离的预训练管线，这让骨干模型、数据混合和训练配方的实验很难干净地开展。
- 与文本和图文数据相比，机器人数据更稀缺，所以上游 LLM 和 VLM 的训练选择会明显影响下游机器人性能。
- 研究者需要一个支持全流程实验、可模块化替换骨干和数据集、并能复现大规模训练的系统。

## 方法
- 该框架用一个共享代码库处理 LLM、VLM 和 VLA 训练，配有 YAML/dataclass 配置、可插拔注册表、共享训练循环，并支持从零训练和 Hugging Face 骨干。
- 它标准化了多模态数据处理：文本、图像描述和机器人数据集可以按加权采样混合，机器人数据则有专门的归一化、动作分块、位姿处理，以及预处理成 WebDataset 分片。
- 在规模上，它支持分布式训练，使用 DDP/FSDP2、混合精度、梯度检查点，并支持多节点运行，基准测试规模达到 16 个节点、128 张 GPU。
- 论文用两类模型展示这个框架：Foundry-VLA-1.7B 从零通过 LLM→VLM→VLA 管线训练，Foundry-Qwen3VLA-2.1B-MT 则建立在预训练的 Qwen3-VL 2B 骨干之上。
- VLA 模型在 VLM 序列中加入一个 observation token，并将其隐藏状态送入一个 3.25 亿参数的 flow-transformer 动作头；这个动作头用 flow matching 训练，用来去噪动作序列。

## 结果
- 从零训练的 LLM 是一个 12 亿参数模型，使用 DCLM 的 5 亿样本 / 1 万亿 token 训练。在标准多项选择基准上，1 万亿 token 的 checkpoint 报告的分数为：HellaSwag **66.7**、MMLU **26.6**、ARC-e **71.7**、ARC-c **39.3**、PIQA **77.5**、WinoGrande **62.6**、OpenBookQA **40.8**、BoolQ **65.4**。
- 从零训练的 VLM 将这个 LLM 与一个 8600 万参数的 ViT 结合，并在 **2 亿** 个 DataCompDR-1B 样本上训练。在 COCO_VAL captioning 上，2 亿样本的 checkpoint 报告的分数为：BLEU-1 **58.64**、BLEU-2 **38.62**、BLEU-3 **24.49**、BLEU-4 **15.57**、ROUGE-L **38.17**、CIDEr **55.14**。
- VLA 栈在 VLM 之上使用一个 3.25 亿参数的 transformer 动作头，得到一个完整的从零训练 VLA 模型，总参数量为 **17 亿**；基于 Qwen 的多任务模型参数量为 **21 亿**。
- 评估基准 lbm_eval_oss 包含 **49** 个 Drake 仿真中的桌面双臂操作任务。
- 摘要声称，在 LBM Eval 的常规闭环评估中，完全开放的从零训练模型与作者先前的闭源工作表现相当；把骨干换成 Qwen3-VL 后，模型在基线之上有明显提升。
- 提供的节选没有包含主要的 VLA 闭环成功率表，所以这里看不到相对基线的精确机器人策略提升数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19728v1](http://arxiv.org/abs/2604.19728v1)
