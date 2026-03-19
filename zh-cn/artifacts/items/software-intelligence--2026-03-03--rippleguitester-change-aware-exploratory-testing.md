---
source: arxiv
url: http://arxiv.org/abs/2603.03121v1
published_at: '2026-03-03T15:56:49'
authors:
- Yanqi Su
- Michael Pradel
- Chunyang Chen
topics:
- gui-testing
- change-impact-analysis
- llm-for-testing
- differential-testing
- regression-detection
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# RippleGUItester: Change-Aware Exploratory Testing

## Summary
RippleGUItester是一种面向代码变更的GUI探索式测试系统：它从PR/Issue和补丁出发，推断哪些用户场景可能被波及，并在变更前后版本上做差分比较来发现回归。论文核心贡献是把LLM驱动的变更影响分析、场景扩展与多模态GUI差分检测结合起来，用于发现传统测试和代码评审漏掉的变更诱发缺陷。

## Problem
- 软件频繁演化时，单次代码修改常会引入新的用户可见缺陷；作者对Firefox **97,347**个PR分析发现，**11,910**个PR引入新bug，占**12.2%**。
- 现有回归测试/CI多依赖预定义路径，探索式测试又缺少“围绕本次代码变更该测什么”的系统性指导，因此容易漏掉**跨场景副作用**、稀有事件序列和特殊测试数据触发的缺陷。
- 这类缺陷的判定标准也很难手工编码：GUI变化可能是预期改动，也可能是回归，需要结合变更意图来理解。

## Approach
- 从给定PR出发，收集**变更意图**（PR描述、关联Issue）与**代码变更**（补丁、修改文件），并通过历史traceability找出同代码区域的**preceding change intents**，用于覆盖潜在跨场景影响。
- 用LLM做**change-impact analysis**，生成面向终端用户的初始测试场景：简单说，就是让模型根据“这次改了什么、为什么改”推断“哪些用户操作路径可能受影响”。
- 用历史issue/PR构建**Scenario Knowledge Base**，检索并注入替代事件序列；再由LLM补全/实例化所需**测试数据**，把抽象场景变成可执行场景。
- 执行时，LLM把高层场景步骤翻译成GUI动作指令（如click/input/scroll），在隔离容器中分别运行于**pre-change**和**post-change**版本。
- 检测时做**differential analysis**：比较前后版本截图中的视觉差异，并结合自然语言变更意图解释这些差异，以区分**预期行为更新**和**非预期bug**。

## Results
- 在**4**个真实软件系统上评估：**Firefox、Zettlr、JabRef、Godot**；测试对象为**hundreds of real-world code changes**（摘要/引言给出定性规模，摘录未提供更细分计数）。
- RippleGUItester共发现**26**个此前未知且在最新版本中仍存在的bug，这些问题此前被**existing test suites、CI pipelines、code review**漏检。
- 报告后处置结果：**16**个已修复，**2**个已确认，**6**个仍在讨论，**2**个被标记为预期行为。
- 运行成本方面，平均每个PR需要**54.8 minutes**和**$5.99**。
- 论文还声称其是**first change-aware GUI testing system**，可在代码合并前或刚合并后更早发现GUI回归。

## Link
- [http://arxiv.org/abs/2603.03121v1](http://arxiv.org/abs/2603.03121v1)
