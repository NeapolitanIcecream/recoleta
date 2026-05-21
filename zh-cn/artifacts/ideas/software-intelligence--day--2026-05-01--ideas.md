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

# 智能体工作负载可见性

## Summary
AI 编码智能体已有足够的本地证据，支持团队做三项具体改变：在真实开发中记录提示词到编辑的追踪记录，用主张级复现任务测试科学智能体，并按完整任务完成时间衡量智能体服务。每项改变都针对一个普通代码指标会掩盖智能体工作成本的位置。

## 用于 AI 辅助代码评审的 VS Code 提示词到编辑回放
采用 Copilot、Cursor、Claude Code 或类似工具的工程团队，应在试点项目中加入轻量级追踪层：记录聊天提示词、细粒度代码编辑、文件保存和影子提交，然后在评审或复盘时把这些记录与 diff 一起回放。评审中的痛点是来源追踪。拉取请求可以显示最终补丁，但通常无法显示哪个提示词造成了有风险的编辑、哪条 AI 建议被丢弃，或开发者是否在长时间会话中反复处理同一个错误。

RECAP 给出了一条具体实现路径。它的 VS Code 扩展会记录 Copilot 聊天 JSON 和影子 git 变更，在五分钟窗口内把文本编辑组与 diff 关联起来，并将编辑标记为 Copilot、人类、部分匹配、未匹配或可能来自外部来源。在一次课程部署中，它记录了 406 个工作会话中的 2,034 条提示词和 8,239 次影子 git 提交。软件团队可以先做一个小测试：在一个 AI 辅助项目中运行这类采集两周，然后检查重复的错误循环、按会话统计的 AI 编辑占比，以及与生成代码相关的评审评论。

### Evidence
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): RECAP 记录 Copilot 聊天、影子 git 提交、提示词到编辑的关联、回放时间线、AI 编辑占比，以及一次包含 2,034 条提示词和 8,239 次提交的课程部署。
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): 这篇关于规格治理的论文指出，评审负担、代码 churn、上下文限制和可靠性风险会阻碍团队采用 AI 生成代码。

## 面向科学编码智能体的主张级复现测试套件
计算科学团队在把编码智能体用作研究助手前，应先测试它们能否复现实验主张。一个实用的测试套件可以打包论文主张、元数据、可选产物、所需领域工具和隐藏的专家复现步骤。智能体提交追踪记录、日志、文件和一份简短报告，评估重点放在证据是否支持该主张。

AutoMat 说明了这项检查的必要性。在 85 条计算材料科学主张中，表现最好的测试设置成功率为 54.1%。仅依靠论文文本进行复现时，各系统的成功率接近于零；基于产物的复现更容易。失败主要出在执行层面：流程不完整、方法偏离、运行脆弱，以及缺少领域选择。实验室可以先选取最近的 10 条内部主张，要求智能体在研究人员使用的同一容器或 HPC 环境中运行，并在信任智能体生成的脚本或后处理结果前，把输出与专家复现笔记进行比较。

### Evidence
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): AutoMat 评估了 85 条材料科学主张，保留隐藏的专家复现步骤，对追踪记录、日志、文件和报告打分，并报告最佳成功率为 54.1%，仅依靠论文复现的成功率接近于零。
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): 论文报告了较低的总体成功率，并指出主要失败来源是不完整流程、方法偏离和执行脆弱性。

## 面向编码智能体服务的工作流级延迟测量
在共享 GPU 上提供编码或浏览器智能体服务的团队，应按任务级别衡量成本和延迟：一次 issue 修复、一次 SWE-bench 运行、一个浏览器任务，或一次完整的工具使用会话。time-to-first-token 等按请求统计的指标会漏掉空闲间隔、工具调用和 KV-cache 再生成，而用户感受到的等待时间包含这些部分。

SAGA 给出了一项具体的系统测试。智能体任务通常会发起 10 到 100 次由工具调用分隔的链式 LLM 调用。在一项 SWE-bench 测量中，38% 的执行时间用于 KV-cache 再生成，平均 GPU 内存使用率为 42%，端到端延迟是仅推理基线的 6.0 倍。SAGA 在工具调用间隔中保留可复用的 KV cache，并把后续步骤路由回同一个 worker。在 64 块 A100 GPU 上，与带 Automatic Prefix Caching 的 vLLM 相比，它在 SWE-bench 上将任务完成时间缩短 1.73 倍，在 WebArena 上缩短 1.55 倍，代价是峰值吞吐量降低约 30%。实际采用前的检查方式是在团队自己的智能体追踪记录上做 A/B 运行，比较完整任务完成时间、SLO 达成率、GPU 内存使用和吞吐量损失。

### Evidence
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): SAGA 报告了包含 10–100 次链式调用的智能体任务、KV-cache 再生成成本、任务级调度，以及在 SWE-bench 和 WebArena 上的完成时间收益。
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): 论文解释了为什么智能体步骤之间的 KV cache 连续性可能占用数 GB 内存，以及为什么丢弃 cache 会增加延迟开销。
