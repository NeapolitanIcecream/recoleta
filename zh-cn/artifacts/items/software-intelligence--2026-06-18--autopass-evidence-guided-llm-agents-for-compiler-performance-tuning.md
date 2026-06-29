---
source: arxiv
url: https://arxiv.org/abs/2606.20373v1
published_at: '2026-06-18T15:35:40'
authors:
- Zepeng Li
- Jie Ren
- Zhanyong Tang
- Jie Zheng
- Zheng Wang
topics:
- compiler-optimization
- llm-agents
- llvm
- code-intelligence
- performance-tuning
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning

## Summary
## 摘要
AutoPass 是一个仅用于推理的 LLVM pass 调优 LLM agent 系统。它使用编译器证据和实测运行时反馈来选择、修复、测试和修改优化 pass 流水线。

## 问题
- 运行时编译器调优很重要，因为固定的 LLVM -O3 流水线不会在每个程序和目标平台上都取得最佳性能。
- 搜索空间很大：LLVM 17 暴露了 100 多个转换 pass，论文评估了 74 个 pass，序列长度最高为 107 个 pass。
- 运行时速度有噪声并且依赖硬件，因此 PGO、黑盒自动调优和学习型策略可能错过有收益的 pass 顺序，或者需要超出部署预算的数据量和运行次数。

## 方法
- AutoPass 从 LLVM -O3 流水线开始，使用四个 agent：Score、Analysis、Reasoning 和 Evaluation。
- Score Agent 使用调用图和 IR 特征对函数排序，这些特征包括基本块、循环、调用和条件分支计数。
- Analysis Agent 读取 LLVM IR 以及 -Rpass、-Rpass-missed 和 -Rpass-analysis 备注，然后输出关于语义提示和错失优化的结构化 JSON。
- Reasoning Agent 根据编译器证据和之前的运行时结果，编辑 pass 顺序和 pass 参数，例如循环展开因子或内联阈值。
- Evaluation Agent 负责编译、验证、运行候选方案，测量运行时间和硬件计数器，只保留更快且有效的流水线；如果没有候选方案带来改进，则回退到 -O3。

## 结果
- 在包含 64 个工作负载的 5 个基准套件中，在 3 轮迭代预算下，AutoPass R3 在 10 个平台-套件设置中的 9 个报告了相对于 Instrumented PGO、CSSPGO、AutoFDO 和 OpenTuner 的最佳结果。
- 摘要报告了相对于 LLVM -O3 的几何平均加速比：x86-64 上为 1.043×，ARM64 上为 1.117×。
- 在 x86-64 上，AutoPass R3 报告的结果为：cBench 1.059×、PolyBench 1.009×、CoreMark 1.137×、MiniFE 1.008×、LULESH 1.102×。
- 在 ARM64 上，AutoPass R3 报告的结果为：cBench 1.111×、PolyBench 1.149×、CoreMark 1.091×、MiniFE 1.068×、LULESH 1.046×。
- 用于说明动机的 Qsort 和 BitCount 实验报告称，在 x86-64 和 ARM64 上，相对于 -O3 的平均加速比为 1.259×。
- 表中显示，一次性 AutoPass R1 弱于 R3。例如，ARM64 PolyBench 从 R1 的 1.129× 提高到 R3 的 1.149×，ARM64 CoreMark 从 1.006× 提高到 1.091×。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20373v1](https://arxiv.org/abs/2606.20373v1)
