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
TRACE 是一个项目级代码编辑系统，把 LLM 预测与 IDE 工具（如重命名和 def-use 分析）结合起来。它面向跨文件后续编辑，这类编辑中，纯神经编辑器要么会漏掉位置，要么扫描整个项目的成本过高。

## 问题
- 开发者经常进行渐进式、项目级的编辑，如重构、修复缺陷和功能变更；论文引用既有证据称，这类编辑占提交历史变更的 70% 以上。
- 现有工具需要在范围、准确率和速度之间取舍：局部编辑器在小范围内效果较好，而项目级神经系统在定位相关位置时成本较高，也可能遗漏或臆造跨文件编辑。
- 用于训练的 Git-diff 风格编辑标签过于粗糙，因为一个 hunk 里可能包含多种编辑语义；作者测得这种情况占 18.04%。

## 方法
- TRACE 根据项目、先前编辑和可选提示来预测下一次编辑。
- 它交替使用**神经归纳**来处理语义编辑，使用**工具演绎**来处理句法编辑模式。简单说，如果最近的编辑看起来像重命名、签名更新、克隆更新或诊断-修复模式，TRACE 就会调用 IDE/LSP 工具来查找相关编辑；否则，它会在代码窗口上运行神经定位和生成模型。
- 系统包含三个部分：决定何时调用工具的编辑组合调用器、将代码行和行间空隙标为编辑目标的编辑定位器，以及编写代码改动的编辑生成器。
- 论文还提出了一种更细粒度的编辑表示，用 6 个标签替代常见的 3 个：`<KEEP>`、`<REPLACE>`、`<DELETE>`、`<NULL>`、`<INSERT>` 和 `<BLOCK-SPLIT>`。这能区分同一个 hunk 内混合出现的编辑语义。
- 这种表示的构建方式是：先用 Tree-sitter 解析代码，再用 LCS 对齐新旧 token，然后为代码行和行间位置分配编辑标签。

## 结果
- 评估覆盖 **3.8 万个 commits**、**678 个项目** 和 **5 种编程语言**。
- 与 **CoEdPilot、GrACE 和 CCT5** 等已有系统相比，TRACE 将**编辑定位精确率提升 43.76%**、**召回率提升 9.96%**，并将**编辑生成准确率提升 11.16%**。
- 编辑组合调用器在决定是否调用工具时达到 **92.45% precision** 和 **94.63% recall**。
- 新的编辑表示让神经**编辑定位器提升 14.57%**，让**编辑生成器提升 7.40%**。
- 在交互式编辑模拟中，TRACE 将**时间成本降低 14.40%**，并达到 **27.71% 的建议接受率**；摘要还称，其接受率**比 Cursor 高 6.15%**。
- 论文报告了一项用户研究，包含 **24 名参与者** 和 **3 个任务**，并称 TRACE 在跨文件全局编辑上表现最好，但给出的摘录没有提供任务层面的详细数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12220v1](http://arxiv.org/abs/2604.12220v1)
