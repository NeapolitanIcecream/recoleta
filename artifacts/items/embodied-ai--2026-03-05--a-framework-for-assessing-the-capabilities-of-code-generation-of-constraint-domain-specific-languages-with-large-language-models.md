---
source: arxiv
url: http://arxiv.org/abs/2603.05278v1
published_at: '2026-03-05T15:23:02'
authors:
- David Delgado
- "Lola Burgue\xF1o"
- "Robert Claris\xF3"
topics:
- llm-code-generation
- domain-specific-languages
- constraint-languages
- evaluation-framework
- prompt-engineering
relevance_score: 0.08
run_id: materialize-outputs
---

# A framework for assessing the capabilities of code generation of constraint domain-specific languages with large language models

## Summary
本文提出了一个用于评估大语言模型从文本规格生成约束类领域专用语言代码能力的通用框架，重点覆盖 OCL 与 Alloy，并与 Python 进行对比。结论是：LLM 在主流语言上明显更强，而在低资源约束 DSL 上更容易失败，但多次采样和代码修复能带来改进。

## Problem
- 论文要解决的问题是：**如何系统评估 LLM 生成低资源约束 DSL 代码的能力**，而不仅是看热门通用语言的表现。
- 这很重要，因为 OCL、Alloy 这类约束语言用于**精确表达系统约束、验证和测试**，但训练数据少、依赖领域模型、且难以直接执行，导致现有代码生成评测方法不够适用。
- 约束 DSL 的额外难点包括：需要同时理解**约束文本和其所在领域模型**、语言偏声明式、以及多个约束可能全局交互。

## Approach
- 提出一个**模块化评估框架**，把流程拆成四步：构造提示、调用 LLM 生成代码、检查代码是否良构、再检查代码是否正确。
- 框架支持多种输入组合：**领域描述、领域模型或两者同时提供**；也支持不同提示模板、任务组织方式和多次生成。
- 设计了 **9 种 prompt templates**，覆盖是否提供自然语言领域描述、形式化/自然语言领域模型，以及是否让 LLM 先解释或生成领域模型。
- 对不良构代码，框架加入**单轮代码修复**：把错误代码和解析/编译错误信息再交给 LLM，让它解释问题并修复代码。
- 用该框架实例化评测 **OCL、Alloy 和 Python**，并比较 **DeepSeek-coder、GPT-4o、GPT-4o-mini、Llama 3.1** 等模型；论文称实验配置总数**超过 90k**。

## Results
- 论文的核心结论是：**LLM 在 Python 上总体优于 OCL 和 Alloy**，说明低资源 DSL 的代码生成显著更难。
- 论文明确指出：**上下文窗口较小的模型**（如部分开源 LLM）可能**无法生成约束相关代码**，因为这类任务需要同时容纳约束描述与领域模型。
- **多次尝试（multiple attempts）** 能提升至少一次生成出正确代码的概率，对应提升 **pass@k**；论文将其作为有效改进手段之一，但摘录中**未给出具体数值**。
- **代码修复（code repair）** 也能提升生成质量，尤其对先生成出不良构代码的情况有帮助；摘录中**未给出修复前后精确提升百分比**。
- 相比之下，**prompt template 的选择影响较小**，至少不如多次采样和修复策略重要；摘录中**未给出不同模板间的量化差值**。
- 可量化的最强具体声明包括：框架覆盖 **3 种语言（OCL、Alloy、Python）**、评测 **4 个 LLM**、探索 **超过 90,000 种配置**；但当前提供的摘录**没有报告最终准确率/pass@k 等具体实验数字**。

## Link
- [http://arxiv.org/abs/2603.05278v1](http://arxiv.org/abs/2603.05278v1)
