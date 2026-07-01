---
source: arxiv
url: https://arxiv.org/abs/2606.31368v1
published_at: '2026-06-30T09:00:31'
authors:
- Jiaxi Liang
- Yuanxiang Shi
- Zezhou Yang
- Chenxiong Qian
topics:
- llm-code-agents
- memory-optimization
- static-analysis
- profiling-guided-repair
- automated-software-engineering
- c-cpp
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale

## Summary
## 摘要
MOA 将性能剖析证据转化为静态检查和补丁，从而在大型 C/C++ 代码库中自动完成内存优化工作。在 OpenHarmony 上，它报告了 13 个反模式、10,067 个检测到的低效实例、769 个生成的补丁，以及 92.5% 的专家接受率。

## 问题
- 内存膨胀和分配抖动会提高资源成本并拖慢生产系统，但它们通常不会导致崩溃，所以团队往往发现得较晚。
- 开发者必须把性能剖析器轨迹关联到源码原因，编写检测规则，并在多个文件中做保持语义不变的修改。
- 如果没有可复用的模式规则和自动修复，本地性能剖析发现无法扩展到 1 亿行以上的操作系统代码库。

## 方法
- Analyzer 代理将性能剖析轨迹载入关系数据库，查询运行时证据，检查源码，并编写结构化的反模式报告。
- 独立的 Reviewer 检查每份报告是否有证据、明确的模式、示例、检测逻辑和优化策略。
- Checker Generator 使用固定骨架、编译器反馈和基于示例的细化，把已接受的报告转化为 Clang Static Analyzer 检查器。
- Patcher 将检测到的目标分组为代码块，用 clangd 收集符号上下文，编辑代码，检查语法，并在验证失败时回滚到检查点。

## 结果
- 在 OpenHarmony 5.0 上，这个 C/C++ 操作系统代码库超过 1 亿行，对 3 个服务进行性能剖析产生了 13 个通过验证的反模式。
- 在论文的比较中，13 个反模式中有 9 个，即 69.3%，没有匹配的 Clang-Tidy 性能检查。
- 这 13 个反模式涵盖 4 个静态对象过度使用模式、2 个低效字符串模式、4 个冗余复制模式和 3 个 const 堆结构模式。
- 候选模式报告的产出率为 65%，每个被接受的模式平均经过 1.5 次细化迭代。
- 合成的检查器在 7 个服务中检测到 10,067 个低效实例，MOA 生成了 769 个优化补丁，专家接受率为 92.5%。
- 已接受的优化实现了平均 42.2% 的堆内存减少和平均 10.6% 的二进制大小减少。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31368v1](https://arxiv.org/abs/2606.31368v1)
