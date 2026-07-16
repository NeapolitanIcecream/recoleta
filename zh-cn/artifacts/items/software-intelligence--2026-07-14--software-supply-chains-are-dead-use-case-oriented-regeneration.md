---
source: arxiv
url: https://arxiv.org/abs/2607.13021v1
published_at: '2026-07-14T17:58:09'
authors:
- Tanmay Singla
- James C. Davis
topics:
- code-intelligence
- automated-software-production
- software-supply-chain
- agentic-coding
- dependency-regeneration
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Software Supply Chains are Dead: Use-Case-Oriented Regeneration

## Summary
## 摘要
论文提出了面向用例的再生成（use-case-oriented regeneration）：代理只在本地重新实现仓库实际使用的依赖行为。在 180 个 JavaScript/TypeScript 仓库—依赖对上，该方法保留了几乎全部仓库观测到的验证行为，同时大幅缩减了暴露的 API 表面，但并未证明完全的语义等价性。

## 问题
- 对于狭窄的功能需求，复用软件包会迫使仓库继承未使用的代码、传递依赖、维护责任、兼容性约束和软件供应链风险。
- 生成式编码代理降低了本地实现的成本，因此有必要重新评估：何时应优先复用依赖，何时应采用由仓库自行维护的代码。
- 这一问题之所以重要，是因为移除依赖可以减少外部信任要求和攻击暴露面，但再生成的代码仍必须经过正确性和可维护性验证。

## 方法
- 将仓库—依赖对，而不是上游软件包，作为替换的基本单位。
- 向代理提供仓库上下文和验证材料；让代理识别依赖调用点、生成本地替代实现、更新调用方、移除依赖，并针对验证失败迭代修改。
- 以仓库观测到的等价性为目标：替代实现必须保留仓库实际使用的行为，而不是原软件包支持的所有行为。
- 对九个 JavaScript/TypeScript 依赖分别选取 20 个仓库进行评估，包括 nanoid、chalk、express、semver、lodash、axios、postcss、change-case 和 zod。

## 结果
- 在 180 个仓库—依赖对中，再生成代码实现了报告所称的 99.8% 总体验证通过率；其中 180 对中的 166 对保留了全部基线验证检查。
- 生成的替代实现将导出 API 表面平均缩减了 93.1%，从原始平均 82.1 个导出项降至再生成后的 5.6 个导出项，平均仅保留原表面的 6.9%。
- 对于边界明确的使用场景，结果最为突出：nanoid 和 zod 的 20 对样本均实现了完全保留，而 lodash 为 16/20，并贡献了报告中最多的失败次数，共 104 次。
- 论文描述了 14 次再生成失败，涉及语义和边界情况不匹配、类身份问题，以及 express 中间件和 axios 模拟拦截器等深度框架集成问题。
- 证据仅限于现有仓库验证材料和选定的公开仓库；通过这些检查并不能证明完全的语义等价性，也不能证明对未来使用场景的覆盖。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13021v1](https://arxiv.org/abs/2607.13021v1)
