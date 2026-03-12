---
source: hn
url: https://usage.jdx.dev/spec/
published_at: '2026-03-08T23:48:27'
authors:
- birdculture
topics:
- cli-specification
- developer-tooling
- command-line-interface
- cross-language
- arg-parsing
relevance_score: 0.6
run_id: materialize-outputs
---

# Usage Specification

## Summary
Usage 是一个用于定义命令行工具的规范与 CLI，目标是把 CLI 的参数、标志、环境变量和配置文件统一描述成可移植的声明式规格。它相当于 CLI 领域的 OpenAPI/LSP，可用于生成补全、文档、man page，并作为跨语言 CLI 框架的中间表示。

## Problem
- 论文/规范要解决的是：CLI 工具的接口定义通常分散在不同语言和框架实现里，导致文档、补全、解析器和配置支持重复开发且难以统一。
- 这很重要，因为 CLI 是软件开发和运维中的基础交互层；如果没有统一规格，开发者需要为每个框架和 shell 单独维护帮助信息、补全脚本和参数解析逻辑。
- 现有 CLI 生态缺少类似 OpenAPI 之于 Web API 的标准描述层，阻碍了跨语言复用、工具链自动生成和一致的人机交互体验。

## Approach
- 核心方法是定义一个声明式 Usage spec：用 KDL 编写 CLI 的元数据、flag、位置参数、子命令，以及环境变量、配置文件和默认值映射。
- 该 spec 充当 CLI 的“单一事实来源”：同一份定义可以被用来生成自动补全脚本、Markdown 文档、man pages，或驱动不同语言中的高级参数解析器。
- 规范支持嵌套子命令、别名、隐藏别名、全局标志、计数标志等常见 GNU 风格 CLI 结构，并显式表达值来源优先级，如 `CLI flag > env var > config file > default`。
- 对框架开发者而言，它被定位为类似“CLI 的 LSP/OpenAPI”：框架只需输出 Usage 定义，就可复用 Usage CLI 生成多 shell 补全和文档，而无需重复实现这些外围能力。
- 该方法明确限定适用范围：主要面向标准 GNU-style CLI，不追求覆盖所有非标准命令行行为，但允许对不推荐模式给出兼容与警告。

## Results
- 文本未提供实验数据、基准测试或定量评测结果，因此没有可报告的准确数值提升。
- 明确声称可从同一份 spec 生成 **3 类** 直接产物：autocompletion scripts、Markdown documentation、man pages。
- 明确声称同一规范可覆盖 **4 类** 输入来源定义：arguments、flags、environment variables、config files，并支持它们的优先级组合。
- 明确声称可将 **1 份** spec 脚手架到不同 CLI framework，甚至不同编程语言，以减少重复实现。
- 兼容性方面的最强具体主张是：主要支持标准 GNU-style options；对某些非标准行为未来可能“允许但警告”，说明其设计重点是实用一致性而非完全表达能力。

## Link
- [https://usage.jdx.dev/spec/](https://usage.jdx.dev/spec/)
