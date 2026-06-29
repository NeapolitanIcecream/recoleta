---
source: arxiv
url: https://arxiv.org/abs/2606.23197v1
published_at: '2026-06-22T11:44:58'
authors:
- Sophie Corallo
- Debora Grupp
- "Dominik Fuch\xDF"
- Jan Keim
- Frederik Reiche
- Tobias Hey
- Anne Koziolek
topics:
- secure-software-engineering
- requirements-traceability
- code-intelligence
- software-architecture
- security-dataset
- ev-charging
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# The EVerest Dataset for Secure Software Engineering

## Summary
## 摘要
EVerest 是一个公共数据集，用于电动汽车充电软件栈中跨需求、架构、文档和代码的端到端安全工程。它的主要贡献在于覆盖多类工件并提供细粒度安全标签；论文没有报告模型基准分数。

## 问题
- 安全验证需要把自然语言需求连接到架构和实现；缺少这些链接可能让不安全的认证令牌存储等缺陷漏检。
- 以往数据集分别覆盖需求、代码或漏洞。在作者的调研中，没有数据集同时提供需求、架构、代码和安全目标标签。
- 这对代码智能和可追溯性研究很重要，因为模型需要把安全意图连接到架构元素和源代码的真实标注。

## 方法
- 作者基于 EVerest 构建了该数据集。EVerest 是一个开源电动汽车充电站软件栈。源代码快照为 2024-06-03 的 everest-core，包含约 50 kloc，分布在 500 多个文件中，约有 40 名贡献者。
- 他们向 EVerest 社区发送问卷，以引出初始安全需求。7 名参与者提交了 67 条需求；清理后保留 57 条，并按安全目标标注。
- 他们通过 4 次各 90 分钟的开发者访谈细化粗粒度需求，产出 93 条组件级安全需求。后续需求检查后，数据集中保留 84 条安全需求。
- 他们从源代码推导出 Palladio 架构模型，覆盖 29 个组件、34 个接口、144 条服务效果规约和 14 个使用场景。
- 3 名标注者标注了 1,445 个安全元素、接受窗口、引用、共指和架构追踪链接。标注工作耗时约 100 人时。

## 结果
- 数据集包含 84 条人工引出的安全需求、1,445 个细粒度安全元素标签、一个架构模型、源代码和自然语言文档。
- 安全元素标签包括 195 个组件、105 个数据项、41 个节点、143 个实体、597 个状态、36 条连接、51 条数据流、207 个活动和 70 条控制流。
- 追踪链接黄金标准为类实体元素包含模型元素 ID。论文报告了 77 个已追踪的组件提及、32 个已追踪的数据提及和 3 个已追踪的实体提及。
- 架构模型包括 29 个组件、34 个接口、144 条服务效果规约和 14 个使用场景，包括固件更新、充电器启用或禁用操作，以及限制配置。
- 在数据集构建过程中，作者发现了一个真实的 CWE-1295 弱点：PN532TokenProvider 模块的 auth_token_providerImpl.cpp 中以明文存储认证令牌。他们向 PIONIX 披露了该问题，问题随后得到修复。
- 论文没有报告准确率、F1、MAP 或其他模型基准结果。论文的证据来自数据集规模、相较于调研数据集的工件覆盖范围，以及发现的安全弱点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23197v1](https://arxiv.org/abs/2606.23197v1)
