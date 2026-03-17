---
source: arxiv
url: http://arxiv.org/abs/2603.10621v1
published_at: '2026-03-11T10:33:14'
authors:
- Juan M. Murillo
- "Ignacio Garc\xEDa Rodr\xEDguez de Guzm\xE1n"
- Enrique Moguel
- "Javier Romero-\xC1lvarez"
- Jaime Alvarado-Valiente
- "\xC1lvaro M. Aparicio-Morales"
- Jose Garcia-Alonso
- "Ana D\xEDaz Mu\xF1oz"
- "Eduardo Fern\xE1ndez-Medina"
- Francisco Chicano
- Carlos Canal
- "Jos\xE9 Daniel Viqueira"
- "Sebasti\xE1n Villarroya"
- "Eduardo Guti\xE9rrez"
- "Adri\xE1n Romero-Flores"
- "Alfonso E. M\xE1rquez-Chamorro"
- Antonio Ruiz-Cortes
- Cyrille YetuYetu Kesiku
- "Pedro S\xE1nchez"
- "Diego Alonso C\xE1ceres"
- "Lidia S\xE1nchez-Gonz\xE1lez"
- Fernando Plou
topics:
- quantum-software-engineering
- quantum-computing
- software-engineering
- nisq
- hybrid-systems
relevance_score: 0.44
run_id: materialize-outputs
---

# QuantumX: an experience for the consolidation of Quantum Computing and Quantum Software Engineering as an emerging discipline

## Summary
本文总结了 QuantumX 这一首次聚焦量子计算与量子软件工程交叉领域的会议轨道，梳理了西班牙相关研究群体的代表性工作、共同主题与开放挑战。其核心价值在于推动量子软件工程从分散研究走向更系统的工程学科建设。

## Problem
- 量子计算正从理论走向实践，但量子软件仍缺少成熟的软件工程方法来保障**质量、可维护性、可测试性、治理能力与复用性**。
- 现有量子硬件受限于 NISQ 条件、云端排队、高错误率和高成本，导致大规模开发、测试与部署非常困难。
- 若没有统一的工程抽象、质量模型、编排机制和工具链，量子技术很难真正进入工业级软件生产与服务化场景，这对学科发展和产业落地都很关键。

## Approach
- 论文本身不是提出单一新算法，而是**系统性综述/综合** QuantumX 会议上的多项工作，按研究群体与主题组织，提炼量子软件工程的共性问题与未来方向。
- 归纳的核心机制包括：把经典软件工程原则迁移到量子领域，例如**质量模型、服务工程、自动代码生成、静态分析、测试与变异测试、编排与治理、可复用抽象**。
- 在执行与运维层面，相关工作探索了**量子任务调度、跨多家 NISQ 云提供商的编排、混合量子-经典 SaaS 治理**，以降低成本、减少失败执行并提升可用性。
- 在编程与建模层面，相关工作提出了**更高层抽象**（如 quantum integer、Locus）、自动化电路生成、QML 基准测试工具，以及用于混合/仿真环境的可重复实验框架。

## Results
- 作为综述性论文，它**没有给出单一统一实验指标**；但汇总了会议中多个工作的代表性结果与具体数字。
- QCRAFT Scheduler 报告：相较于单独执行，量子电路分组与组合调度可使**平均成本降低约 84%**、**任务数降低约 84%**。
- 量子变异测试工作报告：在 IBM Quantum 场景中，通过规划与任务组合执行量子电路变异体，**成本最高可降低约 94%**，并声称证明了 NISQ 时代大规模量子测试的可行性。
- 量子服务工程工作评估了**40 个量子算法实现**，发现质量属性（如 analyzability）存在明显差异，并据此提出持续改进建议。
- eVIDA 的临床文本分类工作声称：在 **MIMIC-III/IV** 数据集上，结合 1D CNN、量子 BiLSTM 和量子注意力的混合模型，在**F1 与 MCC** 上优于经典基线，但文摘未提供具体数值。
- 其余贡献多为定性或方法性主张，例如更高层量子编程抽象、张量网络提升 QML 仿真效率、变分电路可训练性改进、多云量子编排、量子数据库路线图等；在给定文本中多数**未提供可核对的统一数值对比**。

## Link
- [http://arxiv.org/abs/2603.10621v1](http://arxiv.org/abs/2603.10621v1)
