---
kind: ideas
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software verification
- code review automation
- vulnerability repair
- agent evaluation
- program analysis
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/code-review-automation
- topic/vulnerability-repair
- topic/agent-evaluation
- topic/program-analysis
language_code: zh-CN
---

# Generated Code Quality Gates

## Summary
编码 agent 的普及正在带来审核队列、薄弱的正确性证据和重复的安全修复工作。可行的做法是：给低风险 diff 加更窄的门控，在缺少测试时对生成代码做可执行检查，以及为漏洞修复 agent 保存修复记忆。

## Risk-gated auto-landing for low-risk AI-generated diffs
看到 AI 生成的 diff 数量超过人工审核能力的团队，可以为低风险改动建立一条更窄的自动审核路径。RADAR 给出了一种具体做法：按来源分类 diff，排除敏感文件和作用域，用风险模型给每个 diff 打分，运行 LLM 审核，再跑确定性检查，只在配置好的阈值内自动落地。Meta 报告称，RADAR 审核了超过 535K 个 diff，落地了超过 331K 个 diff，在该部署中，回滚率和生产事故率都低于非 RADAR diff。一个小版本可以先从 codemod、生成的 runbook 改动，或白名单所有者开始，再把回滚率、事故率和审核墙时长与普通审核做对比。

### Evidence
- [Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency](../Inbox/2026-05-28--automating-low-risk-code-review-at-meta-radar-risk-calibration-and-review-efficiency.md): RADAR combines source eligibility rules, Diff Risk Score thresholds, LLM review, deterministic checks, and production results for more than 535K reviewed diffs.
- [How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions](../Inbox/2026-05-28--how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment-in-20574-real-world-sessions.md): Real coding-agent sessions show frequent constraint violations and low visible self-resolution, which supports review gates that preserve developer control.

## Specification-based execution checks for generated code without trusted tests
开发者拿到生成代码时，常常还没有可信的测试套件。TRAILS 给出了一种可以落地的检查方式：先从自然语言规格里提取行为类别和前置条件，生成候选输入，执行候选程序，再让 LLM 在看不到代码的情况下判断每个输入输出对是否符合规格。这个方法在 LiveCodeBench 和 CoCoClaNeL 上的 Matthew correlation coefficient 高于 zero-shot chain-of-thought 基线，但每个任务消耗的 token 也更多。它适合那些接受错误函数代价很高、又没有完整测试套件的代码生成场景，比如内部脚本工具、数据转换和生成的辅助函数。

### Evidence
- [Inferring Code Correctness from Specification](../Inbox/2026-05-28--inferring-code-correctness-from-specification.md): TRAILS describes the spec-to-input-output checking workflow, reports MCC gains, and documents the higher token cost.

## CWE-keyed repair memory for vulnerability-fix agents
做 agentic 漏洞修复的安全团队，可以把修复尝试按 CVE 或 CWE 存成可复用经验。EvoRepair 会记录漏洞分析、修复策略、轨迹分析、可复用规则和后续备注；它会先检索相关经验，再在 Docker 中尝试补丁，之后为每次尝试打分并更新经验库。论文报告在 GPT-5-mini 上，PATCHEVAL 达到 93.47%，SEC-bench 达到 87.00%，在对比中超过了 12 个自动漏洞修复基线。实际试点可以先选一个反复出现的弱点类别，比如路径穿越或命令注入，再看 agent 是否更少重复失败编辑，并且能在更少轮次内通过安全测试。

### Evidence
- [EvoRepair: Enhancing Vulnerability Repair Agents Through Experience-Based Self-Evolution](../Inbox/2026-05-28--evorepair-enhancing-vulnerability-repair-agents-through-experience-based-self-evolution.md): EvoRepair provides the cyclic repair-memory workflow and benchmark results for automated vulnerability repair.
- [Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs](../Inbox/2026-05-28--minimal-prompt-perturbations-lead-to-code-vulnerabilities-prompt-fragility-and-hidden-state-signals-in-coding-llms.md): The prompt-fragility study shows that small prompt changes can flip generated code from secure to vulnerable, supporting extra security checks around generated fixes.
