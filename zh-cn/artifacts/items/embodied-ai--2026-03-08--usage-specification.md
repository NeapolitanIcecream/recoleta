---
source: hn
url: https://usage.jdx.dev/spec/
published_at: '2026-03-08T23:48:27'
authors:
- birdculture
topics:
- cli-specification
- developer-tools
- command-line-interface
- kdl
- documentation-generation
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Usage Specification

## Summary
Usage 是一个用于定义命令行工具的规范与 CLI，可统一描述参数、标志、环境变量和配置文件。它试图成为类似 OpenAPI 之于 Web API 的 CLI 描述层，从而支持文档、补全和跨语言脚手架生成。

## Problem
- CLI 工具的参数、子命令、环境变量和配置逻辑通常分散在各语言/框架实现中，难以统一复用。
- CLI 生态里常见需求如自动补全、Markdown 文档、man page、跨框架迁移，往往需要重复开发，成本高且不一致。
- 缺少一个标准化的 CLI 规格会阻碍工具链互操作，这很重要，因为开发者和框架作者都需要可移植、可生成、可验证的 CLI 定义。

## Approach
- 提出一个名为 Usage 的声明式规范，用 KDL 编写 CLI 定义，统一描述元数据、flags、args、subcommands、别名等结构。
- 将环境变量、配置文件、默认值与命令行参数整合到同一规范中，并明确优先级顺序，例如 `CLI flag > env var > config file > default`。
- 提供配套 CLI 工具，可基于同一份规范生成自动补全脚本、Markdown 文档、man pages，并为任意语言提供更高级的参数解析输入。
- 面向 CLI 框架开发者，Usage 被定位为类似“CLI 的 LSP/OpenAPI”，使框架只需输出 Usage 定义，就能复用通用生态能力。
- 在兼容性上主要面向 GNU 风格 CLI；对非标准行为可考虑支持，但会给出不推荐警告。

## Results
- 文本**没有提供定量实验结果**，没有基准、数据集或数值指标可用于比较。
- 明确宣称可支持的产出包括 **3 类生成结果**：自动补全脚本、Markdown 文档、man pages。
- 规范可统一 **4 类输入来源**：命令行参数、环境变量、配置文件、默认值，并定义了确定性的优先级链路。
- 文中给出了 **2 个示例规格**：一个基础 CLI 定义示例、一个包含嵌套子命令和别名的复杂示例，说明其可表达常见 CLI 结构。
- 最强的具体主张是：开发者可用一份 Usage 规格在**不同 CLI 框架甚至不同语言之间**进行脚手架转换与能力复用，但文中未给出量化验证。

## Link
- [https://usage.jdx.dev/spec/](https://usage.jdx.dev/spec/)
