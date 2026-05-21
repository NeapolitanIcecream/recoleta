---
kind: trend
trend_doc_id: 793
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
topics:
- "AI \u7F16\u7801\u4EE3\u7406"
- "\u8F6F\u4EF6\u5DE5\u7A0B"
- "\u5956\u52B1\u6A21\u578B"
- "\u4EE3\u7406\u7F16\u6392"
- "\u53EF\u590D\u73B0\u6027"
- "GPU \u670D\u52A1"
- "\u5F00\u53D1\u8005\u5DE5\u5177"
run_id: materialize-outputs
aliases:
- recoleta-trend-793
tags:
- recoleta/trend
- "topic/ai-\u7F16\u7801\u4EE3\u7406"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B"
- "topic/\u5956\u52B1\u6A21\u578B"
- "topic/\u4EE3\u7406\u7F16\u6392"
- "topic/\u53EF\u590D\u73B0\u6027"
- "topic/gpu-\u670D\u52A1"
- "topic/\u5F00\u53D1\u8005\u5DE5\u5177"
language_code: zh-CN
---

# AI 编码代理正按控制、轨迹和完整任务成本接受评判

## Overview
当天最有力的工作把 AI 编码视为受治理的工程过程。AutoMat 测试科学可复现性，SAGA 测量完整代理延迟，RECAP 记录真实的提示到编辑轨迹。共同要求是：在信任生成代码或代理工作流之前，先拿出具体证据。

## Clusters

### 代理输出需要规范、轨迹和可复现性检查
几篇论文让 AI 编码工作的检查层承受更大压力。规范治理论文把 AI 编码收益与审查负担、上下文限制和可测试规范联系起来。它引用了任务级研究中的正面结果，也报告了这样的证据：经验丰富的开发者在成熟代码库上变慢，交付稳定性随 AI 采用率上升而下降。

AutoMat 给出了最强的经验证据警告。测试中表现最好的编码代理设置复现了 85 个计算材料科学主张中的 54.1%。仅凭论文复现时，各系统的成功率接近零，这指向当前的失效点：缺少流程细节、领域工具，以及脆弱的执行过程。

RECAP 处理编辑器内部的测量问题。它在 VS Code 中记录 Copilot 聊天、影子 git 提交和细粒度编辑。在一次课程部署中，它捕获了 2,034 条提示和 8,239 次提交，让重复错误循环和 AI 编辑占比可以在会话层面被观察。

#### Evidence
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): 总结了规范驱动治理、混合的生产力证据和可靠性风险。
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): 报告了 AutoMat 的 85 项主张复现基准和成功率。
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): 描述了 RECAP 的提示到编辑捕获方法和部署测量结果。

### 代码奖励研究正在测试更密集的信号是否有帮助
奖励研究给出的信号偏谨慎。通过率奖励研究用 DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B 和 Qwen2.5-7B-Instruct 测试用于代码生成的强化学习（RL）。密集的部分给分反馈没有让最终 pass@k 超过二元的全测试通过奖励。在使用 GRPO 的 Qwen3-4B 上，二元奖励在平均 pass@1 上优于通过率奖励，46.4% 对 44.2%；在 pass@16 上也是 59.1% 对 56.8%。

Themis 扩展了代码奖励模型应评分的内容。它构建了一个基准，包含约 8.9k 个成对偏好，覆盖八种语言和五项标准：正确性、运行时间、内存、可维护性和安全性。摘录中没有给出该论文的模型数值提升，所以有依据的贡献是基准、训练数据和多标准设置。

#### Evidence
- [Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation](../Inbox/2026-05-01--exploring-pass-rate-reward-in-reinforcement-learning-for-code-generation.md): 比较了不同模型、算法和 pass@k 指标下的通过率奖励与二元奖励。
- [Themis: Training Robust Multilingual Code Reward Models for Flexible Multi-Criteria Scoring](../Inbox/2026-05-01--themis-training-robust-multilingual-code-reward-models-for-flexible-multi-criteria-scoring.md): 描述了 Themis-CodeRewardBench、偏好数据、语言和评分标准。

### 代理编排正在成为系统问题
SAGA 表明，服务一个代理不同于服务孤立的 LLM 调用。代理任务常常发起 10 到 100 次链式调用，中间夹着工具调用间隔。SAGA 调度整个工作流，在工具调用之间保留可复用的键值缓存，并把后续步骤路由回同一工作节点。在 64 块 A100 GPU 上，与带 Automatic Prefix Caching 的 vLLM 相比，它在 SWE-bench 上将任务完成时间缩短了 1.73x，在 WebArena 上缩短了 1.55x。

另一篇立场论文为贝叶斯决策规则提出了控制层论点。它没有给出实验，所以其价值在概念层面：编排层可以跟踪任务不确定性、代理可靠性、成本和停止决策，而无需让语言模型本身成为贝叶斯模型。

#### Evidence
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): 报告了 SAGA 的工作流级调度器、KV-cache 复用、延迟收益和吞吐量权衡。
- [Position: agentic AI orchestration should be Bayes-consistent](../Inbox/2026-05-01--position-agentic-ai-orchestration-should-be-bayes-consistent.md): 总结了贝叶斯一致编排提案及其缺少实证结果这一点。
