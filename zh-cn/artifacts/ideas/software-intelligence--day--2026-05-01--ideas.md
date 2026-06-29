---
kind: ideas
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- software engineering
- reward models
- agent orchestration
- reproducibility
- GPU serving
- developer tooling
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-engineering
- topic/reward-models
- topic/agent-orchestration
- topic/reproducibility
- topic/gpu-serving
- topic/developer-tooling
language_code: zh-CN
---

# Agent Workload Visibility

## Summary
AI 编码代理现在已经有足够的局部证据，可以支持三项具体改动：在真实开发中记录 prompt-to-edit 轨迹，用结论级复现任务测试科学代理，以及按完整任务完成时间衡量代理服务。每一项改动都指向一个常见问题：普通代码指标会把代理工作的成本藏起来。

## VS Code prompt-to-edit replay for AI-assisted code review
采用 Copilot、Cursor、Claude Code 或类似工具的工程团队，应在试点项目里加一层轻量级追踪：记录聊天提示、细粒度编辑、文件保存和 shadow commit，然后在评审或复盘时把这些记录和 diff 一起回放。评审时最难追的是来源。拉取请求能显示最终补丁，但通常看不出是哪条提示触发了有风险的编辑，哪条 AI 建议被丢弃了，或者开发者是否在同一个错误上卡了很长时间。

RECAP 给出了一条可直接落地的路径。它的 VS Code 扩展会记录 Copilot 聊天 JSON 和 shadow git 变更，在五分钟窗口内把文本编辑组和 diff 关联起来，并将编辑标记为 Copilot、人类、部分匹配、未匹配，或很可能来自外部来源。在一项课程部署中，它捕获了 2,034 条提示和 8,239 次 shadow-git 提交，覆盖 406 个工作会话。软件团队可以先做一个小测试：在一个 AI 辅助项目上跑两周这种采集，然后查看重复的错误循环、按会话统计的 AI 编辑占比，以及和生成代码相关的评审意见。

### Evidence
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): RECAP records Copilot chat, shadow git commits, prompt-to-edit links, replay timelines, AI edit share, and a course deployment with 2,034 prompts and 8,239 commits.
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): The specification-governance paper identifies review load, churn, context limits, and reliability risk as adoption blockers for AI-generated code.

## Claim-level reproduction harnesses for scientific coding agents
计算科学团队在把编码代理当作研究助手之前，应先让它们做已复现的结果检查。一个可用的测试框架应当打包论文中的一个结论、元数据、可选工件、所需领域工具和隐藏的专家复现步骤。代理提交轨迹、日志、文件和简短报告，评估重点放在证据是否支持该结论。

AutoMat 说明了这个检查为什么重要。在 85 个计算材料科学结论上，最佳测试设置的成功率只有 54.1%。只靠论文文本复现时，各系统几乎都失败；基于工件的复现更容易。失败模式是操作层面的：步骤不完整、方法偏离、执行不稳定，以及缺少领域选择。实验室可以先拿最近的 10 个内部结论做起，要求代理在研究人员使用的同一个容器或 HPC 环境里运行，再把输出和专家复现笔记对比，然后再信任代理生成的脚本或后处理。

### Evidence
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): AutoMat evaluates 85 materials-science claims, keeps hidden expert reproduction steps, scores traces/logs/files/reports, and reports 54.1% best success with near-zero paper-only reproduction.
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): The paper reports low overall success and identifies incomplete procedures, methodological deviations, and execution fragility as main failure sources.

## Workflow-level latency measurement for coding-agent serving
为共享 GPU 上的编码代理或浏览器代理提供服务的团队，应按任务级别衡量成本和延迟：一次缺陷修复、一次 SWE-bench 运行、一个浏览任务，或一次完整的工具使用会话。像首 token 时间这类按请求计的指标，忽略了用户实际感受到的等待时间里那些空闲间隔、工具调用和 KV-cache 重新生成。

SAGA 给出了一次明确的系统测试。代理任务通常会发起 10 到 100 次串联的 LLM 调用，中间夹着工具调用。在一次 SWE-bench 测量里，38% 的执行时间花在 KV-cache 重新生成上，平均 GPU 内存使用率是 42%，端到端延迟是只算推理基线的 6.0 倍。SAGA 在工具调用间保留可复用的 KV cache，并把后续步骤路由回同一个 worker。在 64 块 A100 GPU 上，它把 SWE-bench 的任务完成时间降到 vLLM 加 Automatic Prefix Caching 的 1.73 倍提升，把 WebArena 的任务完成时间降到 1.55 倍提升，但峰值吞吐量大约低了 30%。实际接入时，可以先在团队自己的代理轨迹上做一次 A/B 运行，对比完整任务完成时间、SLO 达成率、GPU 内存使用和吞吐损失。

### Evidence
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): SAGA reports agent tasks with 10–100 chained calls, KV-cache regeneration costs, task-level scheduling, and completion-time gains on SWE-bench and WebArena.
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): The paper explains why KV cache continuity across agent steps can consume gigabytes and why discarding cache adds latency overhead.
