---
source: arxiv
url: http://arxiv.org/abs/2604.15663v1
published_at: '2026-04-17T03:35:35'
authors:
- Jiahui Geng
- Qing Li
- Fengyu Cai
- Fakhri Karray
topics:
- multimodal-code-retrieval
- code-search
- retrieval-augmented-generation
- vision-language-code
- benchmark-datasets
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# CodeMMR: Bridging Natural Language, Code, and Image for Unified Retrieval

## Summary
## 摘要
CodeMMR 是一个多模态代码检索器，把自然语言、代码和图像放进同一个嵌入空间，因此同一个模型可以在这三种模态之间做检索。论文还提出了 **MMCoIR**，这是该设定下的一个基准，并表明标准多模态检索器会遗漏代码产物中大量视觉语义。

## 问题
- 现有代码检索模型大多把代码当作文本处理，忽略了与代码相关的视觉输出，例如网页、图表、SVG、示意图和 UML。
- 这会影响代码搜索和代码 RAG，因为开发者经常需要根据图像检索代码、根据代码检索图像，或在编辑和生成代码时结合文本与视觉信息。
- 在这项工作之前，还没有一个覆盖多领域、多语言、多种检索方向的多模态代码检索通用基准。

## 方法
- 论文构建了 **MMCoIR**，这是一个覆盖 5 个视觉领域、8 种编程语言和 11 个库的基准，任务包括 text-to-code、image-to-code、code-to-image，以及 text+image-to-code 这类组合查询。
- 它训练了 **CodeMMR**，这是一个单一检索器，以预训练视觉语言模型为初始化基础，并进一步适配，使其能够把文本、代码和图像编码到共享语义空间中。
- 每个查询都包含一条说明检索意图的指令，例如检索与某张图像匹配的代码。模型对“查询+指令”进行嵌入，再与候选目标进行匹配。
- 训练使用对比式 InfoNCE 目标：匹配的查询-目标对被拉近，batch 内负样本和困难负样本被推远。
- 这一设计的目标是在模态、编程语言以及编辑和修复任务中未见过的检索设定之间实现泛化。

## 结果
- 在 **MMCoIR** 上，**CodeMMR (2B)** 的 **平均 nDCG@10 为 68.0**，高于 **VLM2Vec-v2 (2B)** 的 **58.0**、**GME (7B)** 的 **53.8** 和 **GME (2B)** 的 **51.5**。摘要称，相比 UniIR、GME 和 VLM2Vec 等强基线，平均提升约 **10 个绝对 nDCG@10 点数**。
- 在 MMCoIR 的 **Hit@1** 指标上，**CodeMMR (2B)** 的 **平均值达到 65.4**，高于 **VLM2Vec-v2 (2B)** 的 **53.3** 和 **GME (7B)** 的 **49.5**。
- 各数据集上的强结果包括：在 **Chart2Code image-to-code** 上 **99.8 nDCG@10**，在 **Web2Code image-to-code** 上 **98.6**，在 **DATIKZv3 code-to-image / image-to-code** 上 **97.8/97.0**，以及在 **PlantUML code-to-image / image-to-code** 上 **100.0/100.0**。
- 在以 SVG 为主的设定中，任务仍然很难：在 **MMSVG** 上，CodeMMR 在列出的检索方向上的 **nDCG@10** 分别为 **11.2**、**12.3**、**9.4** 和 **58.2**。这些结果仍明显好于若干基线，但远低于它在 WebUI、图表和 UML 上的分数。
- 在结合检索的下游生成任务中，论文称在未见过的 image-to-code 任务上取得提升：与不使用检索的基线相比，**ChartMimic Direct** 的 **Execution Rate 提高 +10.0 点**，**WebCode2M-Mid** 的 **Visual Accuracy 提高 +9.4 点**；同时也超过了使用基线检索器的 RAG 系统。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15663v1](http://arxiv.org/abs/2604.15663v1)
