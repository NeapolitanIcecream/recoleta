---
source: arxiv
url: https://arxiv.org/abs/2607.08981v1
published_at: '2026-07-09T23:01:54'
authors:
- Viraaji Mothukuri
- Reza M. Parizi
topics:
- code-intelligence
- software-foundation-model
- automated-software-production
- static-analysis
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# The Patchwork Problem in LLM-Generated Code

## Summary
## 摘要
论文定义了“拼 patch 问题”：LLM 生成的代码可以通过局部检查，却违反整个代码库的结构约束。论文提出基于图的不变量检查，用于发现跨文件、配置、依赖、资源、控制流和安全连接方面的故障，而这些故障经常无法被标准 CI 发现。

## 问题
- 生成的代码可能通过编译和测试，却引用缺失的配置键、不存在的软件包、未定义的资源、不兼容的模式，或未受保护的路由。
- 对于跨越多个文件和代码库构件的故障，类型检查、测试和 SAST 工具的覆盖范围有限。
- 这些缺陷可能一直隐藏到部署阶段才暴露。人类需要审查或整合大量 AI 生成代码时，这种风险尤其明显。

## 方法
- 将代码库构件建模为八类相互协同的图：导入图、调用图、依赖图、配置图、模式图、资源图、控制流图和路由图。
- 定义八类结构故障及其明确的一致性不变量，其中包括虚构依赖、虚构的内部 API、跨文件契约违规和安全结构回归。
- 使用混合验证器：将语言特定的检查交给 mypy、tsc、pylint 和 ESLint，同时使用自定义检测器检查现有工具无法覆盖的跨图约束。
- 通过 PyPI 和 npm 验证依赖，检查配置和资源引用，比较生产者与消费者的模式，并检查路由防护的覆盖情况。
- 生成局部化证据轨迹，其中包含被违反的不变量、受影响的文件和代码行，以及保持结构一致性所需的约束。

## 结果
- 评估涵盖 2 个前沿模型在 4 种提示策略下生成的 336 个样本。
- 论文称，大多数结构故障无法被类型检查、测试和 SAST 发现，但摘要没有提供故障率、精确率、召回率或基线比较数据。
- 2 个模型的故障特征存在定性差异，这对假设模型无关错误模式的缓解方法提出了挑战。
- 对 43 个真实世界 AI 生成代码库的外部验证表明，结构故障也会出现在受控实验之外。
- 最明确的具体主张是覆盖范围：该验证器针对八类代码库图和八类结构故障，其中包括传统 CI 无法检测的故障。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08981v1](https://arxiv.org/abs/2607.08981v1)
