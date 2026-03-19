---
source: hn
url: https://mdxjs.com/
published_at: '2026-03-03T23:45:04'
authors:
- mjtk
topics:
- mdx
- markdown-jsx
- component-authoring
- frontend-tooling
- documentation
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# Markdown for the Component Era

## Summary
MDX 是一种把 Markdown 与 JSX 结合的内容编写与编译方案，用于在长文档中直接嵌入可复用组件。它面向组件化前端生态，强调内容表达能力、构建期编译和与主流框架/工具链的集成。

## Problem
- 传统 Markdown 适合静态文档，但难以原生表达交互式图表、提示框等组件化内容。
- 纯 JSX/前端代码虽然灵活，但对长文档写作不够简洁，降低内容生产效率与可读性。
- 在现代前端与文档系统中，需要一种同时兼顾 **易写作**、**可组合**、**可集成** 的内容格式，这对软件文档、知识库和开发者内容生产很重要。

## Approach
- 核心方法是把 **JSX 直接嵌入 Markdown**：用户主要写 Markdown，只在需要交互或复用 UI 时插入 JSX 组件。
- 支持 **导入组件与变量**，例如在文档中导入 `Chart` 并传入参数，从而把内容与界面逻辑组合在一起。
- 采用 **构建期编译** 而非运行时解释，官方明确称“no runtime”，即编译发生在 build 阶段，以获得更轻量的产物与更快执行。
- 提供 **可定制的 Markdown 渲染映射**，可指定某类 Markdown 结构应渲染为哪个组件，例如自定义 `h1` 对应组件。
- 面向现有生态集成，兼容多种 bundler、framework 和 editor，如 Next.js、Vite、webpack、esbuild、React、Vue 等。

## Results
- 文本未提供标准论文式实验或基准测试，因此 **没有量化精度/速度/效果指标** 可报告。
- 明确产品性结果包括：**MDX 3** 发布，升级点包含 **Node 16+** 支持要求、加入 **ES2024** 支持、支持 **`await` in MDX**（前提是框架支持）、并移除若干废弃选项。
- 官方声称其主要优势是：**Powerful**（Markdown+JSX 融合）、**Everything is a component**、**Customizable**、**Markdown-based**、以及 **“no runtime, all compilation occurs during the build stage”**。
- 集成覆盖面上的具体主张包括支持多数主流工具链与框架，例如 **Docusaurus / Next.js / Vite / Rollup / esbuild / webpack / React / Preact / Vue**。
- 最强的具体能力声明是：可在 Markdown 文档中直接嵌入类似交互图表的组件，并把其他 MDX 文件作为组件导入复用。

## Link
- [https://mdxjs.com/](https://mdxjs.com/)
