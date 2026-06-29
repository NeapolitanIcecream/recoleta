---
kind: ideas
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- harness repair
- agent memory
- repository context
- software engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/harness-repair
- topic/agent-memory
- topic/repository-context
- topic/software-engineering
language_code: zh-CN
---

# Coding Agent Feedback Loops

## Summary
编码代理评估在记录完整运行循环后更有用：请求、轨迹、反馈、harness 变更和下一次尝试。实际工作是围绕失败轨迹、浏览器可见的 UI 行为，以及经过测量的仓库记忆做小型评估器，然后再把代理使用范围扩大到更多团队。

## Trace-based harness repair queue for coding agents
运行编码代理的团队应该为失败轨迹加一个修复队列。队列里要保存工具调用、观察结果、文件变更、最终提交，以及每次运行产生的 harness 代码版本。之后，审查者或修复代理就能把每个失败归到具体的 harness 区域，比如工具 schema、上下文组装、生命周期控制、日志、验证、沙箱或策略检查。

HarnessFix 给出了一种可用模式：把原始轨迹转成步骤级记录，把每个错误结果连到某个 harness 层，生成范围受限的补丁，再验证补丁是否能减少目标缺陷，同时不引入大范围回归。RHO 为没有标注验证集的团队提供了更轻量的部署循环：挑出困难且多样的历史失败，重新运行，让代理比较自己的 rollout，然后接受比基线更受偏好的 harness 更新。一个小的起步测试可以用 20 到 30 个最近失败的编码代理任务，并在选出候选补丁后，只把相似问题的留出集用于检验。

### Evidence
- [From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws](../Inbox/2026-06-04--from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws.md): HarnessFix grounds harness repair in failed execution traces, harness layers, scoped patches, and held-out gains across four benchmarks.
- [Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts](../Inbox/2026-06-04--retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts.md): RHO shows a self-supervised harness update loop using past trajectories, hard-task selection, rollout comparison, and held-out pass-rate gains without external grading.

## Browser-feedback test runs for generated web applications
评估编码代理的 Web 团队应该通过已部署的 UI 来测试代理，而不只看源代码差异或单元测试。一个实用的配置是：隐藏的产品需求文件、刻意不完整的用户请求、针对可见行为的浏览器测试，以及两到三轮反馈，把失败转成自然语言用户反馈。

Asuka-Bench 说明了为什么这值得为 web 应用代理构建。它从未明确完整需求的请求开始，隐藏澄清后的全部要求，测试浏览器渲染出的行为，并把直接的失败反馈送入后续轮次。在 13 种模型-运行时配置里，三轮后的加权 Task Pass Rate 从 51.8% 到 90.1%，说明这个循环能区分那些在一次性代码生成里看起来相近的配置。首个内部版本可以做得很小：10 个常见 UI 任务，按前置行为排列的 Playwright 检查，以及一个把首轮成功和反馈后的恢复分开计分的方案。

### Evidence
- [Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement](../Inbox/2026-06-04--asuka-bench-benchmarking-code-agents-on-underspecified-user-intent-and-multi-round-refinement.md): Asuka-Bench evaluates web-app code agents with hidden requirements, browser-rendered checks, multi-round feedback, and large performance spread across configurations.

## Metric-gated repository memory for software-engineering agents
仓库记忆在加入编码代理上下文前，应该先做准入测试。一个有用的门槛是：用同一任务分别带上候选记忆和不带记忆跑一遍，只有在测得结果不变或变好，而且在成功率、定位、解决效率或相关任务指标上至少有一项提升时，才保留这条记忆。

MemOp 在软件工程代理上报告了这种效用测试，接受的记忆来自基于轨迹的拒绝采样，并在 SWE-Bench Verified 上评估。报告的提升包括单轮任务成功率最高 +5.25 个百分点，以及至少 9.79% 更低的计算成本。CL-Bench 还补上了采用检查：在总的归一化回报和收益上，Claude Sonnet 4.6 的 full-context in-context learning 优于几种专用记忆系统。团队可以先在同一仓库的重复任务上，把自己最好的长上下文基线和一个带记忆门控的版本做对比，再把代理写下的笔记保存下来供后续复用。

### Evidence
- [Enhancing Software Engineering Through Closed-Loop Memory Optimization](../Inbox/2026-06-04--enhancing-software-engineering-through-closed-loop-memory-optimization.md): MemOp defines memory utility by downstream task metrics and reports success-rate and compute-cost gains for software-engineering agents.
- [Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments](../Inbox/2026-06-04--continual-learning-bench-evaluating-frontier-ai-systems-in-real-world-stateful-environments.md): CL-Bench finds that full-context in-context learning outperforms several dedicated memory systems on aggregate results, which supports baseline comparison before memory adoption.
