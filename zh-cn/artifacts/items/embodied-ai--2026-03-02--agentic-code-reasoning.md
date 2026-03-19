---
source: arxiv
url: http://arxiv.org/abs/2603.01896v2
published_at: '2026-03-02T09:17:06'
authors:
- Shubham Ugare
- Satish Chandra
topics:
- code-reasoning
- llm-agents
- static-analysis
- patch-verification
- fault-localization
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Code Reasoning

## Summary
本文研究LLM在**不执行代码**时，是否能像代理一样遍历代码库并做可靠的语义推理。作者提出一种比自由推理更受约束的**semi-formal reasoning**，用结构化“证书”强迫模型写出前提、执行路径和结论，从而在多种代码理解任务上提升准确率。

## Problem
- 目标问题：让LLM代理在**不运行程序/测试**的条件下，判断补丁是否等价、定位缺陷、回答代码语义问题。
- 这很重要，因为执行真实仓库代码通常昂贵、依赖复杂且难以扩展，而很多场景（RL奖励、代码审查、静态分析）都需要低成本但可靠的语义判断。
- 现有方法要么是**非结构化推理**，容易跳步和无依据断言；要么是**完全形式化验证**，对真实多语言仓库过于重。

## Approach
- 提出**agentic code reasoning**设置：代理可用工具浏览仓库、追踪跨文件依赖，但**不能执行仓库代码或测试**。
- 核心方法是**semi-formal reasoning**：给代理一个结构化模板，要求其显式填写前提、逐测试/逐路径分析、反例或对比、以及形式化结论。
- 简单说，就是把“想一想再回答”改成“先列证据、再逐步追踪、最后下结论”，从而减少拍脑袋猜测。
- 模板按任务定制：补丁等价任务要求比较每个测试的行为；fault localization要求列可疑区域并解释其如何导致失败；code QA要求函数追踪、数据流和语义性质证据。
- 论文在三类任务上比较单次调用、普通agentic reasoning与semi-formal reasoning，并分析步数与错误模式的权衡。

## Results
- **补丁等价（curated, 170例, Opus-4.5）**：总体准确率从**78.2%**提升到**88.8%**；非等价样本从**78.6%**到**82.9%**，等价样本从**78.0%**到**93.0%**；平均步数从**10.08**增至**28.17**。
- **真实agent生成补丁验证（200例, 有测试补丁）**：Opus-4.5下，semi-formal agentic达到**93.0%**，优于single-call **86.0%**、single-call+file context **87.5%**、agentic standard **87.0%**，也明显高于**difflib 73%**；Sonnet-4.5下，semi-formal agentic为**91.5%**，高于agentic standard **84.5%**。
- **代码问答（RubberDuckBench）**：摘要声称semi-formal达到**87%**准确率，相比标准agentic提升约**9个百分点**；贡献段还给出相对single-shot **76%**提升**10.8个百分点**、相对标准agentic提升**8.7个百分点**。
- **缺陷定位（Defects4J，小规模43个可评估bug）**：Opus-4.5的agentic semi-formal在严格**All**指标上达到**Top-5 72.1%**，高于agentic standard的**60.5%**（+**11.6pp**）；在**Any**指标上为**88.4%**，高于**81.4%**（+**7.0pp**）。
- **缺陷定位（Defects4J，大规模90个可评估bug）**：文中明确声称Opus-4.5的semi-formal相较standard在**Top-5 (All)**上提升约**5个百分点**；给出的标准基线为**43.3%**，说明semi-formal约为**48.3%**，但截断文本未完整展示最终表格数值。
- 最强结论：结构化、可核查的推理“证书”能在**不执行代码**的前提下，显著提升代码语义分析可靠性，并接近可用于**execution-free RL reward**的补丁验证精度。

## Link
- [http://arxiv.org/abs/2603.01896v2](http://arxiv.org/abs/2603.01896v2)
