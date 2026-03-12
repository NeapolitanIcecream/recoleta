---
source: hn
url: https://github.com/janbjorge/gyml
published_at: '2026-03-08T22:55:51'
authors:
- jeeybee
topics:
- config-language
- yaml-subset
- json-semantics
- parser-design
- zero-dependencies
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: GYML – YAML syntax, JSON semantics, zero runtime dependencies

## Summary
GYML 提出一种 **YAML 语法、JSON 语义** 的严格配置格式子集，目标是消除 YAML 常见的隐式类型转换、重复键和高级特性带来的生产事故。它强调可预测性、易读性和零运行时依赖，定位为更安全的配置解析方案。

## Problem
- 传统 YAML 过于复杂：规范包含 **211 个语法产生式**、多种标量写法、anchors/aliases/tags，以及因实现不同而变化的隐式类型转换规则。
- 这种灵活性会导致真实 bug，例如著名的 **Norway Problem**：`NO` 在 YAML 1.1 中会被解析为布尔值 `False`，而不是字符串。
- 配置文件中的重复键、隐式类型、流式写法和“像程序一样”的特性会降低可预测性，进而影响生产系统稳定性，因此这个问题很重要。

## Approach
- 核心方法是把 GYML 设计成 **YAML 的严格子集**：任何合法 GYML 都是合法 YAML，但大量合法 YAML 在 GYML 中会被拒绝。
- 它保留 YAML 的块缩进书写体验，但采用 **JSON 的类型语义**：布尔值只能写 `true/false`，空值只能写 `null`，数值使用十进制整数/浮点，字符串使用双引号，做到“写什么就是什么”。
- 它显式禁用复杂特性：拒绝 **anchors (`&`)、aliases (`*`)、tags (`!!`)**，不支持流式映射 `{a:1}` 和流式序列 `[a,b]`，从源头减少歧义和副作用。
- 它强化配置安全性：**重复键直接报错**，缩进必须是 **2 空格的倍数**，禁止 tab；解析失败时返回精确的行列号和修复提示。
- 实现层面返回原生 Python 类型（`dict/list/str/int/float/bool/None`），且主打 **zero runtime dependencies**，降低集成复杂度。

## Results
- 文本**没有提供标准基准测试、准确率、吞吐量或性能数字**，因此不存在可核验的定量 SOTA 结果。
- 明确的设计性结果是：将 YAML 中大量易出错特性收缩为一套可记忆的规则，作者概括为“规则可以写在一张便签上”。
- 与通用 YAML 相比，GYML 声称消除了隐式类型惊喜，例如 `port: 8080` 会解析为 `int`，`debug: false` 会解析为 `bool`，而不是字符串。
- 对非法输入会给出精确错误定位；示例中 `port: 0xFF` 会在 **line 1, col 7** 报错，并明确指出 **hex/octal/binary literals are not allowed**。
- 在语义约束上，它宣称提供若干强保证：**每种类型一种写法**、**重复键为硬错误**、**tabs 全部拒绝**、**anchors/aliases/tags 在词法阶段就拒绝**。
- 工程结果方面，项目支持将 `.gyml` 转换为格式化 JSON，并要求测试、lint、format、type-check **四项检查全部通过** 后才接受变更，但未给出覆盖率或质量指标数字。

## Link
- [https://github.com/janbjorge/gyml](https://github.com/janbjorge/gyml)
