---
source: hn
url: https://theconsensus.dev/p/2026/03/12/mojos-not-yet-python.html
published_at: '2026-03-14T22:56:28'
authors:
- ibobev
topics:
- programming-languages
- python-interop
- language-compatibility
- systems-language
- developer-tooling
relevance_score: 0.27
run_id: materialize-outputs
language_code: zh-CN
---

# Mojo's Not (Yet) Python

## Summary
这篇文章质疑 Mojo 当前被宣传为“Pythonic”或未来“Python++”的定位，核心观点是：就作者实际尝试而言，Mojo 还远不能被视为可直接替代或严格兼容 Python 的语言。它的重要性在于，开发者若基于“现成 Python 代码大多可运行”的预期评估 Mojo，可能会严重高估其现实可用性与互操作成熟度。

## Problem
- 文章要解决的问题是：**Mojo 现在到底是不是一个足够接近 Python、可让既有 Python 代码基本直接工作的语言**。
- 这很重要，因为 Mojo 的宣传强调“Pythonic”“未来是 Python 严格超集”以及 Python 互操作；若这些表述与现状存在落差，会影响开发者采用、迁移和性能评估决策。
- 作者特别关心的实际问题是：Mojo 是否像 PyPy 或 Cython 一样，能让普通 Python 脚本和库在不依赖底层运行时细节时大致正常工作。

## Approach
- 作者采用**动手验证**的方式，而不是只看宣传文案：在 Ubuntu 24.04 环境中安装 Python 3、Cython、PyPy、hyperfine 和 Mojo，然后直接检查版本与可用性。
- 文章以一个非常朴素的判准来衡量 Mojo：**如果它真接近 Python，那么现有 Python 代码、生态和互操作能力应当在常见场景下基本可用**。
- 作者将 Mojo 隐式对比到 PyPy、Cython 这类开发者熟悉的“Python 兼容/加速”路径，用它们作为现实预期基线。
- 核心机制并非提出新算法，而是通过**环境搭建 + 兼容性预期校验**来说明：宣传中的“Pythonic”不等于现实中的“可运行现有 Python 代码”。

## Results
- 文中给出的明确环境/版本信息包括：Ubuntu **24.04**，Python **3.12.3**，Cython **3.0.8**，PyPy **7.3.15**（Python **3.9.18**），Mojo **0.26.1.0**。
- 摘录中**没有提供正式基准测试结果、数据集、性能指标或误差条**，也没有出现与 Python/PyPy/Cython 的定量对比数字。
- 最强的具体结论性主张是：**尽管 Mojo 被宣传为“Pythonic”并强调未来会成为 Python 严格超集，但以作者当前体验看，它“还不是”Python**。
- 文章还明确指出作者原先的预期是“像 PyPy 或 Cython 那样，大多数现有代码应基本可工作”，而标题与论述方向表明：**这一预期在当前版本 Mojo 0.26.1.0 上并不成立**。

## Link
- [https://theconsensus.dev/p/2026/03/12/mojos-not-yet-python.html](https://theconsensus.dev/p/2026/03/12/mojos-not-yet-python.html)
