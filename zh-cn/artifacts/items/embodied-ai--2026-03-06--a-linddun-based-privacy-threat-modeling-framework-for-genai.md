---
source: arxiv
url: http://arxiv.org/abs/2603.06051v1
published_at: '2026-03-06T09:04:32'
authors:
- Qianying Liao
- Jonah Bellemans
- Laurens Sion
- Xue Jiang
- Dmitrii Usynin
- Xuebing Zhou
- Dimitri Van Landuyt
- Lieven Desmet
- Wouter Joosen
topics:
- privacy-threat-modeling
- generative-ai
- linddun
- security-privacy
- ai-agents
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# A LINDDUN-based Privacy Threat Modeling Framework for GenAI

## Summary
本文提出一个面向生成式 AI 应用的隐私威胁建模框架，在 LINDDUN 基础上补足 GenAI 场景中常被忽略的隐私风险。它试图把分散的研究结论整理成软件工程师可直接使用的实践化知识库与流程。

## Problem
- 现有安全/隐私威胁建模框架通常过于通用，难以覆盖 GenAI 系统中特有的数据流、提示词、记忆、代理和外部工具带来的隐私风险。
- 组织正在快速部署 GenAI，但工程师往往缺少系统识别隐私威胁的方法；这会导致合规、用户信任和敏感信息泄露风险。
- 论文明确关注两个问题：GenAI 系统带来了哪些新隐私威胁，以及如何把这些知识转化为非专家也能使用的建模框架。

## Approach
- 以 **LINDDUN** 作为底座，而不是另起炉灶；这样可复用已有方法学、威胁树和工具支持，并针对 GenAI 做增量扩展。
- 采用“双路径”构建知识：**自顶向下**系统综述 GenAI 隐私文献，论文中说识别了 65 篇文献，并在贡献陈述中总结为对 **58 篇 SOTA 论文** 的系统化分析。
- 采用**自底向上**案例研究：对一个代表性的 HR Chatbot 建立数据流图，用传统 LINDDUN Pro 由 3 名研究者进行威胁识别，再与 2 名行业专家复核。
- 将文献与案例中的发现映射到 LINDDUN，提炼出 **4 类 GenAI 系统范式** 与 **6 个 common attacker models (CAMs)**，并对新增威胁进行专家共识审查。
- 最终形成一个 GenAI 专用知识库：论文声称该框架**影响了 LINDDUN 七类隐私威胁中的 3 类**，并向知识库新增 **100 个 GenAI 示例**，再在一个多智能体 AI Agent 系统上验证覆盖性与实用性。

## Results
- 论文的核心产出是一个**领域特定的 GenAI 隐私威胁建模框架**，不是新模型或新防御算法；其主要结果是方法学与知识库扩展。
- 定量/半定量结果包括：基于 **58 篇**（贡献声明）/ **65 篇**（方法部分检索到）文献的综述；识别 **4** 种 GenAI 系统范式、**6** 个 CAM；扩展涉及 LINDDUN **7 类中的 3 类**；新增 **100** 个 GenAI 威胁示例。
- 案例与验证方面：HR Chatbot 威胁分析由 **3 名**研究人员执行，并由 **2 名**行业从业者审阅；框架验证由 **3 名**学术威胁建模专家和 **2 名**行业隐私专家参与，应用于一个更复杂的 AI Agent 系统。
- 文中还引用外部研究强调问题重要性：GPT-4 与 ChatGPT 在某些上下文下分别有 **39%** 和 **57%** 的时间会泄露私人信息；但这不是本文自己的实验结果，而是作为动机证据。
- 提供的摘录**没有报告标准基准数据集上的性能指标**（如准确率、召回率、F1、覆盖率提升百分比或与基线框架的定量对比）；最强的具体主张是该框架能支持对 GenAI 应用进行更全面的隐私分析，并已在 AI Agent 案例中得到验证。

## Link
- [http://arxiv.org/abs/2603.06051v1](http://arxiv.org/abs/2603.06051v1)
