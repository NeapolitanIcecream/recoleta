---
source: hn
url: https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/
published_at: '2026-07-11T23:05:50'
authors:
- s1291
topics:
- coding-agents
- code-migration
- mathematical-visualization
- human-ai-collaboration
- educational-software
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Old and new apps, via modern coding agents

## Summary
## 摘要
现代编码代理在几小时内帮助作者恢复了约两 dozen 个已经废弃的 Java 数学小程序，并制作了新的交互式可视化工具。这段经历表明，在人工引导下，AI 编码可以让非关键的教学和研究可视化工具更易于维护和制作。

## 问题
- 1999 年制作的 Java 小程序在网页标准停止支持相应版本的 Java 后无法使用，使原本有用的数学可视化工具无法访问。
- 手工编写新的可视化软件耗时较长。作者此前曾因此放弃过一些项目，例如狭义相对论编辑器。

## 方法
- 作者使用现代 AI 编码代理，将旧的 Java 小程序移植到 JavaScript，并更新了图形效果。
- 他引导代理制作了一个新的狭义相对论可视化工具，其设计参考了类似 Inkscape 的闵可夫斯基空间编辑器。
- 他用同样的流程制作了 Gilbreath 猜想的可视化工具，并计划在今后的论文中附上类似工具。
- 作者亲自测试这些应用并审查生成的代码。由于这些工具属于辅助工具，不是关键组件，他接受了少量残留错误带来的风险。

## 结果
- 约两 dozen 个旧小程序在几小时内恢复运行，其中包括蜂窝结构和 Besicovitch 集的可视化工具。
- 移植后的应用中发现了一个小错误：在一个复分析小程序中，将对象拖到主框之外时，拖动事件的行为不符合预期。
- 代理发现了原始代码中的两个错误，而作者此前并不知道这些错误。按作者的评估，修复和新增错误相抵后，代码质量大致没有变化。
- 一个此前被放弃的狭义相对论可视化工具在几小时的 AI 辅助编码后完成；Gilbreath 猜想的可视化工具又经过几小时制作完成。
- 摘录没有报告正式基准测试、用户研究或量化质量指标。现有证据主要来自作者的实际测试，以及这些应用成功上线并恢复使用。

## Problem

## Approach

## Results

## Link
- [https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/](https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/)
