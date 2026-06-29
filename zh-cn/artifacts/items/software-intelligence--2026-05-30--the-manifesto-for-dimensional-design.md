---
source: hn
url: https://dimensionaldesign.org/
published_at: '2026-05-30T23:09:09'
authors:
- etothepii
topics:
- ai-validation
- software-engineering
- human-ai-interaction
- document-processing
- workflow-design
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# The Manifesto for Dimensional Design

## Summary
## 总结
Dimensional Design 认为，AI 系统应该处理可以接受近似答案的任务，而确定性软件或小规模人工检查应该把关那些需要精确答案的地方。它的主要贡献是一份围绕预测型 AI 的设计宣言，讨论验证、文件格式和审查任务。

## 问题
- 预测型 AI 会产出看起来合理但错误的结果；链式步骤会累积错误，所以逐行审查和多数投票都可能漏掉缺陷。
- Word、PowerPoint 和 PDF 等格式里的隐藏结构会给 AI 留下更多需要保持的状态，这会在编辑时增加出错风险。
- 这会影响软件和文档工作流，因为 AI 生成的内容量可能超过既有审查流程能检查的范围。

## 方法
- 按容错程度分工：在“可能正确”可以接受的地方用 AI，在需要精确性的地方用确定性检查。
- 在独立维度上验证输出，例如把数字化发票金额和印刷总额对比，而不是重新读取每一项。
- 把确定性程序当作通过/失败的闸门；如果 AI 输出未通过，就重新生成，直到通过。
- 协作时把内容保留为纯文本或其他低维形式；在发布时再用确定性工具添加格式和版式。
- 如果无法做确定性验证，就把人工审查做得很小、逐项列出并记录下来。

## 结果
- 这段内容没有给出任何实证基准：没有数据集、基线、样本量、准确率、运行时间或消融结果。
- 它给出一个 99/100 正确率的例子，用来说明逐行审查无法可靠发现那 1 个错误输出。
- 它指出，像发票总额核对和复式记账中的借贷平衡这样的独立检查，可以在不重读每一项的情况下发现错误。
- 它列出 4 个价值取向和 8 条面向 AI 辅助工作的原则：把近似任务和精确任务分开，使用确定性闸门，做独立验证，并在发布前保持内容的低维形式。

## Problem

## Approach

## Results

## Link
- [https://dimensionaldesign.org/](https://dimensionaldesign.org/)
