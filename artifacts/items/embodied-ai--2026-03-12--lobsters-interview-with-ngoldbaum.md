---
source: hn
url: https://alexalejandre.com/programming/interview-with-ngoldbaum/
published_at: '2026-03-12T23:24:34'
authors:
- birdculture
topics:
- python-free-threading
- gil-removal
- scientific-python
- numpy
- pyo3
- rust-in-python
relevance_score: 0.0
run_id: materialize-outputs
---

# Lobsters Interview with Ngoldbaum

## Summary
这不是一篇机器人或机器学习研究论文，而是一篇关于 Nathan Goldbaum 的访谈，核心内容是 Python 去除 GIL 的自由线程化、科学 Python 生态兼容性、Rust 采用与开源维护实践。
它讨论了为何要推动 free-threaded Python、生态迁移中遇到的 ABI/线程安全问题，以及对 NumPy、PyO3、Cython、测试和社区治理的看法。

## Problem
- 文章要解决的核心问题是：Python 的 GIL 限制了 CPU 密集型多线程扩展性，导致在多核机器上纯 Python 协调代码最终成为瓶颈。
- 这很重要，因为科学计算、数据处理和 Web/AI 相关 Python 生态大量依赖并发与原生扩展；如果线程无法高效工作，就会限制性能、开发体验和生态演进。
- 文中还强调了配套问题：许多历史 C/Cython 扩展并非线程安全，旧 ABI 假设、全局状态和测试不足会阻碍 free-threading 落地。

## Approach
- 核心机制是推动 CPython 的 free-threaded build（PEP 703 方向），让解释器不再依赖全局解释器锁来串行化线程执行。
- 为了让这一机制真正可用，作者团队逐层改造生态底座，如 NumPy、Cython、setuptools、PyO3、cffi 等，修复全局状态、ABI 兼容和线程安全问题。
- 在实现层面，文中解释了 free-threading 需要改变 PyObject 布局、引用计数方式以及对象锁设计，因此扩展模块需要适配新的 ABI，而不是简单“去掉一把锁”。
- 在验证层面，团队使用如 `pytest-run-parallel` 之类工具，通过并发重复执行测试来暴露依赖全局状态或线程不安全的实现。
- 文章还主张用 Rust/PyO3 逐步替代新的 C/Cython 原生代码，以减少内存不安全问题并改善长期可维护性。

## Results
- 文中没有提供标准论文式的定量实验结果、基准数据集或统一性能表，因此**没有可提取的严格量化结果**。
- 明确的项目进展包括：PEP 703 于 **2023 年 10 月**获批；作者称在 **2024 年 3 月**开始推动 NumPy、Cython、setuptools 等底层包适配 free-threaded 解释器。
- 作者提到自己在 **2025 年约有 1500 次 GitHub 贡献**，用于说明生态迁移工作的广度，但这不是研究性能指标。
- 文章声称已推动或帮助支持的关键组件包括 **NumPy、PyO3、cffi、cryptography** 等，其中 Greenlet 也已“实验性支持”。
- 对实际收益的最强具体主张是：free-threading 可让过去依赖 multiprocessing 的工作流改用 multithreading，避免数据复制和 pickle 带来的额外开销，并在多核机器上更好利用线程；但作者同时明确表示**尚不建议直接依赖其作为生产默认方案**。
- 对未来时间表的主张是：作者预计 free-threaded Python 可能在 **3.16 或 3.17** 左右成为更主流甚至唯一构建，但这仍属预测而非已验证结果。

## Link
- [https://alexalejandre.com/programming/interview-with-ngoldbaum/](https://alexalejandre.com/programming/interview-with-ngoldbaum/)
