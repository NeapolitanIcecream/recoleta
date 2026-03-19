---
source: arxiv
url: http://arxiv.org/abs/2603.02032v1
published_at: '2026-03-02T16:16:22'
authors:
- Shuai Liang
- Pengfei Chen
- Bozhe Tian
- Gou Tan
- Maohong Xu
- Youjun Qu
- Yahui Zhao
- Yiduo Shang
- Chongkang Tan
topics:
- root-cause-analysis
- cloud-native-systems
- causal-graph
- llm-knowledge-fusion
- bayesian-updating
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# MetaRCA: A Generalizable Root Cause Analysis Framework for Cloud-Native Systems Powered by Meta Causal Knowledge

## Summary
MetaRCA提出了一个面向云原生系统的可泛化根因分析框架，把“可复用的因果知识”离线沉淀为元因果图，再在故障发生时做轻量级在线推理。其目标是同时提升RCA的准确率、可扩展性和跨系统泛化能力。

## Problem
- 云原生系统由大量微服务、容器和动态依赖组成，故障传播路径复杂，导致根因分析（RCA）很难做到又快又准。
- 现有因果RCA方法常见三大问题：**扩展性差**（系统变大后计算代价暴涨）、**泛化脆弱**（换拓扑/换系统就失效）、**领域知识融合不足**（规则过死或LLM直接推理成本高且易幻觉）。
- 这很重要，因为生产环境需要实时、可靠地定位故障根因，否则会拉长故障恢复时间并影响系统可用性与业务稳定性。

## Approach
- 核心思路是把RCA拆成两部分：**离线建知识库**、**在线做局部推理**。离线先构建一个元数据层面的**Meta Causal Graph (MCG)**，表示“某类组件的某类指标通常会怎样影响另一类组件/指标”。
- MCG的初始骨架由LLM根据组件类型、指标语义和连接模式（如invoke、on）自动抽取潜在因果关系，相当于先生成一个“经验因果模板库”。
- 然后用历史故障报告和历史观测数据对这些边做**证据驱动的贝叶斯更新**：高置信的故障报告和低置信的数据因果发现都会给边增加或衰减置信度，并带时间衰减，从而持续演化MCG。
- 在线时，系统先从当前异常中划定故障相关区域（FRZ），再把MCG按当前拓扑实例化成局部实例因果图（LICG）。随后结合实时异常强度和时滞相关性对边加权、剪枝，最后用图排序方法定位最可能的根因。

## Results
- 在**252个公共故障案例**和**59个生产故障案例**上评测，MetaRCA达到作者声称的**SOTA**表现。
- 相比**最强基线**，其**服务级准确率提升29个百分点**，**指标级准确率提升48个百分点**。
- 构建MCG时使用了大规模历史知识：来自中国联通的**563份生产故障报告**和**614个公共故障数据集**。
- 作者称其优势会随着系统复杂度上升而进一步扩大，同时**运行开销近线性随系统规模增长**，说明比传统高复杂度因果发现更可扩展。
- 在跨系统泛化方面，MetaRCA据称**无需重训即可在多样系统上保持80%以上准确率**。
- 摘要与引言未给出更细粒度的完整指标表、具体基线名称对应数值或方差统计，但上述百分点提升和“>80%”泛化结果是文中最明确的定量主张。

## Link
- [http://arxiv.org/abs/2603.02032v1](http://arxiv.org/abs/2603.02032v1)
