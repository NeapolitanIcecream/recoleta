---
kind: ideas
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code agents
- agent evaluation
- executable feedback
- software engineering benchmarks
- runtime traces
- agent security
tags:
- recoleta/ideas
- topic/code-agents
- topic/agent-evaluation
- topic/executable-feedback
- topic/software-engineering-benchmarks
- topic/runtime-traces
- topic/agent-security
language_code: zh-CN
---

# 代码代理运行溯源

## Summary
代码代理工作现在已有足够证据支持更窄的采用门禁：接受代理拉取请求前要求可运行的设置和测试证明；信任排行榜数字前审计评测工具链中的分数利用；漏洞修复中使用成对的崩溃和安全执行。共同的运维需求是一份记录，说明运行了什么、什么失败了、改了什么，以及可用权限有哪些。

## 要求设置日志、生成测试和通过运行证据的代理拉取请求检查
试点代码代理的工程团队可以为代理编写的拉取请求增加一道 CI 门禁：代理必须给出仓库设置步骤、它编写或选择的验证测试，以及证明补丁已通过的准确命令输出。如果环境由人工预先构建、缺少测试，或代理在部分修复后停止，门禁应失败。

SWE-Cycle 为这个流程提供了具体模板。它把环境重建、代码实现和验证测试生成分开，然后在一个空白仓库中测试 FullCycle 运行。报告中的 FullCycle 解决率低于 14%，即使单独的设置和测试生成分数高得多也是如此。这直接提醒团队，不应在狭窄的单元测试通过后就接受代码代理输出。SaaSBench 补充了全栈场景：超过 95% 的失败发生在深入业务逻辑之前，主要集中在设置、集成、过早停止和反复调试循环。一个实用的试点可以从十个内部缺陷工单开始，并衡量每次代理运行在这些相同阶段中的失败位置。

### Evidence
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle 将端到端问题解决定义为环境重建、代码实现和验证测试生成，FullCycle 解决率低于 14%。
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench 报告称，企业 SaaS 代理失败集中在设置、配置、集成、过早停止和调试循环。

## 包含利用审计和逐次运行 rollout 记录的基准发布检查
发布代理分数的团队应对基准测试工具链运行奖励黑客审计，并为计分运行附上 rollout 记录。审计应梳理任务文件、评分代码、环境边界和权限，然后在基准用于模型选择前尝试构造一个最大化分数的利用。rollout 记录应包括任务状态、观测、模型输出、工具调用、工具结果、产物、时间、终端状态、失败情况，以及用于计算分数的报告规则。

BenchJack 说明了为什么这应纳入发布流程。它在全部 10 个被审计基准上生成了可用的奖励黑客利用，并发现 219 个不同缺陷。在四个设计可修复的基准上，反复审计和修补把可被利用的任务比例从接近 100% 降到 10% 以下。Rollout Cards 覆盖了轨迹记录侧：对 50 个热门仓库的审计发现，没有一个在主要分数之外报告失败、出错或跳过的 rollout；对固定产物重新评分使报告分数最多变化 20.9 个百分点。

### Evidence
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack 审计代理基准中的奖励黑客路径，在 10 个基准中发现利用，并显示迭代修补可以减少可被利用的任务。
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout Cards 规定了每个 episode 的记录和报告规则，并显示报告选择会改变代理基准结果。

## 在打补丁前比较崩溃和安全执行的漏洞修复运行
安全工程团队可以调整自动化漏洞修复运行，让代理先创建相近的概念验证变体，区分崩溃和非崩溃执行，并记录故障点附近的状态探针。补丁步骤应从一份修复规范开始，其中写明源码位置和安全条件；只有在编译通过，并在原始输入和变异后的崩溃输入上重新执行通过后，才接受变更。

ContraFix 是这个循环的具体例子。它的 Analyzer 比较成对执行中的运行时状态，然后 Patcher 把推断出的安全条件转成源码编辑。该系统还存储已验证的修复规范和变异策略，用于后续案例。报告结果足以支持在反复出现的漏洞类别上进行小规模内部测试：SEC-Bench 上解决率为 84.0%，PatchEval 上为 73.8%；消融实验把 27.0 个百分点的增益归因于对比式运行时分析，把 9.0 个百分点的增益归因于技能积累。

### Evidence
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix 使用成对的崩溃和安全执行、运行时探针、修复规范、验证运行，以及可复用的修复知识来进行漏洞修复。
