---
source: arxiv
url: https://arxiv.org/abs/2607.09101v1
published_at: '2026-07-10T05:16:54'
authors:
- Quanjun Zhang
- Ye Shang
- Siqi Gu
- Jianyi Zhou
- Chunrong Fang
- Zhenyu Chen
- Liang Xiao
topics:
- unit-test-generation
- multi-agent-systems
- code-knowledge-graphs
- llm-software-engineering
- automated-testing
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-Agent LLM Collaboration for Unit Test Generation via Human-Testing-Inspired Workflows

## Summary
## 摘要
TestAgent 通过三个协作的 LLM 智能体和面向测试的仓库知识图谱生成单元测试。在六个 Java 项目上，它的覆盖率和变异得分高于 LLM 基线；该方法也扩展到了 Python，并以 92.22% 的精确率发现了 154 个真实世界缺陷。

## 问题
- 手动开发单元测试需要投入大量精力，而传统生成器生成的测试通常在可读性、可维护性和缺陷检测能力方面较弱。
- 现有 LLM 系统采用固定的生成流程和粗粒度上下文提取方式，难以根据执行反馈调整策略，也会遗漏推断测试需求所需的依赖关系。

## 方法
- 需求规划器分析目标方法，为正常、边界和异常情况创建测试需求。
- 测试生成器获取仓库上下文，编写测试，执行语法和编译检查，在沙箱中运行测试，分析失败原因，并修改测试。
- 测试审查器评估测试的正确性、覆盖率和需求匹配度，然后提出额外的测试场景。
- 静态分析构建仓库级知识图谱，其中包含代码依赖、测试专用实体、测试链接、摘要、测试报告和失败分析。
- 智能体按需调用检索、图谱更新、验证、覆盖率和变异分析工具，不再遵循单一的固定流程。

## 结果
- 在六个 Java 项目上，TestAgent 达到 97.46% 的执行率、92.34% 的行覆盖率、90.24% 的分支覆盖率和 83.69% 的变异得分。
- 在相同的 GPT-4o 基础模型下，TestAgent 在报告的六项指标上都优于 LLM 基线 ChatUniTest 和 HITS。
- 与基于搜索的工具 EvoSuite 相比，TestAgent 的变异得分显著更高，为 83.69%，而 EvoSuite 为 43.59%；两者的正确性相近。
- 消融实验显示，加入知识图谱后，行覆盖率提高了 22.31%，分支覆盖率提高了 24.52%，变异得分提高了 26.83%。
- 在 Python 项目上，TestAgent 达到 88.85% 的行覆盖率和 78.89% 的分支覆盖率，超过了 CodaMosa 和 CoverUp 报告的结果。
- 在非回归测试中，TestAgent 以 92.22% 的精确率检测出 154 个真实世界缺陷；工业项目实验和用户研究也表明该方法具有实际应用价值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09101v1](https://arxiv.org/abs/2607.09101v1)
