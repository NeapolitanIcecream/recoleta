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
## 摘要
Prometheus 是一个多智能体自动程序修复系统。它先推断出用 Gherkin 表达的可执行需求，再用该需求引导补丁生成。论文称，这种“规格优先”的流程在 Defects4J 上显著提高了修复准确率，尤其是在强修复智能体单独无法解决的缺陷上。

## 问题
- 现有的智能体式程序修复系统可以生成代码，但经常没有抓住开发者期望的行为；论文将这称为“Intent Gap”。
- 自然语言摘要和生成式对抗测试过于含糊，无法作为严格的修复目标，因此智能体可能会生成改动过大或语义错误的补丁。
- 这很重要，因为一个通过了当前失败测试的补丁，仍然可能违背真实需求、引入回归，或对代码库做出过多修改。

## 方法
- Prometheus 使用三个角色：**Architect** 负责根据失败报告和相关代码推断 Gherkin BDD 规格，**Engineer** 负责验证该规格，**Fixer** 负责生成补丁。
- 核心思路很直接：把缺陷报告和失败行为转换成可执行需求，检查该需求在 \(C_{buggy}\) 上失败、在 \(C_{fixed}\) 上通过，然后要求修复模型满足这个需求。
- 验证步骤是 Requirement Quality Assurance (RQA) Loop，也被称为“Sandwich Verification”：推断出的规格必须在 \(C_{buggy}\) 上失败，并在 \(C_{fixed}\) 上通过。只有通过验证的规格才会用于修复。
- 在实验中，Fixer 被限制只能修改 Defects4J 元数据标出的主要可疑文件，这样研究就能把规格引导的价值与更好的故障定位区分开。
- 实现中，Architect 使用 Gemini-3.0-Pro，Fixer 使用 Qwen-3.0-Coder。

## 结果
- 在 **Defects4J v3.0.1** 的 **680 个缺陷**上（不含 Closure），盲修复模式下的 Fixer 解决了 **520/680 = 76.5%**，而 Prometheus 在剩余 **160** 个失败案例中额外修复了 **119** 个，因此论文给出的总正确补丁率是 **639/680 = 93.97%**。
- 论文报告，在困难集合上的 **Rescue Rate 为 74.4%**，计算方式是盲智能体未修复的 **160** 个缺陷中，Prometheus 修复了 **119/160**。
- 在各项目子集上，论文报告的总修复率包括：**Math: 87/106 = 82.1%**，其中 **39** 个为额外挽回；**Compress: 43/47 = 91.5%**，其中 **14** 个为额外挽回；**Jsoup: 84/93 = 90.3%**，其中 **25** 个为额外挽回。
- 在论文的对比表中，针对同一个 hard-160 设定，**TSAPR** 修复了 **22** 个，**RepairAgent** 修复了 **27** 个，**Prometheus** 修复了 **119** 个。作者将其描述为在困难缺陷上相对 RepairAgent 有 **4.4×** 的优势。
- 论文给出了 **189 次修复会话**的成本数据：每个缺陷的平均总流水线时间为 **1,261.08 s**，平均 token 数为 **5,782,441**；其中 Engineer 验证阶段占比最大，平均 **671.67 s**、**3,365,986 tokens**，约占总成本的 **58.2%**。
- 在定性分析中，论文称该方法会产生更小、更贴合需求的补丁，并避免盲智能体凭空编造变量、删除必要逻辑或进行大范围结构性修改的情况。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17464v1](http://arxiv.org/abs/2604.17464v1)
