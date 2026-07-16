---
kind: ideas
granularity: day
period_start: '2026-04-18T00:00:00'
period_end: '2026-04-19T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent-ops
- evaluation
- runtime-security
- developer-tooling
tags:
- recoleta/ideas
- topic/agent-ops
- topic/evaluation
- topic/runtime-security
- topic/developer-tooling
language_code: zh-CN
---

# 代理可靠性控制

## 摘要
近期最清楚的工作，是给编码代理及其评估加上控制层。证据支持三件具体的事：把共享代理流量放到调度代理后面，为任何用于软件决策的 LLM 评审器加入提示扰动检查，并在上线更重的 AI 工作流之前扫描仓库里缺失的面向代理文档和保护措施。

## 并行编码代理的 HTTP 调度代理
用于编码代理的本地代理已经是可落地的构建，不是研究草图。HiveMind 在现有代理和模型 API 之间加入调度和重试层，代理端不用改代码，并且报告在七个场景里，拥塞时失败率从 72%–100% 降到 0%–18%。在重放的 11 代理案例中，完整 HiveMind 达到 0% 失败；去掉重试后，失败率又回到 63.6%。这说明，对已经在共享模型配额上并行做代码生成、修复或测试编写的团队来说，这里有一个明确的产品切入点：把 admission control、带抖动的重试、反压、token 预算和按任务优先级放到同一个代理里。最先会用上的，是已经看到代理在 429、502 和连接重置中退出的平台团队和开发者体验团队。一个低成本的验证方法很直接：把一条繁忙的内部工作流重放到代理后面，对比完成率、死代理造成的 token 浪费和总耗时，再和直接访问 API 的结果比较。

### 资料来源
- [HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads](../Inbox/2026-04-18--hivemind-os-inspired-scheduling-for-concurrent-llm-agent-workloads.md): 量化了拥塞下的失败率下降，并指出重试是最重要的原语。
- [HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads](../Inbox/2026-04-18--hivemind-os-inspired-scheduling-for-concurrent-llm-agent-workloads.md): 确认不需要改代理代码，并把代理定位为透明插入点。

## LLM 代码评审器的提示扰动测试工具链
把 LLM 评审模型用于补丁排序或候选筛选的团队，在相信分数之前，需要先做一次扰动测试。Bias in the Loop 这篇审计把代码固定，只改评审提示词，然后显示，表面化的提示词线索会让判定结果大幅变化。最清楚的数字出现在单元测试生成任务上，分心提示把一个基于 GPT 的评审器准确率从 77.46% 降到 62.51%。这篇论文还建议了具体控制手段，比如 A/B 顺序交换和受控提示扰动。这支持软件团队和基准作者搭建一个小型评测工具链：在不同提示词变体下重复同一组评审比较，记录敏感性和重测一致性，并让任何会轻易改变排序的评审配置不过关。最先采用的会是用评审模型过滤昂贵执行、排序修复候选或报告排行榜结果的团队。一个低成本检查是把某个内部基准用顺序交换和几种提示扰动重跑一次，再看胜者变化了多少次。

### 资料来源
- [Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering](../Inbox/2026-04-18--bias-in-the-loop-auditing-llm-as-a-judge-for-software-engineering.md): 报告了提示词引起的准确率波动，并建议用明确控制手段报告偏差敏感性。
- [Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering](../Inbox/2026-04-18--bias-in-the-loop-auditing-llm-as-a-judge-for-software-engineering.md): 展示了机制：即使代码不变，提示词内容也会改变排序。

## 带草稿拉取请求的仓库就绪度扫描器
给编码代理做仓库准备，已经足够具体，可以做成扫描器加草稿 PR 的工作流。Workstream 会按代理配置、文档、CI/CD 质量、代码结构和安全性给仓库打分，然后生成缺失文件和建议修复。它最强的量化结果是仓库就绪度提升：作者报告，他们自己的仓库分数从 48 提到 98，外部仓库在应用建议后从 41.6 提到 73.7。修复项都是常见工程产物，比如 AGENTS.md、CLAUDE.md、GEMINI.md、ARCHITECTURE.md、CONTRIBUTING.md、SECURITY.md、pre-commit hooks、Dependabot，以及更多测试覆盖。这对那些因为仓库没有暴露足够运行上下文或护栏而导致代理失败的团队很有用。一个合理的首次部署，是在 CI 里放一个只读扫描器，扫描后开一个包含缺失的面向代理文件和配置改动的草稿 PR，再跟踪补丁合并后代理任务完成率或评审质量是否提升。

### 资料来源
- [Workstream: A Local-First Developer Command Center for the AI-Augmented Engineering Workflow](../Inbox/2026-04-18--workstream-a-local-first-developer-command-center-for-the-ai-augmented-engineering-workflow.md): 描述了就绪度扫描器、分类维度和仓库分数提升。
- [Workstream: A Local-First Developer Command Center for the AI-Augmented Engineering Workflow](../Inbox/2026-04-18--workstream-a-local-first-developer-command-center-for-the-ai-augmented-engineering-workflow.md): 确认了自动补齐缺口和生成草稿 PR 是工作流的一部分。
