---
source: arxiv
url: https://arxiv.org/abs/2606.03618v1
published_at: '2026-06-02T13:17:45'
authors:
- Mehmet Utku Colak
topics:
- code-agents
- prompt-compression
- multilingual-code
- local-llm
- context-optimization
- software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Cross-Lingual Token Arbitrage: Optimizing Code Agent Context Windows via Local LLM Preprocessing

## Summary
本文提出一种本地预处理重写器，在多语言代码代理提示词发送到云模型之前先降低成本。在 OMH-Polyglot 上，它把提示 token 减少了 34–47%，并且在 gpt-3.5-turbo、gpt-4o 和 gemini-2.5-flash-lite 上保持或提升了准确率。

## Problem
- 在常见 LLM 分词器下，非英语开发者提示词可能比等价的英语提示词多用 2–3 倍 token，这会在模型开始处理任务前就抬高 API 成本。
- 对话式提示词会加入填充内容和松散结构，可能让代码代理检索过多上下文，并生成更长的回答。
- 现有提示词压缩方法通常在提示词已经变大后才处理，或者需要额外的云端调用，因此无法在边缘侧消除 token 成本。

## Approach
- 一个 TypeScript 网关会在每次 IDE 或基准查询发送到云端前拦截它。
- 一个通过 Ollama 运行的本地 Llama 3.2 3B 模型会把非英语文本翻译成英语，去掉填充内容，并把请求重写成紧凑的 [CONTEXT]/[TASK] 格式。
- [TASK] 块保留必需的函数名，并逐字复制 Python assert 行，因此云模型仍然能看到可执行的评分约束。
- 一个正则验证器会拒绝空输出、泄漏的代码块、格式错误的分段和其他错误重写，并最多重试两次修复。
- 一个 token 预算保护会在重写结果没有至少缩小 5% 时转发原始提示词，从而避免云端计费 payload 变大。

## Results
- OMH-Polyglot 包含 200 个编码任务，规格分别使用土耳其语、阿拉伯语、中文和代码混合文本；其平均 token 化开销比为 2.05x，p90 为 4.02x，最差情况为 6.15x。
- 在 gpt-3.5-turbo 上，prompt tokens 从 53,713 降到 28,661，total tokens 从 94,338 降到 86,474（-8.3%），准确率保持在 99.50%。
- 在 gpt-4o 上，prompt tokens 从 43,565 降到 28,776，total tokens 从 139,085 降到 127,594（-8.3%），准确率从 98.33% 升到 99.50%；论文说这个准确率变化在运行级波动范围内。
- 在 gemini-2.5-flash-lite 上，prompt tokens 从 44,918 降到 29,398，total tokens 从 116,653 降到 94,725（-18.8%），准确率从 95.00% 升到 98.00%。
- 在相同压缩率下对比 LLMLingua-2 时，该方法在三个后端上的 OckScore 都更高：gpt-3.5-turbo 上是 99.08 对 76.91，gpt-4o 上是 98.88 对 96.56，gemini-2.5-flash-lite 上是 97.54 对 33.85。
- 美元成本变化因后端而异：gpt-3.5-turbo 上为 +15.1%，gpt-4o 上为 -0.4%，gemini-2.5-flash-lite 上为 -12.4%；输出 token 定价抵消了部分输入 token 节省。

## Link
- [https://arxiv.org/abs/2606.03618v1](https://arxiv.org/abs/2606.03618v1)
