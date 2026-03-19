---
source: arxiv
url: http://arxiv.org/abs/2603.11861v1
published_at: '2026-03-12T12:34:49'
authors:
- Quentin Goux
- Nadira Lammari
topics:
- cybersecurity-training
- attack-script-generation
- model-driven-architecture
- tosca
- knowledge-graph
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Automatic Attack Script Generation: a MDA Approach

## Summary
本文提出一种基于MDA（模型驱动架构）的自动攻击脚本生成方法，把非正式攻击场景描述逐步转成可执行脚本与攻击环境，用于网络安全教学与训练。核心价值是减少手工搭建演练环境的时间、错误和技能门槛，并提升跨平台复用性。

## Problem
- 网络安全实训中的攻击脚本与环境通常需要人工配置，成本高、耗时长、且容易出错。
- 现有攻击模型与框架在语法和语义上异构，且多数不能统一描述攻击过程与攻击上下文，导致难以自动生成脚本。
- 手工实现出的训练场景很快过时，也难以迁移到不同平台，限制了教学与训练内容的更新和复用。

## Approach
- 提出一个统一攻击模型作为CIM（计算无关模型），用形式化语言描述攻击步骤、前后条件以及涉及的IT资源/上下文，并通过用户界面引导录入。
- 将形式化攻击场景与上下文存入知识图谱/属性图数据库（Neo4j），并从攻击操作模式自动推导所需资源与环境。
- 在PIM（平台无关模型）层，使用TOSCA Simple Profile 1.3的YAML服务模板表示抽象基础设施与抽象攻击脚本；作者为攻击场景做了最小扩展，如`AttackTransitions`和`HostSystem`。
- 设计12条从CIM到PIM的自动转换规则，把资源映射成拓扑节点/端口，把攻击路径映射成工作流步骤，并通过推理假设（如`iao`、`ig`）为每一步推断执行目标主机。
- 在PSM（平台相关模型）层，将抽象模型落地到具体平台；论文演示了基于OpenTOSCA提供基础设施、Ansible执行自动化脚本的实现流程。

## Results
- 论文主要贡献是提出并演示了一条端到端自动化流程：从非正式攻击描述到CIM、再到TOSCA PIM、最后到可执行PSM与命令行执行。
- 在示例“SnifAttack”中，系统从形式化场景自动推导出**38个资源**，生成的整体知识图谱达到**182个节点、1482条关系**。
- PIM生成中，作者实现了**12条转换规则**，并基于两类推理假设为攻击步骤自动分配目标主机；在SnifAttack的**6个步骤**中，`iao`推断出前**2步**目标，扩展后覆盖另外**2步**，`ig`推断出剩余**2步**。
- 生成的PIM采用**TOSCA Simple Profile v1.3** YAML表示，并通过**TOSCA Toolbox**完成语法与语义检查，随后自动产出对应的UML图。
- 论文未提供与现有方法的标准基准对比、准确率、生成成功率、节省时间比例等系统性定量评测；最强的实证证据是SnifAttack案例的自动生成与在OpenTOSCA+Ansible平台上的可执行演示。

## Link
- [http://arxiv.org/abs/2603.11861v1](http://arxiv.org/abs/2603.11861v1)
