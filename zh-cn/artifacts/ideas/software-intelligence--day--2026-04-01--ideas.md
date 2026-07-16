---
kind: ideas
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- software-agents
- coding-llms
- evaluation
- security
- gpu-kernels
tags:
- recoleta/ideas
- topic/software-agents
- topic/coding-llms
- topic/evaluation
- topic/security
- topic/gpu-kernels
language_code: zh-CN
---

# Agent workflow observability

## 摘要
这段时间的软件代理工作指向三项马上能做的流程改动：跟踪代理代码在合并后是否还能保留，发布可复用的运行包用于评估和训练，并把不可信内容隔离当作代理安全的一部分。共同点是更清楚地看到代理做了什么、保住了什么，以及周边脚手架允许了什么。

## Post-merge churn tracking for agent-authored pull requests
发布编码代理的团队需要一条合并后的复查流程，用来衡量代码在合并后还剩下多少，而不只是代理有没有成功发起 pull request。可行的做法是做一份仓库报告，标记代理作者的 PR，跟踪被改动的行和文件在 7 天、30 天和 90 天后的后续修改，并把结果反馈到复审策略里。先从已经标记 Codex、Claude Code、Copilot、Jules 或 Devin 活动的仓库开始。重点关注反复返工、高比例重写生成测试、或合并后很快又被推翻的大规模重构等模式。这个做法很具体：维护者需要知道哪些代理工作流会给人类留下收尾工作。

现有证据已经足够把它当作常规工程指标。一个 GitHub 规模的研究构建了一个跨五个编码代理的 111,969 个 PR 数据集，发现代理作者编写的代码后续变动更多。另一篇评估论文指出，如果工作只停留在最终任务分数和隐藏运行结果，软件代理的结果就很难比较。把这两条工作合在一起，就得到一套明确流程：保存每个代理 PR 的运行元数据，然后按模型、脚手架、仓库类型和复审路径比较存活率和 churn。一个成本较低的起步检查，是取单个组织四分之一的数据，做 bot 作者 PR 检测和简单的行存活计算。

### 资料来源
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): Real-world PR dataset across five agents with higher later churn in agent-authored code.
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Argues for reproducible agent evaluation with exact versions, prompts, and trajectory logs beyond final scores.

## Standardized run packets with searchable Thought-Action-Result logs
代理团队应该给每次基准测试或内部对比实验都加上一份强制运行包：精确的模型版本、提示词、temperature、工具设置，以及每次运行的 Thought-Action-Result 日志摘要。这是评估所需的支持层，不是研究上的锦上添花。没有这些信息，失败过程就无法检查，基线结论也很难核对，团队最后只能反复重跑昂贵实验，才能回答为什么一个脚手架赢过另一个。

现有证据指向一种窄而实用的格式。对 18 篇软件工程代理论文的综述发现，只有 1 篇拿相关的 agentic 基线做了比较。那篇论文同样建议发布 TAR 轨迹或摘要，这样后续分析才能还原具体失败模式和验证行为。STITCH 又给“保留更丰富轨迹”多了一条理由：它通过把长轨迹筛到决策关键片段来获得收益，在 SWE-bench Verified 上最高相对提升 63.16%，在 HarmonyOS ArkTS 上用少于 1K 条训练轨迹把编译通过率提升到 61.31%。这组结果说明，一个小型内部工具是站得住的：一次收集运行记录，把它们压缩成可搜索的决策片段，再用同一份存储同时做评估复查和后续微调。

### 资料来源
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Calls for exact reporting details and TAR logs; finds weak baseline practice in recent papers.
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): Shows that filtering traces to decision-critical segments can materially improve coding-agent training.

## Attachment and workspace quarantine for high-privilege personal agents
有文件、邮件、浏览器和 shell 访问权限的个人代理，需要先做附件和工作区隔离，再谈模型内部的 prompt-injection 防护。具体做法是加一个执行前网关，按信任级别分类传入的邮件、下载文件、网页内容和本地 skill 文件，移除低信任来源中的指令式内容，并在这些来源影响工具调用或凭证访问之前要求明确批准。团队可以在沙箱里用预置的恶意文档和长上下文会话来测试它。

这对高权限代理已经是操作层面的要求。ClawSafety 做了 2,520 次试验，覆盖 120 个攻击场景，报告的攻击成功率会随模型变化，在 40.0% 到 75.0% 之间；其中 skill 文件注入平均达到 69.4%，而脚手架选择会改变同一模型的结果。关于 Claude Code 的支持性案例研究又补了一条相关暴露路径：minified JavaScript bundle 会把提示词、端点、遥测名称和环境变量以明文泄露出来，13MB 的 bundle 在 1.47 秒内提取出 147,992 个字符串。如果代理构建者假设恶意指令和内部逻辑都很容易被恢复，那更安全的默认做法就是在代理读取之前隔离不可信内容，并把敏感逻辑移出客户端可见代码。

### 资料来源
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): Benchmark quantifies prompt-injection success across vectors, models, and scaffolds in high-privilege agents.
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): Case study shows minified client-visible JavaScript exposes prompts and internal details to fast extraction.
