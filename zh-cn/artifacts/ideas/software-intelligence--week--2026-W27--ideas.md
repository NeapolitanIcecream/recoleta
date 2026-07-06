---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering agents
- LLM operations
- agent security
- identity and access control
- cost control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering-agents
- topic/llm-operations
- topic/agent-security
- topic/identity-and-access-control
- topic/cost-control
language_code: zh-CN
---

# 受控的编码智能体运维

## Summary
编码智能体采用现在需要更窄的闸门：rollout 前进行回放式评审会话测试，按运行设置与 token 遥测绑定的支出预留，并让命令执行把凭证和 shell 影响隔离在持久智能体进程之外。

## 用于编码智能体 rollout 的回放式多轮评审测试
团队在扩大使用编码智能体前，应先用自己代码库中的回放式评审会话来测试候选智能体。测试应保留最初不完整的请求、代码库状态、后续用户修正和最终验证器。评分时把最终正确性和修正次数放在一起看，因为两个智能体可能提交相近的补丁，但需要开发者投入的评审量不同。

SWE-Together 给出了一种可执行的做法：它从 11,260 个记录会话中筛出 109 个代码库级任务，通过状态条件化的用户模拟器回放反馈，并在通过率之外报告 User Correction。SWE-INTERACT 加入了延迟需求带来的压力：在多轮会话中，Opus 4.8 和 GPT 5.5 的解决率从单轮约 50% 降到 26.7% 和 24.7%，GPT 5.5 的单次试验成本从 $2.78 升到 $9.84。一个实用的内部版本可以从最近 20 到 50 个有智能体辅助的工单开始，团队需要能恢复提交、回放首个请求，并把最终测试结果与评审者介入次数进行比较。

### Evidence
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): SWE-Together 定义了回放式多轮编码会话，并在最终正确性之外报告 User Correction。
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): SWE-INTERACT 显示，当智能体在多轮中处理延迟需求时，解决率大幅下降，成本上升。

## 长编码智能体会话的按运行支出预留
LLM 平台团队应在每次编码智能体调用提供商前加入按运行计的预算检查。该检查可以根据当前输入 token、最大输出 token 和带版本的价格表估算最坏情况下的成本；在运行、用户和 key 限额上原子性预留这笔金额；调用后再提交实际用量。智能体应收到机器可读的预算状态，以便缩短上下文、选择更便宜的模型，或干净停止。

TraceLab 给出了在这个层级计量的运维理由。在 4,265 个真实 Claude Code 和 Codex 会话中，前缀 token 占 54.90B 输入 token 中的 52.56B，并占估算 API 成本的 59.5%。缓存未命中仍造成的预填充量是真正新增输入 token 的 3.8 倍。预算 RFC 给出了实现形态：网关 hook、sidecar 或 SDK middleware 在转发请求前预留估算支出，并在之后释放未使用的预留。首次部署检查很简单：按运行记录前缀、追加和输出 token 两周，然后设置软性运行上限，并检查智能体本会收到降档信号的频率。

### Evidence
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): TraceLab 量化了真实编码智能体会话，并显示前缀读取主导估算成本。
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 预算 RFC 描述了按运行计的原子性支出预留，以及面向智能体的机器可读预算状态。

## 面向 DevOps 智能体的可丢弃命令沙箱与 broker 化 OAuth 访问
安全和平台团队在向智能体提供 DevOps 工具时，应把持久智能体循环与命令执行分开。把记忆、任务历史和编排保留在稳定进程中。把 shell 命令放在按会话创建的一次性沙箱中运行，并在高风险步骤前创建检查点。对于 SaaS 和内部 API，通过 broker 和 proxy 路由调用，让智能体环境收到由 broker 签发、绑定到实时 mTLS 客户端证书的 token，而由 proxy 处理真正的 OAuth token。

UnderSpecBench 显示了 DevOps 智能体为什么需要这条边界。在 2,208 个提示变体中，发生行动的运行有 55.8% 到 67.8% 违反行动边界，清理、回滚、剪枝和访问变更任务中出现了目标错误和超范围结果。Fly.io 的 Sprite 模式给出了具体的执行模型：一个共享智能体运行时可以把命令分派到隔离的按会话 Sprite，为单个 `flyctl` 命令注入用户 token，并从检查点恢复受损的文件系统和工具链。Securing Agentic Identity 给出了 API 访问模式，让可复用 OAuth token 留在智能体运行时之外，同时保留无状态 broker 和 proxy 的扩展能力。

### Evidence
- [Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions](../Inbox/2026-07-02--coding-agents-are-guessing-measuring-action-boundary-violations-in-underspecified-devops-instructions.md): UnderSpecBench 衡量了欠明确 DevOps 任务中的目标错误和超范围行为。
- [Building Agents That Don't Break Themselves](../Inbox/2026-07-05--building-agents-that-don-t-break-themselves.md): Fly.io Sprite 模式把长生命周期智能体循环与一次性命令沙箱、单命令 token 注入分开。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Securing Agentic Identity 提出 broker、proxy 和 mTLS 绑定，使真实 OAuth token 留在智能体环境之外。
