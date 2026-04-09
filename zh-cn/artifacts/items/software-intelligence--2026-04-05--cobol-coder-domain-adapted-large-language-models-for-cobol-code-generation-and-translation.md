---
source: arxiv
url: http://arxiv.org/abs/2604.03986v1
published_at: '2026-04-05T06:12:49'
authors:
- Anh T. V. Dau
- Shin Hwei Tan
- Jinqiu Yang
- Nghi D. Q. Bui
- Anh Tuan Nguyen
topics:
- cobol-code-generation
- legacy-language-llm
- code-translation
- domain-adaptation
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation

## Summary
## 摘要
COBOL-Coder 是一个面向 COBOL 的专用 LLM，通过在整理后的真实 COBOL 代码、合成翻译数据和 COBOL 文档混合数据上微调 Qwen2.5-Coder 得到。论文称，它在 COBOL 代码生成和 COBOLJava 翻译上，相比通用模型和开源基线有明显提升，并且在有经验的 COBOL 开发者评价中表现更好。

## 问题
- 现有 LLM 在常见编程语言上表现较好，但在 COBOL 上表现较差，尽管 COBOL 仍在银行、保险和政府等关键系统中运行。
- 公开的 COBOL 数据稀缺、噪声大，而且常常无法编译，这使领域适配更困难，也让现有基准覆盖面较窄。
- 这会影响代码生成和现代化任务，例如 COBOL 与 Java 之间的双向翻译；模型表现弱会拖慢遗留系统的维护和迁移。

## 方法
- 作者构建了一条 COBOL 训练数据流水线，包含三类数据源：公开 GitHub COBOL 文件、合成的 JavaCOBOL 翻译数据，以及 COBOL/主机文档。
- 他们使用基于 GnuCOBOL 的编译器闭环验证和基于 GPT-4o 的修复，把带噪声的 COBOL 文件和翻译程序处理成可编译样本；在清洗后的 40,829 个 GitHub 文件中，保留了 31,492 个可编译程序。
- 对于合成数据，他们先将 Stack-v2-dedup-Java 中的 Java 代码翻译为 COBOL，再用两步检查过滤数据对：阈值为 0.6 的 LLM 相似度打分，以及回译结合 AST/CodeBERTScore、阈值为 0.7 的过滤。最终得到 173,042 个通过验证的翻译数据对和 172,759 个描述代码数据对。
- 他们将代码和文档转换为指令微调数据，然后将 Qwen2.5-Coder 7B 和 14B 微调为 COBOL-Coder。论文还提出了 COBOL-JavaTrans，一个用于 COBOLJava 双向翻译的基准。

## 结果
- 在 COBOLEval 代码生成任务上，COBOL-Coder-14B 的编译成功率达到 73.95%，Pass@1 为 49.33；GPT-4o 分别为 41.8% CSR 和 16.4 Pass@1。
- 在同一任务上，COBOL-Coder-7B 达到 73.80% CSR 和 44.70 Pass@1。论文称，大多数开源基线，如 CodeGemma、CodeLlama、StarCoder2 和 DeepSeek-R1-Distill-Qwen，在 COBOLEval 和 COBOLCodeBench 上的 CSR 和 Pass@1 都为 0%。
- 在 COBOLCodeBench 上，COBOL-Coder-14B 是唯一一个报告了非零表现的模型：26.09% CSR 和 4.35 Pass@1。
- 在 COBOL-JavaTrans 的 COBOL 到 Java 翻译任务上，COBOL-Coder 的 CSR 达到 97.9%，Pass@1 最高为 83.91。论文称这一结果接近规模大得多的通用 LLM。
- 在 Java 到 COBOL 翻译任务上，COBOL-Coder-7B 达到 63.64% CSR 和 27.27 Pass@1，COBOL-Coder-14B 达到 72.03% CSR 和 34.93 Pass@1；论文称通用 LLM 在这个方向上的得分接近 0。
- 在开发者研究中，有经验的 COBOL 开发者在所有 Java-to-COBOL 任务上都将 COBOL-Coder 排名第一；在大多数 COBOL 生成任务上，它排名第一或并列第一。摘录未提供具体调查分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03986v1](http://arxiv.org/abs/2604.03986v1)
