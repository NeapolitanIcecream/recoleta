---
source: hn
url: https://digg.com/tech
published_at: '2026-06-12T23:12:27'
authors:
- ahmedfromtunis
topics:
- multi-agent-software-engineering
- prompt-engineering
- code-generation
- agent-coordination
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Digg

## Summary
## 总结
这段摘录展示了一个用于多智能体代码生成和任务拆分的提示模板。它的重点是要求模型先写出一个目标，再并行启动多个 agent，并把它们的输出合并成最终的软件产物。

## 问题
- 这个提示试图把一个模糊的构建请求改写成一个具体的软件任务，补上功能、行为和输出格式细节。
- 它针对的是 agent 编码里的协调问题：如何拆分工作、同时运行各部分，以及把结果合并起来。

## 方法
- 把用户请求改写成一个结构化的构建提示，里面包含 thing、technology、features、interaction、mood、visuals、environment、effects 和 output format 的占位符。
- 先给模型创建一个新的目标，而不是只照着原始请求执行。
- 并行启动多个 agent，给每个 agent 分配一个专门的目标，把工作拆成独立部分。
- 同时派发这些部分，并在结果返回时合成中间输出。

## 结果
- 这段摘录没有报告定量结果、基准测试或数据集对比。
- 它的具体主张是：把工作拆成独立部分并在之后合并时，并行 agent 可以把任务做得“更好、更快”。
- 它还主张，这种提示能通过强制写出功能、交互、视觉风格和文件类型等明确要求，产出更详细的软件结果。

## Problem

## Approach

## Results

## Link
- [https://digg.com/tech](https://digg.com/tech)
