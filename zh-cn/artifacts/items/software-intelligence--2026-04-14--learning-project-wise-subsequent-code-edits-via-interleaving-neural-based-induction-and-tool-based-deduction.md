---
source: arxiv
url: http://arxiv.org/abs/2604.12220v1
published_at: '2026-04-14T02:56:21'
authors:
- Chenyan Liu
- Yun Lin
- Yuhuan Huang
- Jiaxin Chang
- Binhang Qi
- Bo Jiang
- Zhiyong Huang
- Jin Song Dong
topics:
- project-wise-code-editing
- code-intelligence
- cross-file-refactoring
- llm-tool-integration
- interactive-code-assistance
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction

## Summary
## 摘要
TRACE 是一个面向项目级代码编辑的系统，把 LLM 预测和 IDE 工具结合起来，例如重命名和 def-use 分析。它主要处理跨文件的后续编辑，因为纯神经编辑器要么漏掉位置，要么扫描整个项目的成本太高。

## 问题
- 开发者经常做增量的、项目级的编辑，例如重构、修复 bug 和功能改动；论文引用的先前证据显示，这类改动占提交历史变更的 70% 以上。
- 现有工具在范围、准确率和速度之间存在权衡：局部编辑器在小范围内效果好，而项目级神经系统在定位上成本高，也可能漏掉或幻觉出跨文件编辑。
- Git diff 风格的编辑标签对训练来说太粗，因为一个 hunk 里可能包含多种编辑语义；作者测到这种情况占 18.04% 的 hunk。

## 方法
- TRACE 根据项目、先前编辑和可选提示，预测下一步编辑。
- 它把**神经归纳**和**工具演绎**交错使用：前者处理语义编辑，后者处理语法编辑模式。简单说，如果最近的编辑看起来像重命名、签名更新、克隆更新或诊断-修复模式，TRACE 就调用 IDE/LSP 工具去找相关编辑；否则它会在代码窗口上运行神经定位和生成模型。
- 系统有三个部分：编辑组合调用器，用来决定何时调用工具；编辑定位器，把行和行间空隙标成编辑目标；编辑生成器，负责写出代码改动。
- 论文还加入了一种更细的编辑表示，用 6 个标签代替常见的 3 个：`<KEEP>`、`<REPLACE>`、`<DELETE>`、`<NULL>`、`<INSERT>` 和 `<BLOCK-SPLIT>`。这样可以把一个 hunk 内混合的编辑语义分开。
- 这种表示方法先用 Tree-sitter 解析代码，再用 LCS 对齐新旧 token，然后分配行级和行间编辑标签。

## 结果
- 评估覆盖 **38K commits**、**678 个项目** 和 **5 种编程语言**。
- 与 **CoEdPilot、GrACE 和 CCT5** 等先前系统相比，TRACE 的**编辑定位精度提高 43.76%**、**召回率提高 9.96%**，**编辑生成准确率提高 11.16%**。
- 编辑组合调用器在决定是否调用工具时达到 **92.45% 精度** 和 **94.63% 召回率**。
- 新的编辑表示让神经**编辑定位器**提升 **14.57%**，**编辑生成器**提升 **7.40%**。
- 在交互式编辑模拟中，TRACE 将**时间成本降低 14.40%**，建议采纳率达到 **27.71%**；摘要还说它的采纳率比 Cursor 高 **6.15%**。
- 论文报告了一个包含 **24 名参与者**、**3 个任务** 的用户研究，并说 TRACE 在跨文件全局编辑上表现更好，但摘要没有给出详细的任务级数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12220v1](http://arxiv.org/abs/2604.12220v1)
