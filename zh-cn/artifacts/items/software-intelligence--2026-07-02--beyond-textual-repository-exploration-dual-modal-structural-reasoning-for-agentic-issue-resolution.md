---
source: arxiv
url: https://arxiv.org/abs/2607.01929v1
published_at: '2026-07-02T09:23:48'
authors:
- Jiayi Zhang
- Kai Huang
- Yang Liu
- Chunyang Chen
topics:
- code-intelligence
- software-agents
- program-repair
- swe-bench
- multimodal-reasoning
- repository-graphs
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Textual Repository Exploration: Dual-Modal Structural Reasoning for Agentic Issue Resolution

## Summary
## 摘要
DualView 为软件问题修复代理加入可视化和文本图视图，让代理在编辑代码前检查仓库结构。论文称这提升了 SWE-bench 性能，其中报告的最佳运行解决了 388 个 SWE-bench Pro 实例。

## 问题
- 问题修复代理把大量工作预算用于阅读仓库文本；论文称，在 SWE-bench Verified 上，一个编码代理 76.1% 的 token 预算用于通过 grep 和 cat 等工具读取文件。
- 只用文本探索会让代理在许多步骤中反复重建模块链接、调用路径、类继承和局部数据流，这可能导致在大型仓库中漏掉需要定位的位置。
- 现有基于图的代码工具常把图序列化为文本，这会遮蔽多跳路径、扇入和扇出，以及密集依赖区域。

## 方法
- DualView 为代理提供四种可查询的图视图：用于子系统的 Module Coupling Graph、用于调用方到被调用方路径的 Function Call Graph、用于继承和实现关系的 Class Hierarchy Graph，以及用于语句级数据流和控制流的 Program Dependence Graph。
- 每次查询都会从同一个图切片返回两个同步输出：一张渲染后的节点-边图像，以及一条简洁的文本记录，包含名称、路径、行号、关系类型和查询范围。
- 代理在需要结构信息时使用这些图工具，然后回到搜索、文件检查和编辑等常规工具，处理源码级工作。
- 简单说，DualView 让代理先查看代码库地图，再用文本标签打开正确的文件和行。

## 结果
- 在 SWE-bench Pro 上，DualView 报告最多解决 388 个实例。
- 在使用 OpenCode 和 Kimi K2.5 的 SWE-bench Pro 上，DualView 比论文所述的基线配置多解决 46 个实例。
- 论文称，在 SWE-bench Pro 和 SWE-bench Verified 上，收益覆盖多种代理架构和模型家族，但摘录没有给出完整的逐模型表格。
- 消融实验称，可视化图输出优于等价的文本图描述，且可视化加文本的图输出组合效果最好；摘录没有给出精确的消融数字。
- 论文把该接口封装为可复用工具和 MCP 服务，并称实现已作为开源发布。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01929v1](https://arxiv.org/abs/2607.01929v1)
