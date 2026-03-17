---
source: arxiv
url: http://arxiv.org/abs/2603.09678v1
published_at: '2026-03-10T13:47:15'
authors:
- Aman Sharma
- Paras Chopra
topics:
- code-benchmark
- ood-generalization
- reasoning-evaluation
- esoteric-languages
- code-generation
relevance_score: 0.87
run_id: materialize-outputs
---

# EsoLang-Bench: Evaluating Genuine Reasoning in Large Language Models via Esoteric Programming Languages

## Summary
本文提出 **EsoLang-Bench**，用五种极少出现在训练语料中的深奥编程语言来测试大模型是否具备可迁移的真实编程推理，而不是依赖记忆与基准污染。结果显示，在主流代码基准上接近天花板的模型，到了这些等价但强OOD的任务上几乎全面失效。

## Problem
- 现有代码生成基准（如 HumanEval、MBPP）越来越可能高估能力，因为高分可能来自训练数据记忆、污染或模式匹配，而不是真正的算法推理。
- 研究要解决的问题是：如何构造一个**低污染、低游戏化激励、仍要求相同计算原语**的评测，来分离“检索/记忆”与“可迁移推理”。
- 这很重要，因为如果模型只会在高覆盖训练分布内表现好，就难以支撑软件基础模型、自动化软件生产和新环境下的可靠代码智能。

## Approach
- 作者构建 **EsoLang-Bench**：80 个语言无关的编程题，分 4 个难度层级，映射到 5 种深奥语言（Brainfuck、Befunge-98、Whitespace、Unlambda、Shakespeare），共形成 400 个评测实例。
- 核心机制很简单：题目本身与 Python 中的基础算法题等价，但表达语言换成训练数据极稀缺的 esolang；如果模型还能做好，更可能说明它真的理解了循环、状态、条件和算法，而不是背过模板。
- 这些语言被选中是因为既**图灵完备**、又与主流语言共享计算本质，同时公开仓库数量比 Python 少 **1,000–100,000×**，从而显著降低预训练覆盖和污染概率。
- 评测覆盖 5 个前沿模型与 5 种提示/脚手架策略，包括 zero-shot、few-shot、self-scaffolding、textual self-scaffolding、ReAct，并用解释器执行与 6 个测试用例做自动验证。
- 作者还强调允许文档阅读、解释器反馈和迭代修正，以更接近“人类学习一门新语言”的过程，并检验测试时学习是否真的存在。

## Results
- 论文声称主流代码基准上前沿模型通常可达 **85–95%**，但在等价的 esolang 任务上仅有 **0–11%**，出现巨大能力断层。
- 从表 2 看，**few-shot 仍几乎无效**：例如 GPT-5.2 在 Brainfuck 上 **2.5%→2.5%**，Befunge-98 上 **2.5%→8.8%**，Whitespace 和 Unlambda 都是 **0%**；说明 ICL 对强OOD语言迁移帮助非常有限。
- 按论文摘要与表注，**Easy 以上难度全部为 0%**：所有 **Medium/Hard/Extra-Hard = 0%**，即模型在稍复杂算法任务上完全无法跨语言迁移。
- 单看 zero-shot / 3-shot 表，最佳语言-模型结果只有个位数：O4-mini 在 Befunge-98 zero-shot **6.2%**、few-shot **7.5%**；GPT-5.2 在 Befunge-98 few-shot **8.8%**；多数模型在 Whitespace、Unlambda 上长期 **0%**。
- 图 1 给出的跨五种语言平均准确率中，**Self-Scaffolding 最好也只有 6.2%（GPT-5.2）**，且“所有模型即使用高级脚手架也都 **低于 7%**”。
- 图 2 进一步给出一个更强对比：最佳模型在 esolang 上仅 **3.8%**，而在**等价 Python 问题上为 100%**；作者还报告错误分析中**59% 为编译错误**，表明首先卡在语法与表示层，而非仅仅是高层算法构思。

## Link
- [http://arxiv.org/abs/2603.09678v1](http://arxiv.org/abs/2603.09678v1)
