---
source: arxiv
url: https://arxiv.org/abs/2605.09573v1
published_at: '2026-05-10T14:37:20'
authors:
- Yuandao Cai
- Shuhao Fu
- Wensheng Tang
- Cheng Wen
- Shengchao Qin
- Charles Zhang
topics:
- concurrency-testing
- llm-agents
- test-generation
- code-intelligence
- static-analysis
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing

## Summary
## 总结
ConCovUp 生成多线程 C/C++ 测试驱动，用于在并发测试中触达共享内存访问对。它结合了静态共享访问分析、基于 LLM 的反向路径推理和执行反馈。

## 问题
- ThreadSanitizer 这类动态竞态和并发分析器需要测试来在线程之间建立真实的共享内存交互。
- 现有单元测试和 LLM 编码代理大多面向顺序行为，因此会漏掉库内部的写-读、读-写和写-写交互。
- 这个缺口很重要，因为开源库常被当作线程安全，而它们内部的同步路径几乎没有得到并发执行。

## 方法
- Analysis Agent 用全程序静态分析找出公共入口函数、共享变量、共享内存访问位置和冲突访问对。
- Path Agent 从每个目标访问点出发，沿控制流图反向追踪，推断哪些输入和对象状态可以到达该访问点。
- 系统不把约束交给 SMT 求解器，而是让 LLM 阅读路径摘要并选择具体输入，例如哈希表示例中的新 key 与已有 key。
- Test Generation Agent 编写多线程测试驱动，编译并运行，然后把未覆盖的访问对和失败结果发回去，再做一轮路径搜索。
- 论文把报告实验中的细化预算设为每个测试 3 轮迭代。

## 结果
- 在 9 个真实世界的 C/C++ 库上，总规模约 1,000 kLoC，ConCovUp 将平均 Shared Memory Access Pair Coverage 从 Claude Code 代理基线的 36.6% 提升到 68.1%。
- 在消融实验中，只有静态目标识别时平均 SMAP Coverage 达到 39.2%，完整系统达到 68.1%。
- 模型选择会影响覆盖率：Claude Sonnet 4.6 达到 68.1%，GPT 5.4 达到 55.9%，Kimi K2.5 达到 28.1% 的平均 SMAP Coverage。
- 论文的主要测量收益是冲突共享内存访问对的覆盖率；摘要没有报告发现的新 bug 或竞态数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09573v1](https://arxiv.org/abs/2605.09573v1)
