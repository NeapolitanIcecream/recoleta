---
kind: ideas
granularity: week
period_start: '2026-03-30T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- evaluation
- runtime-verification
- context-control
- software-engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/runtime-verification
- topic/context-control
- topic/software-engineering
language_code: zh-CN
---

# 可执行的 agent 工作流基准

## Summary
本周指向了 coding agent 工作流中的三个实际改动：用真实生产会话搭建离线回放基准，在 agent 循环中加入工具输出裁剪以减少重复上下文加载，以及按相互依赖的 PR 序列来评估 agent，而不是一次只看一个任务。这三个方向都依赖可执行的检查方式，例如稳定测试、保留的仓库状态，以及可测量的 token 或延迟变化。

## 用于 monorepo 中 coding-agent 变更的内部回放基准
在生产代码库上评估 coding agent 的团队，可以用真实助手会话、已落地的 diff 和稳定的测试子集，搭建一个内部回放基准。ProdCodeBench 把这套做法写得足够具体，可以直接照着做：保留原始开发者提示词，从当前仓库状态中回退已落地的改动，然后用重复执行的 fail-to-pass 和 pass-to-pass 测试来给候选 agent 打分。这里有用的不只是更贴近真实环境，也在于速度。论文将其定位为一种更快的离线检查方式，用于模型替换、harness 变更和基础设施更新；这些情况否则往往要等到缓慢的 A/B 测试之后才能判断。第一个可用版本可以收窄范围：先做一个服务、monorepo 中一个语言占比较高的区域，以及只包含那些已经有稳定相关测试的提示词。如果这一小块数据在三次重复运行中都能复现模型之间的相对排名，而且不需要大量人工分诊，它就可以变成 agent 发布流程中的常规闸口。

### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): 基于真实开发者-agent 会话构建的生产环境基准，使用回退后的 diff 和稳定的执行式评分。
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): 解释了为什么在线 A/B 测试缓慢且昂贵时，离线回放对模型和 harness 决策有价值。

## 用于 coding-agent 循环的工具输出裁剪过滤器
coding-agent 团队可以在 shell 或仓库工具与主模型之间，加上一层工具输出裁剪步骤。Squeez 给这个过滤器设定了一个明确目标：只保留能回答当前子任务的最小逐字片段；如果观测结果里没有有用证据，就返回空结果。论文给出的指标足以支持做一次低成本部署测试。在人工审核的测试集上，微调后的 2B 模型在删掉 92% token 的同时，仍把 recall 保持在 0.86、F1 保持在 0.80，而且在负样本场景下比更大的 zero-shot 模型处理得好得多。这对那些会反复读取日志、grep 命中、堆栈追踪和文件内容的循环很有用。一个实际落地方式是把它做成处理管道工具输出的 sidecar CLI，并记录过滤器删掉的行里，后来有多少被证明其实是必要的。论文没有展示端到端任务完成率的提升，所以第一步应该先看调试运行中的 token 节省和单步延迟，再决定是否宣称精度提升。

### Evidence
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): 定义了任务条件化的工具输出裁剪，并报告了在高压缩率下很强的行级证据保留能力。
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): 指出该模型可以作为 CLI 过滤器插入现有 coding-agent 栈中的管道工具输出，几乎不需要改动主循环。

## 用于相关 pull-request 链的序列级评估
使用 coding agent 处理多 PR 工作的团队，可以增加一种序列级验收检查：它在一串相关改动完成后运行，而不是只在每个 pull request 后运行。SWE-STEPS 给出的理由很直接：孤立评估会把成功率高估最多 20 个百分点，而通过单个 PR 检查的 agent，仍可能留下更高的认知复杂度和更多技术债。对应的工作流调整也很直接：把有依赖关系的任务归成一组，在整个运行过程中保留仓库状态，并在序列层面同时评估新功能测试和回归测试。一个小规模试点不需要等待新的 benchmark 发布。团队可以先从一个仓库里挖出几组已经合并、彼此相关的 PR 链，按顺序让 agent 回放，然后比较孤立运行下的通过率和连续运行下的结果差异。如果这个差距接近论文报告的 15% 到 25% 下滑，团队就有了调整评估和发布策略的具体依据。

### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): 引入了带有仓库健康度指标的顺序多 PR 评估，并说明为什么孤立 PR 测试会漏掉累积性损害。
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): 报告了孤立评估下最多 20 个百分点的性能虚高，以及连续场景中的仓库健康度下降。
