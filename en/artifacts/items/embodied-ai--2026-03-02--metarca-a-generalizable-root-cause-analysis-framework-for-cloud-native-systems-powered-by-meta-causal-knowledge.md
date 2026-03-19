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
language_code: en
---

# MetaRCA: A Generalizable Root Cause Analysis Framework for Cloud-Native Systems Powered by Meta Causal Knowledge

## Summary
MetaRCA proposes a generalizable root cause analysis framework for cloud-native systems. It distills “reusable causal knowledge” offline into a Meta Causal Graph, and then performs lightweight online inference when faults occur. Its goal is to improve RCA accuracy, scalability, and cross-system generalization at the same time.

## Problem
- Cloud-native systems consist of large numbers of microservices, containers, and dynamic dependencies, and their fault propagation paths are complex, making root cause analysis (RCA) difficult to do both quickly and accurately.
- Existing causal RCA methods commonly suffer from three major problems: **poor scalability** (computational cost surges as systems grow), **fragile generalization** (they fail when the topology or system changes), and **insufficient integration of domain knowledge** (rules are too rigid, or direct LLM reasoning is costly and prone to hallucination).
- This matters because production environments require real-time and reliable fault root cause localization; otherwise, recovery time is prolonged and system availability and business stability are affected.

## Approach
- The core idea is to split RCA into two parts: **build the knowledge base offline** and **perform local inference online**. Offline, it first constructs a metadata-level **Meta Causal Graph (MCG)** to represent how “a certain type of metric in one class of component typically affects a certain type of component/metric in another class.”
- The initial skeleton of the MCG is automatically extracted by an LLM based on component types, metric semantics, and connection patterns (such as invoke and on), effectively producing an “empirical causal template library” first.
- Then, historical fault reports and historical observability data are used to perform **evidence-driven Bayesian updates** on these edges: high-confidence fault reports and lower-confidence data-driven causal discovery both increase or decay edge confidence, with temporal decay as well, allowing the MCG to evolve continuously.
- Online, the system first identifies the fault-related zone (FRZ) from current anomalies, then instantiates the MCG into a local instance causal graph (LICG) according to the current topology. It then combines real-time anomaly intensity and lag correlation to weight and prune edges, and finally applies graph ranking methods to locate the most likely root cause.

## Results
- Evaluated on **252 public failure cases** and **59 production failure cases**, MetaRCA achieves what the authors claim is **SOTA** performance.
- Compared with the **strongest baseline**, it improves **service-level accuracy by 29 percentage points** and **metric-level accuracy by 48 percentage points**.
- The MCG was built using large-scale historical knowledge: **563 production fault reports** from China Unicom and **614 public failure datasets**.
- The authors state that its advantage widens as system complexity increases, while **runtime overhead grows nearly linearly with system size**, indicating better scalability than traditional high-complexity causal discovery methods.
- In terms of cross-system generalization, MetaRCA is claimed to **maintain over 80% accuracy across diverse systems without retraining**.
- The abstract and introduction do not provide a more fine-grained full metrics table, exact baseline-name-to-value mappings, or variance statistics, but the percentage-point improvements above and the “>80%” generalization result are the clearest quantitative claims in the paper.

## Link
- [http://arxiv.org/abs/2603.02032v1](http://arxiv.org/abs/2603.02032v1)
