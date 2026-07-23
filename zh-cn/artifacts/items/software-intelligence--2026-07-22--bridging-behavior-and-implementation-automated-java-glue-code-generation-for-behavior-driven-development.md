---
source: arxiv
url: https://arxiv.org/abs/2607.19703v1
published_at: '2026-07-22T03:06:45'
authors:
- Xinyu Shi
- Zhou Yang
- An Ran Chen
topics:
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- behavior-driven-development
- code-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development

## Summary
## 总结
AutoGlue 通过结合场景级行为解释，以及从相关 BDD 工件和目标项目代码库中进行检索，生成 Java BDD 胶水代码。在来自 8 个开源 Java 项目的 1,307 个步骤上，它优于提示基线，并为 46.1% 的步骤生成了可直接使用的代码。

## 问题
- BDD 场景使需求变得可执行，但开发者仍需手动通过胶水代码，将每个自然语言步骤连接到项目 API。
- 这一任务之所以重要，是因为步骤通常描述不充分，相关实现细节分散在大型代码库中，而需求变更也使胶水代码的创建和维护需要大量工作。

## 方法
- AutoGlue 采用分层多智能体工作流，包括三个阶段：行为解释、上下文检索和胶水代码生成。
- Behavior Interpreter 根据步骤所在的特性和场景确定步骤意图，而不是孤立地处理该步骤。
- Developer agent 协调独立的 BDD Context Retriever 和 Project Context Retriever agent，查找相似步骤、现有胶水代码，以及相关的 Java 类、方法和 API。
- 最终生成器结合解释后的行为和检索到的项目上下文生成 Java 胶水代码，其中包括特定于框架的注解、参数和项目调用。

## 结果
- 评估使用了来自 8 个开源 Java 项目的 1,307 个步骤—胶水代码对。
- 与少样本提示相比，AutoGlue 将 API F1 提高了 58.7%，将 CodeBLEU 提高了 43.7%；论文还报告称，其性能持续优于普通提示方法。
- 基于 LLM-as-a-Judge 的评估发现，46.1% 的生成实现无需修改即可直接使用。
- 大多数部分正确的输出只需进行小幅编辑，尤其是补充缺失的操作或优化参数。
- 消融实验表明，行为解释和面向项目的上下文检索分别显著提升了生成质量，但基于执行的验证受到环境依赖以及缺乏可靠的步骤级预言机的限制。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19703v1](https://arxiv.org/abs/2607.19703v1)
