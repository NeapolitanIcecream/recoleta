---
source: arxiv
url: https://arxiv.org/abs/2607.19104v1
published_at: '2026-07-21T13:46:52'
authors:
- Weifeng Sun
- Ye Fan
- Yuchen Chen
- Gou Tan
- Jieke Shi
- Yuan Yidi
- Swee Liang Wong
- Jonathan Pan
- David Lo
topics:
- scientific-code-generation
- code-benchmarks
- executable-evaluation
- code-pretraining
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# SciCodePile: A 128GB Corpus and Executable Benchmark for Challenging Scientific Code Generation

## Summary
## 摘要
SciCodePile 将来自 37,737 个代码仓库的 125GB 科学代码语料库，与一个包含 200 个任务、用于测试功能正确性的可执行基准相结合。评估结果表明，科学代码生成仍然困难，而在该语料库上进行持续预训练和指令微调能够显著提升性能。

## 问题
- 通用代码生成基准无法充分测试科学软件；科学软件需要领域特定语义、数值推理、依赖处理和可运行的实现。
- 现有科学代码资源通常只提供小规模评测套件或特定领域语料库，仓库级上下文和可执行验证能力有限。

## 方法
- 使用 198 个科学领域种子关键词在 GitHub 上进行爬取，将其扩展为 213 个查询；随后进行质量筛选和基于 LLM 的相关性筛选，最终从 1,311,568 个候选仓库中保留 37,737 个。
- 构建四种对齐格式：125GB 去重代码文件、37,737 个 README 摘要、500,000 个函数级指令实例，以及 20,000 个问题—解答对。
- 从相关 Python 函数中生成 200 个 HumanEval 风格任务，合成沙箱环境和测试，并仅保留能够成功执行的实例；每个测试套件平均包含 7.3 个断言。
- 在前缀到后缀补全、填空式补全和可执行指令跟随生成三项任务上，评估 15 个开源和闭源 LLM。

## 结果
- 最佳 CodeBLEU 分数分别为：前缀补全 38.13，填空式补全 38.37。
- 在包含 200 个任务的可执行基准上，最强模型的 Pass@1 达到 12.30%，Pass@5 达到 15.50%，表明文本上看似合理的代码与功能正确的科学代码之间仍存在显著差距。
- 在 SciCodePile 上对 GPT-2 (124M) 进行持续预训练，使科学代码补全的 CodeBLEU 提升 2.84 倍。
- 在构建的指令数据上对 Qwen2.5-Coder-0.5B 进行指令微调，使可执行任务的 Pass@1 提升 4.79 倍，从 1.90% 提高到 9.10%。
- 该基准有意限制在带有存根依赖的纯 Python 函数，因此其可执行评测结果不能完全代表多文件项目或生产环境中的科学工作流。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19104v1](https://arxiv.org/abs/2607.19104v1)
