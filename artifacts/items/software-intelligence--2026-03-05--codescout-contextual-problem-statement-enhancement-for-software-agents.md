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
- code-intelligence
- problem-statement-augmentation
- swebench
- repository-analysis
relevance_score: 0.96
run_id: materialize-outputs
---

# CodeScout: Contextual Problem Statement Enhancement for Software Agents

## Summary
CodeScout通过在软件代理真正开始修复前，先对代码仓库做轻量级预探索，把含糊的问题描述改写成更完整、可执行的任务说明。它是一个可插拔的前处理层，不需要改动现有agent框架，却能显著提升真实软件缺陷修复表现。

## Problem
- 论文要解决的是：用户提交给代码代理的问题描述常常过于简略、缺少复现步骤、期望行为和代码上下文，导致代理在仓库中盲目探索、重复尝试错误修复，最终失败。
- 这很重要，因为已有研究显示，输入质量而非单纯模型能力，往往是AI软件工程代理的关键瓶颈；描述不清会直接拉长轨迹、增加成本、降低修复成功率。
- 现有方法多做检索或定位，但不能把“隐含在仓库里的上下文”转成代理真正可执行的自然语言任务规范。

## Approach
- CodeScout的核心机制很简单：先“看懂仓库和问题”，再把原始问题重写成更好的问题说明，让下游agent少走弯路。
- 它先用AST构建仓库知识图谱，表示类、函数、导入、依赖和作用域等结构关系。
- 然后做高层scoping：让LLM根据原始问题和知识图谱挑出最多15个最相关的代码目标，而不是直接全仓库乱搜。
- 接着对这些目标做细粒度分析，提取它们与问题的关系、可能修改位置、技术线索、替代性根因假设，并用相关性过滤去掉噪声。
- 最后把原始问题与筛选后的洞察合成为增强版问题陈述，显式加入增强描述、复现步骤、期望行为、探索提示和修复提示；这一流程无需修改SWE-agent、OpenHands等底层scaffold。

## Results
- 在SWEBench-Verified上，论文声称CodeScout相对默认方法把resolution rate提升约20%，最多可额外解决27个issue。
- 在SWE-Agent消融实验中，已解决问题数从Default的114/194/183提升到125/209/207，分别对应DeepSeek R1 +11（+9.6%）、GPT-5-mini +15（+7.7%）、Qwen3 Coder +24（+13.1%）。
- 让agent在执行轨迹中自行做增强反而更差：109/177/158，相比Default分别为-5、-17、-25，说明“独立预探索”比“边做边补充说明”有效得多。
- 去掉相关性过滤后，收益明显变弱：116/190/190；用BM25替代LLM scoping时为119/195/198，虽优于Default但弱于完整CodeScout，表明语义scoping和过滤都关键。
- 交叉合成实验显示强增强器可显著抬升弱运行模型：当DeepSeek R1作为runtime agent时，默认108，若由Qwen3 Coder做问题增强可到164，增加+56（+51.9%）；而强runtime模型GPT-5-mini从194提升到196/207/209，增益较小但仍稳健。
- 论文还声称增强后文件级和函数级localization均优于默认设置，尤其对较弱模型更明显；成本/token分析表明Qwen3和DeepSeek在相同token预算下通常能解决更多问题，但文中未在摘录里给出完整统一数值表。

## Link
- [http://arxiv.org/abs/2603.05744v1](http://arxiv.org/abs/2603.05744v1)
