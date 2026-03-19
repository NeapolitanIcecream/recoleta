---
source: hn
url: https://github.com/janbjorge/gyml
published_at: '2026-03-08T22:55:51'
authors:
- jeeybee
topics:
- configuration-language
- yaml-subset
- json-semantics
- parser-tooling
- python-library
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: GYML – YAML syntax, JSON semantics, zero runtime dependencies

## Summary
GYML 提出一种更严格、可预测的配置语言：保留 YAML 的缩进书写方式，但采用 JSON 的类型语义，并且没有运行时依赖。它的目标是减少 YAML 因隐式类型转换、重复键和高级特性带来的生产事故。

## Problem
- YAML 规范复杂且实现差异大，包含隐式类型转换、锚点、别名、标签等特性，容易导致“看起来像字符串，实际被解析成别的类型”的错误。
- 典型例子是 *Norway Problem*：`NO` 在 YAML 1.1 中可能被解析为布尔值 `false`，这会让配置、国家代码或标识符等场景产生隐蔽 bug。
- 配置文件需要可预测、易调试、低依赖的解析行为；否则会在软件工程与生产系统中引发难以排查的问题。

## Approach
- 核心机制很简单：**只保留 YAML 的块缩进语法，丢弃大部分会制造歧义的 YAML 能力，并强制使用 JSON 风格的类型语义**，做到“写什么就是什么”。
- 每种类型只允许一种规范写法：布尔值只能是 `true`/`false`，空值只能是 `null`，数值只接受十进制整数/浮点，字符串使用双引号表示保留字场景。
- 仅支持块风格结构；拒绝 flow mapping/sequence（如 `{a: 1}`、`[a, b]`），但允许空字面量 `{}` 和 `[]`。
- 在词法层面直接拒绝 anchors、aliases、tags，并把重复键设为硬错误；同时要求严格 2 空格缩进、禁止 Tab。
- 实现上返回原生 Python 对象（`dict/list/str/int/float/bool/None`），并提供精确到行列的错误信息和 `.gyml -> JSON` CLI 转换能力。

## Results
- 文中**没有提供标准基准测试、精度/速度/吞吐等量化实验结果**，因此没有可报告的学术型数值指标。
- 规格复杂度对比上，作者强调 YAML 有 **211 个 grammar productions、10 个章节**；GYML 则将规则压缩为可放在“sticky note”上的一小组约束，主打可理解性与可预测性。
- 功能约束上，GYML 明确宣称：**所有合法 GYML 都是合法 YAML，但反之不成立**；这是一种通过“严格子集化”换取稳定语义的设计突破。
- 工程行为上，解析结果会直接得到 Python 原生类型；示例中 `port: 8080` 解析为 `int 8080`，`debug: false` 解析为 `bool False`，避免被当作字符串或被隐式错误转换。
- 错误报告上，作者声称可精确定位到 **line/column**，例如 `port: 0xFF` 会报 `line 1, col 7` 并说明不允许十六/八/二进制字面量。
- 项目还宣称 **zero runtime dependencies**、完整类型标注、测试/ruff/type-check 必须全部通过，体现其面向生产配置解析的工程化定位。

## Link
- [https://github.com/janbjorge/gyml](https://github.com/janbjorge/gyml)
