---
kind: ideas
granularity: day
period_start: '2026-06-18T00:00:00'
period_end: '2026-06-19T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent safety
- code evaluation
- compiler tuning
- benchmarking
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/code-evaluation
- topic/compiler-tuning
- topic/benchmarking
language_code: zh-CN
---

# 编码代理发布控制

## 摘要
仓库维护者现在可以把代理指令、拉取请求创建和模型选择当作可测试的软件工作来处理。实际做法包括：在失败探针后修订的紧凑仓库指导、由基线对照测试和权限门禁阻断的 issue 代理拉取请求，以及覆盖生产所用语言和项目规模的评估套件。

## 面向 AGENTS.md 文件的合成 bug 修复探针
使用编码代理的仓库团队应该为 AGENTS.md 或等效的仓库指导文件增加一个小型调优任务。这个任务可以生成合成的 bug 修复任务，让代理执行这些任务，记录指令把代理带到错误子系统或漏掉正确测试命令的位置，然后在大小上限内修改指导文件。

Probe-and-Refine 给出了一个具体模式：每轮 10 个合成 bug 修复探针，每个仓库运行 3 到 5 轮，最终指导文件由编码代理复用。在 500 个 SWE-bench Verified 实例上，精炼后的指导达到 33.0% 的平均解决率，静态指导为 28.3%，无上下文为 25.5%。收益主要来自更频繁地产生可评估补丁，这对应了维护者常见的痛点：代理把预算浪费在错误文件中，或沿用过时的本地习惯。

一个低成本的初版可以是在代理已经打开草稿的重点仓库上运行夜间任务。跟踪代理是否生成了可评估补丁、运行了哪些命令，以及哪些指导行被使用或被事实否定。输出要短到每次运行都能读完；凡是修改发布、安全或数据迁移步骤的指导编辑，都需要人工审查。

### 资料来源
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): 展示了 probe-and-refine 方法、33.0% 对比 28.3% 和 25.5% 的解决率结果，以及精炼指导主要提高可评估补丁产出的发现。
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): 报告称，对真实 issue 拉取请求的人工检查发现了许多通用改动或写到虚构路径的改动，这是更好的仓库指导可以针对的失败模式。

## 面向 issue 代理的基线对照拉取请求门禁
让代理处理 GitHub issue 的团队，应该把代理放进一个拉取请求通道，在其中对比干净基线测试运行和打补丁后的测试运行。这个门禁只应在补丁没有新增失败测试时允许草稿，阻止敏感文件路径或工作流编辑，并记录代理的工具调用、审批和负责人，供审查使用。

Phoenix 是一个有用的参考设计，因为它通过区分既有失败和补丁引入的失败来处理损坏或不稳定的仓库。它的 Tester 先运行未修改分支，再运行打补丁后的分支，并且只在没有新增失败时接受改动。在一个经过筛选的 24 任务 SWE-bench Lite 子集上，Phoenix 报告了 18 个 oracle-resolved 任务，并且成功运行中没有 PASS_TO_PASS 回归。

权限选择也需要在同一通道中单独检查。ToolPrivBench 发现，在低权限工具已经足够时，11 个被评估模型中有 6 个的过度权限工具使用率超过 30%。Eve 展示了让这些门禁更容易上线的生产基础设施：持久会话、沙箱、人工审批、追踪和基于文件的评估。生产仓库可以先要求每个代理 PR 记录三项内容：基线测试哈希、补丁后测试哈希，以及任何高权限工具或审批事件。

### 资料来源
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): 描述了 Phoenix 的基线对比补丁测试门禁、安全控制、拉取请求工作流，以及成功运行中没有 PASS_TO_PASS 回归的报告结果。
- [When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents](../Inbox/2026-06-18--when-lower-privileges-suffice-investigating-over-privileged-tool-selection-in-llm-agents.md): 显示代理经常在低权限工具已经足够时选择更高权限工具，并给出了 11 个模型的 OPUR 结果。
- [Eve](../Inbox/2026-06-18--eve.md): 列出了生产级代理运行时功能，例如持久工作流、沙箱、审批、追踪和评估。
- [The Line Vibe Coding Can't Cross](../Inbox/2026-06-18--the-line-vibe-coding-can-t-cross.md): 把生产 AI 编码与 auth、payments、secrets 和 untrusted input 所需的检查联系起来，包括测试、审查、威胁建模、审计轨迹和具名负责人。

## 编码代理推广前的跨语言和项目规模评估
工程团队不应再把单个 Python 编码分数当作仓库级代理使用的证据。上线评估应包含项目的主要语言、沙箱容器中的编译或运行时检查；对于单元测试无法覆盖主要失败的仓库，还应至少包含一个带行为检查的多文件任务。

Multi-LCB 给出了跨语言模板。它把 LiveCodeBench 扩展到 12 种语言，同时保留发布日期过滤和隐藏测试。报告的分数说明了这一点：Qwen3-235B-A22B-Thinking-2507 在 Python 和 C++ 上高于 GPT-OSS-120B Medium，但在 Rust、Ruby 和 Go 上下降，拉低了 12 语言平均分。

JAMER 增加了项目规模测试。它的 Godot 基准从超过 240,000 个候选仓库中过滤出 8,133 个行为有效项目，并检查编译、启动稳定性、结构完整性和运行时行为。代码补全的运行时通过率从小项目的 80.4% 降到大项目的 5.7%。一个实用的采用测试可以很小：从团队自己的语言中选 20 个任务，再选 5 个大型多文件任务；在选定代理通过开发者也要面对的同一套 CI 和运行时检查之前，阻止全面推广。

### 资料来源
- [Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages](../Inbox/2026-06-18--multi-lcb-extending-livecodebench-to-multiple-programming-languages.md): 展示了 Multi-LCB 对 LiveCodeBench 的 12 语言扩展，以及报告中的语言特定分数差距。
- [JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines](../Inbox/2026-06-18--jamer-project-level-code-framework-dataset-and-benchmark-on-professional-game-engines.md): 展示了 JAMER 的 Godot 项目级评估、行为有效仓库过滤，以及运行时通过率从小项目到大项目的下降。
