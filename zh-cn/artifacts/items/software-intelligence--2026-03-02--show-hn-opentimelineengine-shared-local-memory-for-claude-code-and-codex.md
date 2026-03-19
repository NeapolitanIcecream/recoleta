---
source: hn
url: https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine
published_at: '2026-03-02T22:59:15'
authors:
- joeljoseph_
topics:
- ai-memory
- code-agents
- local-first
- behavioral-cloning
- policy-enforcement
- multi-agent
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: OpenTimelineEngine – Shared local memory for Claude Code and codex

## Summary
Open Timeline Engine 是一个面向 AI 编码代理的本地优先共享记忆与控制平台，目标是让 Claude/Codex/Cursor 等代理跨会话记住真实工作方式，而不是每次从零开始。它把“记忆检索”扩展为“基于时间线的行为克隆、策略约束、审计追踪和双 AI 协作执行”。

## Problem
- 现有 AI 编码代理通常**每次会话都冷启动**，重复遗忘代码库约定、历史修正和用户偏好，导致同样错误反复发生。
- 仅靠聊天记忆或提示词很难支撑**可靠自治执行**：同一个模型既决策又执行，容易把幻觉计划直接付诸行动，也容易被提示注入绕过。
- 对于日常软件开发，用户还需要**本地数据控制、可审计性、跨代理共享上下文和安全约束**，而不仅是“能回忆一些偏好”。

## Approach
- 用一个**本地优先时间线引擎**持续采集真实工作流信号：CLI、Git、VSCode、浏览器、MCP 会话等，把“发生了什么、为什么这样决定、结果如何”沉淀为可检索记忆。
- 采用**双 AI 架构**：执行器代理负责干活；API 侧 advisor 代理只读时间线、提供建议/改写/安全门控，不直接写入事件，从架构上分离“行动”和“监督”。
- 提供**共享或隔离的 workspace memory**，让 Claude、Codex、Cursor 等多个执行器可以共享同一工作区记忆，也可按执行器隔离；默认检索为 user-only，显式请求时才做跨用户/跨执行器扩展。
- 引入**渐进式自治机制**：每回合根据目标清晰度、证据强度、结果稳定性、分类器确定性四项打分，决定走快速继续、审慎检索/深思，还是暂停请求人类确认。
- 通过**策略与防火墙式安全控制**约束执行：ABAC、敏感级别默认拦截、编辑前 `check_context`、保护目录阻断、指令文本剥离、审计日志、嵌入前与响应前脱敏等，避免仅依赖提示词安全。

## Results
- 文本**没有给出标准学术基准或独立实验评测结果**，因此没有可核验的 SOTA 数字；当前公开版本为 **v0.3.0**，项目明确标注为**实验性、未生产就绪**。
- 论文/项目宣称可构建**25 维行为指纹**，覆盖 **6 个类别**（如决策方式、沟通、优先级、上下文切换、学习风格、情绪模式），并把情境归类到 **12 种行为类别**。
- 自治决策置信度由 **4 个因子**加权：目标清晰度 **40%**、证据强度 **25%**、结果稳定性 **20%**、分类器确定性 **15%**；以此决定继续、审议或请求人工。
- 检索预算被严格限制为**每回合总计 ≤120ms**、**每后端/来源 ≤60ms**；当 pgvector 质量分数 **<0.42** 或命中数 **<2** 时，可回退到 Qdrant；工作集质量阈值示例为 **context_quality_score ≥ 0.72**。
- 会话 takeover 状态按 `session_id` 持久化，超时 **120 分钟**；执行指令可设置 **30–120 秒**过期时间；工作集通常**每 6 个回合**刷新一次，目标发现也会在**每第 6 回合**或**2 次以上失败后**重新触发。
- 项目引用外部对比性论述：Stanford 研究称“2 小时访谈可达 **85%** 个性克隆准确率”；作者声称本系统可**被动式**从真实工作行为中逼近此目标，但文中**未提供自家实验精度、对照基线或复现实验数据**。

## Link
- [https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine](https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine)
