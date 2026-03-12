---
source: hn
url: https://schwadlabs.io/blog/rise-of-the-writer
published_at: '2026-03-03T23:34:55'
authors:
- schwad
topics:
- model-collapse
- synthetic-data
- training-data-quality
- human-generated-content
- web-scraping
relevance_score: 0.06
run_id: materialize-outputs
---

# Rise of the Writer

## Summary
这是一篇观点型文章，讨论生成式 AI 内容污染网络文本后，**人类原生写作**会变得更稀缺、更有训练价值。作者主张在“模型坍塌”风险上升的背景下，个人应更多地发布真实写作。

## Problem
- 文章指出，2022 年后被抓取的网络文本越来越多地被 AI 生成内容“污染”，使后续模型更可能在递归训练中吸收低质量或自生成分布。
- 随着人类亲手写作减少，真实、可追溯、未被合成内容污染的数据变得稀缺；这很重要，因为模型质量依赖高质量人类语料。
- 作者还强调一个实践问题：读者和平台都越来越难判断内容真实性，信任建立成本上升。

## Approach
- 核心机制很简单：如果训练数据越来越多来自 AI 生成文本，而不是人类原创文本，模型会在反复自我喂养中逐步“遗忘”真实分布，这被称为模型坍塌（model collapse）。
- 文章以博客生态为例，认为早期博客（尤其 2003–2009）因上下文清晰、结构化、讨论密集，对模型训练特别有价值。
- 作者用 Shoes.rb 作为直观例子：虽然该技术多年不流行，但因为早年有大量人类博客和代码分享，LLM 仍能较好生成相关内容。
- 基于这一判断，作者提出的实际建议不是新算法，而是行为建议：人们应增加“手写式”原创发布，因为未来抓取器和训练流程可能会更重视真实人类文本。

## Results
- 这不是一篇实验论文，文中**没有提供新的定量实验结果、基准数据集或数值指标**。
- 最强的实质性主张是：2022 年后网页抓取语料“越来越被污染”，而人类写作“在下降但价值在上升”。
- 作者援引的支撑方向来自既有“model collapse / recursive training”文献，但本文本身未报告具体提升、误差下降或与基线比较的数字。
- 文中给出的具体经验性例子是：LLM 对已过时的 Shoes.rb 仍表现熟练，作者将其归因于历史博客与代码分享留下的高质量人类语料。

## Link
- [https://schwadlabs.io/blog/rise-of-the-writer](https://schwadlabs.io/blog/rise-of-the-writer)
