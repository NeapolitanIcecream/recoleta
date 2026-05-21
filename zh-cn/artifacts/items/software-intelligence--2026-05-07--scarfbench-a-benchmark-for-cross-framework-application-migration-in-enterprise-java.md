---
source: arxiv
url: https://arxiv.org/abs/2605.06754v2
published_at: '2026-05-07T16:05:35'
authors:
- Advait Pavuluri
- Bridget McGinn
- Ashita Saxena
- George Safta
- Srikanth Tamilselvam
- Raju Pavuluri
- Michele Merler
- Baishakhi Ray
- Rahul Krishna
topics:
- cross-framework-migration
- enterprise-java
- coding-agents
- software-benchmarks
- behavior-preserving-refactoring
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java

## Summary
## 摘要
ScarfBench 是一个基准，用于测试编码智能体能否在 Spring、Jakarta EE 和 Quarkus 之间迁移企业 Java 应用并保持行为一致。当前智能体很少能完成这些迁移，即使生成的代码能够编译和部署。

## 问题
- 企业 Java 框架迁移需要同时修改构建文件、依赖注入、持久化、HTTP 处理、部署和运行时配置。
- 现有编码基准主要测试缺陷修复、功能开发、版本升级或同一技术栈内的现代化，因此没有覆盖跨框架应用重构。
- 这个问题有实际影响，因为长期运行的 Java 系统经常需要迁移到更新的运行时，迁移出错可能导致编译失败、启动失败或用户可见行为异常。

## 方法
- ScarfBench 包含 34 个由 Java 专家在 Spring、Jakarta EE 和 Quarkus 中实现的应用族，共有 102 个框架特定变体和 204 个定向迁移任务。
- 每个任务向智能体提供一个可运行的源应用和一个目标框架；智能体必须在看不到专家目标实现的情况下创建行为等价的目标实现。
- 该基准包含 29 个聚焦单层应用和 5 个完整应用，合计约 151K 行配对 Java 代码，分布在 1,946 个源文件和测试文件中。
- 评估会重新构建候选实现，将其部署到目标容器或 Docker Compose 栈中，并通过可观察接口运行应用特定的行为测试。
- 论文还归纳了构建、部署和测试阶段的 13 类失败，并结合 LLM 标注和专家裁定。

## 结果
- 聚焦层任务的最高汇总行为测试通过率为 15.3%；完整应用的最高得分为 12.2%。
- 在 204 个定向迁移任务中，只有 1 个生成了完全行为等价的目标实现。
- 启用 skills 后，Claude Code with Opus-4.6 在完整应用运行中表现最好：编译成功率 87%，部署成功率 40%，测试成功率 12%。
- 在启用 skills 的聚焦应用上，Claude Code 的编译成功率达到 93%，而 Gemini CLI with Gemini-3.1-Pro 的部署成功率达到 61%，测试成功率达到 15%。
- 迁移目标会影响结果：目标为 Jakarta EE 的迁移只有 2% 能通过行为测试，相比之下，目标为 Spring 的迁移为 12%，目标为 Quarkus 的迁移为 14%；57% 的 Jakarta 目标尝试在编译阶段失败。
- skills 对可运行性的帮助大于对行为一致性的帮助：在 Gemini 的聚焦任务中，部署成功率从未启用 skills 时的 7% 上升到启用 skills 后的 61%，测试成功率从 2% 上升到 15%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06754v2](https://arxiv.org/abs/2605.06754v2)
