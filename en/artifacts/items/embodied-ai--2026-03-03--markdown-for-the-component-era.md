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
language_code: en
---

# Markdown for the Component Era

## Summary
This is not a robotics or machine learning research paper, but a product/technical overview page for MDX. It explains how to embed JSX components in Markdown so that interactive long-form content can be written.

## Problem
- The problem it solves is that traditional Markdown is suitable for writing documents, but it is difficult to natively express interactive, component-based content such as charts, alerts, and reusable UI.
- This is important because modern content systems, documentation sites, and frontend applications increasingly rely on component-based development, while plain Markdown has insufficient expressive power.
- For the given robotics research topic, the relevance is very low, because the content focuses on documentation authoring and frontend tooling rather than embodied AI or robot models.

## Approach
- The core mechanism is to **embed JSX directly in Markdown**, allowing authors to import and use frontend components while writing Markdown.
- MDX allows components to be `import`ed in documents, variables to be exported, and components to be inserted in the body just like writing React/JSX, such as interactive charts.
- It uses **build-time compilation**; the official wording is "no runtime," meaning MDX is converted into executable content during the build stage rather than being additionally parsed at runtime.
- It supports integration with multiple frameworks and build tools, such as Next.js, Vite, Docusaurus, Rollup, esbuild, webpack, and the React/Preact/Vue ecosystem.
- MDX 3 further adds ES2024 support, `await` in MDX, and removes support for older Node versions (requires Node 16+).

## Results
- The text **does not provide standard research experiments, datasets, or quantitative benchmark results**, so there are no paper-style numerical improvements to report.
- The most specific version-update claims are that **MDX 3 requires Node 16 or later** and adds support for **ES2024** and **await in MDX** (provided the framework also supports it).
- The main capability claims given officially include embedding JSX components in Markdown, customizing which rendering component corresponds to each markdown construct, and **"all compilation occurs during the build stage"**, i.e., a claim of no runtime overhead.
- The page also claims compatibility with "most bundlers, frameworks, and editors," and lists Docusaurus, Next.js, Vite, Rollup, esbuild, webpack, React, Preact, and Vue, but **does not provide coverage figures or performance comparisons**.

## Link
- [https://mdxjs.com/](https://mdxjs.com/)
