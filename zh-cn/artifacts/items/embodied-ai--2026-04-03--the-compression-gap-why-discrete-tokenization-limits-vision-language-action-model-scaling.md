---
source: arxiv
url: http://arxiv.org/abs/2604.03191v1
published_at: '2026-04-03T17:06:31'
authors:
- Takuya Shiba
topics:
- vision-language-action
- robot-policy-scaling
- discrete-action-tokenization
- diffusion-policy
- information-bottleneck
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling

## Summary
## 摘要
这篇论文认为，当动作被压缩为离散 token 时，扩大视觉编码器规模并不能稳定提升机器人操作表现。作者把这种失效模式称为 **Compression Gap**：策略流水线中最紧的信息瓶颈，决定了更好的视觉特征能否传到动作输出。

## 问题
- 视觉-语言-动作研究通常假设，更强的视觉编码器会像在视觉-语言建模中那样提升下游控制效果。
- 论文检验了这个假设在策略预测 **离散动作 token** 而不是连续动作时是否仍然成立。
- 这对机器人基础模型很重要，因为许多扩展方案都集中在更大的编码器和更多预训练上，但这些收益可能会被动作表示挡住。

## 方法
- 论文在 **LIBERO-10** 上、在匹配的训练设置和主干网络设置下，对比了两类策略：**Diffusion Policy（连续动作）** 和 **OAT（离散有序动作 token 化）**。
- 论文用信息瓶颈视角来描述整条流水线：在从观测到表征再到动作的链路中，端到端信息流由最窄的一段决定上限。
- 对 OAT 来说，离散 tokenizer 施加了一个硬上限：当词表大小为 **1000**、潜在 horizon 为 **8** 时，动作通道上限约为 **每个动作块 80 比特**。
- 论文进行了三组测试：在两种模型规模下比较编码器升级（**ResNet-18 → SigLIP**）的析因实验；跨 **ResNet-18 / SigLIP / SigLIP 2 / DINOv2** 的编码器质量扫描；以及改变 OAT 容量的 codebook 大小消融实验。

## 结果
- 在 **LIBERO-10** 上，把编码器从 **ResNet-18 升级到 SigLIP** 后，**Diffusion Policy** 在规模 **M** 时从 **36.4% → 57.6%**（**+21.2 个百分点**），在规模 **L** 时从 **44.0% → 70.0%**（**+26.0 个百分点**）。
- 在相同的编码器升级下，**OAT** 的提升小得多：规模 **M** 时从 **53.8% → 57.4%**（**+3.6 个百分点**），规模 **L** 时从 **48.0% → 58.4%**（**+10.4 个百分点**）。
- 在规模 **M** 的编码器扫描中，**Diffusion Policy** 随编码器质量上升：**36.4%（ResNet-18）**、**57.6%（SigLIP）**、**62.8%（SigLIP 2）**、**63.8%（DINOv2 ViT-L/14）**。**OAT** 没有表现出同样的规律：**53.8%**、**57.4%**、**44.2%**、**51.0%**。
- 不同编码器质量下的相对排序发生了反转：使用 **ResNet-18** 时，**OAT 比 DP 高 17.4 个百分点**；使用 **DINOv2** 时，**DP 比 OAT 高 12.8 个百分点**，总反转幅度约 **30.2 个百分点**。
- 在 OAT 的 codebook 实验中，把容量从 **1000（约 80 比特）** 提高到 **1920（约 87 比特）** 后，编码器敏感性从 **+3.6** 变为 **+15.2 个百分点**，因为 **ResNet-18 降到 42.6%**，而 **SigLIP 仍接近 57.8%**。在 **4375（约 97 比特）** 时，OAT 达到 **54.6%（ResNet-18）** 和 **58.6%（SigLIP）**，差距为 **+4.0 个百分点**。
- 论文的核心观点是，离散 token 化会阻断更强感知模块带来的扩展收益。对 VLA 系统来说，限制因素可能是动作 tokenizer，而不是视觉编码器或策略规模。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03191v1](http://arxiv.org/abs/2604.03191v1)
