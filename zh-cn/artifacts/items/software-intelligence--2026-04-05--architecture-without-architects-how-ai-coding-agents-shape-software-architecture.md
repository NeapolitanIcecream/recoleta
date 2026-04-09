---
source: arxiv
url: http://arxiv.org/abs/2604.04990v1
published_at: '2026-04-05T07:32:37'
authors:
- Phongsakon Mark Konrad
- Tim Lukas Adam
- Riccardo Terrenzi
- Serkan Ayvaz
topics:
- ai-coding-agents
- software-architecture
- prompt-engineering
- code-generation
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Architecture Without Architects: How AI Coding Agents Shape Software Architecture

## Summary
## 摘要
这篇立场论文认为，AI 编码代理已经在做软件架构决策，而且这些决策往往没有经过评审，也没有记录决策依据。论文提出了一个模型来说明提示词如何驱动基础设施选择，并通过一个小型案例研究展示：仅仅改变提示词表述，就会产生不同的系统架构。

## 问题
- 论文研究了编码代理在生成代码时如何选择框架、数据库、集成方式和任务拆分策略，即使团队并未把这些选择当作架构决策来对待。
- 这件事重要，因为这些决策发生很快，通常成套出现，而且往往没有 ADR、设计文档或评审记录，这会带来治理、安全和维护风险。
- 论文还认为，结构化输出、工具访问和检索需求等提示词特征会强制引入额外基础设施，因此提示词本身可以充当一种架构规格。

## 方法
- 作者通过梳理编码工具，归纳出代理驱动架构选择的 **五种机制**：模型选择、任务分解、默认配置、脚手架/自主生成，以及集成协议。
- 他们提出了 **六种提示词-架构耦合模式**，分为约束、能力和上下文三类：结构化输出、few-shot 选择、函数调用、ReAct 推理、RAG 和上下文压缩。
- 他们将这些耦合分为 **偶然型** 和 **基础型**：如果模型能力增强后额外基础设施需求可能减少，则属于前者；如果基础设施在逻辑上就是必需的，例如工具编排，则属于后者。
- 他们进行了一个说明性案例研究：使用默认设置的 Claude Code 独立生成三个客服聊天机器人变体，运行时模型固定为 GPT-4o-mini，只改变提示词表述。
- 他们用这个案例追踪提示词具体程度如何改变组件、依赖和故障模式，然后讨论评审实践、ADR 自动生成和具备架构感知能力的治理工具。

## 结果
- 最主要的具体结果是：在同一任务上，仅因提示词表述不同就出现了架构分化。变体 A（“根据 FAQ 回答产品问题”）生成了 **141 LoC, 2 files**；变体 B（结构化 JSON 加 schema validation）生成了 **472 LoC, 4 files**；变体 C（工具访问）生成了 **827 LoC, 6 files**。
- 与变体 A 相比，最复杂的变体代码规模增加了约 **5.9x**（**141 → 827 LoC**），文件数量增加了 **3x**（**2 → 6 files**）。
- 结构化输出引入了更简单提示词中没有的具体组件：**Zod schema、retry handler、fallback generator**。工具访问则增加了 **tool registry、agent loop、SQLite state store**。
- 论文提出了 **五种代理决策机制** 和 **六种重复出现的耦合模式**，但这些是分析性贡献，不是经过实证验证的基准结果。
- 论文**没有提供定量的准确率或基准测试结果**，也没有数据集上的任务成功率，或与人工设计架构、其他代理等基线的对比。证据主要来自工具梳理和一个单独的说明性案例研究。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04990v1](http://arxiv.org/abs/2604.04990v1)
