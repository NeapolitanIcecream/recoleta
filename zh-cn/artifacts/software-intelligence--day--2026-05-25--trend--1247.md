---
kind: trend
trend_doc_id: 1247
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
topics:
- coding agents
- repository reasoning
- agent memory
- software verification
- prompt injection
- AI security
run_id: materialize-outputs
aliases:
- recoleta-trend-1247
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-reasoning
- topic/agent-memory
- topic/software-verification
- topic/prompt-injection
- topic/ai-security
language_code: zh-CN
---

# 编码代理正在按记忆质量、仓库推理和可执行安全来接受评判

## Overview
当天最强的研究信号是编码代理的运行控制。CODESKILL 和 SETUPX 显示，可复用经验能带来可测的提升。RepoMirage 说明，当仓库线索需要跨文件推理时，很多代理仍然会卡住。安全和验证论文把同样的要求说得更具体：代理动作需要受限权限、独立检查和机器可读证据。

## Clusters

### Reusable agent experience
CODESKILL 将编码代理过去的轨迹当作技能管理器的训练数据。它写出带有触发条件和行动步骤的简洁 Markdown 技能，再通过生成、修订、合并和删除操作把技能库保持得很小。以 Qwen3.5-35B-A3B 作为冻结的编码策略时，它在 EnvBench-Python、EnvBench-Java、SWE-Bench Verified 和 Terminal-Bench 2 上的平均成功率为 39.26，而没有技能时为 29.57。

SETUPX 把同样的思路用在仓库初始化上。它把初始化修复存成 eXPerience Units，在 Docker 快照里尝试这些修复，回滚有害尝试，并用 Prosecutor-Judge 检查避免把表面成功当成真正成功。在 EnvBench 的 100 个 Python 仓库上，带经验记忆的 SETUPX 报告 92% 的通过率，比没有记忆的版本高 10 个百分点。

#### Evidence
- [CODESKILL: Learning Self-Evolving Skills for Coding Agents](../Inbox/2026-05-25--codeskill-learning-self-evolving-skills-for-coding-agents.md): CODESKILL approach, skill-bank operations, and benchmark results.
- [SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?](../Inbox/2026-05-25--setupx-can-llm-agents-learn-from-past-failures-in-functionality-correct-code-repository-setup.md): SETUPX experience units, Docker rollback, prosecutor-judge verification, and pass-rate results.

### Repository context reasoning
RepoMirage 识别出普通 SWE-Bench 分数可能掩盖的一种失败模式。它保持问题行为不变，再通过依赖间接、运行时目标遮蔽和常量外置来改变相关仓库上下文的暴露方式。对八个模型来说，平均解决率从 SWE-Bench Verified 上的 66.80% 在扰动后降到 49.78%，而访问文件数从 4.77 增加到 13.24。

文件访问分析说明了这件事为什么重要。GPT-5 在已解出的案例中有 53.8% 只看了一个文件，88.0% 的案例里看了不超过三个文件。RepoMirage-Extend 把这些隐藏瓶颈显式化，并报告 25.25% 的平均成功率，其中多文件问题解决为 17.86%，代理链恢复为 17.19%。

#### Evidence
- [RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations](../Inbox/2026-05-25--repomirage-probing-repository-context-reasoning-in-code-agents-with-perturbations.md): RepoMirage perturbations, file-access analysis, and benchmark drops.

### Verification for generated software
这组语料里的验证工作都很具体，也都绑定了工具。SPDDwL 使用 Rocq 这个交互式定理证明器生成经过验证的纯核心，再导出 C++ 供宿主集成。在它的 RISC-V RV32I 案例研究中，系统在 30 分钟预算内完成 47 条指令，生成 1,859 行已验证的 Rocq 代码和 2,848 行 C++ 代码，通过 265 个生成测试，并在 12 小时 AFL++ fuzzing 中没有崩溃或挂起。

面向生产的工作使用契约和独立审查者。meta-engineering harness 把功能请求变成明确契约，通过按角色分工的代理处理工作，并把失败归类为 bug、规格缺口、验证器噪声或契约歧义。它的早期部署覆盖了 17 个功能，持续了几周，并在合并前发现了 5 个 bug 或实现缺口。ESBMC 提供了更长的验证视角：这篇综述描述了一个有界模型检查器，带有 9 个语言前端、6 个 SMT 求解器后端、k-induction，以及最近与 LLM 驱动修复和 agentic checking 的连接。

#### Evidence
- [Trustworthy Software Project Generation : a Case Study with an Interactive Theorem Prover](../Inbox/2026-05-25--trustworthy-software-project-generation-a-case-study-with-an-interactive-theorem-prover.md): SPDDwL architecture and RISC-V case-study results.
- [Meta-Engineering Harnesses for AI-Native Software Production: A Contract-Driven Adversarial Verification Architecture with Early Deployment Report](../Inbox/2026-05-25--meta-engineering-harnesses-for-ai-native-software-production-a-contract-driven-adversarial-verification-architecture-with-early-deployment-report.md): Contract-driven harness design and early deployment evidence.
- [ESBMC: A Survey of Its Evolution, Integration, and Future Directions in Formal Software Verification](../Inbox/2026-05-25--esbmc-a-survey-of-its-evolution-integration-and-future-directions-in-formal-software-verification.md): ESBMC survey scope, verification capabilities, and LLM/agent integrations.

### Agentic coding security
最强的安全类论文把编码助手当作带有开发者权限的命令执行器。AIShellJack 研究把被污染的编码规则文件加入正常任务，并记录 Cursor 和 GitHub Copilot 执行了什么。覆盖 70 种 MITRE ATT&CK 技术的 314 个载荷里，报告的攻击成功率在 41% 到 84% 之间。

攻击面比项目文件更大。论文把注入路径映射到共享技能、Model Context Protocol 服务器、IDE 设置、网站、API 和消息工具。它还列出 Cursor、GitHub Copilot、Claude Code、Zed.dev、Codex 和 Windsurf 的 14 个 CVE，其中一些攻击在信任对话框出现前就触发了，或者绕过了命令白名单。自托管代理运行时 Nerve 给出了对应的产品回应：计划审批、源代码接入警告、脚本超时和会话日志都写进了运行时设计，不过它没有报告准确率或生产力基准。

#### Evidence
- [How Agentic AI Coding Assistants Become the Attacker's Shell](../Inbox/2026-05-25--how-agentic-ai-coding-assistants-become-the-attacker-s-shell.md): AIShellJack setup, attack payload coverage, success rates, and CVE summary.
- [Show HN: Nerve – self hosted runtime for AI agents](../Inbox/2026-05-25--show-hn-nerve-self-hosted-runtime-for-ai-agents.md): Runtime safety features for long-running agents and lack of benchmark evidence.
