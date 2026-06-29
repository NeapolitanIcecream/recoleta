---
source: hn
url: https://www.jay.ai/blog/ultracoding-the-next-frontier
published_at: '2026-06-15T23:53:18'
authors:
- _jayhack_
topics:
- multi-agent-software-engineering
- code-intelligence
- automated-software-production
- human-ai-interaction
- agent-network
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Ultracoding: The Next Frontier

## Summary
## 摘要
Ultracoding 认为，软件智能体可以在代码执行环境中生成其他智能体，从而扩大软件工作的处理规模。文章提出了一种方案，也观察了市场动向；摘录中没有受控评估。

## 问题
- 大型重构和新软件项目可能超出单个聊天智能体的处理能力，因为这类工作需要并行搜索、编辑、测试和审查。
- 这一点很重要，因为测试覆盖率高的代码库可以把工作拆给多个智能体，再用测试和人工检查合并后的结果。
- 当前用于监督大型智能体群的人机界面较弱；列表和看板为审查和分诊提供的上下文有限。

## 方法
- 给在代码模式中运行的智能体提供一个 `spawn agent` 工具，使它能在任务过程中创建工作智能体。
- 让主智能体在运行时选择工作结构：启动多少个智能体、每个智能体做什么、如何检查输出。
- 使用扇出/扇入工作方式：多个智能体并行编辑或调查，然后由另一个步骤验证、归并，或请求人工批准。
- 将智能体层级与面向具体任务的监督界面配合使用，例如 ClickUp 或 Linear 工作流、批量批准界面，或用于审查的自定义 HTML 应用。

## 结果
- 摘录中没有提供定量基准结果、数据集分数、运行时间数字或准确率指标。
- 文章引用了 3 个公开例子作为该模式的证据：Bun 从 Zig 到 Rust 的重构、Monty 转向 subprocess pool，以及 Cursor 用一群智能体从零构建浏览器。
- 文章称，当测试覆盖率足够高、能够支持自动验证和人工审查时，该方法适用于大型代码重构和 0-1 项目。
- 文章将 RLMs 称为递归调用 LLM 的早期学术证据；摘录没有给出基准名称或分数。
- 文章预测，到 2026 年下半年会出现更强的监督界面惯例，智能体会为人工操作员生成面向具体任务的审查应用。

## Problem

## Approach

## Results

## Link
- [https://www.jay.ai/blog/ultracoding-the-next-frontier](https://www.jay.ai/blog/ultracoding-the-next-frontier)
