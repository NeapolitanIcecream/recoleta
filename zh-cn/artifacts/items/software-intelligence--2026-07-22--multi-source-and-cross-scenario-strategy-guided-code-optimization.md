---
source: arxiv
url: https://arxiv.org/abs/2607.20353v1
published_at: '2026-07-22T16:38:56'
authors:
- Yuwei Zhao
- Qianyu Xiao
- Ye Cui
- Yijun Yu
- Yingfei Xiong
topics:
- code-optimization
- large-language-models
- cross-scenario-transfer
- static-analysis
- software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-Source and Cross-Scenario Strategy-Guided Code Optimization

## Summary
## 总结
MoST 是一个基于 LLM 的代码优化框架，它结合来自提交记录和技术文档的证据，并将优化策略迁移到不同的编程语言和体系结构。根据报告，在历史任务和真实项目上，与 SemOpt 和 Codex 相比，MoST 生成了更多与开发者补丁等价的补丁，并取得了更大的性能提升。

## 问题
- 现有的策略引导型优化器主要挖掘历史提交记录，因此无法利用手册、教材或网页文档中描述的策略。
- 这些方法通常只能针对源示例所代表的语言和体系结构生成规则，限制了策略在不同场景（例如从 C 迁移到 Rust）之间的复用。
- 这一问题之所以重要，是因为低效代码会增加执行时间、资源消耗、运营成本和面向用户的延迟，而许多实际优化需要进行超出编译器级变换的源代码修改。

## 方法
- MoST 将异构输入转换为“证据对象”，其中包含自然语言策略描述、优化前后的代码示例、适用场景标签和来源类型。
- 它使用自平衡加权密度聚类，使质量更高但出现频率较低的文档证据不会被噪声较多或重复的提交证据淹没。
- 当某个策略缺少目标语言或体系结构的示例时，MoST 会从其他场景迁移示例，并首先检查该策略是否适用于目标场景。
- 它根据目标场景的示例生成 Semgrep 规则，并要求每条规则匹配优化前的代码、拒绝优化后的代码，以此验证规则，然后再用规则引导 LLM 生成补丁。
- 该实现处理了 48,440 个源自提交记录的证据对象和 189 个源自文档的证据对象，生成了 356 个策略簇，其中包括 39 个跨场景策略簇。

## 结果
- 在包含 351 个历史优化任务的基准测试中（151 个 C/C++、150 个 Python 和 50 个 Rust 任务），MoST 生成的补丁中，与开发者补丁完全匹配的数量比 SemOpt 多 24.44%–180.00%。
- 在同一基准测试中，MoST 生成的、与开发者补丁语义等价的补丁数量比 SemOpt 多 21.88%–37.50%。
- 在 15 个真实项目上，MoST 实现了 19.72%–717.42% 的最大性能提升和 4.44%–258.17% 的平均性能提升，优于 SemOpt 和 Codex。
- 报告中的表格显示，生成的规则库覆盖了各目标场景，每个场景包含 730 至 9,735 条 Semgrep 规则，其中有 24–137 个策略簇完全通过其他场景的证据添加。
- 摘录未提供各基线方法的详细得分、统计显著性数值或完整的消融实验结果；摘录还指出，在进行完全匹配过滤后，策略库构建所使用的数据与评测数据之间可能仍存在部分重叠。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.20353v1](https://arxiv.org/abs/2607.20353v1)
