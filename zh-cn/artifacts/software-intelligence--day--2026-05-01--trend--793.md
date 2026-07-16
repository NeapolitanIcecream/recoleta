---
kind: trend
trend_doc_id: 793
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
topics:
- AI coding agents
- software engineering
- reward models
- agent orchestration
- reproducibility
- GPU serving
- developer tooling
run_id: materialize-outputs
aliases:
- recoleta-trend-793
tags:
- recoleta/trend
- topic/ai-coding-agents
- topic/software-engineering
- topic/reward-models
- topic/agent-orchestration
- topic/reproducibility
- topic/gpu-serving
- topic/developer-tooling
language_code: zh-CN
---

# AI coding agents are being judged by controls, traces, and full-task cost

## 概览
当天最强的工作把 AI 编码当作受治理的工程过程来处理。AutoMat 测试科学复现性，SAGA 测量智能体的端到端延迟，RECAP 记录真实的提示到编辑轨迹。共同的要求是在信任生成代码或智能体工作流之前先拿出具体证据。

## 研究发现

### Agent output needs specs, traces, and reproducibility checks
几篇论文都在给 AI 编码工作的检查层施压。规格治理论文把 AI 编码收益和审查负担、上下文限制、可测试规格联系起来。它引用了任务层面的正面研究，也报告了经验丰富的开发者在成熟代码库上变慢、随着 AI 采用率提高交付稳定性下降的证据。

AutoMat 给出了最直接的实证警告。在测试过的代码智能体配置里，最佳结果只复现了 85 个计算材料科学主张中的 54.1%。仅靠论文复现时，各系统的成功率几乎为零，这说明缺失的流程、领域工具和脆弱的执行仍然是当前的失败点。

RECAP 直接处理编辑器里的测量问题。它在 VS Code 中记录 Copilot 聊天、shadow git 提交和细粒度编辑。在一次课程部署中，它捕获了 2,034 条提示和 8,239 次提交，让反复的错误循环和 AI 编辑占比在会话层面变得可见。

#### 资料来源
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): Summarizes specification-driven governance, mixed productivity evidence, and reliability risks.
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): Reports AutoMat's 85-claim reproducibility benchmark and success rates.
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): Describes RECAP's prompt-to-edit capture method and deployment measurements.

### Code reward research is testing whether denser signals help
奖励信号这条线更谨慎。pass-rate 奖励研究用 DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B 和 Qwen2.5-7B-Instruct 测试了代码生成的强化学习（RL）。密集的部分得分反馈并没有在最终 pass@k 上超过二元的“通过所有测试”奖励。在使用 GRPO 的 Qwen3-4B 上，二元奖励在平均 pass@1 上优于 pass-rate 奖励，46.4% 对 44.2%；在 pass@16 上也是如此，59.1% 对 56.8%。

Themis 扩展了代码奖励模型该评什么。它构建了一个基准，覆盖八种语言和五个标准，约有 8.9k 对偏好样本：正确性、运行时间、内存、可维护性和安全性。摘要里没有给出论文中的数值模型提升，所以这里最扎实的贡献是基准、训练数据和多标准设置。

#### 资料来源
- [Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation](../Inbox/2026-05-01--exploring-pass-rate-reward-in-reinforcement-learning-for-code-generation.md): Compares pass-rate and binary rewards across models, algorithms, and pass@k metrics.
- [Themis: Training Robust Multilingual Code Reward Models for Flexible Multi-Criteria Scoring](../Inbox/2026-05-01--themis-training-robust-multilingual-code-reward-models-for-flexible-multi-criteria-scoring.md): Describes Themis-CodeRewardBench, preference data, languages, and scoring criteria.

### Agent orchestration is becoming a systems problem
SAGA 说明，给智能体提供服务和给独立的 LLM 调用提供服务不是一回事。智能体任务通常要进行 10 到 100 次串联调用，中间夹着工具调用。SAGA 按整个工作流调度，保留可复用的 key-value cache 跨越工具调用，并把后续步骤路由回同一个 worker。在 64 张 A100 GPU 上，相比使用 Automatic Prefix Caching 的 vLLM，它把 SWE-bench 的任务完成时间降到 1.73x，把 WebArena 的任务完成时间降到 1.55x。

另一篇立场论文从控制层面提出贝叶斯决策规则。它没有实验，所以价值在于概念：编排层可以跟踪任务不确定性、智能体可靠性、成本和停止决策，而不用把语言模型本身做成贝叶斯模型。

#### 资料来源
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): Reports SAGA's workflow-level scheduler, KV-cache reuse, latency gains, and throughput tradeoff.
- [Position: agentic AI orchestration should be Bayes-consistent](../Inbox/2026-05-01--position-agentic-ai-orchestration-should-be-bayes-consistent.md): Summarizes the Bayes-consistent orchestration proposal and its lack of empirical results.
