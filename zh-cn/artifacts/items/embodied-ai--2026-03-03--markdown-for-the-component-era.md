---
source: hn
url: https://mdxjs.com/
published_at: '2026-03-03T23:45:04'
authors:
- mjtk
topics:
- markdown
- mdx
- jsx-components
- documentation-tooling
- build-time-compilation
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Markdown for the Component Era

## Summary
这不是一篇机器人或机器学习研究论文，而是 MDX 的产品/技术说明页面。它介绍了如何在 Markdown 中嵌入 JSX 组件，以便编写可交互的长文档内容。

## Problem
- 解决的问题是：传统 Markdown 适合写文档，但难以原生表达交互式、组件化内容，如图表、提示框和可复用 UI。
- 这很重要，因为现代内容系统、文档站点和前端应用越来越依赖组件化开发，纯 Markdown 的表达能力不足。
- 对给定的机器人研究主题而言，相关性很低，因为内容聚焦文档编写与前端工具链，而非 embodied AI 或机器人模型。

## Approach
- 核心机制是把 **JSX 直接嵌入 Markdown**，让作者在写 Markdown 时也能导入并使用前端组件。
- MDX 允许在文档中 `import` 组件、导出变量，并在正文中像写 React/JSX 一样插入组件，例如交互式图表。
- 它采用 **构建时编译**，官方称“no runtime”，也就是在构建阶段把 MDX 转成可执行内容，而不是在运行时额外解析。
- 它支持与多种框架和构建工具集成，如 Next.js、Vite、Docusaurus、Rollup、esbuild、webpack，以及 React/Preact/Vue 生态。
- MDX 3 进一步加入 ES2024 支持、`await` in MDX，并移除旧 Node 版本支持（需 Node 16+）。

## Results
- 文本**没有提供标准研究实验、数据集或量化 benchmark 结果**，因此没有可报告的论文式数值提升。
- 最具体的版本更新声明是：**MDX 3 需要 Node 16 或更高版本**，并新增 **ES2024 支持** 与 **await in MDX** 支持（前提是框架也支持）。
- 官方给出的主要能力主张包括：可在 Markdown 中嵌入 JSX 组件、可自定义 markdown 构造对应的渲染组件、并且 **“all compilation occurs during the build stage”**，即无运行时开销声明。
- 页面还声称其适配“most bundlers, frameworks, and editors”，并列举了 Docusaurus、Next.js、Vite、Rollup、esbuild、webpack、React、Preact、Vue 等，但**未给出覆盖率数字或性能对比**。

## Link
- [https://mdxjs.com/](https://mdxjs.com/)
