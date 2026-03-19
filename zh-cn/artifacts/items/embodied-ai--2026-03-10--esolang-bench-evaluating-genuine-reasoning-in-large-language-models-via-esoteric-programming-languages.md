---
source: arxiv
url: http://arxiv.org/abs/2603.09678v1
published_at: '2026-03-10T13:47:15'
authors:
- Aman Sharma
- Paras Chopra
topics:
- llm-evaluation
- ood-generalization
- code-generation
- benchmarking
- reasoning
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# EsoLang-Bench: Evaluating Genuine Reasoning in Large Language Models via Esoteric Programming Languages

## Summary
EsoLang-Bench 用五种极少出现在预训练数据中的深奥编程语言，测试大语言模型是否真的会“推理”，而不只是背熟常见代码模式。论文显示：在主流代码基准上接近天花板的模型，到了这些真正分布外任务上几乎全面失效。

## Problem
- 论文要解决的问题是：现有代码生成基准是否高估了 LLM 的真实推理能力，因为高分可能主要来自训练数据记忆、污染和模式匹配。
- 这很重要，因为如果模型只会在高频语言和常见题型上“套模板”，那么它们的泛化、测试时学习和真实智能都被误判了。
- 作者希望构造一个污染风险低、几乎没有“刷榜激励”的基准，专门测可迁移的计算推理能力。

## Approach
- 提出 **EsoLang-Bench**：包含 **80** 道与语言无关的算法题，分成 **4** 个难度层级；在 **5** 种深奥语言上评测，形成 **400** 个 problem-language 组合。
- 选择 **Brainfuck、Befunge-98、Whitespace、Unlambda、Shakespeare** 五种图灵完备但训练数据极稀缺的语言；其公开仓库数量相比 Python 少 **1,000–100,000×**，图中还给出约 **5,000×** 的数量级差距。
- 评测 **5** 个前沿模型，并比较 **5** 种提示/脚手架策略：zero-shot、few-shot、self-scaffolding、textual self-scaffolding、ReAct；同时还考察带工具的 agentic coding 系统。
- 核心机制很简单：把与 Python 等价的基础算法题换到几乎没见过的新语言里，再给文档、解释器反馈和迭代机会，看模型能不能像人一样现学现用。
- 通过解释器执行和 **6** 个测试用例精确匹配来判定是否解题成功，从而尽量把“会说”与“真会做”区分开。

## Results
- 论文最核心的结果是巨大能力落差：在标准代码基准上常见的 **85–95%** 水平，在等价的深奥语言任务上只剩 **0–11%**。
- 摘要称前沿模型在该基准上的总体成绩只有 **0–11%**，且 **Easy 以上难度全部为 0%**；表 2 也明确写到 **Medium/Hard/Extra-Hard = 0%**。
- 图 1 显示，跨五种语言和多种策略的平均准确率中，最好的 self-scaffolding 配置下 **GPT-5.2 仅 6.2%**，且“所有模型即便用高级脚手架也都低于 **7%**”。
- 图 2 进一步给出等价 Python 对比：**最佳模型仅 3.8%（GPT-5.2） vs 等价 Python 任务 100%**。
- few-shot 和 self-reflection 类方法基本没有带来显著提升；作者据此主张，ICL 在这类 OOD 任务上的效果依赖预训练覆盖，而不代表真实的快速学习能力。
- 错误分析称 **59%** 的失败属于编译错误，说明模型首先卡在最基本的语法和执行层面，而不是高层算法构思。

## Link
- [http://arxiv.org/abs/2603.09678v1](http://arxiv.org/abs/2603.09678v1)
