---
source: arxiv
url: https://arxiv.org/abs/2606.24446v1
published_at: '2026-06-23T11:27:35'
authors:
- Frank Reyes
- Benoit Baudry
- Martin Monperrus
topics:
- code-repair
- ast-transformation
- dependency-updates
- coding-agents
- java-maven
- software-maintenance
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Generation of AST Transformation Rules for Fixing Breaking Updates

## Summary
## 摘要
BigBag 生成可执行的 Java AST 转换程序，用来修复由破坏性依赖更新导致的编译失败。论文的主要主张是，同一个生成的转换可以修复受同一次库更新影响的多个客户端项目。

## 问题
- Dependabot 和 Renovate 等依赖更新工具可以修改版本，但在更新后的库删除方法、变更签名或移动类型时，它们不会修复客户端代码。
- 现有修复方法通常为单个项目生成补丁，因此同一个 API 破坏需要在每个受影响项目中再次修复。
- 这很重要，因为 Maven 客户端即使在小版本和补丁版本发布中也可能出错；针对单个项目的重复修复无法扩展到使用同一次库更新的多个项目。

## 方法
- BigBag 向编码代理提供一个已损坏的 Maven 客户端项目、新依赖 API 文档、一个 Java AST 引擎模板，以及该 AST 引擎的 Javadoc。
- 代理运行 `mvn compile`，读取编译器错误，编写一个独立的 Java 转换，将其应用到客户端源代码树，并根据构建反馈重复这一过程。
- 生成的程序遍历 AST，找到对已损坏 API 的使用，将其重写为匹配新 API 的形式，并输出修改后的源文件。
- 论文测试了两个 AST 引擎：Spoon v11.2.1 和 JavaParser v3.27.1，并使用了四个模型：GPT-5.4-mini、Qwen3-30B、DeepSeek-v3.2 和 Gemini-3.1-Pro。
- BigBag 在代理循环之外重新应用每个生成的转换，然后在受同一次依赖更新影响的其他项目上测试已验证的转换。

## 结果
- 评估使用了 BUMP 中 157 个导致编译失败的破坏性依赖更新，覆盖 69 个客户端项目和 70 个库。
- 数据集包含 3 个补丁更新（1.9%）、63 个小版本更新（40.1%）和 91 个主版本更新（58.0%）。主版本更新的编译错误中位数为 5，最大值为 100；小版本更新的中位数为 2，最大值为 35。
- 在 8 种模型与引擎配置中，最佳配置达到 94.3% 的可编译转换率。
- 将生成的转换应用到原始已损坏客户端后，最佳配置达到 78.6% 的修复率。
- 生成的转换可跨项目迁移，整体跨项目修复率为 33.3%。
- 对于所有客户端都以相同方式使用受影响 API 元素的破坏性更新，跨项目修复率达到 80% 或更高；JavaParser 通常表现更好，引擎选择会使可编译转换率最多相差 17.8 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24446v1](https://arxiv.org/abs/2606.24446v1)
