---
source: arxiv
url: http://arxiv.org/abs/2603.10808v1
published_at: '2026-03-11T14:14:53'
authors:
- Linghao Zhang
topics:
- llm-agents
- knowledge-crystallization
- memory-augmented-agents
- human-ai-collaboration
- agent-development-methodology
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Nurture-First Agent Development: Building Domain-Expert AI Agents Through Conversational Knowledge Crystallization

## Summary
本文提出一种面向领域专家智能体的开发方法论：**Nurture-First Development (NFD)**，主张让智能体在真实对话中持续“被培养”，而不是先用代码或提示词一次性构建完成。核心思想是把日常交互中零散的专家知识，周期性沉淀为可复用的结构化知识资产。

## Problem
- 论文要解决的是：如何把**隐性、个人化、持续变化**的领域专家知识有效编码进AI agent，而不仅是依赖通用大模型能力。
- 传统 **code-first** 方法偏重显式规则，难捕捉专家判断；**prompt-first** 方法依赖静态提示词，随着复杂度上升会遇到上下文窗口和维护问题。
- 这很重要，因为很多高价值场景（如金融、医疗、法律、研究）依赖不断演化的实践经验与情境判断，静态配置很快过时，导致“能力有了，但不值得信任”的配置鸿沟。

## Approach
- 提出 **NFD**：开发与部署不再分离，智能体先以最小脚手架上线，再通过与领域从业者的日常对话持续成长。
- 核心机制是 **Knowledge Crystallization Cycle**：先在对话中获取零散经验，再把这些经验定期提炼、验证并写成结构化知识，供以后复用。
- 设计了 **Three-Layer Cognitive Architecture**，把知识分成三层：**Constitutional**（身份/原则，低变化）、**Skill**（任务技能与参考资料，中等变化）、**Experiential**（交互日志与案例记忆，高变化）。
- 提出 **Dual-Workspace Pattern** 与 **Spiral Development Model**：一个工作区用于日常“养成式”使用，另一个用于外科手术式整理和升级知识；系统在多轮循环中逐步提高能力。
- 论文还给出形式化定义，包括知识状态、结晶操作与效率指标，并用美国股票研究金融分析agent作案例说明。

## Results
- 论文的主要产出是**方法论、架构与形式化框架**，而不是标准基准上的模型性能提升；摘录中**没有提供可核验的定量实验结果**。
- 明确声称 NFD 相比 code-first / prompt-first 的关键差异：开发与部署是**连续并发**过程，而不是先开发后上线。
- 表1给出若干定性比较：**time to first value** 从 code-first 的“**weeks–months**”、prompt-first 的“**hours–days**”变为 NFD 的“**minutes**（最小脚手架）并持续增长”。
- 论文指出 NFD 的扩展瓶颈不再主要是工程人力或上下文窗口，而是**memory search quality**；这是一种新的系统设计权衡，而非已通过数字实验验证的结论。
- 案例层面，作者展示了一个面向**U.S. equity analysis** 的金融研究agent，作为该范式可操作性的说明，但摘录中未报告任务成功率、准确率、成本、用户研究或与基线系统的数值对比。

## Link
- [http://arxiv.org/abs/2603.10808v1](http://arxiv.org/abs/2603.10808v1)
