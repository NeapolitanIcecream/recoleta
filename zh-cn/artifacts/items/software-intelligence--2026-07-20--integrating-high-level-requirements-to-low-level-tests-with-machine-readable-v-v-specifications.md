---
source: arxiv
url: https://arxiv.org/abs/2607.17686v1
published_at: '2026-07-20T08:36:54'
authors:
- Mansur Arief
- Nur Ahmad Khatim
- Ali Akarma
- Ahmad Alfan Alfian Irfan
topics:
- requirements-traceability
- verification-validation
- software-testing
- ai-compliance
- executable-specifications
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications

## Summary
## 摘要
VNVSpec 通过机器可读的规范和可追溯图，将高层需求连接到可执行测试以及可用于审计的验证证据。该框架面向需要需求覆盖、标准映射和在开发者工作流中持续更新证据的软件与 AI 系统。

## 问题
- 高层需求和低层测试通常存在于不同工具中，导致团队无法可靠识别未覆盖的需求，也无法确定哪些证据支持某项标准条款。
- 对于 AI 驱动系统和信息物理系统而言，这一缺口十分关键，因为监管机构和安全标准要求提供可追溯证据，而原始的测试通过/失败结果缺少这种结构。

## 方法
- 将需求、危害、契约、标准映射、测试链接和证据表示为类型化、不可变对象，并存储在 Python、YAML 或 TOML 中。
- 将用户需求分解为具有明确度量指标和验收标准的模块级需求，然后通过有向无环可追溯图连接测试和其他验证活动。
- 通过 pytest 插件、用于 JavaScript、Java 和 C++ 测试运行器的 JUnit XML 导入、用于分析和形式化验证的证据收集器，以及面向 PyTorch 和 HuggingFace 模型的适配器，接入现有工具。
- 执行八项需求质量检查，以保守方式将证据汇总为通过、失败或结论不确定的判定，并导出开发者报告、合规矩阵、GSN 保证论证，以及 EU AI Act 附件 IV 文档框架。

## 结果
- 在自应用评估中，VNVSpec 持续评估自身的规范；该规范包含 36 项需求，并由 449 个测试验证。
- 论文指出，评估时间呈线性增长，在所述的有限时间评估条件下，该工作流可以处理最多 10,000 项需求；摘录未提供详细的运行时间数值。
- 五个示例目录共包含 116 项需求，其中 82 项至少映射到一条标准条款，占 71%。
- 该框架展示了来自普通 pytest 测试、通过 JUnit XML 导入的 Jest 结果，以及针对连续扰动范围内神经网络属性的基于 CROWN 的形式化边界的关联证据。
- 所提供的文本没有报告与其他可追溯性或需求管理系统的对比基准，也没有给出质量检查器检测率或集成开销的量化数据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.17686v1](https://arxiv.org/abs/2607.17686v1)
