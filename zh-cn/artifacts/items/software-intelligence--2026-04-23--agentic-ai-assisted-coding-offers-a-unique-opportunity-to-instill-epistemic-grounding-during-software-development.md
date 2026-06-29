---
source: arxiv
url: http://arxiv.org/abs/2604.21744v1
published_at: '2026-04-23T14:50:35'
authors:
- Magnus Palmblad
- Jared M. Ragland
- Benjamin A. Neely
topics:
- agentic-coding
- code-intelligence
- context-engineering
- scientific-software
- epistemic-grounding
- proteomics
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic AI-assisted coding offers a unique opportunity to instill epistemic grounding during software development

## Summary
## 总结
这篇论文提出 **GROUNDING.md**，一种按领域划分的文档，给编码代理明确的领域规则，并且这些规则优先于用户和项目指令。目标是在非专家使用代理式编码工具时，仍然让 AI 生成的科学软件保持有效。

## 问题
- 代理式编码可以生成符合用户请求的软件，但同时会破坏领域有效性规则，比如在蛋白质组学中对假发现率（FDR）的处理错误。
- 现有的上下文文件，如 `plan.md`、项目规则和 `SKILL.md`，能指导任务和方法，但不能强制执行领域级的科学约束。
- 这很重要，因为定制科学软件越来越容易生成，而有效性检查仍然依赖专家知识，很多用户和代理都可能缺少这种知识。

## 方法
- 作者将 **GROUNDING.md** 定义为一个由社区治理、按领域划分的 grounding 文档，用于代理式软件开发。
- 它编码两类规则：**Hard Constraints (HCs)**，用于不可协商的有效性要求；**Convention Parameters (CPs)**，用于社区默认选择，这些选择可能随时间变化。
- 该文档设计为在推理时以最高优先级加载，优先于 `plan.md`、`AGENTS.md` 或 `CLAUDE.md` 等项目规则文件，以及 `SKILL.md` 等方法文件。
- 论文提供了一个蛋白质组学版本草案 `proteomics_GROUNDING.md`，其中包含功能正确性、算法效率、互操作性、测试、验证、来源记录和 QC 的规则。
- 预期的代理行为是：拒绝违反 HCs 的请求，引用被违反的规则，解释请求为何无效，并给出符合要求的替代方案。

## 结果
- 论文报告了在隔离的新会话中，使用 **Claude Code v2.1.90** 和 **NVIDIA Nemotron-3-Super-120B-A12B-FP8** 进行的**初步概念验证测试**。
- 代理的 HC 遵从性通过 **6 个提示词** 进行了测试，这些提示词旨在违反不同的硬约束；给定的成功标准是拒绝生成不符合要求的代码，并引用相关 HC。
- 作者表示，在他们的测试中，用 **system prompt** 加载 `GROUNDING.md` 比 **XML 标记** 更一致。
- 他们还测试了与一个**对抗性的 `CLAUDE.md`** 的冲突，该文件要求模型忽略科学有效性，并主张 `GROUNDING.md` 应该在上下文层级中具有最高优先级。
- 摘要中**没有**给出汇总准确率、拒绝率、通过/失败表或基准指标，所以这些证据是定性的，而不是一次有测量指标的性能研究。
- 具体且明确的主张包括：阻止过于宽泛的修改搜索请求，执行蛋白质组学有效性规则，如 FDR 约束，以及更好地记录来源信息，例如软件版本和 `GROUNDING.md` 的 commit SHA。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21744v1](http://arxiv.org/abs/2604.21744v1)
