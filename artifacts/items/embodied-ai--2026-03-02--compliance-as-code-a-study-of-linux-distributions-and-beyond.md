---
source: arxiv
url: http://arxiv.org/abs/2603.01520v1
published_at: '2026-03-02T06:50:28'
authors:
- Jukka Ruohonen
- Esmot Ara Tuli
- Hiraku Morita
topics:
- compliance-as-code
- linux-distributions
- cybersecurity-compliance
- security-controls
- cra-mapping
relevance_score: 0.03
run_id: materialize-outputs
---

# Compliance as Code: A Study of Linux Distributions and Beyond

## Summary
本文对一个真实的“compliance as code”开源项目做了大规模实证分析，研究 Linux 发行版中的合规规则覆盖、相似性、控制来源以及与欧盟 CRA 要求的映射。它的重要性在于为自动化、持续化网络安全合规提供了少见的经验数据，并评估了其面向 2027 年 CRA 执法的可扩展性。

## Problem
- 论文要解决的问题是：现有“compliance as code”研究很少，缺乏对真实合规规则库本身的系统经验分析，不清楚不同 Linux 发行版的规则覆盖、规则之间的相似性、所覆盖的安全控制，以及这些规则能否支撑新法规如 CRA。
- 这很重要，因为手工合规检查和系统加固难以规模化、易出错，而监管要求（尤其是欧盟 Cyber Resilience Act）正在增加，企业需要自动化、持续化的合规验证能力。
- 具体聚焦四个问题：五家 Linux 发行版供应方的规则覆盖是否不同；规则文本/代码是否相似；规则覆盖了哪些外部安全控制；规则能否映射到 CRA 基本网络安全要求。

## Approach
- 作者选取 ComplianceAsCode 项目在 2025-11-20 的归档数据，构建了覆盖 **5** 个供应方、**14** 个 Linux 发行版发布、**102** 个 guide、**1,504** 条唯一规则的数据集。
- 用描述性统计和 Kruskal-Wallis 检验比较不同供应方/版本之间的 guide 数、规则数、带 warning 的规则数和严重性分布差异。
- 为分析规则相似性，分别提取每条规则的简短 rationale 和代码片段，对它们做分词后用 **cosine similarity**，并分别采用 **TF** 与 **TF-IDF** 权重；核心想法很简单：看规则说明和脚本是否只是“换了几个词/参数的近似模板”。
- 为评估法规关联，作者将规则手工映射到已有研究定义的 **12** 类 CRA 基本要求分组，采用一对一映射；并对 **500** 条随机规则做三位作者盲评一致性验证，用 Cohen/Fleiss kappa 检查主观性。
- 还统计规则所引用的外部安全控制来源，分析其跨组织、跨标准的覆盖范围。

## Results
- 数据规模上，作者报告共 **102** 个 guides、**1,504** 条唯一规则，覆盖 **14** 个发行版、**5** 个供应方；每个发行版平均约 **12** 个 guides、**740** 条规则、**179** 条带 warning 的规则。
- 发行版覆盖存在显著差异：例如 **RHEL 10** 有 **1,000** 条规则，约占全部唯一规则的 **66%**；相比之下 **Debian 11** 仅 **51** 条、**Ubuntu 24.04** 为 **635** 条。跨供应方 Kruskal-Wallis 检验显示 guides、rules、rules-with-warnings 的差异具有统计显著性（分别为 **p=0.036, 0.031, 0.031**）。
- 规则严重性方面，多数规则属于 **medium**；跨供应方中只有 medium 类频数差异达到常用显著性水平（**p=0.031**），low/high/others 分别为 **p=0.087/0.054/0.209**，说明严重性结构总体更接近，而覆盖规模差异更大。
- 相似性分析表明：**代码片段比自然语言 rationale 更相似**，且 TF 会显示出比 TF-IDF 更多的相似性；作者未在给定摘录中提供具体平均相似度数值，但明确声称代码层存在一定模板化复用，而 rationale 之间没有统计上的相似性。
- 外部控制覆盖方面，规则映射到 **24** 类控制，来自 **10+** 个组织。覆盖最多的包括 **os-srg: 835** 条规则、**nist: 808**、**stigid: 734**、**stigref: 723**、**cis: 703**；其中多项控制横跨 **14** 个产品和 **5** 个供应方。
- 关于 CRA，作者声称这些规则**可以**映射到 CRA 的基本网络安全要求，因此现有项目有望通过新增检查来支持未来法规合规；但三位作者对单条规则映射的一致性只有**较 modest 的 agreement**。摘录未给出具体 kappa 数值，因此无法报告更精确的定量一致性结果。

## Link
- [http://arxiv.org/abs/2603.01520v1](http://arxiv.org/abs/2603.01520v1)
