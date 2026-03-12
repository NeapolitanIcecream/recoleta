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
- security-controls
- automated-compliance
- cyber-resilience-act
relevance_score: 0.58
run_id: materialize-outputs
---

# Compliance as Code: A Study of Linux Distributions and Beyond

## Summary
本文对一个真实的“compliance as code”开源项目做了大规模实证分析，研究 Linux 发行版中的合规规则覆盖、规则相似性、外部控制框架覆盖以及与欧盟 CRA 要求的映射关系。它的重要性在于说明合规检查可以被程序化，并为 2027 年起实施的 Cyber Resilience Act 自动化合规提供前期证据。

## Problem
- 论文要解决的问题是：现有“compliance as code”研究很少，缺乏对真实合规规则库的经验性分析，不清楚不同 Linux 发行版的规则覆盖、复用模式和监管适配能力如何。
- 这很重要，因为手工合规检查难扩展、易出错，而网络连接产品中的操作系统即将受到 CRA 等法规约束，自动化与持续合规会越来越关键。
- 作者还特别关注：这些现有规则能否支撑未来法规更新，尤其是 CRA 的基本网络安全要求。

## Approach
- 以 ComplianceAsCode 项目为案例，采集了 **102** 个 guide、覆盖 **14** 个 Linux 发行版版本、来自 **5** 个 vendor/community 的 **1,504** 条唯一规则。
- 通过描述统计和 **Kruskal-Wallis** 检验，比较不同 vendor/release 的 guide、rule、warning 与严重性分布差异。
- 将规则的简短 rationale 与代码片段分别做 **cosine similarity** 分析，使用 **TF** 和 **TF-IDF** 权重，判断规则在文本解释与实现层面的相似程度。
- 统计规则所引用的外部 security controls，发现覆盖 **24** 类 control、来自 **10+** 个组织，包括 NIST、DISA、CIS、ISO、ANSSI、BSI、PCI SSC 等。
- 手工把规则映射到 **12** 类 CRA 基本要求组，并用 **500** 条随机规则的三作者盲评与 kappa 一致性检查来评估主观性；作者说明个别映射一致性仅为“适度”。

## Results
- 数据规模上，论文分析了 **1,504** 条唯一规则和 **102** 个 guide；每个 release 平均约 **740** 条规则、**12** 个 guide、**179** 条带 warning 的规则。覆盖差异明显：**RHEL 10** 拥有 **1,000** 条规则，约占全部唯一规则的 **66%**；而 **Debian 11** 仅 **51** 条，**Ubuntu 24.04** 为 **635** 条。
- 统计检验显示不同 vendor 的覆盖差异显著：guides 的 Kruskal-Wallis **p=0.036**，rules **p=0.031**，rules with warnings **p=0.031**；严重性方面仅 **medium** 类显著（**p=0.031**），low/high/others 不显著（分别 **p=0.087/0.054/0.209**）。
- 平均来看，约略低于 **1/4** 的规则带有 warnings；严重性分布上，大多数规则被标为 **medium**，各发行版总体模式相近。
- 相似性分析表明：规则的**代码片段**比自然语言 rationale **更相似**，而两者相似性彼此**不相关**；作者未给出统一阈值或完整数值表，但明确指出 TF 比 TF-IDF 检出更多相似，且代码复用/模板化现象明显。
- controls 覆盖方面，规则可映射到 **24** 类 control、**10+** 家组织；高覆盖 control 包括 **os-srg: 835** 条规则、**nist: 808**、**stigid: 734**、**stigref: 723**、**cis: 703**，显示该项目已连接多个主流安全基线与标准。
- 关于法规适配，作者声称这些规则**可以映射到 CRA 的基本网络安全要求**，从而说明项目未来可扩展以支持新的自动化合规检查；但在 **500** 条样本的人工验证中，三位作者对单条规则映射的 agreement 只有**适度/有限一致性**，说明这一部分仍带有较强解释性。

## Link
- [http://arxiv.org/abs/2603.01520v1](http://arxiv.org/abs/2603.01520v1)
