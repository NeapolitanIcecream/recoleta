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
## 总结
CodeMMR 是一个多模态代码检索器，把自然语言、代码和图像放进同一个嵌入空间里，这样同一个模型就能跨三种模态检索。论文还引入了用于这一设定的基准 MMCoIR，并表明常见的多模态检索器会遗漏代码工件中的大量视觉含义。

## 问题
- 现有代码检索模型大多把代码当作文本处理，忽略了与代码相关的视觉输出，例如网页、图表、SVG、示意图和 UML。
- 这会影响代码搜索和代码 RAG，因为开发者常常需要从图像检索代码、从代码检索图像，或在编辑和生成代码时同时结合文本和视觉信息。
- 在这项工作之前，还没有一个覆盖领域、语言和检索方向的广泛多模态多语言代码检索基准。

## 方法
- 论文构建了 **MMCoIR**，覆盖 5 个视觉领域、8 种编程语言和 11 个库，任务包括文本到代码、图像到代码、代码到图像，以及文本+图像到代码这类组合查询。
- 论文训练了 **CodeMMR**，这是一个单一检索器，以预训练视觉语言模型初始化，并调整为把文本、代码和图像编码到共享语义空间。
- 每个查询都带有一条说明检索意图的指令，例如检索与图像匹配的代码。模型把查询和指令一起编码，再与候选目标进行匹配。
- 训练使用对比式 InfoNCE 目标：匹配的查询-目标对会被拉近，批内负样本和难负样本会被推远。
- 这种设计旨在跨模态、跨编程语言，以及编辑和修复任务中使用的未见检索设置泛化。

## 结果
- 在 **MMCoIR** 上，**CodeMMR (2B)** 的 **nDCG@10 平均值为 68.0**，超过了 **VLM2Vec-v2 (2B)** 的 **58.0**、**GME (7B)** 的 **53.8** 和 **GME (2B)** 的 **51.5**。摘要还说，它比 UniIR、GME 和 VLM2Vec 等强基线平均高出约 **10 个绝对 nDCG@10 点**。
- 在 MMCoIR 的 **Hit@1** 上，**CodeMMR (2B)** 的 **平均值为 65.4**，高于 **VLM2Vec-v2 (2B)** 的 **53.3** 和 **GME (7B)** 的 **49.5**。
- 单个数据集上的高分包括：**Chart2Code** 图像到代码的 **99.8 nDCG@10**、**Web2Code** 图像到代码的 **98.6**、**DATIKZv3** 代码到图像 / 图像到代码的 **97.8/97.0**，以及 **PlantUML** 代码到图像 / 图像到代码的 **100.0/100.0**。
- 在 SVG 密集场景下，任务仍然很难：在 **MMSVG** 上，CodeMMR 在列出的检索方向中报告了 **11.2、12.3、9.4 和 58.2 nDCG@10**。这些结果仍然明显优于若干基线，但远低于它在 WebUI、图表和 UML 上的分数。
- 在带检索的下游生成任务上，论文声称在未见过的图像到代码任务中有提升：在 **ChartMimic Direct** 上 **Execution Rate 提高 10.0 个点**，在 **WebCode2M-Mid** 上 **Visual Accuracy 提高 9.4 个点**，相对于一个不带检索的基线，同时也超过了使用基线检索器的 RAG 系统。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15663v1](http://arxiv.org/abs/2604.15663v1)
