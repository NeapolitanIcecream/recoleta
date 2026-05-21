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
## 摘要
ConCovUp 生成多线程 C/C++ 测试驱动，用于在并发测试中触达共享内存访问对。它结合了静态共享访问分析、基于 LLM 的反向路径推理和执行反馈。

## 问题
- ThreadSanitizer 等动态竞争和并发分析器需要能够在线程之间产生真实共享内存交互的测试。
- 现有单元测试和 LLM 编码代理主要针对顺序行为，因此会漏掉库内部的写-读、读-写和写-写交互。
- 这个缺口会造成实际影响，因为开源库可能被当作线程安全组件使用，但其内部同步路径很少经过并发执行验证。

## 方法
- Analysis Agent 使用全程序静态分析来查找公共入口函数、共享变量、共享内存访问位置和冲突访问对。
- Path Agent 从每个目标访问开始，沿控制流图反向追踪，推断哪些输入和对象状态可以到达该访问。
- 系统没有把约束发送给 SMT 求解器，而是让 LLM 读取路径摘要并选择具体输入，例如在哈希表示例中选择新键或已有键。
- Test Generation Agent 编写多线程测试驱动，编译并运行它们，然后把未覆盖的访问对和失败反馈给系统，用于下一轮路径搜索。
- 论文在报告的实验中将每个测试的细化预算设为 3 次迭代。

## 结果
- 在 9 个真实 C/C++ 库上，这些库总计约 1,000 kLoC，ConCovUp 将平均 Shared Memory Access Pair Coverage 从 Claude Code 代理基线的 36.6% 提高到 68.1%。
- 在消融研究中，仅使用静态目标识别达到 39.2% 的平均 SMAP Coverage，完整系统达到 68.1%。
- 模型选择会改变覆盖率：Claude Sonnet 4.6 达到 68.1%，GPT 5.4 达到 55.9%，Kimi K2.5 达到 28.1% 的平均 SMAP Coverage。
- 论文主要衡量的提升是冲突共享内存访问对的覆盖率；摘录未报告发现的新 bug 或竞争数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09573v1](https://arxiv.org/abs/2605.09573v1)
