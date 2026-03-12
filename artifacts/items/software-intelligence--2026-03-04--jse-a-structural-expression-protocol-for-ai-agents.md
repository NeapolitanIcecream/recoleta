---
source: hn
url: https://news.ycombinator.com/item?id=47255567
published_at: '2026-03-04T23:41:43'
authors:
- mars_liu
topics:
- agent-protocols
- structured-output
- json-representation
- ai-orchestration
- tool-calling
relevance_score: 0.84
run_id: materialize-outputs
---

# JSE: A Structural Expression Protocol for AI Agents

## Summary
JSE 提出了一种把类似 S 表达式的结构化意图编码进标准 JSON 的轻量协议，目标是让 AI 代理更一致地表达调用、计划和变换。它强调既保持 JSON 兼容性，又提供比普通 JSON 数据模式更接近“可执行结构”的表示。

## Problem
- 现有 AI 系统虽然很容易生成 JSON，但 JSON 通常只被当作静态数据，难以统一表达推理计划、工具流水线、DSL 指令等结构化意图。
- 目前常见做法依赖临时 JSON schema、工具专用协议或嵌入代码字符串，导致表示方式碎片化、难复用、跨系统兼容性差。
- 这很重要，因为多代理协作、工具调用和结构化软件自动化都需要一种既机器可解释、又易于模型稳定生成的通用中间表示。

## Approach
- 核心方法是定义 **JSE (JSON Structural Expression)**：在**完全合法 JSON** 中编码 **S-expression 风格** 结构。
- 机制非常简单：以 `$` 开头的字符串视为符号，例如 `"$add"`；JSON 数组或对象可表示表达式；`$quote` 用于保留原始数据不被解释。
- 例如 ` ["$add", 1, 2] ` 表示一个结构化调用；对象形式如 `{"$call":"$search","query":"JSON S-expression","top_k":5}` 则可同时携带元数据与操作意图。
- 设计上不追求完整 Lisp 或图灵完备，而是作为一个最小规则集，让不同实现按需支持部分表达式空间。
- 其目标特性包括：确定性、机器可解释、易于 LLM 生成、便于人阅读、可嵌入提示词或 API 响应，并允许不理解 JSE 的系统仍把它当普通 JSON 处理。

## Results
- 文本**没有提供定量实验结果**，没有数据集、基准、准确率、延迟或与 JSON Schema / tool calling 的数值对比。
- 最强的具体主张是：JSE 保持 **100% valid JSON**，同时支持 S-expression 风格逻辑表达、元数据共存和 `$quote` 原始数据段。
- 作者声称 JSE 相比临时 schema 或工具专用格式，更适合作为统一的结构化意图表示，用于 **agent communication protocols、AI orchestration systems、structured reasoning traces、prompt-embedded DSLs、cross-model communication formats**。
- 从贡献性质看，这更像**早期协议/规范提案**而非经过实验验证的研究成果；当前状态是公开规范与示例，并主动征求 prior art、语义边界与可用性反馈。

## Link
- [https://news.ycombinator.com/item?id=47255567](https://news.ycombinator.com/item?id=47255567)
