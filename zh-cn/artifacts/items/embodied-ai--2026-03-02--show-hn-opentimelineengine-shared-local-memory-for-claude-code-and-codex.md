---
source: hn
url: https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine
published_at: '2026-03-02T22:59:15'
authors:
- joeljoseph_
topics:
- agent-memory
- local-first
- ai-coding-agent
- dual-agent-architecture
- policy-enforcement
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: OpenTimelineEngine – Shared local memory for Claude Code and codex

## Summary
Open Timeline Engine 是一个本地优先的 AI 代理共享记忆与行为约束平台，目标是让 Claude/Codex/Cursor 等执行器不再每次从零开始。它强调可审计记忆、策略强制、双 AI 架构和基于真实工作流的被动学习，但当前仍是实验性项目。

## Problem
- 解决 AI 编程代理**会话失忆**的问题：用户需要反复重述代码规范、架构背景和历史纠错，导致效率低且错误重复出现。
- 解决单模型代理**既决策又执行**带来的风险：一旦计划出错、被提示注入或忽略约束，就缺少独立制衡与安全门控。
- 解决团队/个人对 AI 使用中的**本地控制、审计追踪和风格一致性**需求，这对长期使用同一代码库的开发者尤其重要。

## Approach
- 构建一个**local-first 时间线记忆引擎**：从 CLI、Git、编辑器、浏览器等多源被动采集用户真实工作流，形成可检索的决策时间线，而不只是聊天记录。
- 采用**双 AI 架构**：执行器 AI 负责干活，顾问 AI 在 API 侧读取时间线并给出约束/改写/仲裁；两者共享记忆，但顾问不能写入事件，降低自我污染风险。
- 通过**接管（takeover）机制**实现渐进式自治：每回合计算 4 因子置信度（目标清晰度 40%、证据强度 25%、结果稳定性 20%、分类确定性 15%），再决定继续执行、进入审议，或请求人工。
- 用**架构级安全策略**代替纯提示词：ABAC、敏感级别默认阻断、编辑前 `check_context`、受保护目录封锁、指令文本剥离、防止 advisor 写事件、审计日志与版本化 schema。
- 将历史行为挖掘成**模式与人格指纹**：声称从时间线中持续更新 25 维行为指纹、6 大类别、12 类情境标签，并把成功/失败反馈回后续检索与建议。

## Results
- 文本**没有给出标准学术基准上的定量实验结果**，也没有提供在公开数据集上的对比指标、消融实验或统计显著性结果。
- 项目给出的最具体系统级数字包括：**25 维**行为指纹、覆盖**6 类**行为维度；情境分类为**12 类**；检索预算为**每回合 ≤120ms**、每后端**≤60ms**；会话接管超时约**120 分钟**；指令过期时间**30–120 秒**。
- 记忆/检索流程中声明：优先使用 pgvector，当质量分数**<0.42**或命中数**<2**时回退到 Qdrant；若 `context_quality_score ≥ 0.72`，则跳过昂贵检索并使用缓存上下文。
- 目标发现与工作集刷新规则给出具体阈值：目标选择分数**>0.45**时继续；首次、目标变化或**每 6 轮**刷新工作集；在**2 次以上失败**后重新触发目标发现；若低相关连续**3 个周期**则停止。
- 项目引用外部研究称“斯坦福研究表明 2 小时访谈可达**85%**人格克隆准确率”，并借此论证自身被动行为克隆方向，但**这不是该项目自身实验结果**。
- 最强的核心主张是：相比一般 memory layer，系统可提供**共享本地记忆、行为风格学习、双 AI 执行/顾问分离、可审计安全门控、跨执行器一致约束**，用于提升长期 AI 编程代理的连续性与可控性。

## Link
- [https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine](https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine)
