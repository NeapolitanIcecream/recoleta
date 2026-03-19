---
source: arxiv
url: http://arxiv.org/abs/2603.10072v1
published_at: '2026-03-10T05:34:56'
authors:
- Amir Al-Maamari
topics:
- llm-security
- automated-program-repair
- vulnerability-repair
- benchmark-evaluation
- failure-analysis
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# Why LLMs Fail: A Failure Analysis and Partial Success Measurement for Automated Security Patch Generation

## Summary
这篇论文系统分析了LLM在自动化安全补丁生成中的失败原因，发现模型大多不是不会写代码，而是不理解该如何真正修复漏洞。作者还提出了一个连续评分指标SRS，用来衡量“部分成功”的安全修复质量。

## Problem
- 论文要解决的问题是：**LLM生成的安全补丁到底为什么失败，以及传统只看测试通过与否的评估为什么不足**。
- 这很重要，因为一个补丁即使通过常规功能测试，也可能依然**可被攻击利用**，从而在CI/CD中被误判为“可部署”。
- 安全修复和普通程序修复不同，必须同时验证**能编译、能阻止攻击、且不破坏原功能**。

## Approach
- 作者在 **Vul4J** 基准上评估了 **64 个可复现Java漏洞**，共收集 **319 个** 由 **Gemini 3.0 Flash** 通过**zero-shot**提示生成的补丁。
- 采用“三轴评估”：**编译是否成功**、**安全性是否通过PoV攻击测试并减少Semgrep告警**、**功能性是否通过开发者测试套件**。
- 将补丁分成 5 类：**Correct & Secure、Compilation Error、Security Failure、Functionality Failure、Insecure & Breaking**，用于做失败模式分析。
- 提出 **Security Repair Score (SRS)**：先分别计算安全得分和功能得分，再在补丁可编译时加权合成为 **0 到 1** 的连续指标，以衡量“部分修好但未完全正确”的情况。
- 进一步分析哪些因素影响修复难度，包括 **CWE类型、代码复杂度、人工补丁大小** 等。

## Results
- 在 **319** 个补丁中，仅 **79 个（24.8%）** 完全正确且安全；**164 个（51.4%）** 同时在安全和功能上失败；**42 个（13.2%）** 编译失败；**33 个（10.3%）** 功能正常但仍不安全；只有 **1 个（0.3%）** 安全但破坏功能。
- 论文声称主导失败模式是**语义误解**：模型通常能生成语法正确的Java代码（总体编译率 **86.8%**），但采取了**错误的修复策略**，而非简单语法出错。
- 连续指标显示模型更擅长保留功能而非修复安全：平均 **Functionality Score = 0.832**，平均 **Security Score = 0.251**，平均 **SRS = 0.542**；功能得分约是安全得分的 **3.3 倍**。
- 成功分布呈明显双峰：**Perfect (SRS=1.0)** 为 **79 个（24.8%）**，**Near-success (0.8≤SRS<1.0)** 只有 **1 个（0.3%）**，**Partial** 为 **188 个（58.9%）**，**Complete failure (SRS=0)** 为 **51 个（16.0%）**。作者据此认为安全补丁生成更像“全成或全败”，几乎没有接近成功的案例。
- 漏洞类型强烈影响难度：在样本较多的CWE中，**CWE-20 Input Validation** 修复率 **0%**（编译率 **95%**，SRS **0.469**），而 **CWE-835 Infinite Loop** 修复率 **45%**（编译率 **100%**，SRS **0.725**）；**CWE-611 XXE** 修复率 **40%**，**CWE-264 Permissions** 修复率 **15%** 且“功能正常但不安全”比例高。
- 难度预测上，**人工补丁大小**与平均SRS存在显著负相关（**Spearman ρ = -0.331, p = 0.008**），而 **LOC** 和 **圈复杂度** 与成功率无显著相关，说明难点主要在“理解该改什么”，不是代码结构复杂度。

## Link
- [http://arxiv.org/abs/2603.10072v1](http://arxiv.org/abs/2603.10072v1)
