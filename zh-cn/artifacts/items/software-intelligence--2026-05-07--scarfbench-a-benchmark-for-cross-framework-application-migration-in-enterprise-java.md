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
ScarfBench 是一个基准，用来测试编码代理能否在保持行为一致的前提下，在 Spring、Jakarta EE 和 Quarkus 之间迁移企业 Java 应用。现有代理很少能完成这些迁移，即使代码能编译并部署也一样。

## 问题
- 企业 Java 的框架迁移需要协调修改构建文件、依赖注入、持久化、HTTP 处理、部署和运行时配置。
- 现有编码基准大多测试缺陷修复、功能开发、版本升级或同栈现代化，因此没有覆盖跨框架应用重构。
- 这个问题有现实意义，因为长期运行的 Java 系统经常需要迁移到更新的运行时，而失败的迁移可能在编译、启动或用户可见行为上出错。

## 方法
- ScarfBench 包含 34 个应用家族，由 Java 专家分别用 Spring、Jakarta EE 和 Quarkus 实现，形成 102 个框架特定变体和 204 个有向迁移任务。
- 每个任务都会给代理一个可运行的源应用和一个目标框架；代理必须生成一个与源行为等价的目标实现，且不能看到专家写出的目标版本。
- 基准包含 29 个聚焦的单层应用和 5 个完整应用，总计约 151K 行配对 Java 代码，分布在 1,946 个源文件和测试文件中。
- 评估会重新构建候选实现，将其部署到目标容器或 Docker Compose 栈中，并在可观察接口上运行应用特定的行为测试。
- 论文还通过 LLM 标注和专家裁决，总结出 13 类失败原因，覆盖构建、部署和测试阶段。

## 结果
- 最强的聚焦层得分是 15.3% 的总体行为测试通过率；最强的完整应用得分是 12.2%。
- 204 个有向迁移任务中，只有 1 个产出了完全行为等价的目标实现。
- 在启用技能后，带有 Opus-4.6 的 Claude Code 在完整应用上的表现最好：编译成功率 87%，部署成功率 40%，测试成功率 12%。
- 在启用技能的聚焦应用上，Claude Code 的编译成功率达到 93%，而带有 Gemini-3.1-Pro 的 Gemini CLI 的部署成功率为 61%，测试成功率为 15%。
- 目标框架会影响迁移结果：迁移到 Jakarta EE 目标时，行为测试通过率只有 2%；Spring 目标为 12%，Quarkus 目标为 14%；57% 的 Jakarta 目标迁移尝试在编译阶段失败。
- 技能对可运行性的帮助大于对行为的一致性：对 Gemini 的聚焦任务来说，部署成功率从没有技能时的 7% 升到启用技能后的 61%，测试成功率从 2% 升到 15%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06754v2](https://arxiv.org/abs/2605.06754v2)
