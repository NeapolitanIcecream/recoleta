---
kind: trend
trend_doc_id: 1777
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
topics:
- coding agents
- software engineering
- agent evaluation
- open-source software
- agent security
run_id: materialize-outputs
aliases:
- recoleta-trend-1777
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/open-source-software
- topic/agent-security
language_code: zh-CN
---

# 编码智能体正被当作仓库协作者来测量，而不只是代码生成器

## Overview
当天最有力的证据把编码智能体视为在真实工作流中训练、行动并失败的仓库参与者。KAT-Coder-V2.5、EvoAgentBench 和 EdgeBench 重视可执行环境、长时程运行和可复用过程；GitHub 研究补充了维护者面对的成本。

## Clusters

### 可执行仓库训练和长时程评测
仓库级编码智能体需要可重建的项目、真实测试和长轨迹。KAT-Coder-V2.5 报告称，AutoBuilder 将可执行环境构建成功率从 16.5% 提高到 57.2%，并在 12 种语言中生成了超过 100,000 个可验证环境。它的训练流水线还按探索、定位、补丁质量、验证、恢复和诚实性筛选轨迹。

长时程评测也采用同样的重点。EdgeBench 用 134 个真实任务评测智能体，其中包括 36 个系统与软件工程任务，交互时长约 38,000 小时。它报告称，12 小时学习曲线符合 log-sigmoid 形式，平均 R² = 0.998。EvoAgentBench 加入了过程迁移测试：每个测试任务都与一个训练任务共享至少一个已验证的 Ability，但自动记忆方法仍显示出不稳定的收益，并出现了一些较大的负迁移案例。

#### Evidence
- [KAT-Coder-V2.5 Technical Report](../Inbox/2026-07-06--kat-coder-v2-5-technical-report.md): KAT-Coder-V2.5 的训练流水线、可执行环境构建和基准测试主张。
- [EdgeBench: Unveiling Scaling Laws of Learning from Real-World Environments](../Inbox/2026-07-06--edgebench-unveiling-scaling-laws-of-learning-from-real-world-environments.md): EdgeBench 的任务设计、长时程智能体交互和学习曲线结果。
- [EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer](../Inbox/2026-07-06--evoagentbench-benchmarking-agent-self-evolution-via-ability-transfer.md): EvoAgentBench 的 Ability 迁移构造和自动迁移的混合结果。

### 开源证据揭示集成成本
面向 GitHub 的研究补充了维护者关心的测量结果。一项研究把 13,360 次 AI 聊天会话与 1,240 个开源仓库的历史记录关联起来。Code Writing 占会话的 34.7%；论文报告称，采用 AI 后，可观测的代码质量信号或拉取请求合并率没有出现大范围恶化。问卷回复仍指出一种社会成本：开发者认为他人生成的 AI 代码比自己生成的 AI 代码更难维护。

并发的智能体拉取请求造成了更明确的操作负担。在 AIDev-pop 中，带有智能体作者拉取请求的仓库里有 40.2% 出现精确时间重叠，覆盖 79.4% 的智能体 PR。合并回放发现，同一智能体配对有 19.8% 出现文本冲突，跨智能体配对为 41.7%。一篇相关的变异分类论文显示，带性能标签的智能体 PR 很少，占 AIDev-pop 不到 1%，但它们的差异模式会随智能体和优化目标变化。

#### Evidence
- [From Conversation to Contribution: Characterizing Coding Agent in Open-Source Software](../Inbox/2026-07-06--from-conversation-to-contribution-characterizing-coding-agent-in-open-source-software.md): 大规模 OSS 聊天日志关联、贡献影响和开发者调查结果。
- [AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates](../Inbox/2026-07-06--ai-agent-pull-requests-on-github-frequency-structure-and-merge-conflict-rates.md): 共同活跃的智能体拉取请求频率和合并冲突率。
- [What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests](../Inbox/2026-07-06--what-do-ai-agents-actually-change-an-empirical-taxonomy-of-mutation-patterns-in-performance-improving-pull-requests.md): 面向性能改进型智能体拉取请求的变异分类。

### 智能体内部状态和团队设计成为可测变量
多篇论文把智能体行为视为可探测或可配置的对象，而非只在末尾打分。Latent Programming Horizons 收集了 22,714 条修复轨迹和 2,240 万个隐藏状态向量。线性探针解码当前正确性和部分正确性的表现高于随机水平，在 Qwen3.6-35B-A3B 上最佳 AUC 约为 0.83–0.84。未来标签信号在约 25 步内保持高于随机水平。

团队结构也开始被测量。pm4aa 原型挖掘 GitHub 事件日志，以推导项目特定角色和约束，然后生成一个 LangGraph 应用。在 Commitizen 上，它将 589 名用户分配到 8 个角色，并构建了一个 5 智能体概念验证。另一项关于人格和情绪提示的研究发现，配置选择会让不同模型的代码生成 pass@1 变化 7.1 到 11.3 个百分点；恐惧提示和高尽责性提示会增加修订活动和 token 使用量，但没有带来稳定的性能收益。

#### Evidence
- [Latent Programming Horizons in Coding Agents](../Inbox/2026-07-06--latent-programming-horizons-in-coding-agents.md): 多步修复过程中对编码智能体隐藏状态的探测。
- [Using Process Mining to Generate AI Agents from Software Engineering Process Records](../Inbox/2026-07-06--using-process-mining-to-generate-ai-agents-from-software-engineering-process-records.md): 从仓库记录推导软件工程智能体角色的过程挖掘流水线。
- [Agents with Feelings? Personality and Emotion in Multi-Agent Software Teams](../Inbox/2026-07-06--agents-with-feelings-personality-and-emotion-in-multi-agent-software-teams.md): 多智能体软件团队中人格和情绪配置的测量效果。

### 连接工具的智能体需要更严格的数据边界
安全证据集中在工具响应内部的信任边界。关于智能体数据注入的论文显示，攻击者可以把分隔符、类 JSON 结构、标签或伪造元数据放入不可信内容，使大语言模型把它读作可信的智能体数据。该攻击可通过伪造 UI 标识符作用于 Web 智能体，也可通过伪造 GitHub issue 评论或伪造工具响应作用于编码智能体。

报告的成功率已经高到会影响部署决策。在 6 个模型上，概率式分隔符注入对 JSON 数据的攻击成功率达到 31.3%–43.3%，DOM 风格数据达到 33.3%–100.0%。面对论文引用的防御方法，指令注入只达到 0.0%–0.7%，而智能体数据注入最高达到 50.0%。作者报告了针对 Chrome、Antigravity 和 Nanobrowser 中 Claude 的任意点击攻击，以及针对 Claude Code、Codex 和 Gemini CLI 的远程代码执行与供应链路径。

#### Evidence
- [Agent Data Injection Attacks are Realistic Threats to AI Agents](../Inbox/2026-07-06--agent-data-injection-attacks-are-realistic-threats-to-ai-agents.md): 智能体数据注入的定义、方法、攻击设置和报告的成功率。
