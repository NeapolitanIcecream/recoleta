---
source: arxiv
url: http://arxiv.org/abs/2603.09086v1
published_at: '2026-03-10T01:56:17'
authors:
- Rongxiang Zeng
- Yongqi Dong
topics:
- world-models
- autonomous-driving
- latent-representation
- evaluation-framework
- survey
relevance_score: 0.18
run_id: materialize-outputs
---

# Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges

## Summary
本文是一篇关于自动驾驶潜在世界模型的综述/立场论文，提出了统一分类体系、评测框架与开放问题清单。核心观点是：应以“潜在表示如何支撑闭环决策”为主线，而不是按任务或网络结构割裂地看待现有方法。

## Problem
- 自动驾驶需要在高维多传感器输入下进行长时序、安全关键的决策，但真实长尾/危险场景稀缺，纯仿真又存在 sim-to-real gap。
- 现有研究常按预测、规划、扩散、Transformer、开环/闭环等维度割裂组织，难以解释哪些共同机制真正决定鲁棒性、泛化性和可部署性。
- 开环感知/生成指标与闭环驾驶安全表现常不一致，因此需要更统一、面向决策的建模与评测框架。

## Approach
- 论文提出一个统一的 latent-space taxonomy，按**潜在表示目标**（latent worlds / latent actions / latent generators）、**表示形式**（continuous / discrete / hybrid）和**结构先验**（geometry / topology / semantics）组织自动驾驶世界模型。
- 它将神经仿真、潜在规划与强化学习、生成式数据合成/场景编辑、认知推理与 latent chain-of-thought 四大方向放入同一框架中比较。
- 论文总结出五个跨领域“内部机制”：结构同构、长时域时间稳定性、语义与推理对齐、价值对齐目标与后训练、以及自适应计算/审慎推理，并分析它们如何影响闭环鲁棒性与部署。
- 同时提出评测建议：不仅看开环指标，还应采用闭环指标套件，并加入 resource-aware deliberation cost，以衡量推理/审慎计算带来的代价。
- 最终给出面向未来的研究议程，强调 decision-ready、verifiable、resource-efficient 的潜在世界模型设计。

## Results
- 该文主要贡献是**框架性与方法论性**，而非提出新的实验模型；摘录中**没有提供新的定量实验结果或统一 benchmark 数字**。
- 明确声称的成果包括 **5 项贡献**：统一 taxonomy、总结 **5 个**内部机制、提出 **1 套**闭环评测处方、给出设计建议与研究议程、汇总代表性 benchmark/methods 以支持复现。
- 覆盖的方法版图被组织为 **4 类**：Neural Simulation & World Modeling、Latent-Centric Planning & RL、Generative Data Synthesis & Scene Editing、Cognitive Reasoning & Latent CoT。
- 文中给出的最具体主张是：闭环评测应补足开环/闭环不匹配，并显式计入 deliberation cost；但摘录未报告该评测框架相对既有标准带来的量化提升。

## Link
- [http://arxiv.org/abs/2603.09086v1](http://arxiv.org/abs/2603.09086v1)
