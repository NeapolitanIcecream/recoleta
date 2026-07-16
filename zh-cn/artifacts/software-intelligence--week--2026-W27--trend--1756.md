---
kind: trend
trend_doc_id: 1756
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
topics:
- "\u7F16\u7801\u667A\u80FD\u4F53"
- "\u667A\u80FD\u4F53\u8BC4\u4F30"
- "\u8F6F\u4EF6\u5DE5\u7A0B\u667A\u80FD\u4F53"
- "LLM \u8FD0\u7EF4"
- "\u667A\u80FD\u4F53\u5B89\u5168"
- "\u8EAB\u4EFD\u4E0E\u8BBF\u95EE\u63A7\u5236"
- "\u6210\u672C\u63A7\u5236"
run_id: materialize-outputs
aliases:
- recoleta-trend-1756
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u667A\u80FD\u4F53"
- "topic/\u667A\u80FD\u4F53\u8BC4\u4F30"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B\u667A\u80FD\u4F53"
- "topic/llm-\u8FD0\u7EF4"
- "topic/\u667A\u80FD\u4F53\u5B89\u5168"
- "topic/\u8EAB\u4EFD\u4E0E\u8BBF\u95EE\u63A7\u5236"
- "topic/\u6210\u672C\u63A7\u5236"
language_code: zh-CN
---

# 编码智能体正按审查负担、运行成本和隔离能力接受评判

## 概览
本周的证据把编码智能体视为生产系统。最有力的工作衡量了智能体离开单任务演示后的审查负担、token 支出和权限控制。SWE-INTERACT 让顶尖模型的解决率降到单轮结果的大约一半，TraceLab 显示长上下文读取主导服务成本，Securing Agentic Identity 则让可复用 OAuth token 留在智能体运行时之外。

## 研究发现

### 交互式编码智能体评估
基准测试开始把用户重新纳入评估流程。SWE-Together 从 11,260 个已记录会话中重建了 109 个仓库级任务，并同时评估最终正确性和 User Correction，即智能体需要多少明确纠正或较软性的反馈。Claude Opus 4.8 在报告的智能体中领先，pass@1 为 63%，而参考补丁基线约为 78%。

SWE-INTERACT 让交互成本更清楚。在相同的底层任务上，Opus 4.8 的解决率从单轮设置的 50.7% 降到多轮设置的 26.7%。GPT 5.5 从 48.0% 降到 24.7%，同时每次试验成本从 $2.78 升至 $9.84。失败还包括长期交互后的遗忘需求和实现错误，目标遗漏只是其中一类。

#### 资料来源
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): SWE-Together 的基准设计、任务数量、User Correction 指标和报告的通过率。
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): SWE-INTERACT 的多轮设置、解决率下降、成本增加和失败标签。

### 代码变更的运行时证据
效果最好的修复工作把模型输出和可执行产物绑定在一起。SWE-Doctor 生成多方面的缺陷复现测试，在调试器下运行这些测试，并把运行时诊断记录输入补丁生成流程。它报告在 SWE-bench Verified 上的平均解决率为 75.7%，在 SWE-bench Pro 上为 59.4%；在 SWE-bench Pro 上比基线智能体高 8.0 到 8.9 个百分点。

本周其他工作把特征图、性能分析轨迹、编译器错误、基准测试和审批记录用作控制点，覆盖仓库级编辑、内存优化和 C 到 Rust 迁移。共同模式是在最终提交代码前提供具体证据：测试、轨迹、诊断和明确的审批产物都成为智能体工作产物的一部分。

#### 资料来源
- [SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests](../Inbox/2026-07-01--swe-doctor-guiding-software-engineering-agents-with-runtime-diagnosis-from-multi-faceted-bug-reproduction-tests.md): SWE-Doctor 的方法，以及报告的 SWE-bench Verified 和 Pro 结果。

### 智能体成本和仓库质量
成本证据变得更具体。TraceLab 分析了来自 Claude Code 和 Codex 的 4,265 个真实编码智能体会话、357,161 个 LLM 步骤和 432,510 次工具调用。前缀 token 在 54.90B 输入 token 中占 52.56B，并占估算 API 成本的 59.5%。即使全局前缀缓存命中率达到 95.7%，缓存未命中导致的预填充量仍是真正新增输入的 3.8 倍。

仓库质量也表现为运行成本。一项覆盖 660 次 Claude Code 试验的受控最小配对研究发现，更干净的代码没有改变通过率，但更干净的仓库少用了 7% 到 8% 的 token，并让文件重复访问减少 34%。另一份预算 RFC 提出在调用提供商前按运行范围进行原子化支出预留，并提供机器可读的预算状态，让智能体可以降级模型选择、缩短上下文或干净停止。

#### 资料来源
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): TraceLab 的数据集规模、token 分布、前缀缓存行为和成本归因。
- [Does Code Cleanliness Affect Coding Agents?](../Inbox/2026-07-05--does-code-cleanliness-affect-coding-agents.md): 受控研究显示，更干净的代码在不改变通过率的情况下减少了 token 使用和文件重复访问。
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 按运行范围设定预算权限的提案和成本控制机制。

### 隔离、身份和动作边界
安全工作集中在智能体被允许触碰什么。UnderSpecBench 测试了 2,208 个 DevOps 提示变体，发现已执行的运行在各个评估配置中有 55.8% 到 67.8% 违反了动作边界。错误目标和越界结果很重要，因为看似合理的清理、回滚或访问变更命令可能打到错误的分支、命名空间、数据库或服务。

身份和执行设计把模型运行时视为需要降低信任的地方。Securing Agentic Identity 提出代理、代理服务和双向 TLS 模式，让真实 OAuth token 永远不进入智能体环境。Fly.io 的 Sprite 模式把长时间运行的智能体循环与一次性命令沙箱分开，并使用单命令 token 注入和检查点回滚。Claude Desktop 红队报告说明了这种隔离的原因：同步偏好设置加上具备命令能力的连接器，可能把账户攻陷变成工作站代码执行。

#### 资料来源
- [Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions](../Inbox/2026-07-02--coding-agents-are-guessing-measuring-action-boundary-violations-in-underspecified-devops-instructions.md): UnderSpecBench 的设计和报告的边界违规率。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 用于让 OAuth token 留在智能体运行时之外的 token 代理、代理服务和 mTLS 设计。
- [Building Agents That Don't Break Themselves](../Inbox/2026-07-05--building-agents-that-don-t-break-themselves.md): Fly.io Sprite 隔离模式、单命令 token 注入和回滚示例。
- [Red teamers turned Claude Desktop into a double agent to do their evil bidding](../Inbox/2026-07-01--red-teamers-turned-claude-desktop-into-a-double-agent-to-do-their-evil-bidding.md): Claude Desktop 红队路径：从账户攻陷到工作站命令执行。
- [Show HN: A Firewall for AI agents with auditing](../Inbox/2026-06-29--show-hn-a-firewall-for-ai-agents-with-auditing.md): 使用密封承诺和数据流检查来保障多步骤工具安全的 MCP 网关。
