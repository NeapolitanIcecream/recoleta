---
source: arxiv
url: http://arxiv.org/abs/2604.17464v1
published_at: '2026-04-19T14:27:27'
authors:
- Yongchao Wang
- Zhiqiu Huang
topics:
- automated-program-repair
- multi-agent-systems
- executable-specifications
- code-intelligence
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Project Prometheus: Bridging the Intent Gap in Agentic Program Repair via Reverse-Engineered Executable Specifications

## Summary
## 总结
Prometheus 是一个多智能体自动程序修复系统，它先推断出一个用 Gherkin 表达的可执行需求，再用这个需求指导补丁生成。论文声称，这种先规格、后修复的流程显著提高了 Defects4J 上的修复准确率，尤其是在强修复代理本身无法解决的缺陷上。

## 问题
- 现有的代理式程序修复系统可以生成代码，但常常抓不住开发者想要的行为；论文把这称为“意图差距（Intent Gap）”。
- 自然语言摘要和生成的对抗测试太含糊，不能作为严格的修复目标，所以代理可能生成侵入性很强或语义错误的补丁。
- 这很重要，因为一个补丁即使通过了当前失败测试，仍可能违背真实需求、引入回归，或过度修改代码库。

## 方法
- Prometheus 使用三个角色：**Architect** 根据失败报告和相关代码推断 Gherkin BDD 规格，**Engineer** 验证该规格，**Fixer** 生成补丁。
- 核心思路很直接：把 bug 报告和失败行为转成可执行需求，检查这个需求在有 bug 的代码上会失败、在开发者修复后的代码上会通过，然后让修复模型满足这个需求。
- 验证步骤是 Requirement Quality Assurance（RQA）Loop，也称为“Sandwich Verification”：推断出的规格必须在 \(C_{buggy}\) 上失败，并在 \(C_{fixed}\) 上通过。只有经过验证的规格才用于修复。
- 在实验中，Fixer 只被限制在 Defects4J 元数据里的主要可疑文件上，这样研究就能把重点放在规格引导的价值，而不是更好的故障定位上。
- 实现中使用 Gemini-3.0-Pro 作为 Architect，使用 Qwen-3.0-Coder 作为 Fixer。

## 结果
- 在 **Defects4J v3.0.1** 的 **680 个缺陷** 上（不含 Closure），盲修复器解决了 **520/680 = 76.5%**，Prometheus 又挽回了剩余 **160** 个失败中的 **119** 个，因此论文声称总正确补丁率达到 **639/680 = 93.97%**。
- 论文报告在困难集合上的 **Rescue Rate 为 74.4%**，按 **119/160** 个盲代理未修复的 bug 计算。
- 在项目子集上，报告的总修复率包括：**Math：87/106 = 82.1%**，其中 **39** 个被挽回；**Compress：43/47 = 91.5%**，其中 **14** 个被挽回；**Jsoup：84/93 = 90.3%**，其中 **25** 个被挽回。
- 在论文针对同一 hard-160 设置的对比表中，**TSAPR** 解决了 **22** 个，**RepairAgent** 解决了 **27** 个，**Prometheus** 解决了 **119** 个，作者把这描述为在困难 bug 上相对 RepairAgent 的 **4.4×** 优势。
- 论文给出了来自 **189 次修复会话** 的成本数据：每个缺陷的平均总流程时间为 **1,261.08 s**，平均 **5,782,441** 个 token；Engineer 验证阶段占比最大，为 **671.67 s**、**3,365,986** 个 token，约占成本的 **58.2%**。
- 从定性分析看，这种方法能生成更小、更贴合需求的补丁，并避免盲代理臆造变量、删除必要逻辑或做大范围结构修改。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17464v1](http://arxiv.org/abs/2604.17464v1)
