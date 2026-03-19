---
source: arxiv
url: http://arxiv.org/abs/2603.11861v1
published_at: '2026-03-12T12:34:49'
authors:
- Quentin Goux
- Nadira Lammari
topics:
- model-driven-architecture
- attack-script-generation
- cybersecurity-training
- tosca
- knowledge-graph
relevance_score: 0.55
run_id: materialize-outputs
language_code: zh-CN
---

# Automatic Attack Script Generation: a MDA Approach

## Summary
本文提出一种基于模型驱动架构（MDA）的自动化方法，把非正式攻击场景描述转成可执行的攻击脚本与攻击环境，用于网络安全教学与训练。核心价值在于减少人工搭建训练演练的成本、错误率与平台绑定问题。

## Problem
- 网络安全实训中的攻击脚本与环境通常需要**手工**搭建，过程耗时、易错，并且依赖较强的技术、编程与建模能力。
- 现有攻击模型与框架在语法和语义上**异构**，且通常不能统一描述攻击步骤与攻击上下文，导致难以复用、难以自动生成实现。
- 训练环境更新快、攻击手法变化快，手工构建的演练内容**容易过时**，难以迁移到不同平台。

## Approach
- 作者以**MDA三层抽象**组织流程：把统一攻击模型作为 CIM，基于 TOSCA 构建 PIM，再生成特定平台的 PSM。
- 在 CIM 层，使用其先前提出的**统一攻击模型**与形式化语言描述攻击操作路径和攻击上下文，并通过用户界面辅助录入；上下文还能从攻击步骤中自动推导。
- 将 CIM 存入 **Neo4j 知识图谱**，再通过一组**12条转换规则**自动生成 TOSCA YAML 的抽象基础设施拓扑和抽象攻击工作流。
- 为弥补 TOSCA 对攻击语义支持不足，作者做了最小扩展，引入 `AttackTransitions` 接口与 `HostSystem` 类型，以表达攻击动作与宿主目标。
- 在目标推断上，作者提出如 `iao` 与 `ig` 两类**推理假设**，从知识图谱中为每个攻击步骤自动找到应执行该操作的主机；随后把 PIM 落地到 OpenTOSCA + Ansible 平台，生成具体执行脚本与环境。

## Results
- 论文主要给出的是**方法可行性验证**，没有报告标准基准数据集上的准确率、成功率、时间开销等系统性定量实验结果。
- 在示例 **SnifAttack** 中，形式化后自动推导出 **38 个资源**，使整体知识图谱达到 **182 个节点、1482 条关系**。
- PIM 生成阶段，作者定义了 **12 条转换规则**，并成功自动生成 TOSCA 拓扑与工作流；工作流覆盖示例中的 **6 个攻击步骤**：Scanning、UseOfDefaults、Sniffing、Disclosure、Discovery、Checkmate。
- 目标推断方面，`iao` 假设在示例中推断出前 **2** 个步骤目标，并在扩展后额外覆盖 **2** 个步骤；`ig` 假设推断出剩余 **2** 个步骤，从而补全全部 **6/6** 步骤的执行目标。
- 生成的 TOSCA 服务模板通过了 **TOSCA Toolbox** 的语法与语义检查，并自动产出了 UML 图，说明生成结果在标准层面是可验证的。
- 在 PSM 层，作者展示了面向其自建平台的具体落地：通过 **OpenTOSCA** 提供基础设施、**Ansible** 执行具体脚本，并给出了命令行输出示例，但未提供与人工方法或现有自动化方法的直接数值对比。

## Link
- [http://arxiv.org/abs/2603.11861v1](http://arxiv.org/abs/2603.11861v1)
