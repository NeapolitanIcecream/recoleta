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
- observability
- bayesian-inference
relevance_score: 0.61
run_id: materialize-outputs
---

# MetaRCA: A Generalizable Root Cause Analysis Framework for Cloud-Native Systems Powered by Meta Causal Knowledge

## Summary
MetaRCA提出了一种面向云原生系统的可泛化根因分析框架，把“通用因果知识”的离线构建与“具体故障”的在线推理分开，以提升准确性、扩展性和跨系统复用性。它核心依赖一个元因果图，将LLM、历史故障报告和监控数据融合成可复用的因果知识库。

## Problem
- 云原生系统由大量微服务、容器和动态依赖组成，故障传播链路复杂，导致根因分析难以及时、准确地定位问题。
- 现有因果RCA方法通常有三大瓶颈：**扩展性差**（系统变大后计算成本爆炸）、**泛化性弱**（换拓扑/换系统就要重建或重训）、**知识融合不足**（规则太死，或直接靠LLM又易幻觉、延迟高、成本高）。
- 这件事重要，因为生产环境需要**实时 incident 响应**；若RCA不准或不稳，会直接影响系统可靠性、恢复时间和运维成本。

## Approach
- 论文的核心方法是先离线构建一个**Meta Causal Graph, MCG**：它不是针对某个具体系统实例，而是定义在“组件类型—指标—连接模式”这一元数据层上的通用因果图。
- MCG的初始骨架由**LLM引导抽取**得到：给定组件类型（如Microservice、MySQL、Redis）和连接模式（如invoke、on），让LLM推断哪些指标之间可能存在因果关系。
- 然后用一个**证据驱动的贝叶斯信念演化模型**持续更新每条边的可信度：高置信度的历史故障报告与低置信度的数据驱动因果发现都被转成标准化证据，并用带时间衰减的log-odds更新因果置信分数。
- 当线上发生故障时，系统先在异常组件上划出**Fault Relevance Zone**，再把MCG按当前拓扑实例化成局部图；随后结合实时异常强度和滞后相关性对边进行**加权与剪枝**，最后用图排序方法定位最可能的根因。
- 用最简单的话说：它先学会“数据库变慢常会拖慢上游服务”这类可迁移经验，再在具体事故发生时，只在相关局部快速套用和筛选这些经验，而不是每次从零发现因果关系。

## Results
- 论文声称在**252个公开故障案例**和**59个生产故障案例**上评估，MetaRCA达到**SOTA**表现。
- 相比**最强基线**，其**service-level accuracy**提升**29个百分点**，**metric-level accuracy**提升**48个百分点**。
- 用于构建知识库的数据规模包括**563份生产故障报告**（China Unicom）和**614个公开故障数据集**。
- 论文声称其优势会随着**系统复杂度增加而进一步扩大**，同时在线/整体开销随系统规模**近线性增长**，优于传统会快速膨胀的因果发现式方法。
- 在跨系统泛化方面，MetaRCA据称在多样化系统上**无需重训练仍保持80%以上准确率**。
- 摘要与引言未给出更细粒度的绝对准确率、具体基线名称对应数值、方差或显著性检验；当前能确认的最强定量结论主要是上述提升幅度与“>80%”泛化准确率。

## Link
- [http://arxiv.org/abs/2603.02032v1](http://arxiv.org/abs/2603.02032v1)
