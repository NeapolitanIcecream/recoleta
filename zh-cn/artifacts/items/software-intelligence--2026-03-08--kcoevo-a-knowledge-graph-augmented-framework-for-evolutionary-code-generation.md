---
source: arxiv
url: http://arxiv.org/abs/2603.07581v1
published_at: '2026-03-08T10:39:48'
authors:
- Jiazhen Kang
- Yuchen Lu
- Chen Jiang
- Jinrui Liu
- Tianhao Zhang
- Bo Jiang
- Ningyuan Sun
- Tongtong Wu
- Guilin Qi
topics:
- code-generation
- api-migration
- knowledge-graph
- llm-reasoning
- software-evolution
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# KCoEvo: A Knowledge Graph Augmented Framework for Evolutionary Code Generation

## Summary
KCoEvo解决的是**随API版本演化而失效的代码迁移生成**问题：普通LLM常输出过时或不兼容API，而该方法用知识图谱显式表示API演化路径来约束生成。论文将迁移拆成“先找演化路径、再按路径生成代码”两步，并在多个模型与迁移类型上显著提升准确率与可执行性。

## Problem
- 目标问题：把依赖旧版本第三方库的代码，自动迁移为兼容新版本的代码，同时保持原始功能不变。
- 重要性：现代项目高度依赖第三方库，API频繁变更会导致代码失效、维护成本上升；作者举例称典型项目可能含有**20–70个传递依赖**，而直接依赖只有**6–10个**。
- 现有LLM缺陷：缺少对**版本间关系、弃用/重命名/迁移**等演化知识的显式结构化表示，因此容易生成过时API、语义不一致代码或无法执行的输出。

## Approach
- 构建两层API知识图谱：**static API graph**表示单版本内的结构关系，**dynamic alignment graph**表示跨版本的演化关系，如 retain、remove、rename、relocate。
- 将迁移分成两阶段：先做**evolution path retrieval**，从图中检索从旧API到新API的可行迁移轨迹；再做**path-informed code generation**，让LLM依据这些路径生成目标代码。
- 动态对齐时，系统先从查询代码里定位API节点，再基于**BFS图遍历**结合版本元数据与关系类型，找出有效的跨版本候选路径。
- 规划模块直接复用LLM，不单独训练新模型：LLM先把对齐子图转成显式的“演化计划”，再由推理/生成模块按计划完成代码迁移。
- 训练监督来自**真实API diff自动合成**的数据，而非大量人工标注，从而提升可扩展性并降低人力成本。

## Results
- 在VersiCode基准上，方法相对基础LLM在所有迁移类型上都有提升。示例：**DeepSeek-V3**在**Major→Major**上，CDC@1从**59.52**升至**96.83**，EM@1从**59.52**升至**100.00**（分别**+37.31**、**+40.48**）。
- 在更难的跨版本迁移中提升更大。**DeepSeek-V3**在**Major→Minor**上EM@1从**33.84**到**94.44**（**+60.60**），在**Minor→Major**上从**15.74**到**95.37**（**+79.63**）。
- **Qwen2.5-Coder-32B-Instruct**收益也很大：**Major→Minor**上EM@1从**16.16**到**92.42**（**+76.26**）；**Minor→Major**上从**7.41**到**87.96**（**+80.55**）。
- 高性能闭源模型仍能受益。**GPT-5**基线已很强，但加入KG后在**Minor→Minor**上CDC@1从**46.30**到**92.60**（**+46.30**），EM@1从**72.23**到**100.00**（**+27.77**）；在**Minor→Major**上CDC@1从**82.83**到**100.00**。
- 对比代码块RAG，普通检索增强收益有限甚至退化。例如**Qwen2.5-7B-Instruct**在**Major→Major**的EM@1基线为**38.89**，加入**Downstream Code**后为**38.10**，加入**Library Source**仍仅**38.10**；说明结构化演化知识比原始代码检索更有效。
- 论文的核心主张是：知识图谱不仅提高**准确率/EM@1**，也提高**CDC@1对应的语法与执行成功性**，并带来更强的可控性与可解释的迁移路径。

## Link
- [http://arxiv.org/abs/2603.07581v1](http://arxiv.org/abs/2603.07581v1)
