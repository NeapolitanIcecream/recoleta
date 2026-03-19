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
language_code: en
---

# MetaRCA: A Generalizable Root Cause Analysis Framework for Cloud-Native Systems Powered by Meta Causal Knowledge

## Summary
MetaRCA proposes a generalizable root cause analysis framework for cloud-native systems, separating the offline construction of “general causal knowledge” from the online inference of “specific faults” to improve accuracy, scalability, and cross-system reusability. It centers on a Meta Causal Graph that fuses LLMs, historical fault reports, and monitoring data into a reusable causal knowledge base.

## Problem
- Cloud-native systems consist of large numbers of microservices, containers, and dynamic dependencies, making fault propagation paths complex and root cause analysis difficult to perform accurately and in a timely manner.
- Existing causal RCA methods typically face three major bottlenecks: **poor scalability** (computational cost explodes as systems grow), **weak generalization** (changing topology or system requires rebuilding or retraining), and **insufficient knowledge integration** (rules are too rigid, while relying directly on LLMs can cause hallucinations, high latency, and high cost).
- This matters because production environments require **real-time incident response**; if RCA is inaccurate or unstable, it directly affects system reliability, recovery time, and operational cost.

## Approach
- The core method first constructs an offline **Meta Causal Graph, MCG**: rather than targeting a specific system instance, it is a general causal graph defined at the metadata level of “component type–metric–connection pattern.”
- The initial skeleton of the MCG is obtained through **LLM-guided extraction**: given component types (such as Microservice, MySQL, Redis) and connection patterns (such as invoke, on), the LLM infers which metrics may have causal relationships.
- Then an **evidence-driven Bayesian belief evolution model** continuously updates the confidence of each edge: high-confidence historical fault reports and lower-confidence data-driven causal discovery results are both converted into standardized evidence, and causal confidence scores are updated using log-odds with time decay.
- When an online fault occurs, the system first defines a **Fault Relevance Zone** around anomalous components, then instantiates the MCG into a local graph according to the current topology; it then **weights and prunes** edges using real-time anomaly intensity and lag correlation, and finally uses a graph-ranking method to locate the most likely root cause.
- Put simply: it first learns transferable experience such as “when a database slows down, it often slows upstream services,” and then, when a specific incident occurs, quickly applies and filters that experience only within the relevant local area instead of rediscovering causal relationships from scratch every time.

## Results
- The paper claims evaluation on **252 public failure cases** and **59 production failure cases**, where MetaRCA achieves **SOTA** performance.
- Compared with the **strongest baseline**, its **service-level accuracy** improves by **29 percentage points**, and its **metric-level accuracy** improves by **48 percentage points**.
- The data used to build the knowledge base includes **563 production fault reports** (China Unicom) and **614 public fault datasets**.
- The paper claims that its advantage further widens as **system complexity increases**, while online/overall overhead grows **near-linearly** with system size, outperforming traditional causal-discovery-based methods whose cost expands rapidly.
- In terms of cross-system generalization, MetaRCA reportedly maintains **over 80% accuracy without retraining** across diverse systems.
- The abstract and introduction do not provide more fine-grained absolute accuracies, exact values for specific baseline names, variance, or significance tests; the strongest quantitative conclusions currently supported are mainly the improvement margins above and the “>80%” generalization accuracy.

## Link
- [http://arxiv.org/abs/2603.02032v1](http://arxiv.org/abs/2603.02032v1)
