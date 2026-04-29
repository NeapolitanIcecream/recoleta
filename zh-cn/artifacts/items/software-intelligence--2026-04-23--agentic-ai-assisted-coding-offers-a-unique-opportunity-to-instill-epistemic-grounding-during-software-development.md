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
## 摘要
论文提出了 **GROUNDING.md**，这是一种按领域划分的文档，为编码代理提供明确的领域规则，并且这些规则优先于用户和项目指令。目标是在非专家使用智能体式编码工具时，仍然让 AI 生成的科学软件保持有效。

## 问题
- 智能体式编码可能生成表面上符合用户请求、但违反领域有效性规则的软件，例如在蛋白质组学中错误处理假发现率（FDR）。
- 现有的上下文文件，如 `plan.md`、项目规则和 `SKILL.md`，可以指导任务和方法，但不能强制执行领域层面的科学约束。
- 这很重要，因为定制科学软件越来越容易生成，而有效性检查仍然依赖专家知识，许多用户和代理可能并不具备这些知识。

## 方法
- 作者将 **GROUNDING.md** 定义为一种由社区治理、按领域划分的智能体软件开发基础文档。
- 它编码两类规则：**Hard Constraints (HCs)**，用于不可妥协的有效性要求；**Convention Parameters (CPs)**，用于会随时间变化的社区默认选择。
- 该文档设计为在推理时加载，并具有最高优先级，高于 `plan.md`、`AGENTS.md` 或 `CLAUDE.md` 等项目规则文件，以及 `SKILL.md` 等方法文件。
- 论文给出了一个蛋白质组学草案版本 `proteomics_GROUNDING.md`，其中包含功能正确性、算法效率、互操作性、测试、验证、溯源和 QC 的规则。
- 预期的代理行为是拒绝违反 HCs 的请求，引用被违反的规则，解释请求为何无效，并提出符合要求的替代方案。

## 结果
- 论文报告了使用 **Claude Code v2.1.90** 和 **NVIDIA Nemotron-3-Super-120B-A12B-FP8** 在隔离的全新会话中进行的**初步原理验证测试**。
- 代理对 HCs 的遵守情况通过 **6 个提示词** 进行测试，这些提示词旨在违反不同的硬约束；文中给出的成功条件是拒绝生成不合规代码，并引用相关 HC。
- 作者表示，在他们的测试中，使用 **system prompt** 加载 `GROUNDING.md` 比 XML 标记**更一致**。
- 他们还测试了与一个**对抗性 `CLAUDE.md`** 的冲突，该文件指示模型忽略科学有效性，并认为 `GROUNDING.md` 应在上下文层级中拥有最高优先级。
- 摘录中**没有提供总体准确率、拒绝率、通过/失败表或基准指标**，因此证据属于定性描述，而不是有测量结果的性能研究。
- 文中较强且具体的主张包括：阻止无效请求，例如范围过宽的修饰搜索；执行蛋白质组学中的有效性规则，如 FDR 约束；以及更好地记录溯源信息，例如软件版本和 `GROUNDING.md` 的 commit SHA。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21744v1](http://arxiv.org/abs/2604.21744v1)
