---
source: hn
url: https://github.com/s2-streamstore/parallax
published_at: '2026-03-02T23:04:19'
authors:
- infiniteregrets
topics:
- multi-agent-systems
- durable-streams
- agent-orchestration
- adversarial-reasoning
- persistent-memory
relevance_score: 0.11
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Parallax – Coordinate adversarial AI agents over durable streams

## Summary
Parallax 是一个用于协调多组相互隔离的 AI 代理进行“对抗式/并行式”研究的概念验证系统，核心依托 S2 durable streams 来持久化状态并支持崩溃恢复。它试图改进单模型单上下文的研究方式，让不同代理群体独立推理后再统一综合。

## Problem
- 现有很多 AI 研究工具通常只让**一个模型在一个上下文**里自我扮演多种视角，容易出现视角耦合、相互污染和群体思维。
- 多代理协作如果没有**持久化、可恢复、可动态编排**的通信基础设施，长时任务、多人/多机加入、分阶段推理会很脆弱。
- 这很重要，因为更可靠的多视角分析、审计、预测和决策支持，可能比单代理流程更适合复杂商业、技术和安全问题。

## Approach
- 系统先由一个**planner**生成策略 JSON，定义拓扑（如 groups、rounds、hierarchical、custom）、代理模式和聚合方式。
- 然后 **executor** 在 S2 streams 上为不同组生成独立代理会话；各组在生成阶段**彼此隔离，不能读到其他组内容**。
- 一个**autonomous moderator** 读取所有组的流，决定是否转向、拆分新 stream、进入下一阶段或结束，再做最终综合。
- 所有状态都存放在 **S2 durable streams** 中，因此代理会话是持久的，支持“从 tail 恢复”，并允许任意有凭证的机器或人类加入同一个 swarm。
- 系统支持把不同 backend 分配给不同组，例如用 Claude 做威胁建模、Codex 做代码审查，还可通过超参数限制动态 stream 数、阶段转换次数和总超时。

## Results
- 文本**没有提供正式实验、基准数据或定量指标**，也没有论文式评测结果，因此无法确认性能提升幅度。
- 给出的最强具体主张是：可运行 **3 个独立组 × 每组 2 个代理** 的研究会话，例如 `--groups 3 --agents-per-group 2 --max-messages 15`。
- 还展示了 **5 个独立 panelists、3 轮 Delphi forecasting** 的用法示例，声称 moderator 会把聚合结果反馈回去并让估计“收敛”，但**未给出收敛误差、方差或基线比较**。
- 系统声称支持动态创建 streams，并可通过 `--max-dynamic-streams 4`、`--max-phase-transitions 3`、`--timeout 15` 等参数约束长流程运行。
- 在可靠性方面，明确声称“**all state lives in S2 - crash and resume from the tail**”，即状态持久化并支持崩溃恢复，但**没有恢复成功率、延迟或吞吐量数字**。
- 作者明确说明这是 **“vibecoded proof of concept”**，因此当前更像工程原型与设计信号，而不是经过严格验证的研究突破。

## Link
- [https://github.com/s2-streamstore/parallax](https://github.com/s2-streamstore/parallax)
