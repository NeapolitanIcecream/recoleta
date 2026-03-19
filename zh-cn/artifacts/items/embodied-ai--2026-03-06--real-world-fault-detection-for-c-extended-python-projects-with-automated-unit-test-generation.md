---
source: arxiv
url: http://arxiv.org/abs/2603.06107v1
published_at: '2026-03-06T10:05:29'
authors:
- Lucas Berg
- Lukas Krodinger
- Stephan Lukasczyk
- Annibale Panichella
- Gordon Fraser
- Wim Vanhoof
- Xavier Devroey
topics:
- automated-test-generation
- python-c-extensions
- fault-detection
- subprocess-isolation
- software-testing
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Real-World Fault Detection for C-Extended Python Projects with Automated Unit Test Generation

## Summary
本文针对带有 C 扩展的 Python 项目在自动生成单元测试时容易因原生代码崩溃而中断的问题，提出了基于子进程隔离的 Pynguin 执行模型。它的核心价值是让测试生成器在真实世界 C-extension 库上继续工作、发现崩溃并产出可复现的崩溃测试用例。

## Problem
- 许多 Python 库通过 FFI 调用 C/C++ 代码以获得性能，但原生异常（如 segmentation fault）会绕过 Python 异常机制并直接崩溃解释器。
- 传统自动测试生成在同一解释器内执行测试；一旦 SUT 崩溃，整个生成过程停止，既无法继续覆盖其他代码，也难以稳定复现和分析故障。
- 这很重要，因为这些崩溃发生在公开 API 调用上时属于真实缺陷，会影响科学计算、数据分析和机器学习生态中的软件可靠性与安全性。

## Approach
- 作者将 Pynguin 的“测试生成”和“测试执行”解耦：每个生成的测试不再只在线程中运行，而是放到隔离的子进程中执行。
- 最简单地说：如果某个测试触发了 C 扩展崩溃，只会杀死那个子进程，不会杀死主测试生成器；主进程检测到崩溃后保存该测试并继续搜索其他测试。
- 为支持跨进程执行，作者重构了观察者架构：把只需在主进程维护的观察者与需在远端执行时收集覆盖率/断言信息的 remote observers 分开，并通过序列化在进程间传输。
- 系统还加入崩溃测试导出与重执行机制，用于确认 crash-revealing tests 的可复现性，便于开发者调试和修复。
- 为平衡鲁棒性与开销，作者加入三种自动执行模式选择策略：heuristic（检测 FFI 后选子进程）、restart（先线程，崩溃后切换）、combined（两者结合）。

## Results
- 作者构建了一个新数据集 DS-C，包含 **21** 个热门 Python 库中的 **1,648** 个带 C-extensions 的模块。
- 使用子进程执行后，自动生成了 **120,176** 个测试，并发现 **213** 个唯一 crash causes。
- 其中人工分析识别出 **32** 个此前未知的真实缺陷，并已向相应开发团队报告。
- 论文摘要称，子进程执行使得自动测试能够覆盖“最多 **56.53685674547984** 更多模块”；文段未进一步解释该数值的单位/基线，但其核心含义是相比非隔离执行，更多模块能被成功测试。
- 具体案例中，生成的崩溃测试揭示了 SciPy 的 `idd_reconid` 对参数校验不足，错误输入会导致 segmentation fault。
- 文段没有给出完整的覆盖率提升/下降表格数值，但明确指出：对子系统含 FFI 的模块，子进程执行能避免生成过程整体崩溃，并继续测试未崩溃部分。

## Link
- [http://arxiv.org/abs/2603.06107v1](http://arxiv.org/abs/2603.06107v1)
