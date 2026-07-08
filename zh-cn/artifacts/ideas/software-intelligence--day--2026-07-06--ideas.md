---
kind: ideas
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent evaluation
- open-source software
- agent security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/open-source-software
- topic/agent-security
language_code: zh-CN
---

# 编码代理的仓库控制

## Summary
仓库所有者可以在编码代理已经造成运维负担的位置增加控制：重叠的拉取请求、混合信任级别的工具数据，以及漏掉长时间仓库工作的评估。证据支持在现有 GitHub 和 CI 工作流中加入小规模、可测试的变更。

## 并发代理拉取请求的合并前冲突检查
使用编码代理的维护者应在评审前增加一个队列或检查，重放仍处于打开状态、由代理创建的拉取请求之间的合并。这个检查可以对同时活跃的 PR 对运行 `git merge-tree`，发布冲突摘要，并阻止触及相同源文件的低优先级代理 PR，直到第一个 PR 合入或关闭。

GitHub 数据已经显示了这种运维负担。在 AIDev-pop 中，40.2% 的含代理 PR 仓库出现了精确时间重叠，覆盖了 79.4% 的代理 PR。合并重放发现，同一代理 PR 对的文本冲突率为 19.8%，跨代理 PR 对为 41.7%，大多数冲突文件是源代码。一个简单的初始测试是：在代理会打开多个 PR 的仓库中运行该检查两周，然后把冲突评论、CI 重跑次数和维护者 rebase 工作量与前两周对比。

### Evidence
- [AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates](../Inbox/2026-07-06--ai-agent-pull-requests-on-github-frequency-structure-and-merge-conflict-rates.md): 报告 AIDev-pop 中代理创建的拉取请求的重叠率，以及合并重放冲突率。
- [AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates](../Inbox/2026-07-06--ai-agent-pull-requests-on-github-frequency-structure-and-merge-conflict-rates.md): 说明抽样合并重放结果，并指出大多数冲突来自源代码变更。
- [From Conversation to Contribution: Characterizing Coding Agent in Open-Source Software](../Inbox/2026-07-06--from-conversation-to-contribution-characterizing-coding-agent-in-open-source-software.md): 显示维护者认为他人生成的 AI 代码更难维护，即使可观察的仓库信号没有普遍变差。

## 编码代理使用的 GitHub 评论和工具响应的类型化信任边界
在 issue、拉取请求和 CI 输出上运行编码代理的团队，应把每个外部文本字段都视为不可信数据，并为可信元数据使用单独的类型化封套。一个可行做法是构建工具响应适配器：作者、资源 ID、工具名和执行历史通过解析器拥有的字段传递，而评论、日志、网页文本和模型可见摘录保留为带引号的数据。同一个适配器还应拒绝或转义不可信字段中的类 JSON 分隔符、伪造标签、仿冒工具输出块和复制的 UI 标识符。

这项控制应放在代理运行时中，不能只写在提示词规则里。agent data injection 论文显示，攻击者可以把分隔符、类 JSON 结构、标签或仿冒元数据放进不可信内容中，让模型把它读成可信的代理数据。报告的攻击包括针对编码代理的仿冒 GitHub issue 评论和伪造工具响应，并在 Claude Code、Codex 和 Gemini CLI 上展示了远程代码执行和供应链攻击路径。一个低成本验证步骤是：用论文中的分隔符和元数据仿冒案例重放测试团队自己的 GitHub issue 读取器和 PR 评审工具；如果不可信文本能改变可信字段，就让构建失败。

### Evidence
- [Agent Data Injection Attacks are Realistic Threats to AI Agents](../Inbox/2026-07-06--agent-data-injection-attacks-are-realistic-threats-to-ai-agents.md): 定义 agent data injection，描述仿冒 GitHub 评论和伪造工具响应，并报告攻击成功率。
- [Agent Data Injection Attacks are Realistic Threats to AI Agents](../Inbox/2026-07-06--agent-data-injection-attacks-are-realistic-threats-to-ai-agents.md): 报告编码代理上的远程代码执行和供应链攻击路径，并指出可信数据与不可信数据之间缺少隔离。
- [Agent Data Injection Attacks are Realistic Threats to AI Agents](../Inbox/2026-07-06--agent-data-injection-attacks-are-realistic-threats-to-ai-agents.md): 解释代理输入中可信元数据与不可信内容的区别。

## 带重建验证和长时程进度日志的仓库代理评估运行
选择编码代理的工程团队，应把候选代理放进可重建的仓库沙箱中运行，用真实测试、隐藏评测检查和多小时工作进度日志来评估。评估应记录代理是否搜索了正确文件、定位了故障、生成了补丁、完成了验证、在失败后恢复，并在卡住时给出诚实状态。可以先从五到十个已有已知修复和测试用例的内部 bug 开始。

几项新结果指向同一种评估形态。KAT-Coder-V2.5 报告称，AutoBuilder 将可执行环境构建成功率从 16.5% 提高到 57.2%，并按探索、定位、补丁质量、验证、恢复和诚实度筛选轨迹。EdgeBench 在 12 小时可执行任务上测量代理，并发现早期进度可以以高拟合度预测后续表现。EvoAgentBench 通过把任务连接到可复用的搜索、调试和验证流程来加入迁移检查，而当前自动记忆方法仍出现负迁移案例。一张有用的内部评分卡应包括环境重建成功率、通过/失败结果、首次有效测试耗时、失败补丁后的恢复情况，以及任何已存流程是否帮助或伤害后续任务。

### Evidence
- [KAT-Coder-V2.5 Technical Report](../Inbox/2026-07-06--kat-coder-v2-5-technical-report.md): 描述可执行环境构建、轨迹筛选，以及报告的 AutoBuilder 成功率提升。
- [EdgeBench: Unveiling Scaling Laws of Learning from Real-World Environments](../Inbox/2026-07-06--edgebench-unveiling-scaling-laws-of-learning-from-real-world-environments.md): 描述 12 小时可执行任务、进度曲线和长时程代理评估设计。
- [EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer](../Inbox/2026-07-06--evoagentbench-benchmarking-agent-self-evolution-via-ability-transfer.md): 描述通过 Ability 单元进行流程迁移测试，并报告自动迁移结果不一且存在负迁移案例。
