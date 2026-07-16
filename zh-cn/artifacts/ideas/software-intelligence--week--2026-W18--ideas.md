---
kind: ideas
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- benchmarks
- verification
- security repair
- agent infrastructure
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/benchmarks
- topic/verification
- topic/security-repair
- topic/agent-infrastructure
language_code: zh-CN
---

# 可检查的编码代理控制点

## 摘要
编码代理的采用正在转向更小、可检查的控制点：聚焦文件查看、更安全的补丁应用、产品决策检查、带回退行为的 SAST 分诊，以及包含轨迹、文件、测试和状态变化的评估记录。

## 面向仓库代理的聚焦文件查看和补丁应用工具
仓库代理需要在探索和编辑之间使用更薄的接口。SWE-Edit 给出了一种可落地的设计：Viewer 针对文件和查询只返回与任务相关的代码块，Editor 根据自然语言编辑指令应用补丁。主代理保留缺陷推理和修复计划，减少上下文中的文件搜索残留，也减少脆弱的查找替换失败。

报告中的问题解决率提升不大，但成本和编辑可靠性提升更明确。在 SWE-bench Verified 上，SWE-Edit 将解决率从 69.9% 提高到 72.0%，将推理成本降低 17.9%，并将编辑成功率从 93.4% 提高到 96.9%。Viewer 平均返回所请求文件内容的 39.7%，这可以直接用来测试该接口是否在不隐藏所需代码行的情况下减少代码表面积。

在内部 monorepo 上运行编码代理的团队可以在不更换模型的情况下测试这一点：增加一个接收路径和查询的文件查看端点，增加一个接收编辑指令的补丁端点，然后比较代理在近期缺陷上的运行结果。跟踪已解决问题、失败补丁、非缓存输入 token，以及评审者对无关编辑的抱怨。

### 资料来源
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit 报告了 Viewer 和 Editor 的拆分、成本降低、编辑成功率提升、token 减少，以及 SWE-bench Verified 结果。
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): 论文摘要描述了上下文耦合问题和双子代理设计。

## 面向编码代理 pull request 的决策合规检查
编码代理可能通过 lint 和 typecheck，却漏掉存储在仓库外的团队决策。实际做法是建立 PR 门禁，把产品和工程决策转成显式检查项：必需的审计日志、获准使用的 UI 组件、功能开关、ORM 选择、认证包装器和废弃模式。代理可以在编写规格和构建中途评审时接收检索到的决策，最终 diff 可以按同一份决策列表评分。

Context-Augmented Code Generation 在一个小型 clean-room 基准上报告了大幅提升：只有代码库访问权限的 Claude Code 加权决策合规得分为 46%，Claude Code 加 Brief 得分为 95%。该设置还通过规格、验收标准和构建中途指导改变了工作流，因此更稳妥的操作结论是：团队应衡量代理 PR 是否遵循已存储的决策，而不能只看代码是否能编译。

便宜的第一版可以覆盖一个产品区域和十个重复出现的决策。为每条决策存储负责人、示例，以及一个正则表达式或评审清单。让编码代理处理旧工单，然后在检索前后分别将生成的 diff 与清单比较。

### 资料来源
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 论文定义了决策合规，描述了 Brief，并报告了 46% 到 95% 的合规变化和基准限制。
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 来源文本称，产品决策可能存在于工具、设计文档或 wiki 中，并且在代码中不可见。

## 使用带上下文的 LLM 评审分诊 Semgrep 告警，并在失败时保留告警
SAST 的采用会被开发者不再信任的告警队列阻碍。QASecClaw 指向一种边界清楚的编码模型用法：保留 Semgrep 作为高召回扫描器，将每个发现连同 CWE 类型、文件位置和源码上下文发送给 LLM 评审器，并且只抑制被判断为误报的发现。如果模型超时或返回格式错误的 JSON，就保留原始 Semgrep 告警。

在 OWASP Benchmark v1.2 上，QASecClaw 将误报从 560 降到 64，并将 F1 从 78.39% 提高到 90.93%，召回率下降 3.1%。对于已经评审 Semgrep 输出的安全团队，这种取舍可用，因为模型是在判断一个已知候选告警，而非搜索整个代码库。

首次部署应在现有 CI 告警上以影子模式运行。选择几个 CWE 类别，将模型抑制的发现与人工分诊结果比较；在审计视图中保留所有被抑制的告警；并要求结构化理由绑定到附近的净化、校验、编码或参数化 API。

### 资料来源
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw 先使用 Semgrep，应用带上下文的 LLM 评审，在模型失败时保留告警，并报告 OWASP Benchmark 结果。
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): 摘要描述了 SAST 误报问题，以及 Semgrep 加面向编码的专用 LLM 过滤器设置。
