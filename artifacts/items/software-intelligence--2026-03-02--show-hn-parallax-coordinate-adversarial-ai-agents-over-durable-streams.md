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
- code-intelligence
- human-ai-collaboration
relevance_score: 0.89
run_id: materialize-outputs
---

# Show HN: Parallax – Coordinate adversarial AI agents over durable streams

## Summary
Parallax 是一个基于持久化流的多智能体研究协调原型，核心想法是让多个相互隔离的 agent 群组独立推理，再由协调者统一综合。它强调“对抗式/并行视角 + 可恢复执行”，面向研究、分析和代码审计等任务。

## Problem
- 现有很多 AI 研究工具本质上让**单个模型在单一上下文里扮演多个视角**，容易产生视角耦合、从众推理和上下文污染。
- 多智能体流程如果缺少**持久、可恢复、可分叉的执行基础设施**，长任务、多人/多机协作、分阶段推理会很脆弱。
- 这很重要，因为在研究分析、预测软件决策、代码审计等场景中，**独立观点生成后再汇总**往往比在一个共享上下文中直接讨论更能暴露分歧与风险。

## Approach
- Parallax 先用一个 planner 生成策略 JSON，定义拓扑（如 groups、rounds、hierarchical）、agent 模式和聚合方式。
- executor 按策略在 **S2 durable streams** 上生成多个独立 agent 群组；每组只读取自己的流，**生成阶段彼此隔离，不能互相看到内容**。
- autonomous moderator 持续读取各组输出，决定是否转向、创建 breakout streams、进入下一阶段或结束，然后做最终 synthesis。
- agent 是持久会话（Claude 或 Codex），通过双向 stream-json I/O 工作；所有状态存在 S2 中，因此支持**crash-and-resume from the tail**。
- 系统支持人类或其他机器中途加入指定 swarm/group，也支持按群组分配不同后端模型与工具能力，用于研究、威胁建模、代码审查等工作流。

## Results
- 文本**没有提供正式基准测试、对照实验或量化评测结果**，因此没有可报告的准确率、胜率、成本或吞吐数字。
- 给出的最具体能力声明包括：可运行 **3 个独立群组 × 每组 2 个 agent** 的对抗式研究流程，并在综合前保持组间隔离。
- 示例还展示了 **5 个独立 panelists、3 轮 Delphi forecasting** 的流程，声称 moderator 会聚合并回灌上下文，使估计“收敛”，但未给出收敛指标或误差数据。
- 系统提供若干可控边界参数，如 `--max-messages 15`、`--max-dynamic-streams 4`、`--max-phase-transitions 3`、`--timeout 15`，表明其重点在**可编排、可恢复、可约束的多智能体执行**而非已验证的模型效果提升。
- 作者明确说明这是 **“vibecoded proof of concept”**，并提示“Expect rough edges”，说明当前贡献更偏**系统原型与交互机制**，而非成熟研究结果。

## Link
- [https://github.com/s2-streamstore/parallax](https://github.com/s2-streamstore/parallax)
