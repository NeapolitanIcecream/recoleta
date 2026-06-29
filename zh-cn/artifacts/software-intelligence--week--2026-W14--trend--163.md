---
kind: trend
trend_doc_id: 163
granularity: week
period_start: '2026-03-30T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- coding-agents
- evaluation
- runtime-verification
- context-control
- software-engineering
run_id: materialize-outputs
aliases:
- recoleta-trend-163
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/runtime-verification
- topic/context-control
- topic/software-engineering
language_code: zh-CN
---

# 软件智能体研究正收紧到可执行证据和控制循环上

## Overview
本周的软件智能体研究在“结论能否通过执行和明确控制来检验”这一点上最有说服力。重心很务实：更严格的评估、更紧的上下文与权限边界，以及更强地使用编译器、测试和运行时信号。ProdCodeBench、SWE-STEPS 和 Squeez 很能体现这种重点。

## Clusters

### 有状态评估正成为默认门槛
评估正在更接近真实的软件工作。每日趋势综述反复聚焦执行、重放和仓库状态。SWE-STEPS 和 ABTest 让智能体在连续变更和行为驱动测试中行动。ProdCodeBench 和 IndustryCode 让相关结论继续锚定在源自生产环境或工业场景的任务上。共同的门槛很明确：智能体必须能在状态、工具和更长任务跨度下稳定完成工作。

#### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md)
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md)
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md)
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md)
- [BACE: LLM-based Code Generation through Bayesian Anchored Co-Evolution of Code and Test Populations](../Inbox/2026-03-30--bace-llm-based-code-generation-through-bayesian-anchored-co-evolution-of-code-and-test-populations.md)
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md)

### 上下文与动作控制正在被更明确地规定
对智能体循环的控制现在已是研究的核心面向。本周最有力的综述强调智能体可以读取、记住、运行和修改什么。Squeez 直接处理上下文膨胀问题。AmPermBench 检查权限覆盖范围。本周更早的时候，关于代码上下文压缩和 NL/PL 边界分析的工作已经指向同一方向：更紧的输入和更清晰的动作边界，比一味扩展提示词更能产生干净的证据。

#### Evidence
- [Context Engineering: A Practitioner Methodology for Structured Human-AI Collaboration](../Inbox/2026-04-05--context-engineering-a-practitioner-methodology-for-structured-human-ai-collaboration.md)
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md)
- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](../Inbox/2026-04-03--inside-the-scaffold-a-source-code-taxonomy-of-coding-agent-architectures.md)
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md)
- [KAIJU: An Executive Kernel for Intent-Gated Execution of LLM Agents](../Inbox/2026-03-31--kaiju-an-executive-kernel-for-intent-gated-execution-of-llm-agents.md)
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md)

### 可信信号来自编译器、测试和验证器门控
验证信号正进入生成和修复循环内部。每日综述显示，代码执行、证明义务、测试行为、编译器检查和验证器门控，是研究者最信任的信号。Think-Anywhere 和 WybeCoder 在本周早些时候就符合这一模式。到周末，编译器与 LLM 的协作，以及受安全约束的待办编排，把同样的思路扩展到优化和更广泛的开发工作流中。

#### Evidence
- [WybeCoder: Verified Imperative Code Generation](../Inbox/2026-03-31--wybecoder-verified-imperative-code-generation.md)
- [VeriAct: Beyond Verifiability -- Agentic Synthesis of Correct and Complete Formal Specifications](../Inbox/2026-03-31--veriact-beyond-verifiability-agentic-synthesis-of-correct-and-complete-formal-specifications.md)
- [Measuring LLM Trust Allocation Across Conflicting Software Artifacts](../Inbox/2026-04-03--measuring-llm-trust-allocation-across-conflicting-software-artifacts.md)
- [COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation](../Inbox/2026-04-05--cobol-coder-domain-adapted-large-language-models-for-cobol-code-generation-and-translation.md)
- [Fuzzing with Agents? Generators Are All You Need](../Inbox/2026-04-01--fuzzing-with-agents-generators-are-all-you-need.md)
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md)

### 失效分析正聚焦已暴露的操作风险
风险分析正在变得具体。趋势文档点出了提示注入暴露、长期代码 churn、被污染的技能，以及对架构理解薄弱等问题。这些不是抽象的安全提示。它们与仓库规模的研究和明确控制措施一起出现，因此更容易检查和比较失效模式。即使循环的其余部分已有较完整的监测，架构相关工作看起来仍不如代码编写时的辅助稳定。

#### Evidence
- [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](../Inbox/2026-04-02--beyond-resolution-rates-behavioral-drivers-of-coding-agent-success-and-failure.md)
- [No-AI code analysis found issue in HF tokenizers](../Inbox/2026-04-03--no-ai-code-analysis-found-issue-in-hf-tokenizers.md)
- [LLM-Enabled Open-Source Systems in the Wild: An Empirical Study of Vulnerabilities in GitHub Security Advisories](../Inbox/2026-04-05--llm-enabled-open-source-systems-in-the-wild-an-empirical-study-of-vulnerabilities-in-github-security-advisories.md)
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md)
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md)
- [When Labels Are Scarce: A Systematic Mapping of Label-Efficient Code Vulnerability Detection](../Inbox/2026-03-31--when-labels-are-scarce-a-systematic-mapping-of-label-efficient-code-vulnerability-detection.md)
