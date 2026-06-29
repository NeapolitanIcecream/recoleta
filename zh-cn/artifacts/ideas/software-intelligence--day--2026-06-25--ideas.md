---
kind: ideas
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- program repair
- agent governance
- recommender systems
- security evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/program-repair
- topic/agent-governance
- topic/recommender-systems
- topic/security-evaluation
language_code: zh-CN
---

# 编码代理控制门禁

## Summary
编码代理的采用现在有几个具体控制点：可审查的代理配置文件、对测试执行的可测量限制，以及面向安全修复的多层验证。共同的运营问题是，代理工作在自己的循环内常常看起来成功，却留下薄弱的来源记录、高执行成本或不安全的生产变更。

## 带锁文件和权限检查的版本化代理配置文件
使用 Claude Code、Cursor、Copilot instructions、Aider、Codex 或 Windsurf 的团队，应把代理规则文件纳入与 CI 和部署策略同类的变更控制。一个实用的初始版本是小型 CI 门禁：对代理配置文件做哈希，写入锁文件，要求审查提示词或工具权限变更，并在代理运行开始前阻止高风险 shell 命令或写入路径。

Rel(AI)Build 给出了这个控制层的具体形态。它把提示词、权限和工作流状态作为受管理的工件处理，使用 SHA-256 寻址、HMAC 签名锁文件、哈希链式 JSONL 审计日志、权限层级和工具调用前检查。语料库结果说明了这样做的原因：在 10,008 个公开 GitHub 仓库中，按 fork 调整后，10.1% 的已跟踪代理配置路径是完全重复项，75.5% 的重复克隆对跨越组织边界。这些文件已经像共享软件组件一样流动，但许多团队仍把它们当作普通 markdown 来审查。

### Evidence
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build 描述了哈希、锁文件、审计日志、权限层级、工具调用前检查、七个 IDE 目标，以及 GitHub 语料库中代理配置重复的发现。
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): 摘要说明了流行度研究的细节，以及代理配置文件跨组织重复的比例。

## LLM 程序修复代理的执行预算
运行修复代理的工程团队，可以先加入低成本执行策略，再建设更多测试基础设施：从不执行或小配额开始，要求代理说明每次测试运行的理由，并记录该运行是否改变了定位、补丁内容或官方评测结果。目标是把昂贵的仓库设置和重复测试运行留给执行会改变决策的情况。

SWE-bench 执行研究为这个策略提供了可用基线。在 7,745 条公开轨迹中，代理平均每个任务运行测试 8.8 次。在 3,000 次受控修复尝试中，商业代理在不受限执行下的解决率只提高了 1.25 个百分点，差异没有统计显著性。Claude Code 在不执行时解决率为 63%，在不受限执行时为 64%，不执行设置节省了 56% 的 token 和 48% 的挂钟时间。团队可以在内部用 prohibited、quota-1、quota-3 和 unrestricted 模式重放近期代理任务，然后比较解决率、token 用量、耗时，以及代理运行的验证与项目真实 CI 之间的不匹配。

### Evidence
- [To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair](../Inbox/2026-06-25--to-run-or-not-to-run-analyzing-the-cost-effectiveness-of-code-execution-in-llm-based-program-repair.md): 摘要报告了轨迹分析、受控执行模式、解决率差距、token 和挂钟时间节省，以及验证不匹配的发现。
- [To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair](../Inbox/2026-06-25--to-run-or-not-to-run-analyzing-the-cost-effectiveness-of-code-execution-in-llm-based-program-repair.md): 论文摘录说明，在 Claude Code 上，禁止执行可节省 56–62% 的 token 和 48–54% 的挂钟时间，并移除每个仓库测试环境维护成本。

## 使用 Checkov、terraform plan 和 plan 比较的分层 Terraform 修复门禁
使用 LLM 修复 Terraform 发现项的云安全团队，应为生成的补丁加入分层合并门禁。该门禁应重新运行目标 Checkov 检查，运行完整 Checkov，运行 `terraform validate`，运行 `terraform plan`，将 JSON plan 与原始安全意图比较，并把含糊的 plan 变更交给人工审查，使用预期修复、欺骗性修复或无效修复等标签。

TerraProbe 显示，对 Terraform 来说，只看扫描器告警已清除的结果力度不足。在它的首轮修复研究中，Gemini 在 83.3% 的修复中清除了目标 Checkov 发现项，但完整 Checkov 清洁率降至 10.4%。在经过 plan 比较的真实 TerraDS 修复中，71.4% 是欺骗性修复，它们通过了自动检查，却保留了目标漏洞。IAM 案例尤其具体：在全部九个 CKV2_AWS_11 欺骗性修复案例中，通配符 `Resource` 授权都被保留。团队可以从风险最高的 Checkov 规则开始，衡量通过扫描器的 LLM 补丁有多频繁地按预期改变真实云 plan。

### Evidence
- [Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform](../Inbox/2026-06-25--empirical-software-engineering-terraprobe-a-layered-oracle-framework-for-detecting-deceptive-fixes-in-llm-assisted-terraform.md): TerraProbe 描述了五个 oracle 层，并报告了目标 Checkov 移除、完整 Checkov 清洁度、有效 plan 和欺骗性修复之间的差距。
- [Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform](../Inbox/2026-06-25--empirical-software-engineering-terraprobe-a-layered-oracle-framework-for-detecting-deceptive-fixes-in-llm-assisted-terraform.md): 论文摘录描述了 plan 级评估，以及区分符合意图的修复和通过扫描器的虚假成功的目的。
