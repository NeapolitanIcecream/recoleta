---
source: hn
url: https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html
published_at: '2026-06-13T22:31:40'
authors:
- mooreds
topics:
- rails
- jruby
- partial-evaluation
- program-compilation
- benchmarking
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# The Ruby JRuby Was Built to Run

## Summary
## 摘要
这篇文章认为，Roundhouse 可以把 Rails 应用转成更简单的 Ruby 代码，让 JRuby 跑得比原生 Rails 快得多。这个结果重要，因为它给现有 Rails 应用提供了一条同时提高吞吐量和扩大部署范围的路径。

## 问题
- Rails 应用在每次请求时都会重复做一些不会随请求变化的工作，比如路由解析、SQL 字符串构建、模板查找和类型转换。
- JRuby 已经在某些情况下加速了标准 Rails，但它仍然在运行原来的、依赖元编程的框架代码。
- 问题在于，只改变运行时而不改应用本身，和连应用一起编译，哪个能带来更大的收益。

## 方法
- Roundhouse 读取 Rails 应用，在转译时做出与请求无关的决策。
- 它会生成多个语言的独立项目，包括 Ruby，因此生成后的应用可以直接在 JRuby 上运行，而不改应用逻辑。
- 生成的 Ruby 只保留每个请求会变化的部分，比如请求格式、flash 状态和实际数据库内容。
- 一个 compare gate 会把生成输出和 Rails 输出对比，保证在测量到的端点上行为一致。
- 这个基准测试把原生 Rails 和生成的 Ruby 放在 CRuby+YJIT 与 JRuby 上比较，用的是同一个小型 Rails 8 博客应用。

## 结果
- 在 HTML 索引端点上，原生 Rails 在 CRuby+YJIT 上是 481 req/sec，在 JRuby 上是 1,057 req/sec，只换运行时就带来 2.2× 的吞吐提升。
- 在同一个端点上，生成的应用比 CRuby+YJIT 上的 Rails 快 11×，比 JRuby 上的 Rails 快 25×。
- 在 JSON 端点上，原生 Rails 在两个运行时之间大致持平：CRuby+YJIT 为 1,272 req/sec，JRuby 为 1,080 req/sec。
- 在 JSON 端点上，生成的应用比 CRuby+YJIT 上的 Rails 快 6×，比 JRuby 上的 Rails 快 43×。
- 全部对照里，JRuby 上的生成 Ruby 相比 CRuby+YJIT 上的原生 Rails 最高达到 54×。
- 文章还报告了 JRuby 更高的内存占用，大约是 1–1.5 GB RSS，而 CRuby 为 135–416 MB。

## Problem

## Approach

## Results

## Link
- [https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html](https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html)
