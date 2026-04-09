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

# 代理工作流可观测性

## Summary
这个时间窗口里的软件代理研究指向三项可以立刻调整的工作流：跟踪代理代码在合并后是否留存、发布可复用的运行包用于评估和训练，以及把不可信内容隔离当作代理安全的一部分。共同点是更清楚地看到代理做了什么、哪些结果留了下来，以及外围 scaffold 放开了哪些行为。

## 跟踪代理撰写 pull request 的合并后变动
发布编码代理的团队需要一条合并后审查流程，用来衡量代码在合并后留下了多少，而不只是看代理是否成功发起了 pull request。一个可落地的做法是生成仓库报告：标记由代理撰写的 PR，跟踪相关代码行和文件在 7、30 和 90 天后的后续修改，并把结果反馈到审查策略中。可以先从已经标注 Codex、Claude Code、Copilot、Jules 或 Devin 活动的仓库开始。重点标记这类模式：反复出现的后续修复、生成测试中的高重写率，或合并后很快又被推翻的大型重构。目的很直接：维护者需要看清哪些代理工作流会给人工维护带来收尾负担。

现有证据已经足以把这当作常规工程指标。一个 GitHub 规模的研究构建了一个包含 111,969 个 PR 的数据集，覆盖五种编码代理，并发现代理撰写的代码在后期比人工撰写的代码出现更多变动。另一篇评估论文指出，如果工作停留在最终任务分数和未公开的运行过程上，软件代理结果就很难比较。把这两条工作合起来，可以得到一套明确流程：为每个代理 PR 保存运行元数据，再按模型、scaffold、仓库类型和审查路径比较代码留存和后续变动。一个低成本的起步方案是，先用单个组织一个季度的数据，检测 bot 撰写的 PR，并计算简单的代码行留存率。

### Evidence
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): 覆盖五种代理的真实世界 PR 数据集显示，代理撰写的代码在后期有更高的变动率。
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): 主张用精确版本、提示词和轨迹日志做可复现的代理评估，而不只看最终分数。

## 带可搜索 Thought-Action-Result 日志的标准化运行包
代理团队应该给每一次基准测试或内部对比加上强制性的轨迹包：精确模型版本、提示词、temperature、工具设置，以及每次运行的 Thought-Action-Result 摘要日志。这是评估所需的基础支持层，不是可有可无的研究细节。没有这些信息，就无法检查失败原因，基线结论也很难核实，团队还会为了回答“为什么这个 scaffold 比另一个更好”这类基本问题，重复运行昂贵实验。

现有证据指向一种范围明确且实用的格式。一项对 18 篇软件工程代理论文的回顾发现，只有 1 篇与相关的 agentic 基线做了比较。同一篇论文建议公开 TAR 轨迹或其摘要，这样后续分析才能找出具体失效模式和验证行为。STITCH 又给了一个保留更丰富轨迹的理由：它通过把长运行过程筛到决策关键片段来获得提升，在 SWE-bench Verified 上相对基础模型最高提升 63.16%，在 HarmonyOS ArkTS 上用不到 1K 条训练轨迹把编译通过率提升到 61.31%。这让一个小型内部工具变得可信：一次收集运行记录，把它们压缩成可搜索的决策片段，并把同一套存储同时用于评估审查和后续微调。

### Evidence
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): 要求公开精确报告细节和 TAR 日志，并指出近期论文中的基线实践较弱。
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): 表明把轨迹筛到决策关键片段，可以切实提升编码代理训练效果。

## 面向高权限个人代理的附件与工作区隔离
拥有文件、邮件、浏览器和 shell 访问权限的个人代理，在模型内部的提示注入防御之前，还需要一层附件和工作区隔离机制。一个具体做法是在执行前设置关卡：按信任级别对传入邮件、下载文件、网页内容和本地 skill 文件进行分类，去除低信任来源中类似指令的内容，并要求显式批准后，这些来源才能影响工具调用或凭证访问。团队可以在沙箱中用预置恶意文档和长上下文会话来测试它。

这已经是高权限代理的运行要求。ClawSafety 在 120 个攻击场景上运行了 2,520 次试验，报告的攻击成功率会随模型不同落在 40.0% 到 75.0% 之间，skill-file 注入的平均成功率达到 69.4%，而 scaffold 的选择会让同一模型出现不同结果。Claude Code 的配套案例研究又补充了一条相关暴露路径：压缩后的 JavaScript bundle 也会以明文泄露提示词、端点、遥测名称和环境变量；研究者在 1.47 秒内就从一个 13MB bundle 中提取出 147,992 个字符串。如果代理构建者接受这样一个前提：恶意指令和内部逻辑都很容易被恢复出来，那么更安全的默认做法就是在代理读取之前先隔离不可信内容，并把敏感逻辑移出客户端可见代码。

### Evidence
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): 该基准量化了高权限代理在不同攻击向量、模型和 scaffold 下的提示注入成功率。
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): 案例研究显示，客户端可见的压缩 JavaScript 会快速暴露提示词和内部细节。
