---
source: hn
url: https://alexalejandre.com/programming/interview-with-ngoldbaum/
published_at: '2026-03-12T23:24:34'
authors:
- birdculture
topics:
- python-free-threading
- gil-removal
- cpython-abi
- scientific-python
- rust-bindings
relevance_score: 0.42
run_id: materialize-outputs
---

# Lobsters Interview with Ngoldbaum

## Summary
这是一篇围绕 Nathan Goldbaum 的访谈，核心讨论 Python 生态向无 GIL/自由线程（free-threading）迁移的工程实践、挑战与路线图。它不是学术论文，而是对 Python 科学计算、扩展 ABI、线程安全测试与 Rust 采用趋势的经验性总结。

## Problem
- Python 的 GIL 会让 **CPU-bound 的 Python 编排代码** 在多核机器上成为扩展瓶颈，即使底层原生代码已能并行，整体扩展性仍受限。
- 现有 Python/C 扩展生态长期默认 GIL 存在，隐藏了大量 **线程安全问题、全局状态问题和 ABI 假设**，阻碍无 GIL 解释器落地。
- 多进程虽可绕过 GIL，但会带来 **数据拷贝、pickle 开销、Jupyter 等环境下的使用复杂性**，影响科学计算与数据处理工作流效率。

## Approach
- 核心机制是推动 **PEP 703 的 free-threaded CPython** 落地：让 Python 线程不再依赖全局解释器锁，从而真正利用多核并行。
- 配套工作集中在 **生态兼容与底层改造**：为 NumPy、Cython、setuptools、PyO3、cffi 等关键基础包增加对 free-threaded build 的支持。
- 关键技术点包括 **重新处理 CPython ABI 与对象布局**：free-threaded build 下 `PyObject` 布局改变，引入每对象锁等机制，因此需要重写或适配依赖旧 ABI 的扩展层，尤其是 PyO3/FFI。
- 在线程安全验证上，采用 **pytest-run-parallel** 等方式，让测试在多线程池中并发重复运行，以暴露依赖全局状态的实现缺陷，并辅以显式多线程测试模式。
- 长期方向还包括 **推动 Rust/PyO3 在 Python 扩展中的采用**，以替代更易出错的 C/C++/Cython 绿色地带实现。

## Results
- 文中没有提供严格的基准实验表或论文式定量结果，因此 **缺少可复现的性能指标、数据集和基线数值比较**。
- 关键里程碑：**PEP 703 于 2023 年 10 月获批**，标志着 CPython 官方正式接受 free-threading 路线。
- 生态推进时间线：作者称 **2024 年 3 月** 开始集中处理 NumPy、Cython、setuptools 等底层项目，以让 free-threaded 解释器“栈底可用”。
- 人力投入：Steering Council 要求 Meta 资助 **2 个全职当量（2 FTE）** 支持生态迁移；作者提到自己在 **2025 年约有 1500 次 GitHub 贡献**，显示该工程推进强度较高。
- 支持状态方面，访谈声称已推动 **NumPy、PyO3、cffi、Greenlet（实验性）** 等关键项目取得兼容进展，并特别指出为让大量 Web 栈可用而优先处理了 PyO3/cryptography 相关支持。
- 未来判断：作者预计 free-threading 可能在 **Python 3.16 或 3.17** 左右成为更主流甚至唯一构建目标，但明确表示当前仍需社区继续测试、修复 GC 停顿和扩展兼容性问题。

## Link
- [https://alexalejandre.com/programming/interview-with-ngoldbaum/](https://alexalejandre.com/programming/interview-with-ngoldbaum/)
