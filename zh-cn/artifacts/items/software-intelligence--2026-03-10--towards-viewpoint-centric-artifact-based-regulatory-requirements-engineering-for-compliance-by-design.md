---
source: arxiv
url: http://arxiv.org/abs/2603.09492v1
published_at: '2026-03-10T10:51:40'
authors:
- Oleksandr Kosenkov
topics:
- regulatory-requirements
- compliance-by-design
- artifact-based-re
- viewpoint-coordination
- privacy-by-design
relevance_score: 0.47
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Viewpoint-centric Artifact-based Regulatory Requirements Engineering for Compliance by Design

## Summary
本文提出一种以视点协调为核心的工件化监管需求工程框架 AM4RRE，目标是在软件开发生命周期中更系统地实现“合规即设计”。其核心贡献是把法律、业务、需求与架构视点通过共享工件模型连接起来，以降低当前合规实践中的临时性和割裂性。

## Problem
- 软件工程中的监管合规越来越复杂，法规数量、范围和知识密度持续增加，而业界仍多依赖孤立、临时的合规做法。
- 监管需求不同于一般业务需求：它通常是对法规解释后的“后置”需求，会反向影响已有需求与架构，并要求跨法律、需求、架构等多视点持续协调。
- 现有以流程/活动为中心的方法难以在敏捷和真实项目变化下保证一致性、完整性与可验证性，因此难以支撑可证明的 compliance by design。

## Approach
- 作者基于文献研究与多项实证研究，扩展 AMDiRE，提出工件模型 AM4RRE，用“要产出什么工件”而非“按什么流程做”来组织监管需求工程。
- AM4RRE 包含 5 个核心部分：角色模型、目标模型、项目上下文模型、里程碑模型、内容模型；并围绕 4 个视点组织：legal、business、requirements、architecture。
- 其最核心机制是用法律规格作为基础，把法规文本中的法律概念先标注和结构化，再映射到软件上下文、需求和系统规格中，形成跨视点的一致关系。
- 模型通过三类裁剪落地：法规特定裁剪（从法规中提取概念与属性）、项目内容裁剪（把法律概念映射到工程工件）、目标驱动裁剪（按组织/项目目标决定需要哪些内容项）。
- 论文还报告了用于支撑该模型的前期证据：系统映射/综述、访谈、焦点小组、实践研究，以及对 GDPR/privacy by design 场景下法律概念实例化方法的初步验证。

## Results
- 文中没有给出对 AM4RRE 最终整体效果的定量实验结果；这是一个博士研究阶段论文，最终模型仍计划在未来与从业者一起验证。
- 文献研究发现了 **11 类**监管需求工程挑战，其中最突出的问题与法律/IT/隐私安全知识密度、法规抽象性以及专家间交互困难有关。
- 在 privacy by design 相关实践研究中，**15 名**参与者中仅 **2 名**使用了系统化方法，其余多数仍依赖非系统化实践，支持了该问题的重要性。
- 在隐私设计方法综述中，仅识别出 **5 篇**同时明确覆盖需求与系统设计的方法研究，且作者指出**没有**一种方法是可直接系统复用于其他法规的。
- 作者从实践访谈中提炼出 **11 个** privacy by design 的高层 RE 目标，并据此将目标模型纳入 AM4RRE，用于支持跨视点协调与裁剪。
- 对法律视点和 GDPR 概念实例化方法的验证结论是**总体积极/可适用**：法律专家 walkthrough 反馈正向；从业者验证表明，该方法可用于捕获法律领域知识并分配到需求层与系统层，但文中未报告精确指标或基线对比数值。

## Link
- [http://arxiv.org/abs/2603.09492v1](http://arxiv.org/abs/2603.09492v1)
