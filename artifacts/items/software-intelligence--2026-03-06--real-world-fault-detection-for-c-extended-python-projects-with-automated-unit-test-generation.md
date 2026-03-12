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
- process-isolation
- unit-testing
relevance_score: 0.85
run_id: materialize-outputs
---

# Real-World Fault Detection for C-Extended Python Projects with Automated Unit Test Generation

## Summary
本文针对带有 C 扩展的 Python 项目在自动单元测试生成时容易因原生代码崩溃而中断的问题，提出了基于子进程隔离的 Pynguin 执行模型。该方法让测试生成器在遇到段错误等致命错误时仍能继续工作，并自动产出可复现的崩溃触发测试。

## Problem
- 许多 Python 库通过 C/C++ 扩展提升性能，但这会让原生异常绕过 Python 异常机制，直接导致解释器崩溃。
- 传统自动测试生成工具在同一解释器内执行测试；一旦触发 segfault/bus error 等，整个生成过程停止，既难以发现故障，也无法复现和分析。
- 这很重要，因为这些崩溃发生在公共 API 调用上时就是真实软件缺陷，会影响可靠性，甚至带来安全风险。

## Approach
- 核心方法很简单：把“生成测试”和“执行测试”分离，让每个生成出的测试在隔离子进程中运行，而不是只在同一进程的线程里运行。
- 这样如果某个测试触发 C 扩展崩溃，只会杀死该子进程，不会杀死运行 Pynguin 搜索与覆盖率优化的主进程。
- 作者重构了 Pynguin 的观察者架构，把观察器拆成主进程观察器和远程观察器，通过序列化与进程间通信收集覆盖率、断言和执行结果。
- 系统会导出触发崩溃的 pytest 测试，并加入重执行步骤，以验证这些 crash-revealing tests 是否可复现。
- 为降低开销，论文还设计了三种自动执行模式选择策略：heuristic、restart、combined，在纯 Python 模块与 FFI 模块之间切换线程/子进程执行。

## Results
- 作者构建了一个新的真实世界数据集 DS-C，包含 **21** 个流行 Python 库中的 **1,648** 个使用 C 扩展相关模块。
- 使用子进程执行后，系统可自动为这些库生成 **120,176** 个测试，并识别出 **213** 个唯一崩溃原因（unique crash causes）。
- 通过人工分析这些崩溃，作者确认了 **32** 个此前未知的真实故障，并已报告给相应开发团队。
- 摘要中声称，子进程执行使自动测试能够覆盖“最多多出 **56.53685674547984** 个模块”；原文摘录未给出更清晰的单位或对比基线描述，但其含义是相比非子进程执行，能成功测试更多模块。
- 定性突破在于：方法不仅能避免测试生成器自身崩溃，还能持续探索未崩溃代码区域，同时产出可复现的崩溃测试以支持调试与缺陷定位。

## Link
- [http://arxiv.org/abs/2603.06107v1](http://arxiv.org/abs/2603.06107v1)
