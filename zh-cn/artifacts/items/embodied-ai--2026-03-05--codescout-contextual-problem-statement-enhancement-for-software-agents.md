---
source: arxiv
url: http://arxiv.org/abs/2603.05744v1
published_at: '2026-03-05T23:10:09'
authors:
- Manan Suri
- Xiangci Li
- Mehdi Shojaie
- Songyang Han
- Chao-Chun Hsu
- Shweta Garg
- Aniket Anand Deshmukh
- Varun Kumar
topics:
- software-agents
- query-refinement
- code-repair
- repo-understanding
- swebench
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# CodeScout: Contextual Problem Statement Enhancement for Software Agents

## Summary
CodeScout通过在代理执行前先对代码库做轻量级预探索，把含糊的问题描述改写成更完整、可执行的任务说明，从而提升软件工程代理的修复成功率。核心思想是先“看清问题”再“动手解决”，且无需修改下游代理框架。

## Problem
- 论文解决的是**软件工程代理面对描述不充分的问题单时容易失败**的问题；这很重要，因为真实开发中的issue常缺少复现步骤、预期行为和代码上下文，导致代理长时间盲目探索或反复尝试同一修复。
- 作者指出，现有失败常表现为**过度探索**与**顽固重复修复**，瓶颈不一定是模型推理能力，而是输入规格质量不足。
- 目标是在**不改动代理scaffold**的前提下，把原始问题陈述增强为更清晰、可操作的说明，从而提升下游任务表现。

## Approach
- CodeScout是一个**前处理式查询/问题增强管线**：输入原始问题陈述和代码仓库，输出增强后的问题陈述，再交给现有软件代理执行。
- 首先构建**仓库知识图谱**，从AST中抽取类、函数、导入关系、变量作用域等结构化实体与关系，形成代码库的语义索引。
- 然后用LLM做**高层范围界定（scoping）**，基于原始问题与知识图谱挑选最多15个最相关的探索目标，而不是直接全仓库盲搜。
- 对每个目标做**细粒度上下文分析**，提取它与问题的关系、可能修复位置、技术实现线索、备选根因假设，并通过相关性阈值过滤噪声。
- 最后做**问题合成**：把原始描述与筛选后的洞察融合成增强版问题说明，显式补充复现步骤、预期行为、探索提示和修复提示；本质上就是把隐含仓库知识翻译成代理更容易利用的自然语言任务规格。

## Results
- 在**SWEBench-Verified**上，论文声称CodeScout相对默认方法带来**20% resolution rate提升**，并且**最多多解决27个问题**。
- 在SWE-Agent消融实验中，相比Default，CodeScout将已解决问题数从**114→125（DeepSeek R1，+11，+9.6%）**、**194→209（GPT-5-mini，+15，+7.7%）**、**183→207（Qwen3 Coder，+24，+13.1%）**。
- 让代理在执行过程中**自行做增强**反而更差：相对Default变为**109 vs 114（DeepSeek R1，-5）**、**177 vs 194（GPT-5-mini，-17）**、**158 vs 183（Qwen3 Coder，-25）**，说明独立的前置增强阶段比“边做边补”有效。
- 去掉相关性过滤后收益明显下降：**116/190/190** 对比 Default 的 **114/194/183**，表明过滤噪声上下文是关键组件。
- 用**BM25实体选择**替代LLM scoping虽仍优于默认，但弱于完整方法：**119/195/198**，低于CodeScout的**125/209/207**，说明语义范围界定优于词法检索。
- 交叉增强结果显示强增强器能显著帮助弱运行模型：以DeepSeek R1作为运行代理时，被Qwen3增强可从**108提升到164（+56，+51.9%）**；而强运行模型GPT-5-mini被DeepSeek增强仅从**194到196（+2，+1.0%）**，说明收益对弱代理更显著。

## Link
- [http://arxiv.org/abs/2603.05744v1](http://arxiv.org/abs/2603.05744v1)
