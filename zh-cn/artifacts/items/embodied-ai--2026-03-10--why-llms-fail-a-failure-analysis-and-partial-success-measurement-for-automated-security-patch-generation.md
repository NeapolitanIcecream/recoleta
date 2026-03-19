---
source: arxiv
url: http://arxiv.org/abs/2603.10072v1
published_at: '2026-03-10T05:34:56'
authors:
- Amir Al-Maamari
topics:
- llm-security
- automated-program-repair
- vulnerability-patching
- failure-analysis
- benchmarking
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Why LLMs Fail: A Failure Analysis and Partial Success Measurement for Automated Security Patch Generation

## Summary
这篇论文系统评估了LLM在自动生成安全补丁时为什么失败，结论是模型大多不是不会写Java，而是不真正理解漏洞该如何修。作者还提出了一个连续指标 SRS，用来衡量“部分修好但没完全正确”的程度。

## Problem
- 论文要解决的问题是：**LLM 生成的安全补丁到底有多可靠、通常怎么失败、以及是否存在“差一点修好”的情况**。
- 这很重要，因为传统测试只看功能是否通过，**一个补丁即使通过测试，仍可能保留可利用漏洞**，会在 CI/CD 中伪装成“正确修复”。
- 安全修复与普通程序修复不同，需要同时满足**可编译、不可利用、且不破坏原功能**，现有APR评估往往无法完整反映这一点。

## Approach
- 作者在 **Vul4J** 上评估 **64 个可复现的 Java 漏洞**，用 **Gemini 3.0 Flash** 以 **zero-shot** 方式为每个漏洞生成 **5 个补丁**，共得到 **319 个有效补丁**。
- 采用**三轴评估**：①是否能编译；②是否真正修复安全问题（PoV exploit 测试 + Semgrep 静态扫描）；③是否保留功能（开发者测试套件）。
- 将补丁分成五类：**Correct & Secure、Compilation Error、Security Failure、Functionality Failure、Insecure & Breaking**，从而分析失败模式。
- 提出 **Security Repair Score (SRS)**：只有编译通过才计分，然后把**安全得分**与**功能得分**各占 50% 加权，范围为 0 到 1，用于刻画“部分成功”。
- 进一步分析哪些因素预测修复难度，包括 **CWE 类型、代码行数、圈复杂度、人工补丁大小**。

## Results
- 在 **319** 个补丁中，只有 **79 个（24.8%）** 完全正确；**164 个（51.4%）** 同时在安全和功能上失败；**42 个（13.2%）** 编译失败；**33 个（10.3%）** 功能正常但仍不安全；**1 个（0.3%）** 安全但破坏功能。
- 主要失败原因是**语义误解/错误修复策略**，不是语法问题：编译率达到 **86.8%**，但正确修复率只有 **24.8%**。作者指出 **143 个（44.8%）** 补丁采用错误策略并改变程序行为，**17 个（5.3%）** 违反 API 契约，**4 个（1.3%）** 过度修复。
- 连续指标显示模型更会“保功能”而不会“修安全”：**Functionality Score 均值 0.832**，**Security Score 均值 0.251**，相差约 **3.3×**；**SRS 均值 0.542**，中位数 **0.499**。
- SRS 呈**双峰分布**：**79 个（24.8%）** 为完美成功（SRS=1.0），只有 **1 个（0.3%）** 属于 near-success（0.8≤SRS<1.0），**188 个（58.9%）** 只是部分成功，**51 个（16.0%）** 完全失败。作者据此认为安全补丁生成更像“全有或全无”，而不是容易通过小修改逼近正确答案。
- 安全与功能之间**没有显著权衡关系**：相关性 **r = 0.267, p > 0.05**，说明修好安全并不必然以破坏功能为代价，失败更像是因为没理解漏洞本质。
- 不同漏洞类型差异很大：**CWE-835 (Infinite Loop)** 修复率 **45%**、SRS **0.725**；**CWE-611 (XXE)** 修复率 **40%**、编译率 **80%**；**CWE-20 (Input Validation)** 虽然编译率 **95%**，但修复率 **0%**；**CWE-264 (Permissions)** 有 **35%** 的补丁“功能正常但仍不安全”，远高于总体 **10.3%**。此外，人工补丁大小与成功率呈显著负相关：**Spearman ρ = -0.331, p = 0.008**。

## Link
- [http://arxiv.org/abs/2603.10072v1](http://arxiv.org/abs/2603.10072v1)
