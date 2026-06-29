---
source: arxiv
url: https://arxiv.org/abs/2606.17612v1
published_at: '2026-06-16T07:18:37'
authors:
- Yu Cheng
- Zhongxin Liu
- Zhenchang Xing
- Chao Ni
- Qing Huang
- Xiaoxue Ren
topics:
- automated-program-repair
- llm-code-repair
- execution-traces
- debugging-agents
- code-intelligence
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices

## Summary
## 摘要
PRACREPAIR 是一种基于 LLM 的自动程序修复方法，把执行轨迹和验证轨迹差异加入修复循环。论文报告称，它在 Defects4J 上的修复数量高于此前的 APR 基线方法，并声称在多个基础模型上取得了最好的 RWB 结果。

## 问题
- 现有基于 LLM 的 APR 方法通常依赖静态代码、检索到的上下文、错误消息和测试通过/失败反馈，因此会遗漏缺陷的运行时原因。
- 这一点很重要，因为开发者约 35% 到 50% 的时间以及项目预算的 50% 到 75% 会花在测试、验证和调试上，报告中的年度成本超过 1000 亿美元。
- 原始轨迹太大，无法直接交给 LLM；当一次补丁尝试改变了行为但测试仍然失败时，通过/失败验证也很少提供有效指导。

## 方法
- PRACREPAIR 使用 Joern 通过代码属性图构建静态上下文，覆盖 AST、CFG、调用关系和定义-使用关系。
- 它通过 JavaAgent 和 ASM 字节码插桩，从失败的 Java 测试中记录动态上下文：缺陷函数内执行过的语句、作用域内变量值和分支结果。
- LLM 通过工具调用访问这些证据，而不是一次性接收整个项目和完整轨迹。
- 该方法提出诊断问题，询问发生了什么、为什么失败以及有缺陷的逻辑应如何改变，然后把答案转化为明确的修复假设。
- 对失败的候选补丁，方法会结合验证诊断、代码差异和轨迹差异进行分析，然后更新修复假设；细化最多进行 3 轮，诊断预算最多为 10 轮。

## 结果
- 在 Defects4J V1.2/V2.0 上使用 GPT-3.5 时，PRACREPAIR 分别正确修复 139 个和 136 个缺陷。
- 在 Defects4J V1.2/V2.0 上使用 GPT-4o 时，它分别正确修复 162 个和 171 个缺陷。
- 与 ReInFix 相比，PRACREPAIR 使用 GPT-3.5 报告了 75 个独有的正确修复，使用 GPT-4o 报告了 93 个独有的正确修复。
- 论文称，PRACREPAIR 在 Defects4J 上优于 ChatRepair、ThinkRepair、RepairAgent 和 ReInFix 等基线方法，但摘录没有提供各基线方法的修复数量。
- 在 RWB V1.0/V2.0 上，摘录没有给出确切修复数量；论文声称它在多个基础模型上表现最好。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17612v1](https://arxiv.org/abs/2606.17612v1)
