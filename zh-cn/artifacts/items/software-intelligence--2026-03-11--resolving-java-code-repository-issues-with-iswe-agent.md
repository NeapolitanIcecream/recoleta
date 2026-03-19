---
source: arxiv
url: http://arxiv.org/abs/2603.11356v1
published_at: '2026-03-11T22:43:55'
authors:
- Jatin Ganhotra
- Sami Serhan
- Antonio Abu Nassar
- Avraham Shinnar
- Ziv Nevo
- Martin Hirzel
topics:
- java-issue-resolution
- software-engineering-agent
- static-analysis-tools
- react-agents
- code-repair
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Resolving Java Code Repository Issues with iSWE Agent

## Summary
本文提出 iSWE Agent，一个面向 Java 代码仓库 issue 自动修复的专用智能体，通过把“定位问题位置”和“生成修改”拆成两个子智能体，并结合规则式静态分析工具，提高 Java 场景下的自动修复效果与成本效率。

## Problem
- 现有自动 issue 修复系统大多围绕 Python 优化，Java 上表现明显较弱，但 Java 在企业软件中非常重要。
- Java 代码通常涉及更多跨文件修改、强静态类型和依赖构建流程，导致仅靠通用 LLM 或轻量工具更难可靠修复问题。
- 研究问题是：Java issue 修复是否需要语言特定知识与工具，以及这种设计能否在公开基准上显著提升成功率与效率。

## Approach
- 将任务拆成两个 ReAct 子智能体：**localization agent** 先根据 issue 描述和代码库定位应修改的文件/类/方法；**editing agent** 再基于这些位置生成补丁。
- 为定位子智能体提供 7 个**只读 Java 静态分析工具**，如文件/类/方法/符号查询、继承层次、调用者、调用链，底层基于 CLDK 和 Tree-Sitter。
- 定位结果先由 LLM 输出简化 JSON，再用**规则式 sanitizer** 补全行号、作用域并消解矛盾，降低纯 LLM 输出的不稳定性。
- 编辑子智能体使用**merge-conflict 风格 search-replace** 生成补丁，并对候选修改做分层校验：格式检查、匹配修复、Java linter、最后在容器中执行项目构建/编译。
- 整体设计强调“**规则 + 模型**”结合：更少依赖任意 bash/code 执行，减少副作用、降低迭代次数，并尽量只在必要时启用容器化环境。

## Results
- 论文声称 iSWE 在 **Multi-SWE-bench Java 子集（128 个实例）** 和 **SWE-PolyBench Java 子集（165 个实例）** 上都达到**最先进（state-of-the-art）或接近榜首**的 issue resolution rate。
- 总评测覆盖 **293 个 Java 实例（128 + 165）**，是作者用于支撑结论的主要实验规模。
- 成本方面，作者声称在**使用相同基础 LLM** 时，iSWE 的模型 API 推理费用比其他领先智能体低 **2× 到 3×**。
- 文中还说明结果部分分析了**localization precision/recall** 以及按 issue 复杂度的细分表现，但在给定摘录中**没有提供这些指标的具体数值**。
- 在定性层面，论文的最强主张是：Java 专用工具链不仅提升修复成功率，还能减少 LLM 轮次、降低副作用风险，并更适配企业级 Java 仓库。

## Link
- [http://arxiv.org/abs/2603.11356v1](http://arxiv.org/abs/2603.11356v1)
