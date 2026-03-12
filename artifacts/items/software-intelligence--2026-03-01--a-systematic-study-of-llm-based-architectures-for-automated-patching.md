---
source: arxiv
url: http://arxiv.org/abs/2603.01257v1
published_at: '2026-03-01T20:26:22'
authors:
- Qingxiao Xu
- Ze Sheng
- Zhicheng Chen
- Jeff Huang
topics:
- automated-patching
- llm-agents
- software-security
- multi-agent-systems
- code-intelligence
relevance_score: 0.93
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# A Systematic Study of LLM-Based Architectures for Automated Patching

## Summary
**TL;DR:** 这篇论文系统比较了4类基于LLM的自动安全补丁架构，发现**架构设计与迭代深度**比单纯换更强模型更决定补丁系统的可靠性/成本；令人意外的是，**通用代码代理**整体补丁效果最好，但代价是更高的token与时间开销。

**Problem:**
- 自动修复软件安全漏洞很难：不仅要消除漏洞，还要保持程序语义、通过功能测试，并能在大型真实代码库中稳定工作。
- 现有工作多关注提示词或单个agent设计，但**缺少对不同系统架构的受控、统一比较**，导致难以判断哪些设计真正有效。
- 这很重要，因为漏洞检测越来越自动化，而**修复仍是主要瓶颈**；若架构选错，系统可能低效、脆弱或成本过高。

**Approach:**
- 作者提出并统一评测4种LLM补丁范式：**fixed-workflow、single-agent、multi-agent、general-code-agent**。
- 在统一框架中重实现前三类补丁系统，并以 **Claude Code** 代表第四类通用代码代理进行对比。
- 统一评测维度包括：**补丁正确性、工具使用、token消耗、执行时间**，尽量把“架构差异”而非“实现细节”作为主要变量。
- 基准为 **AIxCC delta-scan Java** 漏洞任务，共 **19个真实漏洞**，覆盖 **6个大型Java项目**：Apache Commons Compress、ZooKeeper、Log4j、Tika、PDFBox、POI。
- 核心机制上，论文不是提出新的修补算法，而是用**同一基准+同一评测协议**来观察不同架构如何组织推理、工具调用、编辑、验证与迭代。

**Results:**
- **通用代码代理表现最好**：代表系统 Claude Code 成功修复 **16/19** 个漏洞。
- 最好的补丁专用agent（文中为 **multi-agent on GPT-5**）最多修复 **13/19**，比通用代码代理少 **3个任务**。
- 作者认为通用代码代理的优势来自**更通用的工具接口**，使其能跨不同漏洞类型和大代码库更好适配。
- **fixed-workflow** 的特点是高效但脆弱；**single-agent** 在灵活性与成本之间更均衡；**multi-agent** 泛化更强，但带来**显著更高的开销**，且在复杂任务上更容易出现**reasoning drift（推理漂移）**。
- 论文还引用AIxCC背景结果说明任务重要性：比赛系统曾在 **70** 个注入漏洞中检测出 **54/70（77%）**，并正确修复 **43/70（61%）**；但这些并非本文四类架构直接对比的实验结果。
- 对token与时间，摘要与引言只给出定性结论：**通用代码代理成本更高**，补丁专用架构**更省token且更快**；摘录中未提供更细的定量表格数值。

## Links
- Canonical: http://arxiv.org/abs/2603.01257v1
