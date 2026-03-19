---
source: hn
url: https://news.ycombinator.com/item?id=47255567
published_at: '2026-03-04T23:41:43'
authors:
- mars_liu
topics:
- structured-output
- json-format
- agent-protocol
- s-expression
- llm-tooling
relevance_score: 0.15
run_id: materialize-outputs
language_code: zh-CN
---

# JSE: A Structural Expression Protocol for AI Agents

## Summary
JSE 提出一种把类似 S 表达式的“结构化意图”编码进标准 JSON 的轻量协议，目标是让 AI 更稳定地输出可解释、可执行的结构，而不依赖特定工具调用接口。它本质上是一个早期格式规范，而不是经过实验验证的模型或系统论文。

## Problem
- 现有 AI 系统虽然擅长生成 JSON，但 JSON 通常只被当作数据容器，不擅长直接表达“意图、计算、计划、DSL 指令”等结构化操作。
- 目前这类需求常靠临时 JSON schema、工具专用协议或嵌入代码字符串来实现，导致表示方式分散、协议耦合强、跨系统复用差。
- 这很重要，因为 agent 编排、工具链调用、结构化推理轨迹和跨模型通信都需要一种统一、机器可解释且模型容易生成的表达格式。

## Approach
- 核心方法是定义 **JSE（JSON Structural Expression）**：在**保持 100% 合法 JSON** 的前提下，用少量约定把 JSON 解释为类似 S-expression 的结构。
- 最简单机制是：**以 `$` 开头的字符串视为 symbol**，再用 **JSON 数组或对象表示表达式/调用结构**；例如 `["$add", 1, 2]` 表示一个加法表达式。
- 对象形式支持把**元数据与表达式共存**，例如 `{"$call":"$search","query":"JSON S-expression","top_k":5}` 可表示带参数的结构化调用。
- 通过 **`$quote`** 机制可标记原始数据区域，避免所有内容都被当作可执行表达式解释。
- 设计上刻意**不追求完整 Lisp 或图灵完备**，而是让不同实现按需支持表达式子集，以便嵌入提示词、API 响应和 agent 协议中。

## Results
- 文本**没有提供实验、基准或定量结果**；没有数据集、准确率、延迟、成本或与 JSON Schema / tool calling / MCP 的数值对比。
- 最强的具体主张是该格式可保持 **100% valid JSON**，同时表达 **S-expression style logic**。
- 作者声称 JSE 相比临时 schema 或工具专用协议，能提供更**统一**的 structured intent representation，用于 reasoning plans、tool pipelines、structured transformations、query languages 和 cross-model communication。
- 设计目标上的具体优势主张包括：**deterministic、machine interpretable、easy for LLMs to generate、easy for humans to read**，但这些均为规范层面的宣称，未给出实证验证。

## Link
- [https://news.ycombinator.com/item?id=47255567](https://news.ycombinator.com/item?id=47255567)
