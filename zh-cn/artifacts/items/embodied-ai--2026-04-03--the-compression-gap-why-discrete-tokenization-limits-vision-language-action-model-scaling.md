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
本文认为，当动作被压缩成离散 token 时，提升视觉编码器并不能稳定改善机器人操作性能。作者把这种失效模式称为**压缩缺口**：策略管线中最窄的信息瓶颈决定更好的视觉特征能否传到动作输出。

## 问题
- 视觉-语言-动作工作通常假设，更强的视觉编码器会改善下游控制，就像它在视觉-语言建模中那样。
- 论文检验的是：当策略预测的是**离散动作 token**而不是连续动作时，这个假设是否仍然成立。
- 这对机器人基础模型很重要，因为很多扩展方案都把重点放在更大的编码器和更多预训练上，但这些收益可能会被动作表示挡住。

## 方法
- 论文在**LIBERO-10**上比较了两类策略，并保持训练和骨干设置一致：**Diffusion Policy（连续动作）**和**OAT（离散有序动作 token 化）**。
- 论文用信息瓶颈视角描述这条管线：从观测到表示再到动作，端到端的信息流由最窄的一段决定上限。
- 对于 OAT，离散分词器带来硬上限：词表大小为**1000**、潜在时间跨度为**8**时，动作通道的上限约为每个动作块**80 bit**。
- 论文做了三项测试：在两个模型规模上比较编码器升级（**ResNet-18 → SigLIP**）的因子实验；在**ResNet-18 / SigLIP / SigLIP 2 / DINOv2**上做编码器质量扫描；以及一个改变 OAT 容量的 codebook 大小消融。

## 结果
- 在**LIBERO-10**上，把编码器从**ResNet-18**升级到**SigLIP**时，**Diffusion Policy**在规模**M**下从**36.4% → 57.6%**（**+21.2** 个百分点），在规模**L**下从**44.0% → 70.0%**（**+26.0** 个百分点）。
- 在相同的编码器升级下，**OAT**的提升小得多：规模**M**下从**53.8% → 57.4%**（**+3.6** 个百分点），规模**L**下从**48.0% → 58.4%**（**+10.4** 个百分点）。
- 在规模**M**的编码器扫描中，**Diffusion Policy**会随着编码器质量提高而上升：**36.4%（ResNet-18）**、**57.6%（SigLIP）**、**62.8%（SigLIP 2）**、**63.8%（DINOv2 ViT-L/14）**。**OAT**没有出现同样的趋势：**53.8%**、**57.4%**、**44.2%**、**51.0%**。
- 不同编码器质量下，二者的相对排名会反转：使用**ResNet-18**时，**OAT 领先 DP 17.4 个百分点**；使用**DINOv2**时，**DP 领先 OAT 12.8 个百分点**，反转幅度约为**30.2** 个百分点。
- 在 OAT 的 codebook 实验中，把容量从**1000（约 80 bit）**提高到**1920（约 87 bit）**后，编码器敏感性从**+3.6** 个百分点变为**+15.2** 个百分点，因为**ResNet-18**降到**42.6%**，而**SigLIP**仍接近**57.8%**。在**4375（约 97 bit）**时，OAT 达到**54.6%（ResNet-18）**和**58.6%（SigLIP）**，差值为**+4.0** 个百分点。
- 论文的核心结论是，离散 token 化会挡住更好感知带来的扩展收益。对 VLA 系统来说，限制因素可能是动作分词器，而不是视觉编码器或策略规模。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03191v1](http://arxiv.org/abs/2604.03191v1)
