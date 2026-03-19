---
source: hn
url: https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai
published_at: '2026-03-08T23:52:42'
authors:
- walterbell
topics:
- prompt-engineering
- ai-agents
- llm-agents
- meta-prompting
- evaluation
- tool-use
relevance_score: 0.12
run_id: materialize-outputs
language_code: zh-CN
---

# State-of-the-Art Prompting for AI Agents (2025)

## Summary
这是一篇关于构建 AI agent 的提示工程实践总结，而不是严格意义上的学术论文。它整理了多种被业界团队采用的 prompting 技巧，目标是提升代理系统的可靠性、可控性与可调试性。

## Problem
- 它试图解决 AI agents 在复杂任务中**不稳定、易幻觉、输出不一致、难调试**的问题。
- 这很重要，因为 agent 往往要执行多步流程、调用工具、生成结构化输出；如果提示设计不好，系统就会频繁出错或难以上线。
- 文本还强调：单靠 prompt 不够，**评测集（evals）** 才是持续迭代和判断效果的关键资产。

## Approach
- 核心方法很简单：把 LLM 当成“新员工”管理，给它**非常具体、详细、结构化**的指令，明确角色、任务、约束和输出格式。
- 使用**角色设定**与**步骤化任务分解**，让模型知道“自己是谁”“要做什么”“按什么流程做”。
- 用 **Markdown / XML-like tags** 约束输出结构，例如为工具调用审核定义固定标签，提升机器可读性与一致性。
- 通过**few-shot 示例、meta-prompting、动态子提示生成**来适配复杂场景：先给示例，再让模型帮助改 prompt，甚至在多阶段工作流中按上下文生成后续专用 prompt。
- 加入**escape hatch、debug info/thinking traces、evals 驱动迭代、模型个性与蒸馏**，以减少幻觉、提升可调试性，并在质量与成本之间折中。

## Results
- 文本**没有提供系统性的实验设计或基准测试结果**，因此没有可核验的 quantitative SOTA 指标。
- 唯一较具体的数字化信息是案例：Parahelp 的客服 agent prompt 长度达到 **6+ pages**，用于细致定义工具调用管理规则。
- 文中声称这些技巧可提升 agent 的**可靠性、输出一致性、结构化程度、信任度和调试效率**，但未给出数据集、指标、baseline 或 ablation 数字。
- 还给出若干定性案例：Jazzberry 用**困难样例**做 few-shot；某些系统通过**分类器 prompt 生成更专用的下一阶段 prompt**；Gemini 1.5 Pro 被提及可提供某种 **thinking traces** 用于调试。
- 因此，这篇内容更像**行业最佳实践综述**，突破点在经验总结与可操作性，而非经过严格实验验证的新算法结果。

## Link
- [https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai](https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai)
