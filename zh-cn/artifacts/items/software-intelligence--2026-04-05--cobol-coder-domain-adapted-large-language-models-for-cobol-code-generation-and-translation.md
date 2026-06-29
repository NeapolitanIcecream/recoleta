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
COBOL-Coder 是一个面向 COBOL 的专用大语言模型，通过在真实 COBOL 代码、合成翻译数据和 COBOL 文档的整理数据上微调 Qwen2.5-Coder 构建而成。论文称，它在 COBOL 代码生成和 COBOL\u000bJava 翻译上，相比通用模型和开源基线有明显提升，经验丰富的 COBOL 开发者也给出更高评价。

## 问题
- 现有大语言模型在常见语言上表现不错，但在 COBOL 上表现很差，而 COBOL 仍然运行着银行、保险和政府中的关键系统。
- 公开 COBOL 数据稀缺、噪声大，而且常常无法编译，这让领域适配很难，也让现有基准的覆盖面很窄。
- 这会影响代码生成和现代化任务，比如在 COBOL 和 Java 之间翻译；模型表现弱会拖慢遗留系统的维护和迁移。

## 方法
- 作者构建了一个 COBOL 训练流水线，数据来自三部分：公开 GitHub COBOL 文件、合成的 Java\u000bCOBOL 翻译，以及 COBOL/主机文档。
- 他们用编译器在环验证配合 GnuCOBOL 和基于 GPT-4o 的修复，把有噪声的 COBOL 文件和翻译程序整理成可编译样本；在 40,829 个清洗后的 GitHub 文件中，保留了 31,492 个可编译程序。
- 对合成数据，他们把 Stack-v2-dedup-Java 中的 Java 翻译成 COBOL，然后用两道检查过滤配对：阈值为 0.6 的 LLM 相似度评分，以及带有回译和 AST/CodeBERTScore 过滤、阈值为 0.7 的检查。这样得到 173,042 对已验证翻译配对和 172,759 对描述\u000b代码配对。
- 他们把代码和文档转换成指令微调数据，再把 Qwen2.5-Coder 7B 和 14B 微调成 COBOL-Coder。论文还引入了 COBOL-JavaTrans，一个用于双向 COBOL\u000bJava 翻译的基准。

## 结果
- 在 COBOLEval 代码生成任务上，COBOL-Coder-14B 的编译成功率达到 73.95%，Pass@1 为 49.33；GPT-4o 分别是 41.8% 和 16.4。
- 在同一任务上，COBOL-Coder-7B 的编译成功率是 73.80%，Pass@1 是 44.70。论文说，大多数开源基线，如 CodeGemma、CodeLlama、StarCoder2 和 DeepSeek-R1-Distill-Qwen，在 COBOLEval 和 COBOLCodeBench 上的 CSR 和 Pass@1 都是 0%。
- 在 COBOLCodeBench 上，COBOL-Coder-14B 是唯一一个报告出非零且有一定意义表现的模型：CSR 26.09%，Pass@1 4.35。
- 在 COBOL-JavaTrans 的 COBOL-to-Java 翻译任务上，COBOL-Coder 的 CSR 最高达到 97.9%，Pass@1 最高达到 83.91；论文说这已经接近更大的通用大语言模型。
- 在 Java-to-COBOL 翻译任务上，COBOL-Coder-7B 的 CSR 为 63.64%，Pass@1 为 27.27；COBOL-Coder-14B 的 CSR 为 72.03%，Pass@1 为 34.93。论文说，通用大语言模型在这个方向上的分数接近于零。
- 在开发者研究中，有经验的 COBOL 开发者把 COBOL-Coder 在所有 Java-to-COBOL 任务上排第一，并在大多数 COBOL 生成任务上排第一或并列第一。摘要片段没有给出具体的调查分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03986v1](http://arxiv.org/abs/2604.03986v1)
